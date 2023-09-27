// Main source file for the Harmony model checker.  It contains the main
// loop of the model checker, the subsequent analysis of the Kripke
// structure, and the code to regenerate a counter-example.

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include "head.h"

#ifdef __linux__
#include <sched.h>   //cpu_set_t, CPU_SET
#ifdef NUMA
#include <numa.h>
#endif
#endif

#include <stdint.h>

#ifdef USE_ATOMIC
#include <stdatomic.h>
#endif

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/param.h>
#include <unistd.h>
#include <signal.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <errno.h>
#include <assert.h>
#include <time.h>

#include "global.h"
#include "thread.h"
#include "value.h"
#include "strbuf.h"
#include "ops.h"
#include "dot.h"
// #include "iface/iface.h"
#include "hashdict.h"
#include "dfa.h"
#include "thread.h"
#include "spawn.h"

// The model checker leverages partial order reduction to reduce the
// number of states and interleavings considered.  In particular, it
// will combine virtual machine instructions that have no effect on
// the shared state.
#define MAX_STEPS       4096        // limit on partial order reduction

// To optimize memory allocation, each worker thread allocates large
// chunks of memory and then uses parts of that.
#define WALLOC_CHUNK    (16 * 1024 * 1024)

// This is use for reading lines from the /proc/cpuinfo file
#define LINE_CHUNK      128

// Newly discovered  nodes are kept in arrays of this size
#define NRESULTS        4096

// All global variables should be here
struct global global;

// For -d option
// TODO: this is still experimental and not fully fleshed out
unsigned int run_count;  // counter of #threads
mutex_t run_mutex;       // to protect count
mutex_t run_waiting;     // for main thread to wait on

extern bool has_countLabel;     // TODO.  Hack for backward compatibility

// TODO.  Move into global
struct scc {
    uint32_t component;     // strongly connected component id
    int32_t index, lowlink; // only needed for Tarjan
} *scc;

// Info about virtual processors (cores or hyperthreads).  Virtual
// processors are thought of a organized in a tree, for example based
// on cache affinity.  Each processor is therefore uniquely identified
// by a path of identifiers of nodes in this tree.  Each worker thread
// runs on its own virtual processor.
struct vproc_info {
    int *ids;            // path of ids identifying this processor
    unsigned int nids;   // length of path
    bool selected;       // selected to be used for a worker
} *vproc_info;
unsigned int n_vproc_info;

// To select virtual processors, the user specifies a disjunct
// of patterns using the -w flag.  Each pattern is a list of
// ids or wildcards.
struct pattern {
    struct id_opt {
        bool wildcard;      // any id will do
        int id;             // specific id
    } *ids;
    unsigned int nids;
};

// Nodes in the vproc_tree map local node identifiers to children.
struct vproc_map {
    int local_id;
    struct vproc_tree *child;
};

// Virtual processors are organized into a tree
struct vproc_tree {
    unsigned int n_vprocessors;  // #virtual processors in this subtree
    unsigned int virtual_id;     // virtual processor id, only for leaf nodes
    unsigned int nchildren;
    struct vproc_map *children;
} *vproc_root;

struct results_block {
    struct results_block *next;
    unsigned int nresults;
    struct node *results[NRESULTS];
};

// One of these per worker thread
struct worker {
    double timeout;              // deadline for model checker (-t option)
    struct failure *failures;    // list of discovered failures (not data races)
    unsigned int index;          // index of worker
    struct worker *workers;      // points to array of workers
    unsigned int nworkers;       // total number of workers
    unsigned int vproc;          // virtual processor for pinning
    unsigned int si_total, si_hits;
    struct edge_list *el_free;
    bool loops_possible;         // cycles in graph are possible

    // The worker thread loop through three phases:
    //  1: model check part of the state space
    //  2: fix forward edges and allocate larger tables if needed
    //  3: copy from old to new hash table
    // The barriers are to synchronize these three phases.
    barrier_t *start_barrier, *middle_barrier, *end_barrier;

    // Statistics about the three phases for optimization purposes
    double start_wait, middle_wait, end_wait;
    unsigned int start_count, middle_count, end_count;
    double phase1, phase2a, phase2b, phase3a, phase3b;
    unsigned int fix_edge;
    unsigned int dequeued;      // total number of dequeued states
    unsigned int enqueued;      // total number of enqueued states

    // A pointer to the Kripke structure, which is a hash table that
    // maps states to nodes.  Nodes contain the list of edges and more.
    struct dict *visited;

    // Thread 0 periodically prints some information on what it's
    // working on.  To avoid it getting the time too much, which might
    // involve an expensive system call, we do it every timecnt steps.
    int timecnt;                 // to reduce gettime() overhead

    // State maintained while evaluating invariants
    struct step inv_step;        // for evaluating invariants

    // When a worker creates a new state, it puts the corresponding node
    // in a list.  The nodes are added to the graph table after the
    // graph table has been grown.
    struct results_block *results;       // linked list of nodes
    struct results_block *rb_free;
    unsigned int count;         // size of the results list
    unsigned int total_results;
    unsigned int process_step;

    // New nodes are assigned node identifiers in phase 3.  This is
    // done in parallel by the various workers.  Each worker gets
    // 'count' node_ids starting at the following node_id.
    unsigned int node_id;

#ifdef USE_EDGES
    // When new edges are in the Kripke structure are discovered, we
    // avoid workers stalling trying to get a lock on the source node
    // and instead keep an NxN table of edge lists (N is the number of
    // workers) that need to be inserted.  Worker i puts the edge in
    // cell (i, j) if j is the worker that is responsible for the
    // source node (node_id % N).
    struct edge **edges;        // lists of edges to fix, one for each worker
#endif

    // Workers optimize memory allocation.  In particular, it is not
    // necessary for the memory to ever be freed.  So the worker allocates
    // large chunks of memory (WALLOC_CHUNK) and then use a pointer into
    // the chunk for allocation.
    char *alloc_buf;            // allocated buffer
    char *alloc_ptr;            // pointer into allocated buffer
    char *alloc_buf16;          // allocated buffer, 16 byte aligned
    char *alloc_ptr16;          // pointer into allocated buffer
    unsigned long allocated;    // keeps track of how much was allocated
    unsigned long align_waste;
    unsigned long frag_waste;

    // This is used in the code when a worker must allocate memory.
    struct allocator allocator;

    // Each worker keeps track of how often it executes a particular
    // instruction for profiling purposes.
    unsigned int *profile;      // one for each instruction in the HVM code

    // Some space to compute a new state in
    char state_space[sizeof(struct state) + 256*sizeof(hvalue_t)];

    // These need to be next to one another.  When a worker performs a
    // "step", it's on behalf of a particular thread with a particular
    // context (state of the thread).  The context structure is immediately
    // followed by its stack of Harmony values.
    struct context ctx;
    hvalue_t stack[MAX_CONTEXT_STACK];

    // We also keep space for an optimization for atomic sections
    char as_state[sizeof(struct state) + MAX_CONTEXT_BAG * (sizeof(hvalue_t) + 1)];
    struct context as_ctx;
    hvalue_t as_stack[MAX_CONTEXT_STACK];
};

#ifdef CACHE_LINE_ALIGNED
#define ALIGNMASK       0x3F
#else
#define ALIGNMASK       0xF
#endif

// Per thread one-time memory allocator (no free(), although the last
// thing allocated can be freed with wfree()).
static void *walloc(void *ctx, unsigned int size, bool zero, bool align16){
    struct worker *w = ctx;
    void *result;

    if (size > WALLOC_CHUNK) {
        panic("TODO: TOO LARGE");       // TODO
        return zero ? calloc(1, size) : malloc(size);
    }

    if (align16) {
        unsigned int asize = (size + ALIGNMASK) & ~ALIGNMASK;     // align to 16 bytes
        w->align_waste += asize - size;
        if (w->alloc_ptr16 + asize > w->alloc_buf16 + WALLOC_CHUNK) {
            w->frag_waste += WALLOC_CHUNK - (w->alloc_ptr16 - w->alloc_buf16);
#ifdef ALIGNED_ALLOC
            w->alloc_buf16 = my_aligned_alloc(ALIGNMASK + 1, WALLOC_CHUNK);
            w->alloc_ptr16 = w->alloc_buf16;
#else // ALIGNED_ALLOC
            w->alloc_buf16 = malloc(WALLOC_CHUNK);
            w->alloc_ptr16 = w->alloc_buf16;
            if (((hvalue_t) w->alloc_ptr16 & ALIGNMASK) != 0) {
                w->alloc_ptr16 = (char *) ((hvalue_t) (w->alloc_ptr16 + ALIGNMASK) & ~ALIGNMASK);
            }
#endif // ALIGNED_ALLOC
            w->allocated += WALLOC_CHUNK;
        }
        result = w->alloc_ptr16;
        w->alloc_ptr16 += asize;
    }
    else {
        unsigned int asize = (size + 0x7) & ~0x7;     // align to 8 bytes
        w->align_waste += asize - size;
        if (w->alloc_ptr + asize > w->alloc_buf + WALLOC_CHUNK) {
            w->frag_waste += WALLOC_CHUNK - (w->alloc_ptr - w->alloc_buf);
            w->alloc_buf = malloc(WALLOC_CHUNK);
            w->alloc_ptr = w->alloc_buf;
            w->allocated += WALLOC_CHUNK;
        }
        result = w->alloc_ptr;
        w->alloc_ptr += asize;
    }
    if (zero) {
        memset(result, 0, size);
    }
    return result;
}

// This is only allowed to release the last thing that was allocated
static void wfree(void *ctx, void *last, bool align16){
    struct worker *w = ctx;

    if (align16) {
        w->alloc_ptr16 = last;
    }
    else {
        w->alloc_ptr = last;
    }
}

// Part of experimental -d option, running Harmony programs "for real".
static void run_thread(struct state *state, struct context *ctx){
    struct step step;
    memset(&step, 0, sizeof(step));
    step.ctx = ctx;

    for (;;) {
        int pc = step.ctx->pc;
        struct instr *instrs = global.code.instrs;
        struct op_info *oi = instrs[pc].oi;
        (*oi->op)(instrs[pc].env, state, &step);
        if (step.ctx->terminated) {
            break;
        }
        if (step.ctx->failed) {
            char *s = value_string(ctx_failure(step.ctx));
            printf("Failure: %s\n", s);
            free(s);
            break;
        }
        if (step.ctx->stopped) {
            printf("Context has stopped\n");
            break;
        }

        if (step.ctx->pc == pc) {
            fprintf(stderr, ">>> %s\n", oi->name);
        }
        assert(step.ctx->pc != pc);
        assert(step.ctx->pc >= 0);
        assert(step.ctx->pc < global.code.len);
    }

    mutex_acquire(&run_mutex);
    if (--run_count == 0) {
        mutex_release(&run_waiting);
    }
    mutex_release(&run_mutex);
}

// Part of experimental -d option, running Harmony programs "for real".
static void wrap_thread(void *arg){
    struct spawn_info *si = arg;
    run_thread(si->state, si->ctx);
}

// Part of experimental -d option, running Harmony programs "for real".
void spawn_thread(struct state *state, struct context *ctx){
    mutex_acquire(&run_mutex);
    run_count++;
    mutex_release(&run_mutex);

    struct spawn_info *si = new_alloc(struct spawn_info);
    si->state = state;
    si->ctx = ctx;
    thread_create(wrap_thread, si);
}

// Apply the effect of evaluating a context (for a particular assignment
// of shared variables and possibly some choice) to a state.  This leads
// to a new edge in the Kripke structure, possibly to a new state.
static void process_step(
    struct worker *w,
    struct edge *edge,
    struct state *sc
) {
    struct step_condition *stc = edge->sc;
    assert(stc->type == SC_COMPLETED);
    struct step_input *si = (struct step_input *) &stc[1];
    struct step_output *so = stc->u.completed;
    struct node *node = edge->src;

    w->process_step++;
    sc->vars = so->vars;

    // Remove old context from the bag
    context_remove(sc, si->ctx);

    // Update state with spawned and resumed threads.
    for (unsigned int i = 0; i < so->nspawned; i++) {
        if (context_add(sc, step_spawned(so)[i]) < 0) {
            panic("too many threads 1");
        }
    }
    for (unsigned int i = 0; i < so->nunstopped; i++) {
        hvalue_t ctx = step_unstopped(so)[i];
        // TODO.  Write function (same code in op_Go)
        hvalue_t count;
        if (value_tryload(&w->allocator, sc->stopbag, ctx, &count)) {
            assert(VALUE_TYPE(count) == VALUE_INT);
            assert(count != VALUE_INT);
            count -= 1 << VALUE_BITS;
            if (count != VALUE_INT) {
                sc->stopbag = value_dict_store(&w->allocator, sc->stopbag, ctx, count);
            }
            else {
                sc->stopbag = value_dict_remove(&w->allocator, sc->stopbag, ctx);
            }
        }
    }

    // Add new context to state unless it's terminated.
    int new_index = -1;
    if (so->stopped) {
        sc->stopbag = value_bag_add(&w->allocator, sc->stopbag, so->after, 1);
    }
    else if (!so->terminated) {
        new_index = context_add(sc, so->after);
        if (new_index < 0) {
            panic("too many threads 0");
        }
    }

    // If choosing, save in state.  If some invariant uses "pre", then
    // also keep track of "pre" state.
    //
    // The issue here is subtle.  Invariants are only checked when entering
    // a normal state, not a choosing state, because choosing states can be
    // in the middle of an atomic section.  So, we either need to keep track
    // of the pre-state (as we do) or we need a much more complicated way of
    // checking invariants with "pre" variables.  But always storing the
    // pre-state in an old state can result in significant state explosion.
    // So we only do it in case there are such invariant, and then only for
    // choosing states.
    if (so->choosing) {
        sc->chooser = new_index;
        // sc->pre = global.inv_pre ? node_state(node)->pre : sc->vars;
    }
    else {
        sc->chooser = -1;
        // sc->pre = sc->vars;
    }

    edge->failed = so->failed || so->infinite_loop;

    if (global.dfa != NULL) {
        for (unsigned int i = 0; i < so->nlog; i++) {
            int nstate = dfa_step(global.dfa, sc->dfa_state, step_log(so)[i]);
            if (nstate < 0) {
                struct failure *f = new_alloc(struct failure);
                f->type = FAIL_BEHAVIOR;
                f->edge = edge;
                edge->failed = true;
                add_failure(&global.failures, f);
                break;
            }
            sc->dfa_state = nstate;
        }
    }

    // If a failure has occurred, keep track of that too.
    if (edge->failed) {
        struct failure *f = new_alloc(struct failure);
        f->type = edge_output(edge)->infinite_loop ? FAIL_TERMINATION : FAIL_SAFETY;
        f->edge = edge;
        f->next = w->failures;
        w->failures = f;
    }

    // See if this state has been computed before by looking up the node,
    // or allocate if not.
    unsigned int size = state_size(sc);
    mutex_t *lock;
    bool new;
    struct dict_assoc *hn = dict_find_lock_new(w->visited, &w->allocator,
                sc, size, &new, &lock);
    edge->dst = (struct node *) &hn[1];
    if (new) {
        assert(node->len == global.diameter);
        struct node *next = edge->dst;
        next->reachable = true;         // TODO.  Do we need this?
        next->failed = edge->failed;
        next->to_parent = edge;
        next->len = node->len + 1;
#ifdef OBSOLETE
        next->dead_end = true;
        next->u.ph1.lock = lock;
#endif

        // Add new node to results list kept per worker
        struct results_block *rb = w->results;
        if (rb == NULL || rb->nresults == NRESULTS) {
            if ((rb = w->rb_free) == NULL) {
                rb = walloc(w, sizeof(*rb), false, false);
            }
            else {
                w->rb_free = rb->next;
            }
            rb->nresults = 0;
            rb->next = w->results;
            w->results = rb;
        }
        rb->results[rb->nresults++] = next;

        w->count++;
        w->enqueued++;
        w->total_results++;
        mutex_release(lock);
    }

    // See if the node points sideways or backwards, in which
    // case cycles in the graph are possible
    if (edge->dst != node && edge->dst->len <= node->len) {
        w->loops_possible = true;
    }

#ifdef OBSOLETE
    // Keep track of whether 'node' is a candidate for a 'final' state
    if (edge->dst != node) {
        mutex_acquire(node->u.ph1.lock);
        node->dead_end = false;
        mutex_release(node->u.ph1.lock);
    }
#endif
}

// This is the main workhorse function of model checking: explore a state and
// a thread executing in this state.  One tricky thing here is an optimization
// in how atomic sections are implemented.  Sometimes, often in assertions,
// there is an atomic section that does not access shared variables.  It would
// be inefficient to "break" in that case, as it would needlessly reduce the
// amount of partial order reduction we can do.  And we do not want to discourage
// programmers from using assertions.  Thus, to execute an atomic section, we
// save the state at the beginning and rollback in case it turns out that we do
// need to break.
static struct step_output *onestep(
    struct worker *w,       // thread info
    struct node *node,      // starting node
    struct state *sc,       // actual state
    hvalue_t ctx,           // context identifier
    struct step *step,      // step info
    hvalue_t choice,        // if about to make a choice, which choice?
    bool infloop_detect,    // try to detect infloop from the start
    bool invariant
) {
    assert(state_size(sc) == state_size(node_state(node)));

    assert(!step->ctx->terminated);
    assert(!step->ctx->failed);

    bool infinite_loop = false;

    // See if we should first try an interrupt.
    if (choice == (hvalue_t) -1) {
        choice = 0;
        assert(step->ctx->extended);
        assert(ctx_trap_pc(step->ctx) != 0);
        interrupt_invoke(step);
    }

#ifdef XYZ
    if (invariant) {
        hvalue_t args[2];
        args[0] = args[1] = sc->vars;
        (void) value_ctx_pop(step->ctx); // HACK
        value_ctx_push(step->ctx, value_put_list(step->allocator, args, sizeof(args)));
    }
#endif

    bool choosing = false;
    struct dict *infloop = NULL;        // infinite loop detector
    unsigned int instrcnt = 0;          // keeps track of #instruction executed
    unsigned int as_instrcnt = 0;       // for rollback

    bool rollback = false, stopped = false;
    bool terminated = false;
    for (;;) {
        int pc = step->ctx->pc;

#ifdef OLD_PACIFIER
        // Worker 0 periodically (every second) prints some stats for long runs.
        // To avoid calling gettime() very often, which may involve an expensive
        // system call, worker 0 only checks every 100 instructions.
        if (w->index == 0 && w->timecnt-- == 0) {
            double now = gettime();
            if (now - global.lasttime > 1) {
                if (global.lasttime != 0) {
                    unsigned int enqueued = 0, dequeued = 0;
                    unsigned long allocated = global.allocated;
#ifdef FULL_REPORT
                    unsigned long align_waste = 0, frag_waste = 0;
#endif

                    for (unsigned int i = 0; i < w->nworkers; i++) {
                        struct worker *w2 = &w->workers[i];
                        enqueued += w2->enqueued;
                        dequeued += w2->dequeued;
                        allocated += w2->allocated;
#ifdef FULL_REPORT
                        align_waste += w2->align_waste;
                        frag_waste += w2->frag_waste;
#endif
                    }
                    double gigs = (double) allocated / (1 << 30);
#ifdef INCLUDE_RATE
                    fprintf(stderr, "pc=%d states=%u diam=%u q=%d rate=%d mem=%.3lfGB\n",
                            step->ctx->pc, enqueued, global.diameter, enqueued - dequeued,
                            (unsigned int) ((enqueued - global.last_nstates) / (now - global.lasttime)),
                            gigs);
#else
#ifdef FULL_REPORT
                    fprintf(stderr, "pc=%d states=%u diam=%u q=%d mem=%.3lfGB %lu %lu %lu\n",
                            step->ctx->pc, enqueued, global.diameter,
                            enqueued - dequeued, gigs, align_waste, frag_waste, global.allocated);
#else
                    fprintf(stderr, "pc=%d states=%u diam=%u q=%d mem=%.3lfGB ph=%u\n",
                            step->ctx->pc, enqueued, global.diameter,
                            enqueued - dequeued, gigs, w->middle_count);
#endif
#endif
                    global.last_nstates = enqueued;
                }
                global.lasttime = now;
                if (now > w->timeout) {
                    fprintf(stderr, "charm: timeout exceeded\n");
                    exit(1);
                }
            }
            w->timecnt = 100;
        }
#endif // OLD_PACIFIER

        // Each worker keeps track of how many times each instruction is executed.
        w->profile[pc]++;

        // See what kind of instruction is next
        struct instr *instrs = global.code.instrs;
        struct op_info *oi = instrs[pc].oi;
        // printf("--> %u %s %u %u\n", pc, oi->name, step->ctx->sp, instrcnt);

        // If it's a Choose instruction, replace the top of the stack (which
        // contains the set of choices) with the choice.
        if (instrs[pc].choose) {
            assert(step->ctx->sp > 0);
            assert(choice != 0);
            ctx_stack(step->ctx)[step->ctx->sp - 1] = choice;
            step->ctx->pc++;
        }


        // See if it's an AtomicInc instruction.
        else if (instrs[pc].atomicinc) {
            // If it's the very first instruction, set the atomicFlag in the context
            if (instrcnt == 0) {
                step->ctx->atomicFlag = true;
            }

            // If not, but the context was not in atomic mode, save the current
            // state to restore to in case we have to "break".
            else if (step->ctx->atomic == 0) {
                memcpy(w->as_state, sc, state_size(sc));
                memcpy(&w->as_ctx, step->ctx, ctx_size(step->ctx));
                as_instrcnt = instrcnt;
            }
            
            // Execute the AtomicInc instruction.
            (*oi->op)(instrs[pc].env, sc, step);
        }

        // If we're no longer in an atomic section after executing the instruction,
        // we can clear the saved state.
        else if (instrs[pc].atomicdec) {
            (*oi->op)(instrs[pc].env, sc, step);
            if (step->ctx->atomic == 0) {
                as_instrcnt = 0;
            }
        }

        // Otherwise just execute the operation.
        else {
            (*oi->op)(instrs[pc].env, sc, step);
        }
        assert(step->ctx->pc >= 0);
        assert(step->ctx->pc < global.code.len);
        // printf("<-- %u %s %u\n", pc, oi->name, step->ctx->sp);

        instrcnt++;

        // If the last instruction terminated the context, break out of the loop.
        if (step->ctx->terminated) {
            terminated = true;
            break;
        }

        // Same if the context has failed.
        if (step->ctx->failed) {
            // printf("FAILED AFTER %d steps\n", (int) instrcnt);
            break;
        }

        // Same if the context has stopped.
        if (step->ctx->stopped) {
            stopped = true;
            break;
        }

        // TODO: Not sure what to do when a thread appears to be creating
        //       an unending stream of new states.  For now we print warnings
        //       and then give up.
        if (instrcnt >= 100000000) {
            printf("fatal: giving up on thread\n");
            exit(1);
        }
        if (instrcnt >= 1000000 && instrcnt % 1000000 == 0) {
            printf("warning: thread seems to be in infinite loop (%u)\n", instrcnt);
        }

        // If infloop_detect is on, that means that in the previous attempt to
        // evaluated onestep() we suspected an infinite loop.  If it's off, we
        // start trying to detect it after 1000 instructions.
        // TODO.  1000 seems rather arbitrary.  Is it a good choice?  See below.
        if (infloop_detect || instrcnt > 1000) {
            if (infloop == NULL) {
                infloop = dict_new("infloop1", sizeof(unsigned int),
                                                0, 0, false);
            }

            // We need to save the global state *and *the state of the current
            // thread (because the context bag in the global state is not
            // updated each time the thread changes its state, aka context).
            int ctxsize = ctx_size(step->ctx);
            int combosize = ctxsize + state_size(sc);
            char *combo = calloc(1, combosize);
            memcpy(combo, step->ctx, ctxsize);
            memcpy(combo + ctxsize, sc, state_size(sc));
            bool new;
            unsigned int *loc = dict_insert(infloop, NULL, combo, combosize, &new);
            free(combo);

            // If we have not seen this state before, keep track of when we
            // saw this state.
            // TODO.  This may be obsolete.
            if (new) {
                *loc = instrcnt;
            }

            // We have seen this state before.
            else {
                // If we reran onestep() because we suspected an infinite loop,
                // report it.
                if (infloop_detect) {
                    // if (*loc != 0) {
                    //     instrcnt = *loc;
                    // }
                    value_ctx_failure(step->ctx, step->allocator, "infinite loop");
                    infinite_loop = true;
                    printf("INFINITE LOOP\n");
                    break;
                }

                // Otherwise start over to create the shortest counterexample.
                else {
                    printf("INFINITE LOOP RETRY\n");
                    return NULL;
                }
            }
        }

        // This should never happen.
        if (step->ctx->pc == pc) {
            fprintf(stderr, ">>> %s\n", oi->name);
        }
        assert(step->ctx->pc != pc);
        assert(step->ctx->pc >= 0);
        assert(step->ctx->pc < global.code.len);

        // If we're not in atomic mode, we limit the number of steps to MAX_STEPS.
        // TODO.  Not sure why.
        if (step->ctx->atomic == 0 && instrcnt > MAX_STEPS) {
            break;
        }

        /* Peek at the next instruction.  We may have to break out of the loop
         * because of it.
         */
        struct instr *next_instr = &global.code.instrs[step->ctx->pc];

        // If the next instruction is Choose, we should break.
        if (next_instr->choose) {
            assert(step->ctx->sp > 0);

#ifdef TODO         // not sure why ifdef'd out
            if (0 && step->ctx->readonly > 0) {    // TODO
                value_ctx_failure(step->ctx, step->allocator, "can't choose in assertion or invariant");
                instrcnt++;
                break;
            }
#endif

            // Check that the top of the stack contains a set.
            hvalue_t s = ctx_stack(step->ctx)[step->ctx->sp - 1];
            if (VALUE_TYPE(s) != VALUE_SET) {
                value_ctx_failure(step->ctx, step->allocator, "choose operation requires a set");
                instrcnt++;
                break;
            }

            // Check that the set contains at least one element.
            // TODO.  We should just be able to check s == VALUE_SET
            unsigned int size;
#ifdef OBSOLETE
            hvalue_t *vals =
#endif
            value_get(s, &size);
            size /= sizeof(hvalue_t);
            if (size == 0) {
                value_ctx_failure(step->ctx, step->allocator, "choose operation requires a non-empty set");
                instrcnt++;
                break;
            }
            
            // If we were lazily executing an atomic section in the hopes of
            // not having to break, we need to restore the state.
            if (step->ctx->atomic > 0 && !step->ctx->atomicFlag) {
                rollback = true;
            }
            else {
                choosing = true;
            }
            break;
        }

        // See if we need to break out of this step.  If the atomicFlag is
        // set, then definitely not.  If it is not set, then it gets
        // complicated.  If the atomic count > 0, then we may have delayed
        // breaking until strictly necessary (lazy atomic), in the hopes
        // of not having to at all (because breaking causes an expensive
        // context switch).  If the instruction is not "breakable" (Load,
        // Store, Del, Print, eager AtomicInc), then there's no need to
        // break yet.  Otherwise, if the atomic count > 0, we should set
        // the atomicFlag and break.  Otherwise  if it's a breakable
        // instruction, we should just break.
        else if (!step->ctx->atomicFlag) {
            bool breakable = next_instr->breakable;

            // If this is a Load operation, it's only breakable if it
            // accesses a global variable
            // TODO.  Can this be made more efficient?
            if (next_instr->load && next_instr->env == NULL) {
                hvalue_t addr = ctx_stack(step->ctx)[step->ctx->sp - 1];
#ifdef VALUE_ADDRESS
                assert(false);
                assert(VALUE_TYPE(addr) == VALUE_ADDRESS);
                assert(addr != VALUE_ADDRESS);
                hvalue_t *func = value_get(addr, NULL);
                if (*func != VALUE_PC_SHARED) {
                    breakable = false;
                }
#else
                if (VALUE_TYPE(addr) != VALUE_ADDRESS_SHARED && VALUE_TYPE(addr) != VALUE_ADDRESS_PRIVATE) {
                    value_ctx_failure(step->ctx, step->allocator, "Load: not an address");
                    instrcnt++;
                    break;
                }
                if ((VALUE_TYPE(addr)) == VALUE_ADDRESS_PRIVATE) {
                    breakable = false;
                }
#endif
            }

            // Deal with interrupts if enabled
            if (step->ctx->extended && ctx_trap_pc(step->ctx) != 0 &&
                                !step->ctx->interruptlevel) {
                // If this is a thread exit, break so we can invoke the
                // interrupt handler one more time (just before its exit)
                if (next_instr->retop && step->ctx->sp == 1) {
                    breakable = true;
                }

                // If this is a setintlevel(True), should try interrupt
                // For simplicity, always try when SetIntLevel is about to
                // be executed.
                else if (next_instr->setintlevel) {
                    breakable = true;
                }
            }

            if (breakable) {
                // If the step is breakable and we're in an atomic section,
                // we should have broken at the beginning of the atomic
                // section.  Restore that state.
                if (step->ctx->atomic > 0 && !step->ctx->atomicFlag) {
                    rollback = true;
                }
                break;
            }
        }
    }

    // No longer need this.  It was wasted effort.
    // TODO.  Perhaps this suggests a way to automatically determine the
    //        number of instructions to run before trying to detect an
    //        infinite loop, which is currently hardwired at 1000.
    if (infloop != NULL) {
        dict_delete(infloop);
    }

    // See if we need to roll back to the start of an atomic section.
    // TODO.  What if the atomic section had some effects like spawning threads  etc?
    if (rollback) {
        struct state *state = (struct state *) w->as_state;
        memcpy(sc, state, state_size(state));
        memcpy(step->ctx, &w->as_ctx, ctx_size(&w->as_ctx));
        instrcnt = as_instrcnt;
    }

    // Capture the result of executing this step
    struct step_output *so = walloc(w, sizeof(struct step_output) +
            (step->nlog + step->nspawned + step->nunstopped) * sizeof(hvalue_t),
            false, false);
    so->vars = sc->vars;
    so->after = value_put_context(step->allocator, step->ctx);
    so->ai = step->ai;     step->ai = NULL;
    so->nsteps = instrcnt;

    // TODO.  The following 4 can be captured in just 2 bits I think
    so->choosing = choosing;
    so->terminated = terminated;
    so->stopped = stopped;
    so->failed = step->ctx->failed;
    so->infinite_loop = infinite_loop;

    // Copy the logs
    so->nlog = step->nlog;
    so->nspawned = step->nspawned;
    so->nunstopped = step->nunstopped;
    memcpy(step_log(so), step->log, step->nlog * sizeof(hvalue_t));
    memcpy(step_spawned(so), step->spawned, step->nspawned * sizeof(hvalue_t));
    memcpy(step_unstopped(so), step->unstopped, step->nunstopped * sizeof(hvalue_t));
    step->nspawned = 0;
    step->nlog = 0;
    step->nunstopped = 0;
    return so;
}

// Run the given context ctx in the given state, possibly making the given
// choice.  We keep a cache for running contexts given a certain assignment
// of shared variables and a given choice in the hashtable called ``computations''.
// The hashtable maps (vars, choice, ctx) to something called ``struct
// step_condition'' which keeps track of such computations.  The output
// of the computation is ``struct step_output'', which essentially describes
// the ``effect'' of running the computation.  The effect is then applied
// to the given state.  The effect includes updates to shared variables,
// printing values, spawning threads, and deleting contexts from the stopbag.
static void trystep(
    struct worker *w,       // thread info
    struct node *node,      // starting node
    struct state *state,    // actual state
    hvalue_t ctx,           // context identifier
    struct context *cc,     // value of context
    struct step *step,      // step info
    hvalue_t choice,        // if about to make a choice, which choice?
    unsigned int multiplicity,
    bool invariant
) {
    struct step_condition *stc;
    bool si_new;
    mutex_t *si_lock;

    w->si_total++;          // counts the number of edges

    // Allocate the edge and add to the node
    struct edge *edge = walloc(w, sizeof(struct edge), false, false);
    edge->src = node;
    edge->multiple = multiplicity > 1;
    edge->invariant_chk = invariant;
    edge->fwdnext = node->fwd;
    node->fwd = edge;

    struct step_input si = {
        .vars = state->vars,
        .choice = choice,
        .ctx = ctx
    };

    // For backward compatibility, we still support countLabel().  If the
    // Harmony program uses it, we circumvent the cache.
    if (has_countLabel) {
        struct step_comp *comp = walloc(w, sizeof(struct step_comp), false, false);
        si_new = true;
        stc = &comp->cond;
        comp->input = si;
    }
    else {
        // See if we did this already (or are doing this already)
        struct dict_assoc *da = dict_find_lock(global.computations,
            &w->allocator, &si, sizeof(si), &si_new, &si_lock);
        stc = (struct step_condition *) &da[1];
    }
    edge->sc = stc;

    if (si_new) {
        stc->type = SC_IN_PROGRESS;
        stc->u.in_progress = NULL;
    }
    else {
        w->si_hits++;
        if (stc->type == SC_IN_PROGRESS) {
            struct edge_list *el;
            if ((el = w->el_free) == NULL) {
                el = walloc(w, sizeof(struct edge_list), false, false);
            }
            else {
                w->el_free = el->next;
            }
            el->edge = edge;
            el->next = stc->u.in_progress;
            stc->u.in_progress = el;
            mutex_release(si_lock);
            return;
        }
        assert(stc->type == SC_COMPLETED);
    }

    if (!has_countLabel) {
        mutex_release(si_lock);
    }

    // Make a copy of the state.
    //
    // TODO. Don't need to copy if ctx in readonly mode
    unsigned int statesz = state_size(state);
    struct state *sc = (struct state *) w->state_space;
    memcpy(sc, state, statesz);
    sc->chooser = -1;

    // If this is a new step, perform it
    struct edge_list *el = NULL;
    if (si_new) {
        // Make a copy of the context
        assert(!cc->terminated);
        assert(!cc->failed);
        memcpy(&w->ctx, cc, ctx_size(cc));
        step->ctx = &w->ctx;

        // This will first attempt to run onestep() with delayed detection
        // of infinite loops (for efficiency).  If an infinite loop is
        // detected, it will run again immediately looking for infinite
        // loops to find the shortest counterexample.
        struct step_output *so =
            onestep(w, node, sc, ctx, step, choice, false, invariant);
        if (so == NULL) {        // ran into an infinite loop
            // TODO.  Need probably more cleanup of step, like ai
            step->nlog = step->nspawned = step->nunstopped = 0;
            memcpy(sc, state, statesz);
            sc->chooser = -1;
            memcpy(&w->ctx, cc, ctx_size(cc));
            so = onestep(w, node, sc, ctx, step, choice, true, invariant);
        }

        if (has_countLabel) {
            assert(stc->type == SC_IN_PROGRESS);
            assert(stc->u.in_progress == NULL);
            el = stc->u.in_progress;
            stc->type = SC_COMPLETED;
            stc->u.completed = so;
        }
        else {
            mutex_acquire(si_lock);
            assert(stc->type == SC_IN_PROGRESS);
            el = stc->u.in_progress;
            stc->type = SC_COMPLETED;
            stc->u.completed = so;
            mutex_release(si_lock);
        }
    }
    else {
        assert(stc->type == SC_COMPLETED);
    }

    // TODO.  Should I restore sc here?
    process_step(w, edge, sc);
    while (el != NULL) {
        struct node *n = el->edge->src;
        struct state *state = (struct state *) &n[1];
        unsigned int statesz = state_size(state);
        memcpy(sc, state, statesz);
        process_step(w, el->edge, sc);
        struct edge_list *next = el->next;
        el->next = w->el_free;
        w->el_free = el;
        el = next;
    }
}

// This function considers a state (pointed to by node) and a thread to run with
// state ctx. If it is a "choosing state" (the thread is about to execute a
// Choose instruction), then choice contains that choice to be tried.  Since
// threads are anonymous and multiple threads can be in the same state,
// multiplicity gives the number of threads that can make this step.  Any
// resulting states should be buffered in w->results.
//
// The hard work of makestep is accomplished by function onestep().  makestep()
// may invoke onestep() multiple times.  One reason is to explore interrupts
// (which can only happen in non-choosing states).  Another reason is based on
// how infinite loops are detected.  The easy way would be to maintain a set
// of all states that are computed after every machine instruction, and to
// check if a state re-occurs.  But that would be very expensive in the
// presumably normal case where there are no infinite loops in the code.
// So, an optimization that has been made is to explore a certain number
// of instructions without doing this check (currently 1000).  After that
// we start trying to detect an infinite loop.  If we detect one, we restart
// the whole thing to produce a shorter couter example.
//
// So, in total, make_step may call onestep up to four times:
//  1) to explore an interrupt
//  2) restarting 1) if an infinite loop is detected
//  3) explore a normal transition
//  4) restarting 3) if an infinite loop is detected.
static void make_step(
    struct worker *w,
    struct node *node,      // the state we're exploring
    unsigned int ctx_index, // the context that we're running
    hvalue_t choice         // if about to make a choice, which choice?
) {
    struct step step;
    memset(&step, 0, sizeof(step));
    step.allocator = &w->allocator;

    struct state *state = node_state(node);
    hvalue_t ctx = state_contexts(state)[ctx_index];

    // Get the context
    unsigned int size;
    struct context *cc = value_get(ctx, &size);
    assert(ctx_size(cc) == size);

    // See if we need to interrupt
    // TODO.  Should probably also check that the context is not in atomic mode.
    //        This could possibly happen if the thread was stopped in an atomic
    //        section and is then later restarted.
    if (state->chooser < 0 && cc->extended && ctx_trap_pc(cc) != 0 && !cc->interruptlevel) {
        trystep(w, node, state, ctx, cc, &step, (hvalue_t) -1, multiplicities(state)[ctx_index], false);
    }

    // Explore the state normally (not as an interrupt).
    trystep(w, node, state, ctx, cc, &step, choice, multiplicities(state)[ctx_index], false);
}

static void chk_invs(
    struct worker *w,
    struct node *node,     // the state we're exploring
    bool finally           // check finally predicate
) {
    struct step step;
    memset(&step, 0, sizeof(step));
    step.allocator = &w->allocator;

    struct state *state = node_state(node);

    // Check each invariant
    for (unsigned int i = 0; i < global.ninvs; i++) {
        // Get the context
        unsigned int size;
        struct context *cc = value_get(global.invs[i].context, &size);
        assert(ctx_size(cc) == size);
        assert(strcmp(global.code.instrs[cc->pc].oi->name, "Frame") == 0);
        trystep(w, node, state, global.invs[i].context, cc, &step, 0, 1, true);
    }

    if (!finally) {
        return;
    }

    // Check each "finally" predicate
    for (unsigned int i = 0; i < global.nfinals; i++) {
        // Get the context
        unsigned int size;
        struct context *cc = value_get(global.finals[i], &size);
        assert(ctx_size(cc) == size);
        assert(strcmp(global.code.instrs[cc->pc].oi->name, "Frame") == 0);
        trystep(w, node, state, global.finals[i], cc, &step, 0, 1, true);
    }
}

char *ctx_status(struct node *node, hvalue_t ctx) {
    struct state *state = node_state(node);

    if (state->chooser >= 0 && state_contexts(state)[state->chooser] == ctx) {
        return "choosing";
    }
    while (state->chooser >= 0) {
        node = node_to_parent(node)->src;
        state = node_state(node);
    }
    struct edge *edge;
    for (edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
        if (edge_input(edge)->ctx == ctx) {
            break;
        }
    }
    if (edge != NULL && edge->dst == node) {
        return "blocked";
    }
    return "runnable";
}

void print_context(
    FILE *file,
    hvalue_t ctx,
    struct callstack *cs,
    int tid,
    struct node *node,
    char *prefix
) {
    fprintf(file, "%s\"tid\": \"%d\",\n", prefix, tid);
    fprintf(file, "%s\"hvalue\": \"%"PRI_HVAL"\",\n", prefix, ctx);

    unsigned int size;
    struct context *c = value_get(ctx, &size);

    fprintf(file, "%s\"fp\": \"%d\",\n", prefix, cs->sp + 1);
    if (c->initial || c->id != 0) {
        fprintf(file, "%s\"id\": \"%u\",\n", prefix, c->id);
    }

    struct callstack *ecs = cs;
    while (ecs->parent != NULL) {
        ecs = ecs->parent;
    }

    assert(strcmp(global.code.instrs[ecs->pc].oi->name, "Frame") == 0);
    const struct env_Frame *ef = global.code.instrs[ecs->pc].env;
    char *s = value_string(ef->name);
    int len = strlen(s);
    char *a = json_escape_value(ecs->arg);
    if (*a == '(') {
        fprintf(file, "%s\"name\": \"%.*s%s\",\n", prefix, len - 2, s + 1, a);
    }
    else {
        fprintf(file, "%s\"name\": \"%.*s(%s)\",\n", prefix, len - 2, s + 1, a);
    }
    free(s);
    free(a);

    // TODO.  Backwards compatibility
    struct callstack *lcs = cs;
    while (lcs->parent != NULL) {
        lcs = lcs->parent;
    }
    fprintf(file, "%s\"entry\": \"%u\",\n", prefix, lcs->pc);

    fprintf(file, "%s\"pc\": \"%u\",\n", prefix, c->pc);
    fprintf(file, "%s\"sp\": \"%u\",\n", prefix, c->sp);

    fprintf(file, "%s\"stack\": [", prefix);
    for (unsigned int x = 0; x < c->sp; x++) {
        if (x != 0) {
            fprintf(file, ", ");
        }
        char *v = value_json(ctx_stack(c)[x]);
        fprintf(file, "%s", v);
        free(v);
    }
    fprintf(file, "],\n");

    fprintf(file, "%s\"trace\": [\n", prefix);
    value_trace(file, cs, c->pc, c->vars, prefix);
    fprintf(file, "\n");
    fprintf(file, "%s],\n", prefix);

    if (c->failed) {
        s = value_string(ctx_failure(c));
        fprintf(file, "%s\"failure\": %s,\n", prefix, s);
        free(s);
    }

    if (c->extended && ctx_trap_pc(c) != 0) {
        s = value_string(ctx_trap_pc(c));
        a = value_string(ctx_trap_arg(c));
        if (*a == '(') {
            fprintf(file, "%s\"trap\": \"%s%s\",\n", prefix, s, a);
        }
        else {
            fprintf(file, "%s\"trap\": \"%s(%s)\",\n", prefix, s, a);
        }
        free(a);
        free(s);
    }

    if (c->interruptlevel) {
        fprintf(file, "%s\"interruptlevel\": \"1\",\n", prefix);
    }

    if (c->extended) {
        s = value_json(ctx_this(c));
        fprintf(file, "%s\"this\": %s,\n", prefix, s);
        free(s);
    }

    if (c->atomic != 0) {
        fprintf(file, "%s\"atomic\": \"%d\",\n", prefix, c->atomic);
    }
    if (c->readonly != 0) {
        fprintf(file, "%s\"readonly\": \"%d\",\n", prefix, c->readonly);
    }
    if (!c->terminated && !c->failed) {
        struct instr *instr = &global.code.instrs[c->pc];
        struct op_info *oi = instr->oi;
        if (oi->next == NULL) {
            fprintf(file, "%s\"next\": { \"type\": \"%s\" },\n", prefix, oi->name);
        }
        else {
            fprintf(file, "%s\"next\": ", prefix);
            (*oi->next)(instr->env, c, file);
            fprintf(file, ",\n");
        }
    }

    if (c->terminated) {
        fprintf(file, "%s\"mode\": \"terminated\"", prefix);
    }
    else {
        if (c->failed) {
            fprintf(file, "%s\"mode\": \"failed\"", prefix);
        }
        else if (c->stopped) {
            fprintf(file, "%s\"mode\": \"stopped\"", prefix);
        }
        else {
            fprintf(file, "%s\"mode\": \"%s\"", prefix, ctx_status(node, ctx));
        }
    }
    fprintf(file, "\n");

#ifdef notdef
    fprintf(file, "          \"stack\": [\n");
    for (int i = 0; i < c->sp; i++) {
        s = value_string(ctx_stack(k)[i]);
        if (i < c->sp - 1) {
            fprintf(file, "            \"%s\",\n", s);
        }
        else {
            fprintf(file, "            \"%s\"\n", s);
        }
        free(s);
    }
    fprintf(file, "          ],\n");
#endif
}

// Save the state and the context of a microstep.
static void make_microstep(
    struct state *newstate,
    struct context *newctx,
    struct callstack *newcs,
    bool interrupt,
    bool choose,
    hvalue_t choice,
    hvalue_t print,
    struct step *step,
    struct macrostep *macro
) {
    struct microstep *micro = calloc(1, sizeof(*micro));

    // Save the current context
    unsigned int cs = ctx_size(newctx);
    micro->ctx = malloc(cs);
    memcpy(micro->ctx, newctx, cs);

    // Save the current state
    unsigned int ss = state_size(newstate);
    micro->state = malloc(ss);
    memcpy(micro->state, newstate, ss);

    micro->interrupt = interrupt;
    micro->choose = choose;
    micro->choice = choice;
    micro->print = print;
    micro->cs = newcs;
    micro->explain = json_escape(step->explain.buf, step->explain.len);
    unsigned int sz = step->explain_nargs * sizeof(hvalue_t);
    micro->args = malloc(sz);
    memcpy(micro->args, step->explain_args, sz);
    micro->nargs = step->explain_nargs;
    step->explain.len = 0;
    step->explain_nargs = 0;

    if (macro->nmicrosteps == macro->alloc_microsteps) {
        macro->alloc_microsteps *= 2;
        if (macro->alloc_microsteps < 64) {
            macro->alloc_microsteps = 64;
        }
        macro->microsteps = realloc(macro->microsteps,
            macro->alloc_microsteps * sizeof(*macro->microsteps));
    }
    macro->microsteps[macro->nmicrosteps++] = micro;
}

// Similar to onestep.  Used to recompute a faulty execution, that is, to
// generate the detailed execution of a counter-examples.
static void twostep(
    struct state *sc,
    hvalue_t ctx,
    struct callstack *cs,
    hvalue_t choice,
    bool invariant,
    unsigned int nsteps,
    unsigned int pid,
    struct macrostep *macro
){
    sc->chooser = -1;

    struct step step;
    memset(&step, 0, sizeof(step));
    step.keep_callstack = true;
    step.callstack = cs;
    strbuf_init(&step.explain);

    unsigned int size;
    struct context *cc = value_get(ctx, &size);
    step.ctx = calloc(1, sizeof(struct context) +
                            MAX_CONTEXT_STACK * sizeof(hvalue_t));
    memcpy(step.ctx, cc, size);
    if (step.ctx->terminated || step.ctx->failed) {
        panic("twostep: already terminated???");
    }

    if (choice == (hvalue_t) -1) {
        choice = 0;
        assert(step.ctx->extended);
        assert(ctx_trap_pc(step.ctx) != 0);
        interrupt_invoke(&step);
        make_microstep(sc, step.ctx, step.callstack, true, false, 0, 0, &step, macro);
    }

#ifdef XYZ
    if (invariant) {
        hvalue_t args[2];
        args[0] = args[1] = sc->vars;
        (void) value_ctx_pop(step.ctx); // HACK
        value_ctx_push(step.ctx, value_put_list(step.allocator, args, sizeof(args)));
    }
#endif

    struct dict *infloop = NULL;        // infinite loop detector
    unsigned int instrcnt = 0;
    for (;;) {
        int pc = step.ctx->pc;

        hvalue_t print = 0;
        struct instr *instrs = global.code.instrs;
        struct op_info *oi = instrs[pc].oi;
        if (instrs[pc].choose) {
            assert(choice != 0);
            strbuf_printf(&step.explain, "replace top of stack (#+) with choice (#+)");
            step.explain_args[step.explain_nargs++] = ctx_stack(step.ctx)[step.ctx->sp - 1];
            step.explain_args[step.explain_nargs++] = choice;
            ctx_stack(step.ctx)[step.ctx->sp - 1] = choice;
            step.ctx->pc++;
        }
        else if (instrs[pc].atomicinc) {
            if (instrcnt == 0) {
                step.ctx->atomicFlag = true;
            }
            (*oi->op)(instrs[pc].env, sc, &step);
        }
        else if (instrs[pc].print) {
            print = ctx_stack(step.ctx)[step.ctx->sp - 1];
            (*oi->op)(instrs[pc].env, sc, &step);
        }
        else {
            (*oi->op)(instrs[pc].env, sc, &step);
        }

        // Infinite loop detection
        if (!step.ctx->terminated && !step.ctx->failed) {
            if (infloop == NULL) {
                infloop = dict_new("infloop2", 0, 0, 0, false);
            }

            int ctxsize = sizeof(struct context) + step.ctx->sp * sizeof(hvalue_t);
            if (step.ctx->extended) {
                ctxsize += ctx_extent * sizeof(hvalue_t);
            }
            int combosize = ctxsize + state_size(sc);
            char *combo = calloc(1, combosize);
            memcpy(combo, step.ctx, ctxsize);
            memcpy(combo + ctxsize, sc, state_size(sc));
            bool new;
            dict_insert(infloop, NULL, combo, combosize, &new);
            free(combo);
            if (!new) {
                value_ctx_failure(step.ctx, step.allocator, "infinite loop");
            }
        }

        assert(!instrs[pc].choose || choice != 0);
        make_microstep(sc, step.ctx, step.callstack, false, instrs[pc].choose, choice, print, &step, macro);
        if (step.ctx->terminated || step.ctx->failed || step.ctx->stopped) {
            break;
        }
        instrcnt++;
        if (instrcnt >= nsteps) {
            break;
        }
        if (step.ctx->pc == pc) {
            fprintf(stderr, ">>> %s\n", oi->name);
        }
        assert(step.ctx->pc != pc);

        /* Peek at the next instruction.
         */
        oi = global.code.instrs[step.ctx->pc].oi;
        if (global.code.instrs[step.ctx->pc].choose) {
            assert(step.ctx->sp > 0);
#ifdef TODO
            if (0 && step.ctx->readonly > 0) {    // TODO
                value_ctx_failure(step.ctx, step.allocator, "can't choose in assertion or invariant");
                make_microstep(sc, step.ctx, step.callstack, false, global.code.instrs[pc].choose, choice, 0, &step, macro);
                break;
            }
#endif
            hvalue_t s = ctx_stack(step.ctx)[step.ctx->sp - 1];
            if (VALUE_TYPE(s) != VALUE_SET) {
                value_ctx_failure(step.ctx, step.allocator, "choose operation requires a set");
                make_microstep(sc, step.ctx, step.callstack, false, global.code.instrs[pc].choose, choice, 0, &step, macro);
                break;
            }
            unsigned int size;
            hvalue_t *vals = value_get(s, &size);
            size /= sizeof(hvalue_t);
            if (size == 0) {
                value_ctx_failure(step.ctx, step.allocator, "choose operation requires a non-empty set");
                make_microstep(sc, step.ctx, step.callstack, false, global.code.instrs[pc].choose, choice, 0, &step, macro);
                break;
            }
            if (size == 1) {
                choice = vals[0];
            }
            else {
                break;
            }
        }
    }

    // Remove old context from the bag
    context_remove(sc, ctx);

    hvalue_t after = value_put_context(step.allocator, step.ctx);

    // Add new context to state unless it's terminated or stopped
    if (step.ctx->stopped) {
        sc->stopbag = value_bag_add(step.allocator, sc->stopbag, after, 1);
    }
    else if (!step.ctx->terminated) {
        // TODO.  Check failure of context_add
        (void) context_add(sc, after);
    }

    free(step.ctx);
    strbuf_deinit(&step.explain);
    // TODO free(step.log);

    global.processes[pid] = after;
    global.callstacks[pid] = step.callstack;
}

static void *copy(void *p, unsigned int size){
    char *c = malloc(size);
    memcpy(c, p, size);
    return c;
}

// Take the path and put it in an array
void path_serialize(struct edge *e){
    // First recurse to the previous step
    struct node *parent = e->src;
    if (node_to_parent(parent) != NULL) {
        path_serialize(node_to_parent(parent));
    }

    struct macrostep *macro = calloc(sizeof(*macro), 1);
    macro->edge = e;

    if (global.nmacrosteps == global.alloc_macrosteps) {
        global.alloc_macrosteps *= 2;
        if (global.alloc_macrosteps < 8) {
            global.alloc_macrosteps = 8;
        }
        global.macrosteps = realloc(global.macrosteps,
            global.alloc_macrosteps * sizeof(*global.macrosteps));
    }
    global.macrosteps[global.nmacrosteps++] = macro;
}

void path_recompute(){
    struct node *node = global.graph.nodes[0];
    struct state *sc = calloc(1,
        sizeof(struct state) + MAX_CONTEXT_BAG * (sizeof(hvalue_t) + 1));
    memcpy(sc, node_state(node), state_size(node_state(node)));

    for (unsigned int i = 0; i < global.nmacrosteps; i++) {
        struct macrostep *macro = global.macrosteps[i];
        struct edge *e = macro->edge;
        hvalue_t ctx = edge_input(e)->ctx;

        if (e->invariant_chk) {
            global.processes = realloc(global.processes, (global.nprocesses + 1) * sizeof(hvalue_t));
            global.callstacks = realloc(global.callstacks, (global.nprocesses + 1) * sizeof(struct callstack *));
            global.processes[global.nprocesses] = ctx;
            struct context *cc = value_get(ctx, NULL);
            struct callstack *cs = new_alloc(struct callstack);
            cs->pc = cc->pc;
            cs->arg = VALUE_LIST;
            cs->vars = VALUE_DICT;
            // TODO next line
            cs->return_address = (cc->pc << CALLTYPE_BITS) | CALLTYPE_PROCESS;
            global.callstacks[global.nprocesses] = cs;
            global.nprocesses++;
        }

        /* Find the starting context in the list of processes.  Prefer
         * sticking with the same pid if possible.
         */
        unsigned int pid;
        if (global.processes[global.oldpid] == ctx) {
            pid = global.oldpid;
        }
        else {
            // printf("Search for %p\n", (void *) ctx);
            for (pid = 0; pid < global.nprocesses; pid++) {
                // printf("%d: %p\n", pid, (void *) global.processes[pid]);
                if (global.processes[pid] == ctx) {
                    break;
                }
            }
            global.oldpid = pid;
        }
        if (pid >= global.nprocesses) {
            printf("PID %p %u %u\n", (void *) ctx, pid, global.nprocesses);
            panic("bad pid");
        }
        assert(pid < global.nprocesses);

        macro->tid = pid;
        macro->cs = global.callstacks[pid];

        // Recreate the steps
        twostep(
            sc,
            ctx,
            global.callstacks[pid],
            edge_input(e)->choice,
            e->invariant_chk,
            edge_output(e)->nsteps,
            pid,
            macro
        );
        // assert(global.processes[pid] == edge_output(e)->after || edge_output(e)->after == 0);

        // printf("Set %d to %p\n", pid, (void *) edge_output(e)->after);

        // Copy thread state
        macro->nprocesses = global.nprocesses;
        macro->processes = copy(global.processes, global.nprocesses * sizeof(hvalue_t));
        macro->callstacks = copy(global.callstacks, global.nprocesses * sizeof(struct callstack *));
    }

    free(sc);
}

static void path_output_microstep(
    FILE *file,
    struct microstep *micro,
    struct state *oldstate,
    struct context *oldctx,
    struct callstack *oldcs
){
    fprintf(file, "\n        {\n");
    struct json_value *next = global.pretty->u.list.vals[oldctx->pc];
    assert(next->type == JV_LIST);
    assert(next->u.list.nvals == 2);
    struct json_value *opstr = next->u.list.vals[0];
    assert(opstr->type == JV_ATOM);
    char *op = json_escape(opstr->u.atom.base, opstr->u.atom.len);
    fprintf(file, "          \"code\": \"%s\",\n", op);
    free(op);

    if (strlen(micro->explain) == 0) {
        struct json_value *next = global.pretty->u.list.vals[oldctx->pc];
        assert(next->type == JV_LIST);
        assert(next->u.list.nvals == 2);
        struct json_value *codestr = next->u.list.vals[1];
        assert(codestr->type == JV_ATOM);
        char *v = json_escape(codestr->u.atom.base, codestr->u.atom.len);
        fprintf(file, "          \"explain\": \"%s\",\n", v);
        fprintf(file, "          \"explain2\": { \"text\": \"%s\", \"args\": [] },\n", v);
        free(v);
    }
    else {
        // backwards compatibility with explain
        struct strbuf sb;
        strbuf_init(&sb);
        int argc = 0;
        for (char *p = micro->explain; *p != 0; p++) {
            if (*p == '#') {
                p++;
                if (*p == 0) {
                    break;
                }
                if (*p == '+') {
                    strbuf_value_string(&sb, micro->args[argc++]);
                }
                else if (*p == '@') {       // variable address
                    char *p = value_string(micro->args[argc++]);
                    strbuf_append(&sb, p + 1, strlen(p) - 1);
                    free(p);
                }
                else {
                    strbuf_append(&sb, p, 1);
                }
            }
            else {
                strbuf_append(&sb, p, 1);
            }
        }
        char *v = json_escape(strbuf_getstr(&sb), strbuf_getlen(&sb));
        strbuf_deinit(&sb);
        fprintf(file, "          \"explain\": \"%s\",\n", v);
        free(v);

        fprintf(file, "          \"explain2\": { \"text\": \"%s\", \"args\": [", micro->explain);
        for (unsigned int i = 0; i < micro->nargs; i++) {
            if (i != 0) {
                fprintf(file, ",");
            }
            char *s = value_json(micro->args[i]);
            fprintf(file, " %s", s);
            free(s);
        }
        fprintf(file, " ] },\n");
    }

    if (micro->state->vars != oldstate->vars) {
        fprintf(file, "          \"shared\": ");
        print_vars(file, micro->state->vars);
        fprintf(file, ",\n");
    }
    if (micro->interrupt) {
        fprintf(file, "          \"interrupt\": \"True\",\n");
    }
    if (micro->choose) {
        char *val = value_json(micro->choice);
        fprintf(file, "          \"choose\": %s,\n", val);
        free(val);
    }
    if (micro->print != 0) {
        char *val = value_json(micro->print);
        fprintf(file, "          \"print\": %s,\n", val);
        free(val);
    }

    struct context *newctx = micro->ctx;
    struct callstack *newcs = micro->cs;

    fprintf(file, "          \"npc\": \"%d\",\n", newctx->pc);
    if (newcs != NULL && newcs != oldcs) {
        fprintf(file, "          \"fp\": \"%d\",\n", newcs->sp + 1);
#ifdef notdef
        {
            fprintf(stderr, "STACK2 %d:\n", newctx->fp);
            for (int x = 0; x < newctx->sp; x++) {
                fprintf(stderr, "    %d: %s\n", x, value_string(ctx_stack(newctx)[x]));
            }
        }
#endif

        fprintf(file, "          \"trace\": [\n");
        value_trace(file, newcs, newctx->pc, newctx->vars, "          ");
        fprintf(file, "\n");
        fprintf(file, "          ],\n");
    }
    // TODO.  Shouldn't this check if the oldctx is also extended?
    if (newctx->extended && ctx_this(newctx) != ctx_this(oldctx)) {
        char *val = value_json(ctx_this(newctx));
        fprintf(file, "          \"this\": %s,\n", val);
        free(val);
    }
    if (newctx->vars != oldctx->vars) {
        fprintf(file, "          \"local\": ");
        print_vars(file, newctx->vars);
        fprintf(file, ",\n");
    }
    if (newctx->atomic != oldctx->atomic) {
        fprintf(file, "          \"atomic\": \"%d\",\n", newctx->atomic);
    }
    if (newctx->readonly != oldctx->readonly) {
        fprintf(file, "          \"readonly\": \"%d\",\n", newctx->readonly);
    }
    if (newctx->interruptlevel != oldctx->interruptlevel) {
        fprintf(file, "          \"interruptlevel\": \"%d\",\n", newctx->interruptlevel ? 1 : 0);
    }
    if (newctx->failed) {
        char *val = value_string(ctx_failure(newctx));
        fprintf(file, "          \"failure\": %s,\n", val);
        fprintf(file, "          \"mode\": \"failed\",\n");
        free(val);
    }
    else if (newctx->terminated) {
        fprintf(file, "          \"mode\": \"terminated\",\n");
    }

    unsigned int common;
    for (common = 0; common < newctx->sp && common < oldctx->sp; common++) {
        if (ctx_stack(newctx)[common] != ctx_stack(oldctx)[common]) {
            break;
        }
    }
    if (common < oldctx->sp) {
        fprintf(file, "          \"pop\": \"%d\",\n", oldctx->sp - common);
    }
    fprintf(file, "          \"push\": [");
    for (unsigned int i = common; i < newctx->sp; i++) {
        if (i > common) {
            fprintf(file, ",");
        }
        char *val = value_json(ctx_stack(newctx)[i]);
        fprintf(file, " %s", val);
        free(val);
    }
    fprintf(file, " ],\n");

#ifdef notdef
    unsigned int bs = oldstate->bagsize * (sizeof(hvalue_t) + 1);
    if (oldstate->bagsize != micro->state->bagsize ||
            memcmp(state_contexts(oldstate), state_contexts(micro->state), bs) != 0) {
        fprintf(file, "          \"contexts\": \"%d\",\n", micro->state->bagsize);
    }
#endif

    fprintf(file, "          \"pc\": \"%d\"\n", oldctx->pc);

    fprintf(file, "        }");
}

static void path_output_macrostep(FILE *file, struct macrostep *macro, struct state *oldstate){
    fprintf(file, "    {\n");
    fprintf(file, "      \"id\": \"%d\",\n", macro->edge->dst->id);
    // fprintf(file, "      \"len\": \"%d\",\n", macro->edge->dst->len);
    fprintf(file, "      \"tid\": \"%d\",\n", macro->tid);

    fprintf(file, "      \"shared\": ");
    print_vars(file, oldstate->vars);
    fprintf(file, ",\n");

    struct callstack *cs = macro->cs;
    while (cs->parent != NULL) {
        cs = cs->parent;
    }
    assert(strcmp(global.code.instrs[cs->pc].oi->name, "Frame") == 0);
    const struct env_Frame *ef = global.code.instrs[cs->pc].env;
    char *name = value_string(ef->name);
    int len = strlen(name);
    char *arg = json_escape_value(cs->arg);
    if (*arg == '(') {
        fprintf(file, "      \"name\": \"%.*s%s\",\n", len - 2, name + 1, arg);
    }
    else {
        fprintf(file, "      \"name\": \"%.*s(%s)\",\n", len - 2, name + 1, arg);
    }
    free(name);
    free(arg);

    if (edge_input(macro->edge)->choice == (hvalue_t) -1) {
        fprintf(file, "      \"interrupt\": 1,\n");
    }
    else if (edge_input(macro->edge)->choice != 0) {
        char *c = value_json(edge_input(macro->edge)->choice);
        fprintf(file, "      \"choice\": %s,\n", c);
        free(c);
    }

    fprintf(file, "      \"context\": {\n");
    print_context(file, edge_input(macro->edge)->ctx, macro->cs, macro->tid, macro->edge->dst, "        ");
    fprintf(file, "      },\n");

    if (macro->trim != NULL && macro->value != 0) {
        char *value = value_json(macro->value);
        fprintf(file, "      \"trim\": %s,\n", value);
        free(value);
    }

    fprintf(file, "      \"microsteps\": [");
    struct context *oldctx = value_get(edge_input(macro->edge)->ctx, NULL);
    struct callstack *oldcs = NULL;
    for (unsigned int i = 0; i < macro->nmicrosteps; i++) {
        struct microstep *micro = macro->microsteps[i];
        path_output_microstep(file, micro, oldstate, oldctx, oldcs);
        if (i == macro->nmicrosteps - 1) {
            fprintf(file, "\n");
        }
        else {
            fprintf(file, ",\n");
        }
        memcpy(oldstate, micro->state, state_size(micro->state));
        oldctx = micro->ctx;
        oldcs = micro->cs;
    }
    fprintf(file, "\n      ],\n");
  
    fprintf(file, "      \"ctxbag\": {\n");
    struct state *state = node_state(macro->edge->dst);
    for (unsigned int i = 0; i < state->bagsize; i++) {
        if (i > 0) {
            fprintf(file, ",\n");
        }
        assert(VALUE_TYPE(state_contexts(state)[i]) == VALUE_CONTEXT);
        fprintf(file, "          \"%"PRIx64"\": \"%u\"", state_contexts(state)[i],
                multiplicities(state)[i]);
    }
    fprintf(file, "\n      },\n");

    fprintf(file, "      \"contexts\": [\n");
    for (unsigned int i = 0; i < macro->nprocesses; i++) {
        fprintf(file, "        {\n");
        print_context(file, macro->processes[i], macro->callstacks[i], i, macro->edge->dst, "          ");
        fprintf(file, "        }");
        if (i < macro->nprocesses - 1) {
            fprintf(file, ",");
        }
        fprintf(file, "\n");
    }
    fprintf(file, "      ]\n");

    fprintf(file, "    }");
}

// Two edges conflict if they access the same variable and at least one
// of the accesses is a store.  An access is identified by a path.  Two
// accesses are to the same variable if one of the paths is a prefix of
// the other.
bool path_edge_conflict(
    struct edge *edge,
    struct edge *edge2
) {
    for (struct access_info *ai = edge_output(edge)->ai; ai != NULL; ai = ai->next) {
        if (ai->indices != NULL) {
            for (struct access_info *ai2 = edge_output(edge2)->ai; ai2 != NULL; ai2 = ai2->next) {
                if (ai2->indices != NULL && !(ai->load && ai2->load)) {
                    int min = ai->n < ai2->n ? ai->n : ai2->n;
                    assert(min > 0);
                    if (memcmp(ai->indices, ai2->indices,
                               min * sizeof(hvalue_t)) == 0) {
                        return true;
                    }
                }
            }
        }
    }
    return false;
}

// Optimize the path by reordering macrosteps. One cannot reorder macrosteps
// that conflict.  Macrosteps conflict if they are by the same thread or
// if they print something or if they read/write conflicting variables.
static void path_optimize(){
    struct ctxblock {
        hvalue_t before, after;
        unsigned int start, end;
    };
    struct ctxblock *cbs;
    unsigned int ncbs;
    hvalue_t current;

again:

#ifdef notdef
    current = 0;
    printf("Path:");
    for (unsigned int i = 0; i < global.nmacrosteps; i++) {
        struct edge *e = global.macrosteps[i]->edge;
        if (edge_input(e)->ctx != current) {
            printf("\n");
        }
        printf(" %u [", e->src->id);
        for (struct access_info *ai = e->ai; ai != NULL; ai = ai->next) {
            char *p = indices_string(ai->indices, ai->n);
            if (ai->load) {
                printf(" load %s", p);
            }
            else {
                printf(" store %s", p);
            }
            free(p);
        }
        printf(" ]");
        current = edge_output(e)->after;
    }
    printf(" %u\n", global.macrosteps[global.nmacrosteps - 1]->edge->dst->id);
#endif

    cbs = calloc(1, sizeof(*cbs));
    cbs->before = edge_input(global.macrosteps[0]->edge)->ctx;
    ncbs = 0;
    current = edge_output(global.macrosteps[0]->edge)->after;

    // Figure out where the actual context switches are.  Each context
    // block is a sequence of edges executed by the same thread
    for (unsigned int i = 1; i < global.nmacrosteps; i++) {
        if (edge_input(global.macrosteps[i]->edge)->ctx != current) {
            cbs[ncbs].after = current;
            cbs[ncbs++].end = i;
            cbs = realloc(cbs, (ncbs + 1) * sizeof(*cbs));
            cbs[ncbs].start = i;
            cbs[ncbs].before = edge_input(global.macrosteps[i]->edge)->ctx;
        }
        current = edge_output(global.macrosteps[i]->edge)->after;
    }
    cbs[ncbs].after = current;
    cbs[ncbs++].end = global.nmacrosteps;

#ifdef notdef
    printf("%u blocks:\n", ncbs);
    for (unsigned int i = 0; i < ncbs; i++) {
        printf("   %llx %u %u\n", cbs[i].before, cbs[i].start, cbs[i].end);
    }
#endif

    // Now try to reorder and combine context blocks.  Context block 0
    // is for the initial thread, so we can skip it
    for (unsigned int i = 1; i < ncbs; i++) {
        // Find the next context block for the same thread, if any.  Stop
        // if there are any conflicts
        for (unsigned int j = i + 1; j < ncbs; j++) {
            if (cbs[i].after == cbs[j].before) {
                // printf("SWAP %u (%u %u) %u (%u %u)\n", i, cbs[i].start, cbs[i].end, j, cbs[j].start, cbs[j].end);
                // Combine block i with block j by moving block i up
                // First save block i
                unsigned int size = (cbs[i].end - cbs[i].start) *
                                                sizeof(struct macrostep *);
                struct macrostep **copy = malloc(size);
                memcpy(copy, &global.macrosteps[cbs[i].start], size);

                // Then move over the blocks in between
                memcpy(&global.macrosteps[cbs[i].start],
                        &global.macrosteps[cbs[i+1].start],
                        (cbs[j].start - cbs[i+1].start) *
                                            sizeof(struct macrostep *));

                // Move the saved block over
                memcpy(&global.macrosteps[cbs[j].start -
                            (cbs[i].end - cbs[i].start)], copy, size);
                free(copy);
                free(cbs);
                goto again;         // TODO
            }

            // See if there are conflicts
            bool conflict = false;
            for (unsigned int x = cbs[i].start; !conflict && x < cbs[i].end; x++) {
                for (unsigned int y = cbs[j].start; !conflict && y < cbs[j].end; y++) {
                    if ((edge_output(global.macrosteps[x]->edge)->nlog > 0 &&
                                edge_output(global.macrosteps[y]->edge)->nlog > 0) ||
                            path_edge_conflict(
                                    global.macrosteps[x]->edge,
                                    global.macrosteps[y]->edge)) {
                        conflict = true;
                    }
                }
            }
            if (conflict) {
                // printf("%u and %u conflict\n", i, j);
                break;
            }
        }
    }

    // Now fix the edges.
    struct node *node = global.graph.nodes[0];
    for (unsigned int i = 0; i < global.nmacrosteps; i++) {
        // printf("--> %u/%u\n", i, global.nmacrosteps);
        // Find the edge
        hvalue_t ctx = edge_input(global.macrosteps[i]->edge)->ctx;
        hvalue_t choice = edge_input(global.macrosteps[i]->edge)->choice;
        struct edge *e;
        for (e = node->fwd; e != NULL; e = e->fwdnext) {
            if (edge_input(e)->ctx == ctx && edge_input(e)->choice == choice) {
                global.macrosteps[i]->edge = e;
                break;
            }
        }

        // TODO.  This should generally never happen, but it can
        //        happen for the fake edges that are added at the
        //        end in the case of invariant or finally violations.
        if (e == NULL) {
            if (i != global.nmacrosteps - 1)
                printf("KLUDGE %d %d\n", i, global.nmacrosteps - 1);
            assert(i == global.nmacrosteps - 1);
            break;
        }
        global.macrosteps[i]->edge = e;
        node = e->dst;
    }
}

// Output the macrosteps
static void path_output(FILE *file){
    fprintf(file, "\n");
    struct state *oldstate = calloc(1, sizeof(struct state) + MAX_CONTEXT_BAG * (sizeof(hvalue_t) + 1));
    oldstate->vars = VALUE_DICT;
    for (unsigned int i = 0; i < global.nmacrosteps; i++) {
        path_output_macrostep(file, global.macrosteps[i], oldstate);
        if (i == global.nmacrosteps - 1) {
            fprintf(file, "\n");
        }
        else {
            fprintf(file, ",\n");
        }
    }
}

// Remove unneeded microsteps from error trace
static void path_trim(struct allocator *allocator){
    // Find the last macrostep for each thread
    unsigned int *last = calloc(global.nprocesses, sizeof(*last));
    for (unsigned int i = 0; i < global.nmacrosteps; i++) {
        last[global.macrosteps[i]->tid] = i;
    }

    struct instr *instrs = global.code.instrs;
    for (unsigned int i = 1; i < global.nprocesses; i++) {
        // Don't trim the very last step
        if (last[i] == global.nmacrosteps - 1) {
            continue;
        }
        struct macrostep *macro = global.macrosteps[last[i]];

        // Look up the last microstep of this thread, which wasn't the
        // last one to take a step overall
        struct context *cc = value_get(edge_input(macro->edge)->ctx, NULL);
        struct microstep *ls = macro->microsteps[macro->nmicrosteps - 1];
        struct instr *fi = &instrs[cc->pc];
        struct instr *li = &instrs[ls->ctx->pc];
        if ((fi->store || fi->load || fi->print) && (li->store || li->load || li->print)) {

            macro->nmicrosteps = 1;

            macro->trim = fi;
            if (fi->store) {
                struct access_info *ai = edge_output(macro->edge)->ai;
                assert(ai != NULL);
                assert(ai->next == NULL);
                assert(!ai->load);
                assert(!ai->atomic);
                macro->value = value_put_address(allocator, ai->indices, ai->n * sizeof(hvalue_t));
            }
            else if (fi->print) {
                assert(edge_output(macro->edge)->nlog == 1);
                hvalue_t *log = step_log(edge_output(macro->edge));
                macro->value = log[0];
            }

            hvalue_t ictx = value_put_context(allocator, macro->microsteps[0]->ctx);
            for (unsigned int j = last[i]; j < global.nmacrosteps; j++) {
                struct macrostep *m = global.macrosteps[j];
                m->processes[macro->tid] = ictx;
                m->callstacks[macro->tid] = macro->microsteps[0]->cs;
            }
        }
    }
}

// Function to add escapes to a string so it can be used in JSON output.
static char *json_string_encode(char *s, int len){
    char *result = malloc(4 * len + 1), *p = result;

    while (len > 0) {
        switch (*s) {
        case '\r':
            *p++ = '\\'; *p++ = 'r';
            break;
        case '\n':
            *p++ = '\\'; *p++ = 'n';
            break;
        case '\f':
            *p++ = '\\'; *p++ = 'f';
            break;
        case '\t':
            *p++ = '\\'; *p++ = 't';
            break;
        case '"':
            *p++ = '\\'; *p++ = '"';
            break;
        case '\\':
            *p++ = '\\'; *p++ = '\\';
            break;
        default:
            *p++ = *s;
        }
        s++;
        len--;
    }
    *p++ = 0;
    return result;
}

#ifdef notdef

struct enum_loc_env_t {
    FILE *out;
    struct dict *code_map;
};

static void enum_loc(
    void *env,
    const void *key,
    unsigned int key_size,
    void *value
) {
    static bool notfirst = false;
    struct enum_loc_env_t *enum_loc_env = env;
    FILE *out = enum_loc_env->out;
    struct dict *code_map = enum_loc_env->code_map;

    if (notfirst) {
        fprintf(out, ",\n");
    }
    else {
        notfirst = true;
        fprintf(out, "\n");
    }

    // Get program counter
    char *pcc = malloc(key_size + 1);
    memcpy(pcc, key, key_size);
    pcc[key_size] = 0;
    int pc = atoi(pcc);
    free(pcc);

    fprintf(out, "    \"%.*s\": { ", key_size, (char *) key);

    struct json_value **pjv = value;
    struct json_value *jv = *pjv;
    assert(jv->type == JV_MAP);

    struct json_value *file = dict_lookup(jv->u.map, "file", 4);
    assert(file->type == JV_ATOM);
    fprintf(out, "\"file\": \"%s\", ", json_string_encode(file->u.atom.base, file->u.atom.len));

    struct json_value *line = dict_lookup(jv->u.map, "line", 4);
    assert(line->type == JV_ATOM);
    fprintf(out, "\"line\": \"%.*s\", ", line->u.atom.len, line->u.atom.base);

    static char *tocopy[] = { "column", "endline", "endcolumn", NULL };
    for (unsigned int i = 0; tocopy[i] != NULL; i++) {
        char *key2 = tocopy[i];
        struct json_value *jv2 = dict_lookup(jv->u.map, key2, strlen(key2));
        assert(jv2->type == JV_ATOM);
        fprintf(out, "\"%s\": \"%.*s\", ", key2, jv2->u.atom.len, jv2->u.atom.base);
    }

    struct json_value *stmt = dict_lookup(jv->u.map, "stmt", 4);
    assert(stmt->type == JV_LIST);
    assert(stmt->u.list.nvals == 4);
    fprintf(out, "\"stmt\": [");
    for (unsigned int i = 0; i < 4; i++) {
        if (i != 0) {
            fprintf(out, ",");
        }
        struct json_value *jv2 = stmt->u.list.vals[i];
        assert(jv2->type == JV_ATOM);
        fprintf(out, "%.*s", jv2->u.atom.len, jv2->u.atom.base);
    }
    fprintf(out, "], ");

    char **p = dict_insert(code_map, NULL, &pc, sizeof(pc), NULL);
    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, "%.*s:%.*s", file->u.atom.len, file->u.atom.base, line->u.atom.len, line->u.atom.base);
    *p = strbuf_convert(&sb);

    struct json_value *code = dict_lookup(jv->u.map, "code", 4);
    assert(code->type == JV_ATOM);
    fprintf(out, "\"code\": \"%s\"", json_string_encode(code->u.atom.base, code->u.atom.len));
    fprintf(out, " }");
}

#endif // notdef

enum busywait { BW_ESCAPE, BW_RETURN, BW_VISITED };
static enum busywait is_stuck(
    struct node *start,
    struct node *node,
    hvalue_t ctx,
    bool change
) {
    if (scc[node->id].component != scc[start->id].component) {
        return BW_ESCAPE;
    }
    if (node->visited) {
        return BW_VISITED;
    }
    change = change || (node_state(node)->vars != node_state(start)->vars);
    node->visited = true;
    enum busywait result = BW_ESCAPE;
    for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
        if (edge_input(edge)->ctx == ctx) {
            if (edge->dst == node) {
                node->visited = false;
                return BW_ESCAPE;
            }
            if (edge->dst == start) {
                if (!change) {
                    node->visited = false;
                    return BW_ESCAPE;
                }
                result = BW_RETURN;
            }
            else {
                enum busywait bw = is_stuck(start, edge->dst, edge_output(edge)->after, change);
                switch (bw) {
                case BW_ESCAPE:
                    node->visited = false;
                    return BW_ESCAPE;
                case BW_RETURN:
                    result = BW_RETURN;
                    break;
                case BW_VISITED:
                    break;
                default:
                    assert(false);
                }
            }
        }
    }
    node->visited = false;
    return result;
}

void add_failure(struct failure **failures, struct failure *f) {
    f->next = *failures;
    *failures = f;
}

static void detect_busywait(struct node *node){
    for (unsigned int i = 0; i < node_state(node)->bagsize; i++) {
        if (is_stuck(node, node, state_contexts(node_state(node))[i], false) == BW_RETURN) {
            struct failure *f = new_alloc(struct failure);
            f->type = FAIL_BUSYWAIT;
            f->edge = node_to_parent(node);
            add_failure(&global.failures, f);
            // break;
        }
    }
}

// This function evaluates a node just taken from the todo list by the worker.
// Any new nodes that are found are kept in w->workers and not yet added to
// the todo list or the graph.
void do_work1(struct worker *w, struct node *node){
    // If the node is the result of a failed transition, don't explore it
    if (node->failed) {
        return;
    }

#ifndef OLD_PACIFIER
    // Worker 0 periodically (every second) prints some stats for long runs.
    // To avoid calling gettime() very often, which may involve an expensive
    // system call, worker 0 only checks every 100 instructions.
    if (w->index == 0 && w->timecnt-- == 0) {
        double now = gettime();
        if (now - global.lasttime > 3) {
            if (global.lasttime != 0) {
                unsigned int enqueued = 0, dequeued = 0;
                unsigned long allocated = global.allocated;

                for (unsigned int i = 0; i < w->nworkers; i++) {
                    struct worker *w2 = &w->workers[i];
                    enqueued += w2->enqueued;
                    dequeued += w2->dequeued;
                    allocated += w2->allocated;
                }
                double gigs = (double) allocated / (1 << 30);
                fprintf(stderr, "states=%u diam=%u q=%d mem=%.3lfGB\n",
                        enqueued, global.diameter,
                        enqueued - dequeued, gigs);
                global.last_nstates = enqueued;
            }
            global.lasttime = now;
            if (now > w->timeout) {
                fprintf(stderr, "charm: timeout exceeded\n");
                exit(1);
            }
        }
        w->timecnt = 1000;
    }
#endif // OLD_PACIFIER

    // See what type of state it is.  There are two kinds of states: choosing
    // states and non-choosing states.  In case of choosing states, we explore
    // the possible choices for the thread that is executing.  For a non-choosing
    // state, we explore all the different threads that can make a step.
    struct state *state = node_state(node);
    if (state->chooser >= 0) {
        // The actual set of choices is on top of its stack
        hvalue_t chooser = state_contexts(state)[state->chooser];
        struct context *cc = value_get(chooser, NULL);
        assert(cc != NULL);
        assert(cc->sp > 0);
        hvalue_t s = ctx_stack(cc)[cc->sp - 1];
        assert(VALUE_TYPE(s) == VALUE_SET);
        unsigned int size;
        hvalue_t *vals = value_get(s, &size);
        size /= sizeof(hvalue_t);
        assert(size > 0);

        // Explore each choice.
        for (unsigned int i = 0; i < size; i++) {
            make_step(w, node, state->chooser, vals[i]);
        }
    }
    else {
        // Explore each thread that can make a step.
        for (unsigned int i = 0; i < state->bagsize; i++) {
            assert(VALUE_TYPE(state_contexts(state)[i]) == VALUE_CONTEXT);
            make_step(w, node, i, 0);
        }

        // Also check the invariants after initialization
        if (node->id != 0) {
            struct state *state = node_state(node);
            // TODO.  Make this check cheaper somehow
            bool final = global.nfinals > 0
                    && value_state_all_eternal(state)
                    && value_ctx_all_eternal(state->stopbag);
            chk_invs(w, node, final);
        }
    }
}

// A worker thread executes this in "phase 1" of the worker loop, when all
// workers are evaluating states and their transitions.  The states are
// stored in global.graph as an array.  global.graph.size contains the
// number of nodes that have been inserted into the graph.  global.todo,
// or global.atodo (depending on whether atomics are used or not) points
// into this array.  All the nodes before todo have been explored, while the
// ones after todo should be explored.  In other words, the "todo list" starts
// at global.graph.nodes[global.todo] and ends at graph.nodes[graph.size];
// However, there is also a global.goal that indexes into global.graph.nodes.
// Workers move on to phase 2 when the goal is reached, to give charm an
// opportunity to grow the hash tables which might otherwise become inefficient.
static void do_work(struct worker *w){
    unsigned int todo_count = 5;        // TODO probably should just be a constant

    for (;;) {
        // Grab one or a few states to evaluate.  When not using atomics, we
        // do a few to avoid the overhead of contention on the lock.  Note that
        // it is possible that as a result todo or atodo ends up being larger
        // than graph.size.
#ifdef USE_ATOMIC
        unsigned int next = atomic_fetch_add(&global.atodo, todo_count);
#else // USE_ATOMIC
        mutex_acquire(&global.todo_lock);
        unsigned int next = global.todo;
        global.todo += todo_count;
        mutex_release(&global.todo_lock);
#endif // USE_ATOMIC

        // Call do_work1() for each node we picked off the todo list.  It explores
        // the node and adds new nodes that are found to w->results.
        for (unsigned int i = 0; i < todo_count; i++, next++) {
            // printf("W%d %d %d\n", w->index, next, global.graph.size);
            // TODO: why not check for reaching the goal here instead of below?
            if (next >= global.graph.size) {
                return;
            }
            w->dequeued++;
            do_work1(w, global.graph.nodes[next]);
        }

        // Stop if the goal has been reached.
        if (next >= global.goal) {
            break;
        }
    }
}

// Copy all the failures that the individuals worker threads discovered
// into the global failures list.
static void collect_failures(struct worker *w){
    struct failure *f;
    while ((f = w->failures) != NULL) {
        w->failures = f->next;
        add_failure(&global.failures, f);
    }
}

// Add a new virtual processor to the list and determine its
// ``hyper_id'' (hyperthread id) to make the identifier
// (phys_id, core_id, hyper_id) unique.
static bool cpuinfo_addrecord(int processor, int phys_id, int core_id){
    if (processor < 0) {
        fprintf(stderr, "cpuinfo_addrecord: no processor id?\n");
        return false;
    }
    if (phys_id < 0) {
        fprintf(stderr, "cpuinfo_addrecord: processor without physical id\n");
        return false;
    }
    if (core_id < 0) {
        fprintf(stderr, "cpuinfo_addrecord: processor without core id\n");
        return false;
    }
    if ((unsigned) processor >= n_vproc_info) {
        fprintf(stderr, "cpuinfo_addrecord: processor id too large\n");
        return true;        // pretend it didn't happen
    }
    vproc_info[processor].ids[0] = phys_id;
    vproc_info[processor].ids[1] = 0;
    vproc_info[processor].ids[2] = core_id;
    for (int i = 0; i < processor; i++) {
        if (vproc_info[i].ids[0] == phys_id &&
                            vproc_info[i].ids[2] == core_id) {
            vproc_info[processor].ids[1]++;
        }
    }
    return true;
}

// Like POSIX getline, but works in Windows too
int my_getline(char **buf, size_t *cap, FILE *fp) {
    int c = fgetc(fp);
    if (c == EOF) {
        return -1;
    }
    size_t offset = 0;
    do {
        if (offset >= *cap) {
            *cap += LINE_CHUNK;
            if ((*buf = realloc(*buf, *cap)) == NULL) {
                return -1;
            }
        }
        if (((*buf)[offset++] = c) == '\n') {
            break;
        }
    } while ((c = fgetc(fp)) != EOF);
    (*buf)[offset] = '\0';
    return offset;
}

// Read the /proc/cpuinfo file if available to get info about the
// architecture.  Return false if something goes wrong.
static bool get_cpuinfo(){
    FILE *fp;
    if ((fp = fopen("/proc/cpuinfo", "r")) == NULL) {
        return false;
    }
    char *line = NULL;
    size_t alloced = 0;
    int processor = -1, phys_id = -1, core_id = -1;

    // Go through the lines one by one
    for (;;) {
        // Read a line
        int n = my_getline(&line, &alloced, fp);
        if (n <= 0) {
            break;
        }

        // Find the separator
        char *value = strchr(line, ':');
        if (value == NULL) {
            continue;
        }

        // Trim the key
        for (char *q = value;;) {
            q--;
            if (*q != ' ' && *q != '\t') {
                *++q = '\0';
                break;
            }
        }

        // Find the start of the value
        for (;;) {
            value++;
            if (*value == '\0' || (*value != ' ' && *value != '\n')) {
                break;
            }
        }

        // Trim the end of the value
        for (char *q = line + n;;) {
            if (q == value) {
                *q = '\0';
                break;
            }
            q--;
            if (*q != ' ' && *q != '\t' && *q != '\n' && *q != '\r') {
                q[1] = '\0';
                break;
            }
        }

        // See if it's the start of a new processor record.
        if (strcmp(line, "processor") == 0) {
            if (processor >= 0) {
                if (!cpuinfo_addrecord(processor, phys_id, core_id)) {
                    return false;
                }
            }
            int prid = atoi(value);
            processor++;
            if (prid != processor) {
                fprintf(stderr, "/proc/cpuinfo: unexpected processor id\n");
                return false;
            }
            phys_id = core_id = -1;
        }

        // Get info about the processor
        if (strcmp(line, "physical id") == 0) {
            phys_id = atoi(value);
        }
        if (strcmp(line, "core id") == 0) {
            core_id = atoi(value);
        }
    }
    if (!cpuinfo_addrecord(processor, phys_id, core_id)) {
        return false;
    }
    if ((unsigned) processor != n_vproc_info - 1) {
        fprintf(stderr, "/proc/cpuinfo: not all processors?\n");
        return false;
    }
    return true;
}

static void vproc_info_dump(){
    for (unsigned int i = 0; i < n_vproc_info; i++) {
        printf("%u:", i);
        for (unsigned int j = 0; j < vproc_info[i].nids; j++) {
            printf(" %d", vproc_info[i].ids[j]);
        }
        printf("\n");
    }
}

static void vproc_info_create(){
    n_vproc_info = getNumCores();
    vproc_info = calloc(n_vproc_info, sizeof(struct vproc_info));
    for (unsigned int i = 0; i < n_vproc_info; i++) {
        vproc_info[i].nids = 3;     // currently hardwired
        vproc_info[i].ids = calloc(vproc_info[i].nids, sizeof(int));
    }

    // See if we can read /proc/cpuinfo for more info
    if (n_vproc_info > 1 && !get_cpuinfo()) {
        // Pretend there is just one socket and two hyperthreads per core
        unsigned int half = n_vproc_info / 2;
        for (unsigned int i = 0; i < half; i++) {
            vproc_info[i].ids[2] = i;
        }
        for (unsigned int i = 0; i < half; i++) {
            vproc_info[half + i].ids[1] = 1;
            vproc_info[half + i].ids[2] = i;
        }
    }
}

static bool vproc_match(struct vproc_info *vi, struct pattern *pat){
    for (unsigned int k = 0; k < pat->nids; k++) {
        if (k >= vi->nids) {
            return false;
        }
        if (!pat->ids[k].wildcard && pat->ids[k].id != vi->ids[k]) {
            return false;
        }
    }
    return true;
}

// Insert a virtual processor into the tree recursively.  Return
// a pointer to the new leaf node.
static struct vproc_tree *vproc_tree_insert(
    struct vproc_tree *parent,
    int *ids,             // local id 'path'
    unsigned int len,     // length of path
    unsigned int offset   // offset into path
){
    parent->n_vprocessors++;
    if (offset == len) {
        assert(parent->nchildren == 0);
        assert(parent->n_vprocessors == 1);
        return parent;
    }
    for (unsigned int i = 0; i < parent->nchildren; i++) {
        if (parent->children[i].local_id == ids[offset]) {
            return vproc_tree_insert(parent->children[i].child, ids, len, offset + 1);
        }
    }
    struct vproc_tree *vt = calloc(1, sizeof(*vt));
    parent->children = realloc(parent->children,
                (parent->nchildren + 1) * sizeof(struct vproc_map));
    parent->children[parent->nchildren].local_id = ids[offset];
    parent->children[parent->nchildren].child = vt;
    parent->nchildren++;
    return vproc_tree_insert(vt, ids, len, offset + 1);
}

#ifdef OBSOLETE
// Find a virtual processor into the tree recursively.
static struct vproc_tree *vproc_tree_find(
    struct vproc_tree *parent,
    unsigned int *ids,              // local id 'path'
    unsigned int len,               // length of path
    unsigned int offset             // offset into path
){
    if (offset == len) {
        return parent;
    }
    for (unsigned int i = 0; i < parent->nchildren; i++) {
        if (parent->children[i].local_id == ids[offset]) {
            return vproc_tree_find(parent->children[i].child, ids, len, offset + 1);
        }
    }
    return NULL;
}

// For debugging, dump the contents of the virtual processor tree
static void vproc_tree_dump(struct vproc_tree *vt, unsigned int level){
    printf("%p; vid = %u; # = %u", vt, vt->virtual_id, vt->n_vprocessors);
    if (vt->nchildren > 0) {
        printf("; nchildren = %u:", vt->nchildren);
    }
    printf("\n");
    for (unsigned int i = 0; i < vt->nchildren; i++) {
        for (unsigned int j = 0; j < level; j++) {
            printf(" ");
        }
        printf("%u: ", vt->children[i].local_id);
        vproc_tree_dump(vt->children[i].child, level + 1);
    }
}
#endif // OBSOLETE

// This function creates a tree, more or less representing the memory
// hierarchy, with the selected virtual processors at its leaves.
static void vproc_tree_create(){
    // Create the virtual processor tree.
    vproc_root = calloc(1, sizeof(*vproc_root));
    for (unsigned int i = 0; i < n_vproc_info; i++) {
        if (vproc_info[i].selected) {
            struct vproc_tree *vt = vproc_tree_insert(vproc_root, vproc_info[i].ids, vproc_info[i].nids, 0);
            vt->virtual_id = i;
        }
    }
}

// Allocate n virtual processors, eagerly.
void vproc_tree_alloc(struct vproc_tree *vt, struct worker *workers, unsigned int *index, unsigned int n){
    assert(n > 0);
    assert(n <= vt->n_vprocessors);

    // Allocate if this is a leaf node.
    if (vt->nchildren == 0) {
        assert(n == 1);
        assert(vt->n_vprocessors == 1);
        // printf("Alloc %u to %u\n", vt->virtual_id, *index);
        workers[*index].vproc = vt->virtual_id;
        (*index)++;
        return;
    }

    // See if there is a child that can fit them all.
    for (unsigned int i = 0; i < vt->nchildren; i++) {
        if (n <= vt->children[i].child->n_vprocessors) {
            vproc_tree_alloc(vt->children[i].child, workers, index, n);
            return;
        }
    }

    // Spread them over the children
    for (unsigned int i = 0; i < vt->nchildren; i++) {
        struct vproc_tree *child = vt->children[i].child;
        if (n <= child->n_vprocessors) {
            vproc_tree_alloc(child, workers, index, n);
            break;
        }
        vproc_tree_alloc(child, workers, index, child->n_vprocessors);
        n -= child->n_vprocessors;
    }
}

// This is a main worker thread for the model checking phase.  arg points to
// the struct worker record for this worker.
//
// The graph is kept in an array of nodes in global.graph.nodes.  It also acts
// as the todo list, as global.todo (or global.atodo if atomics are used) points
// to the first unexplored node.  Workers then compete to take nodes of the todo
// list.  They buffer new nodes that find in their w->results list.  When the todo
// list has been exhausted, a "layer" of the Kripke structure (all nodes up to a
// certain distance or depth from the initial node) has been completed.  At that
// point the buffered nodes are all added to the graph and the next layer is
// explored.
static void worker(void *arg){
    struct worker *w = arg;
    bool done = false;

    // Pin the thread to its virtual processor.
#ifdef __linux__
    if (w->index == 0) {
        printf("pinning cores\n");
    }
    // Pin worker to a core
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(w->vproc, &cpuset);
    sched_setaffinity(0, sizeof(cpuset), &cpuset);
#endif

    // The worker now goes into a loop.  Each iteration consists of three phases.
    // Only worker 0 ever breaks out of this loop.
    for (;;) {
        // Wait for the first barrier (and keep stats)
        double before = gettime();
        barrier_wait(w->start_barrier);
        double after = gettime();
        w->start_wait += after - before;
        w->start_count++;

        // Worker 0 needs to break out of the loop when the Kripke structure
        // if finished (or when failures have been detected) so that it can
        // go on with analysis and so on.
        if (done) {
            break;
        }

        // First phase starts now.  Call do_work() to do that actual work.
        // Also keep stats.
        before = after;
        do_work(w);
        after = gettime();
        w->phase1 += after - before;

        // Wait for others to finish, and keep stats
        before = gettime();
        barrier_wait(w->middle_barrier);
        after = gettime();
        w->middle_wait += after - before;
        w->middle_count++;
        before = after;

#ifdef USE_EDGES
        // Insert the forward edges.  Each worker is responsible for a subset
        // of the nodes, so this can be done in parallel.
        for (unsigned i = 0; i < w->nworkers; i++) {
            struct edge **pe = &w->workers[i].edges[w->index], *e;
            while ((e = *pe) != NULL) {
                w->fix_edge++;
                *pe = e->fwdnext;
                struct node *src = e->src;
                e->fwdnext = src->fwd;
                src->fwd = e;
            }
        }
#endif

        // Keep more stats
        after = gettime();
        w->phase2a += after - before;
        before = after;

        // Prepare the grow the hash tables (but the actual work of
        // rehashing is distributed among the threads in the next phase
        // The only parallelism here is that workers 1 and 2 grow different
        // hash tables, while worker 0 deals with the graph table
        if (w->index == 1 % global.nworkers) {
            dict_grow_prepare(w->visited);
        }
        if (w->index == 2 % global.nworkers) {
            dict_grow_prepare(global.values);
        }
        if (w->index == 3 % global.nworkers) {
            dict_grow_prepare(global.computations);
        }

        // Only the coordinator (worker 0) does the following
        if (w->index == 0 /* % global.nworkers */) {
            // See where todo (or atodo) is at.  Because of how it's incremented
            // by the workers, it may have exceeded the size of the array of
            // nodes.  If so, we set it back here.
#ifdef USE_ATOMIC
            unsigned int todo = atomic_load(&global.atodo);
#else
            unsigned int todo = global.todo;
#endif
            if (todo > global.graph.size) {
#ifdef USE_ATOMIC
                atomic_store(&global.atodo, global.graph.size);
#else
                global.todo = global.graph.size;
#endif
                todo = global.graph.size;
            }
            // printf("SEQ: todo=%u size=%u\n", todo, global.graph.size);

            // If todo has reached the end of the array of nodes, then we're
            // done with this layer and the nodes that the workers discovered
            // and buffered in w->results must be appended to the graph.
            global.layer_done = todo == global.graph.size;
            if (global.layer_done) {
                global.diameter++;
                // printf("Diameter %d\n", global.diameter);

                // Grow the graph table.  Figure out by how much by adding up
                // the buffer sizes of each worker.  Also, assign to each worker
                // 'node_id', which points to the part of the node identifier
                // space they can use to assign node identifiers to their
                // buffered nodes.
                unsigned int total = 0;
                for (unsigned int i = 0; i < global.nworkers; i++) {
                    struct worker *w2 = &w->workers[i];
                    w2->node_id = global.graph.size + total;
                    total += w2->count;
                }

                // Grow the graph table (but do not yet copy the buffered
                // nodes into it.  The workers themselves do that in the
                // next phase.
                graph_add_multiple(&global.graph, total);
                assert(global.graph.size <= global.graph.alloc_size);

                // Collect the failures of all the workers
                for (unsigned int i = 0; i < global.nworkers; i++) {
                    collect_failures(&w->workers[i]);
                }

                // If there are any failures, pretend we're done by setting
                // todo (or atodo) to the end of the list of nodes.
                if (global.failures != NULL) {
                    // Pretend we're done
#ifdef USE_ATOMIC
                    atomic_store(&global.atodo, global.graph.size);
#else
                    global.todo = global.graph.size;
#endif
                }

                // This is still worker 0. If there are no more nodes to process
                // worker 0 should break out of this loop.
                if (total == 0) {
                    done = true;
                }
            }

            // We check here if more than 10000 nodes are on tbe todo list.  If
            // so, we explore only 10000 for now to give us a chance to grow
            // hash tables if needed for efficiency.
            //
            // TODO.  Why 10000?
            if (global.graph.size - todo > 10000) {
                global.goal = todo + 10000;
            }
            else {
                global.goal = global.graph.size;
            }

            // Compute how much table space is in use (reported in stats)
            global.allocated = global.graph.size * sizeof(struct node *) +
                dict_allocated(w->visited) + dict_allocated(global.values);
        }

        // Start the final phase (and keep stats).
        after = gettime();
        w->phase2b += after - before;
        before = after;
        barrier_wait(w->end_barrier);
        after = gettime();
        w->end_wait += after - before;
        w->end_count++;
        before = after;

        // In parallel, the workers copy the old hash table entries into the
        // new buckets.
        dict_make_stable(global.values, w->index);
        dict_make_stable(w->visited, w->index);
        dict_make_stable(global.computations, w->index);

        after = gettime();
        w->phase3a += after - before;
        before = after;

        // If a layer was completed, move the buffered nodes into the graph.
        // Worker w can assign node identifiers starting from w->node_id.
        if (global.layer_done) {
            // Fill the graph table
            unsigned int node_id = w->node_id;
            while (w->results != NULL) {
                struct results_block *rb = w->results;
                memcpy(&global.graph.nodes[node_id],
                    rb->results, rb->nresults * sizeof(struct node *));
                for (unsigned int i = 0; i < rb->nresults; i++) {
                    rb->results[i]->id = node_id++;
                }
                w->node_id = node_id;
                w->results = rb->next;
                rb->next = w->rb_free;
                w->rb_free = rb;
            }
            w->node_id = node_id;
            w->count = 0;
        }

        // Update stats
        after = gettime();
        w->phase3b += after - before;
    }
}

#define STACK_CHUNK 4096

// The stack contains pointers to either nodes or edges.
// Which of the two it is is captured in the lowest bit.
// Memory space is at premium here...
struct stack {
    struct stack *next, *prev;
    void *ptrs[STACK_CHUNK];          // low bit = 1 --> edge
    unsigned int sp;
};

static void stack_push(struct stack **sp, struct node *v1, struct edge *v2) {
    // See if there's space in the current chunk
    struct stack *s = *sp;
    if (s->sp == STACK_CHUNK) {
        if (s->next == NULL) {
            s->next = malloc(sizeof(*s));
            s->next->prev = s;
            s = s->next;
            s->sp = 0;
            s->next = NULL;
        }
        else {
            assert(s->next->prev == s);
            s = s->next;
            assert(s->sp == 0);
        }
        *sp = s;
    }

    // Push either a node or edge pointer
    if (v2 != NULL) {
        // assert(v1 == v2->src);
        s->ptrs[s->sp++] = (char *) v2 + 1;
    }
    else {
        s->ptrs[s->sp++] = v1;
    }
}

static struct node *stack_pop(struct stack **sp, struct edge **v2) {
    // If the current chunk is empty, go to the previous one
    struct stack *s = *sp;
    if (s->sp == 0) {
        assert(s->prev->next == s);
        s = s->prev;
        assert(s->sp == STACK_CHUNK);
        *sp = s;
    }

    void *ptr = s->ptrs[--s->sp];
    if ((hvalue_t) ptr & 1) {        // edge
        *v2 = (struct edge *) ((char *) ptr - 1);
        return (*v2)->src;
    }
    if (v2 != NULL) {
        *v2 = NULL;
    }
    return ptr;
}

static inline bool stack_empty(struct stack *s) {
    return s->prev == NULL && s->sp == 0;
}

// Tarjan SCC algorithm
static void tarjan(){
    scc = malloc(global.graph.size * sizeof(*scc));
    for (unsigned int v = 0; v < global.graph.size; v++) {
        scc->index = -1;
    }

    unsigned int i = 0, comp_id = 0;
    struct stack *stack = calloc(1, sizeof(*stack));
    struct stack *call_stack = calloc(1, sizeof(*call_stack));
    double now = gettime();
    unsigned int ndone = 0, lastdone = 0;
    for (unsigned int v = 0; v < 1 /*global.graph.size*/; v++) {
        struct node *n = global.graph.nodes[v];
        if (scc[v].index == -1) {
            stack_push(&call_stack, n, NULL);
            while (!stack_empty(call_stack)) {
                struct edge *e;
                n = stack_pop(&call_stack, &e);
                if (e == NULL) {
                    scc[v].index = i;
                    scc[v].lowlink = i;
                    i++;
                    stack_push(&stack, n, NULL);
                    n->on_stack = true;
                    e = n->fwd;
                }
                else {
                    if (scc[e->dst->id].lowlink < scc[v].lowlink) {
                        scc[v].lowlink = scc[e->dst->id].lowlink;
                    }
                    e = e->fwdnext;
                }
                while (e != NULL) {
                    struct node *w = e->dst;
                    if (scc[w->id].index < 0) {
                        break;
                    }
                    if (w->on_stack && scc[w->id].index < scc[v].lowlink) {
                        scc[v].lowlink = scc[w->id].index;
                    }
                    e = e->fwdnext;
                }
                if (e != NULL) {
                    stack_push(&call_stack, n, e);
                    stack_push(&call_stack, e->dst, NULL);
                }
                else if (scc[v].lowlink == scc[v].index) {
                    for (;;) {
                        ndone++;
                        if (ndone - lastdone >= 10000000 && gettime() - now > 3) {
                            printf("completed %u/%u states (%.2f%%)\n", ndone, global.graph.size, 100.0 * ndone / global.graph.size);
                            now = gettime();
                            lastdone = ndone;
                        }
                        struct node *n2;
                        n2 = stack_pop(&stack, NULL);
                        n2->on_stack = false;
                        scc[n2->id].component = comp_id;
                        if (n2 == n) {
                            break;
                        }
                    }
                    comp_id++;
                }
            }
        }
    }
    global.ncomponents = comp_id;
}

// This routine removes all nodes that have a single incoming edge and it's
// an "epsilon" edge (empty print log).  These are essentially useless nodes.
static void destutter1(){
    struct graph *graph = &global.graph;

    // If nothing got printed, we can just return a single node
    if (!global.printed_something) {
        graph->size = 1;
        struct node *n = graph->nodes[0];
        n->final = 1;
        n->fwd = NULL;
    }

#ifdef OBSOLETE
    graph->nodes[0]->reachable = true;
    int ndropped = 0;
    for (unsigned int i = 0; i < graph->size; i++) {
        struct node *parent = graph->nodes[i];
        struct edge **pe, *e;
        for (pe = &parent->fwd; (e = *pe) != NULL;) {
            struct node *n = e->dst;
            if (edge_output(e)->nlog == 0) {     // epsilon edge (no prints)
                assert(n->bwd != NULL);
                if (n->bwd->bwdnext == NULL) {
                    assert(n->bwd == e);

                    if (n->final) {
                        parent->final = true;
                    }

                    // Remove the edge
                    *pe = e->fwdnext;
                    n->bwd = NULL;
                    // free(e);

                    ndropped++;

                    // Move the outgoing edges to the parent.
                    while ((e = n->fwd) != NULL) {
                        n->fwd = e->fwdnext;
                        e->fwdnext = *pe;
                        *pe = e;
                        e->src = parent;
                    }
                    n->reachable = false;
                }
                else {
                    n->reachable = true;
                    pe = &e->fwdnext;
                }
            }
            else {
                n->reachable = true;
                pe = &e->fwdnext;
            }
        }
    }
    // printf("DROPPED %d / %d\n", ndropped, graph->size);
#endif // OBSOLETE
}

static struct dict *collect_symbols(struct graph *graph){
    struct dict *symbols = dict_new("symbols", sizeof(unsigned int), 0, 0, false);
    unsigned int symbol_id = 0;

    for (unsigned int i = 0; i < graph->size; i++) {
        struct node *n = graph->nodes[i];
        if (!n->reachable) {
            continue;
        }
        for (struct edge *e = n->fwd; e != NULL; e = e->fwdnext) {
            for (unsigned int j = 0; j < edge_output(e)->nlog; j++) {
                bool new;
                unsigned int *p = dict_insert(symbols, NULL, &step_log(edge_output(e))[j], sizeof(hvalue_t), &new);
                if (new) {
                    *p = ++symbol_id;
                }
            }
        }
    }
    return symbols;
}

struct symbol_env {
    FILE *out;
    bool first;
};

static void print_symbol(void *env, const void *key, unsigned int key_size, void *value){
    struct symbol_env *se = env;
    const hvalue_t *symbol = key;

    assert(key_size == sizeof(*symbol));
    char *p = value_json(*symbol);
    if (se->first) {
        se->first = false;
    }
    else {
        fprintf(se->out, ",\n");
    }
    fprintf(se->out, "     \"%u\": %s", * (unsigned int *) value, p);
    free(p);
}

struct print_trans_env {
    FILE *out;
    bool first;
    struct dict *symbols;
};

static void print_trans_upcall(void *env, const void *key, unsigned int key_size, void *value){
    struct print_trans_env *pte = env;
    const hvalue_t *log = key;
    unsigned int nkeys = key_size / sizeof(hvalue_t);
    struct strbuf *sb = value;

    if (pte->first) {
        pte->first = false;
    }
    else {
        fprintf(pte->out, ",\n");
    }
    fprintf(pte->out, "        [[");
    for (unsigned int i = 0; i < nkeys; i++) {
        bool new;
        unsigned int *p = dict_insert(pte->symbols, NULL, &log[i], sizeof(log[i]), &new);
        assert(!new);
        if (i != 0) {
            fprintf(pte->out, ",");
        }
        fprintf(pte->out, "%u", *p);
    }
    fprintf(pte->out, "],[%s]]", strbuf_getstr(sb));
    strbuf_deinit(sb);
}

static void print_transitions(FILE *out, struct dict *symbols, struct edge *edges){
    struct dict *d = dict_new("transitions", sizeof(struct strbuf), 0, 0, false);

    fprintf(out, "      \"transitions\": [\n");
    for (struct edge *e = edges; e != NULL; e = e->fwdnext) {
        bool new;
        struct strbuf *sb = dict_insert(d, NULL, step_log(edge_output(e)), edge_output(e)->nlog * sizeof(hvalue_t), &new);
        if (new) {
            strbuf_init(sb);
            strbuf_printf(sb, "%d", e->dst->id);
        }
        else {
            strbuf_printf(sb, ",%d", e->dst->id);
        }
    }
    struct print_trans_env pte = {
        .out = out, .first = true, .symbols = symbols
    };
    dict_iter(d, print_trans_upcall, &pte);
    fprintf(out, "\n");
    fprintf(out, "      ],\n");
    dict_delete(d);
}

// Split s into components separated by sep.  Returns #components.
// Return the components themselves into *parts.  All is malloc'd.
unsigned int str_split(const char *s, char sep, char ***parts){
    // Count the number of components
    unsigned int n = 1;
    for (const char *p = s; *p != '\0'; p++) {
        if (*p == sep) {
            n++;
        }
    }

    // Allocate an array of strings and fill it with the components
    *parts = malloc(n * sizeof(char *));
    n = 0;
    for (const char *p = s;;) {
        // Find the end of the component
        const char *q;
        for (q = p; *q != sep && *q != '\0'; q++)
            ;
        (*parts)[n] = malloc((q - p) + 1);
        memcpy((*parts)[n], p, q - p);
        (*parts)[n++][q - p] = '\0';
        if (*q == '\0') {
            break;
        }
        p = q + 1;
    }

    return n;
}

#ifndef _WIN32
static void inthandler(int sig){
    printf("Caught interrupt\n");
    _exit(1);
}
#endif

// Error in arguments.  Print a "usage" message and exit
static void usage(char *prog){
    fprintf(stderr, "Usage: %s [-c] [-t<maxtime>] [-B<dfafile>] -o<outfile> file.json\n", prog);
    exit(1);
}

// This is the main function.  The general form is
//          charm [arguments] source.hvm
// where source.hvm is a JSON file generated by the compiler containing the code
// to be model checked.  The following arguments are supported:
//
//    -c: suppress looking for busy wait
//    -d: direct execute (no model checking).  Experimental feature at this time
//    -D: dump files "charm.gv" and "charm.dump" for debugging
//    -R: suppress looking for data races
//    -t<time>: maximum time to model check
//    -B<file.hfa>: input "hfa" file for output behavior checking
//    -o<file.hco>: specify the output file (no checking if none given)
//    -w<workers>: specifies what and how many workers to use (see below)
//
int exec_model_checker(int argc, char **argv){
    bool cflag = false, dflag = false, Dflag = false, Rflag = false;
    int i, maxtime = 300000000 /* about 10 years */;
    char *outfile = NULL, *dfafile = NULL, *worker_flag = NULL;
    for (i = 1; i < argc; i++) {
        if (*argv[i] != '-') {
            break;
        }
        switch (argv[i][1]) {
        case 'c':
            cflag = true;
            break;
        case 'd':               // run direct (no model check)
            dflag = true;
            break;
        case 'D':
            Dflag = true;
            break;
        case 'R':
            Rflag = true;
            break;
        case 't':
            maxtime = atoi(&argv[i][2]);
            if (maxtime <= 0) {
                fprintf(stderr, "%s: negative timeout\n", argv[0]);
                exit(1);
            }
            break;
        case 'B':
            dfafile = &argv[i][2];
            break;
        case 'o':
            outfile = &argv[i][2];
            break;
        case 'w':
            worker_flag = &argv[i][2];
            break;
        default:
            usage(argv[0]);
        }
    }
    if (argc - i != 1) {
        usage(argv[0]);
    }
    char *fname = argv[i];
    double timeout = gettime() + maxtime;

#ifndef NDEBUG
    fprintf(stderr, "Warning: NDEBUG not defined in source code\n");
#endif

#ifndef _WIN32
    signal(SIGINT, inthandler);
#endif

    // Get info about virtual processors (cores or hyperthreads)
    vproc_info_create();

    // The -w flag allows specifying which "virtual processors"
    // to consider.  For example, on a server with two CPUs, 16
    // cores per CPU, and two hyperthreads per core, there are
    // 2x16x2 = 64 virtual processors.  OSs organizes them in a
    // particular way.  An important consideration is to look at
    // the cache hierarchy.  When threads run on sibling caches,
    // there are going to be a lot of invalidations across the
    // caches.  It's therefore useful to try and keep threads
    // close together if possible.
    //
    // Charm tries to organize the virtual processors into a
    // hiearchy.  The leaves are the virtual processors, while
    // the internal nodes represent some kind of affinity like
    // a shared cache.  Each node has an identifier so that
    // siblings in the tree do not share identifiers.  As a
    // result, a path of identifiers in the tree uniquely
    // identify a virtual processor.  The OS also assigns an
    // integer id to each virtual processor, so the tree maps
    // identifier paths to the OS id for a virtual processor.
    //
    // Ideally the tree should follow the cache hierarchy, but
    // currently only a rough approximation is implemented
    // using three levels:
    //      - socket id
    //      - hyperthread id
    //      - core id
    // In Linux, this info is extracted from /proc/cpuinfo.
    // Using other OSs, the info is a simple guess based on the
    // number of virtual processors, N: one socket, two
    // hyperthread per core, N/2 cores per socket.
    // That said, the software in theory allows arbitrary trees.
    //
    // The format of the -w flag is as follows:
    //
    //    -w[/]?[n]?[:pattern[+pattern]*]
    //
    // where pattern is a path of ids separated by colons.
    // Omitting an id functions as a wildcard.
    // Here n is the maximum number of threads to use, and a
    // pattern identifies a path in the tree.  If no patterns
    // are specified, all virtual processors are considered.
    // Adding a '/' prints the virtual processors.
    //
    // For example, suppose we have a server as described above
    // (two sockets, two hyperthreads per CPU, 16 cores per server
    //
    //      -w4
    //            this specifies that at most 4 workers should
    //            be spawned
    //
    //      -w/4
    //            same, but print list of virtual processors
    //
    //      -w:0:1
    //            only consider socket 0 and hyperthread 1.
    //            So this should only spawn 16 workers.
    //
    //      -w::1
    //            same, but uses a wildcard for the socket.
    //            So this should run 32 workers on the second
    //            hyperthreads
    //
    //      -w4::1
    //            same, but spawns only 4 workers on those
    //            hyperthreads
    //
    //      -w:1:0:2+1:0:3
    //            2 workers on hyperthread 0 of cores 2 and 3
    //            of socket 1
    //
    //      -w:1:0:2+0:1
    //            1 worker on core 2 of socket 1, and 16 workers
    //            on the second hyperthreads of socket 0, for
    //            a total of 17 workers
    //
    // If -w is not specified, simply use all virtual processors.
    if (worker_flag == NULL) {
        global.nworkers = n_vproc_info;
        for (unsigned int i = 0; i < n_vproc_info; i++) {
            vproc_info[i].selected = true;
        }
    }
    else {
        // -w/... causes virtual processors to be printed.
        if (*worker_flag == '/') {
            vproc_info_dump();
            worker_flag++;
        }

        // The first counter, if any, is the requested number of workers.
        char *endstr;
        long n = strtol(worker_flag, &endstr, 10);
        if (endstr != worker_flag) {
            global.nworkers = n;
            worker_flag = endstr;
        }

        // See if the workers are specified.
        if (*worker_flag == '\0') {
            if (global.nworkers == 0) {
                global.nworkers = n_vproc_info;
            }
            for (unsigned int i = 0; i < n_vproc_info; i++) {
                vproc_info[i].selected = true;
            }
        }
        else if (*worker_flag != ':') {
            fprintf(stderr, "-w flag must be of the form -w[nworkers]?[:id]* but has additional characters (%s)\n", worker_flag);
            exit(1);
        }
        else {
            worker_flag++;

            // Disjuncts of patterns are separated by '+'
            char **disjuncts;
            unsigned int npatterns = str_split(worker_flag, '+', &disjuncts);
            struct pattern *patterns = malloc(npatterns * sizeof(*patterns));
            // The identifiers in a pattern are separated by colons
            for (unsigned int i = 0; i < npatterns; i++) {
                char **parts;
                patterns[i].nids = str_split(disjuncts[i], ':', &parts);
                patterns[i].ids = malloc(patterns[i].nids * sizeof(*patterns[i].ids));
                for (unsigned int j = 0; j < patterns[i].nids; j++) {
                    char *endstr;
                    patterns[i].ids[j].id = strtol(parts[j], &endstr, 10);
                    patterns[i].ids[j].wildcard = endstr == parts[j];
                    if (endstr == parts[j]) {
                        endstr++;
                    }
                }
            }

            // Now that we have the patterns, figure out which
            // virtual processors qualify
            unsigned int nselected = 0;
            for (unsigned i = 0; i < n_vproc_info; i++) {
                for (unsigned int j = 0; j < npatterns; j++) {
                    if (vproc_match(&vproc_info[i], &patterns[j])) {
                        vproc_info[i].selected = true;
                    }
                }
                if (vproc_info[i].selected) {
                    nselected++;
                }
            }
            if (nselected == 0) {
                fprintf(stderr, "no virtual processors match -w pattern\n");
                exit(1);
            }
            if (global.nworkers == 0 || global.nworkers > nselected) {
                global.nworkers = nselected;
            }
        }
    }

    // Create a tree of the selected processors
    vproc_tree_create();
    // vproc_tree_dump(vproc_root, 0);

    // Determine how many worker threads to use
    printf("* Phase 2: run the model checker (nworkers = %d)\n", global.nworkers);

    // Initialize barriers for the three phases (see struct worker definition)
    barrier_t start_barrier, middle_barrier, end_barrier;
    barrier_init(&start_barrier, global.nworkers);
    barrier_init(&middle_barrier, global.nworkers);
    barrier_init(&end_barrier, global.nworkers);

    // initialize modules
    mutex_init(&global.inv_lock);
#ifdef USE_ATOMIC
    atomic_init(&global.atodo, 0);
#else
    mutex_init(&global.todo_lock);
#endif
    global.goal = 1;
    mutex_init(&global.todo_enter);
    mutex_init(&global.todo_wait);
    mutex_acquire(&global.todo_wait);          // Split Binary Semaphore
    global.values = dict_new("values", 0, 0, global.nworkers, true);

    ops_init(NULL);

    graph_init(&global.graph, 1 << 20);
    global.failures = NULL;
    global.seqs = VALUE_SET;

    // First read and parse the DFA if any
    if (dfafile != NULL) {
        global.dfa = dfa_read(NULL, dfafile);
        if (global.dfa == NULL) {
            exit(1);
        }
    }

    // open the HVM file
    FILE *fp = fopen(fname, "r");
    if (fp == NULL) {
        fprintf(stderr, "%s: can't open %s\n", argv[0], fname);
        exit(1);
    }

    // read the file
    json_buf_t buf;
    buf.base = malloc(CHUNKSIZE);
    buf.len = 0;
    int n;
    while ((n = fread(&buf.base[buf.len], 1, CHUNKSIZE, fp)) > 0) {
        buf.len += n;
        buf.base = realloc(buf.base, buf.len + CHUNKSIZE);
    }
    fclose(fp);

    // parse the contents
    char *buf_orig = buf.base;
    struct json_value *jv = json_parse_value(&buf);
    assert(jv->type == JV_MAP);
    free(buf_orig);

    // travel through the json code contents to create the code array
    struct json_value *jc = dict_lookup(jv->u.map, "code", 4);
    assert(jc->type == JV_LIST);
    global.code = code_init_parse(NULL, jc);

    if (has_countLabel) {
        printf("    * compability with countLabel\n");
    }

    // Create an initial state.  Start with the initial context.
    struct context *init_ctx = calloc(1, sizeof(struct context) + MAX_CONTEXT_STACK * sizeof(hvalue_t));
    init_ctx->vars = VALUE_DICT;
    init_ctx->atomic = 1;
    init_ctx->initial = true;
    init_ctx->atomicFlag = true;
    value_ctx_push(init_ctx, VALUE_LIST);

    // Now create the state
    struct state *state = calloc(1, sizeof(struct state) + sizeof(hvalue_t) + 1);
    state->vars = VALUE_DICT;
    hvalue_t ictx = value_put_context(NULL, init_ctx);
    state->chooser = -1;
    state->bagsize = 1;
    state_contexts(state)[0] = ictx;
    multiplicities(state)[0] = 1;
    state->stopbag = VALUE_DICT;
    state->dfa_state = global.dfa == NULL ? 0 : dfa_initial(global.dfa);

    // Needed for second phase
    global.processes = new_alloc(hvalue_t);
    global.callstacks = new_alloc(struct callstack *);
    *global.processes = ictx;
    struct callstack *cs = new_alloc(struct callstack);
    cs->arg = VALUE_LIST;
    cs->vars = VALUE_DICT;
    cs->return_address = CALLTYPE_PROCESS;
    *global.callstacks = cs;
    global.nprocesses = 1;

    // This is an experimental feature: run code directly (don't model check)
    if (dflag) {
        global.run_direct = true;
        mutex_init(&run_mutex);
        mutex_init(&run_waiting);
        mutex_acquire(&run_waiting);
        run_count = 1;

        // Run the initializing thread to completion
        // TODO.  spawned threads should wait...
        run_thread(state, init_ctx);

        // Wait for other threads
        mutex_acquire(&run_mutex);
        if (run_count > 0) {
            mutex_release(&run_mutex);
            mutex_acquire(&run_waiting);
        }
        mutex_release(&run_mutex);
        exit(0);
    }

    // Create the hash table that maps states to nodes
    struct dict *visited = dict_new("visited", sizeof(struct node), 0, global.nworkers, false);

    global.computations = dict_new("computations", sizeof(struct step_condition), 0, global.nworkers, false);

    // Allocate space for worker info
    struct worker *workers = calloc(global.nworkers, sizeof(*workers));
    for (unsigned int i = 0; i < global.nworkers; i++) {
        struct worker *w = &workers[i];
        w->visited = visited;
        w->timeout = timeout;
        w->start_barrier = &start_barrier;
        w->middle_barrier = &middle_barrier;
        w->end_barrier = &end_barrier;
        w->index = i;
        w->workers = workers;
        w->nworkers = global.nworkers;
#ifdef USE_EDGES
        w->edges = calloc(global.nworkers, sizeof(struct edge *));
#endif
        w->profile = calloc(global.code.len, sizeof(*w->profile));

        // Create a context for evaluating invariants
        w->inv_step.ctx = calloc(1, sizeof(struct context) +
                                MAX_CONTEXT_STACK * sizeof(hvalue_t));
        // w->inv_step.ctx->name = value_put_atom(&allocator, "__invariant__", 13);
        w->inv_step.ctx->vars = VALUE_DICT;
        w->inv_step.ctx->atomic = w->inv_step.ctx->readonly = 1;
        w->inv_step.ctx->atomicFlag = true;
        w->inv_step.ctx->interruptlevel = false;
        w->inv_step.allocator = &w->allocator;

        w->alloc_buf = malloc(WALLOC_CHUNK);
        w->alloc_ptr = w->alloc_buf;
        w->alloc_buf16 = malloc(WALLOC_CHUNK);
        w->alloc_ptr16 = w->alloc_buf16;

        w->allocator.alloc = walloc;
        w->allocator.free = wfree;
        w->allocator.ctx = w;
        w->allocator.worker = i;
    }

    // Pin workers to particular virtual processors
    unsigned int worker_index = 0;
    vproc_tree_alloc(vproc_root, workers, &worker_index, global.nworkers);

    // Prefer to allocate memory at the memory bank attached to the first worker.
    // The main advantage of this is that if the entire Kripke structure is stored
    // there, the Tarjan SCC algorithm (executed by worker 0) will run significantly
    // faster.
#ifdef __linux__
#ifdef NUMA
    numa_available();
    numa_set_preferred(vproc_info[workers[0].vproc].ids[0]);
#endif
#endif

    // Put the state and value dictionaries in concurrent mode
    dict_set_concurrent(global.values);
    dict_set_concurrent(visited);
    dict_set_concurrent(global.computations);

    // Put the initial state in the visited map
    mutex_t *lock;
    struct dict_assoc *hn = dict_find_lock(visited, &workers[0].allocator, state, state_size(state), NULL, &lock);
    struct node *node = (struct node *) &hn[1];
    memset(node, 0, sizeof(*node));
#ifdef OBSOLETE
    node->u.ph1.lock = lock;
    node->dead_end = true;
#endif
    mutex_release(lock);
    node->reachable = true;
    graph_add(&global.graph, node);

    // Compute how much table space is allocated
    global.allocated = global.graph.size * sizeof(struct node *) +
        dict_allocated(visited) + dict_allocated(global.values);

    // Start all but one of the workers. All will wait on the start barrier
    for (unsigned int i = 1; i < global.nworkers; i++) {
        thread_create(worker, &workers[i]);
    }

    double before = gettime();

    // Run the last worker.  When it terminates the model checking is done.
    worker(&workers[0]);

    // Compute how much memory was used, approximately
    unsigned long allocated = global.allocated;
#define REPORT_WORKERS
#ifdef REPORT_WORKERS
    double phase1 = 0, phase2a = 0, phase2b = 0, phase3a = 0, phase3b, start_wait = 0, middle_wait = 0, end_wait = 0;
    unsigned int fix_edge = 0;
    for (unsigned int i = 0; i < global.nworkers; i++) {
        struct worker *w = &workers[i];
        allocated += w->allocated;
        phase1 += w->phase1;
        phase2a += w->phase2a;
        phase2b += w->phase2b;
        phase3a += w->phase3a;
        phase3b += w->phase3b;
        fix_edge += w->fix_edge;
        start_wait += w->start_wait;
        middle_wait += w->middle_wait;
        end_wait += w->end_wait;
        printf("W%2u: %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %u %u\n", i,
                w->phase1,
                w->phase2a,
                w->phase2b,
                w->phase3a,
                w->phase3b,
                w->start_wait/w->start_count,
                w->middle_wait/w->middle_count,
                w->end_wait/w->end_count,
                w->total_results,
                w->process_step);
    }
#else
    for (unsigned int i = 0; i < global.nworkers; i++) {
        struct worker *w = &workers[i];
        allocated += w->allocated;
    }
#endif // REPORT_WORKERS
#ifdef notdef
    printf("computing: %lf %lf %lf %lf (%lf %lf %lf %lf %u); waiting: %lf %lf %lf\n",
        phase1 / global.nworkers,
        phase2a / global.nworkers,
        phase2b / global.nworkers,
        phase3 / global.nworkers,
        phase1,
        phase2a,
        phase2b,
        phase3,
        fix_edge,
        start_wait / global.nworkers,
        middle_wait / global.nworkers,
        end_wait / global.nworkers);
#endif

    printf("    * %u states (time %.2lfs, mem=%.3lfGB)\n", global.graph.size, gettime() - before, (double) allocated / (1L << 30));
    unsigned int si_hits = 0, si_total = 0;
    bool loops_possible = false;
    for (unsigned int i = 0; i < global.nworkers; i++) {
        struct worker *w = &workers[i];
        if (w->loops_possible) {
            loops_possible = true;
        }
        si_hits += w->si_hits;
        si_total += w->si_total;
    }
    printf("    * %u/%u computations/edges\n", (si_total - si_hits), si_total);

    if (outfile == NULL) {
        exit(0);
    }

    // Put the hashtables into "sequential mode" to avoid locking overhead.
    dict_set_sequential(global.values);
    dict_set_sequential(visited);
    dict_set_sequential(global.computations);

    printf("* Phase 3: analysis\n");

    bool computed_components = false;

    // Do a cheap check for deadlock if no other errors have been detected
    // TODO.  Could be parallelized
    if (global.failures == NULL) {
        if (global.graph.size > 10000) {
            printf("* Check for deadlock\n");
            fflush(stdout);
        }
        for (unsigned int i = 0; i < global.graph.size; i++) {
            struct node *node = global.graph.nodes[i];
            struct state *state = node_state(node);
            bool dead_end = true;
            for (struct edge *e = node->fwd; e != NULL; e = e->fwdnext) {
                if (e->dst != node) {
                    dead_end = false;
                    break;
                }
            }
            if (dead_end) {
                bool final = value_state_all_eternal(state)
                        && value_ctx_all_eternal(state->stopbag);
                if (final) {
                    // If an input dfa was specified, it should also be in the
                    // final state.
                    if (global.dfa != NULL &&
                            !dfa_is_final(global.dfa, state->dfa_state)) {
                        struct failure *f = new_alloc(struct failure);
                        f->type = FAIL_BEHAVIOR;
                        f->edge = node_to_parent(node);
                        add_failure(&global.failures, f);
                    }
                    else {
                        node->final = true;
                    }
                }
                else {
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_TERMINATION;
                    f->edge = node_to_parent(node);
                    assert(f->edge != NULL);
                    add_failure(&global.failures, f);
                }
            }
        }
    }

    // If no failures were detected (yet), look for deadlock and busy
    // waiting.
    // TODO.  Also look for other final states and evaluate more finally
    //        clauses.  This can happen if an eternal thread sits in
    //        a loop like:  await x and y
    if (global.failures == NULL && loops_possible) {
        if (global.graph.size > 10000) {
            printf("* Determine strongly connected components\n");
            fflush(stdout);
        }
        double now = gettime();
        tarjan();
        computed_components = true;
        printf("    * %u components (%.2lf seconds)\n", global.ncomponents, gettime() - now);

#ifdef DUMP_GRAPH
        printf("digraph Harmony {\n");
        for (unsigned int i = 0; i < global.graph.size; i++) {
            printf(" s%u [label=\"%u/%u\"]\n", i, i, scc[i].component);
        }
        for (unsigned int i = 0; i < global.graph.size; i++) {
            struct node *node = global.graph.nodes[i];
            for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
                printf(" s%u -> s%u\n", node->id, edge->dst->id);
            }
        }
        printf("}\n");
#endif

        // The search for non-terminating states starts with marking the
        // non-sink components as "good".  They cannot contain non-terminating
        // states.  This loop, for each state, looks at what component it is
        // in.  As part of this loop we also determine how many states are in
        // each component, and assign a "representative" state to the component.
        // We also determine a boolean value 'all_same'.  It is true iff all
        // states in the component have the same variable assignment, but also
        // all remaining contexts must be 'eternal' (i.e., all normal threads
        // must have terminated in each state).
        struct component *components = calloc(global.ncomponents, sizeof(*components));
        for (unsigned int i = 0; i < global.graph.size; i++) {
            assert(scc[i].component < global.ncomponents);
            struct component *comp = &components[scc[i].component];
            struct node *node = global.graph.nodes[i];

            // See if this is the first state that we are looking at for
            // this component, make this state the 'representative' for
            // this component.
            if (comp->size == 0) {
                comp->rep = node;
                comp->all_same = value_state_all_eternal(node_state(node))
                    && value_ctx_all_eternal(node_state(node)->stopbag);
            }
            else if (node_state(node)->vars != node_state(comp->rep)->vars
                        || !value_state_all_eternal(node_state(node))
                        || !value_ctx_all_eternal(node_state(node)->stopbag)) {
                comp->all_same = false;
            }
            comp->size++;

            // If we already determined that this component has a way out,
            // we're done.
            if (comp->good) {
                continue;
            }

            // If this component has a way out, it is good
            for (struct edge *edge = node->fwd;
                            edge != NULL && !comp->good; edge = edge->fwdnext) {
                if (scc[edge->dst->id].component != scc[node->id].component) {
                    comp->good = true;
                    break;
                }
            }
        }

        // Components that have only states in which the variables are the same
        // and have only eternal threads are good because it means all its
        // eternal threads are blocked and all other threads have terminated.
        // It also means that these are final states.
        for (unsigned int i = 0; i < global.ncomponents; i++) {
            struct component *comp = &components[i];
            assert(comp->size > 0);
            if (!comp->good && comp->all_same) {
                comp->good = true;
                comp->final = true;
            }
        }

        // Next we'll determine for all 'final' states if they satisfy the
        // 'finally' clauses.  Also, if an input dfa was specified, we check
        // that that dfa is in the final state as welll.

        // Look for states in final components
        for (unsigned int i = 0; i < global.graph.size; i++) {
            struct node *node = global.graph.nodes[i];
            assert(scc[i].component < global.ncomponents);
            struct component *comp = &components[scc[i].component];
            if (comp->final) {
                node->final = true;

                // If an input dfa was specified, it should also be in the
                // final state.
                if (global.dfa != NULL &&
                            !dfa_is_final(global.dfa, node_state(node)->dfa_state)) {
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_BEHAVIOR;
                    f->edge = node_to_parent(node);
                    add_failure(&global.failures, f);
                    // break;
                }
            }
        }

        // If we haven't found any failures yet, look for states in bad components.
        // If there are none, look for busy waiting states.
        if (global.failures == NULL) {
            // Report the states in bad components as non-terminating.
            int nbad = 0;
            for (unsigned int i = 0; i < global.graph.size; i++) {
                struct node *node = global.graph.nodes[i];
                if (!components[scc[i].component].good) {
                    nbad++;
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_TERMINATION;
                    if (node->fwd != NULL && node->fwd->fwdnext == NULL) {
                        f->edge = node->fwd;
                    }
                    else {
                        f->edge = node_to_parent(node);
                        assert(f->edge != NULL);
                    }
                    add_failure(&global.failures, f);
                    // TODO.  Can we be done here?
                    // break;
                }
            }

            // If there are no non-terminating states, look for busy-waiting
            // states.
            if (nbad == 0 && !cflag) {
                // TODO.  Why are we clearing the visited flags??
                for (unsigned int i = 0; i < global.graph.size; i++) {
                    global.graph.nodes[i]->visited = false;
                }
                for (unsigned int i = 0; i < global.graph.size; i++) {
                    if (components[scc[i].component].size > 1) {
                        detect_busywait(node);
                    }
                }
            }
        }
    }

    // The -D flag is used to dump debug files
    if (Dflag) {
        FILE *df = fopen("charm.gv", "w");
        if (df == NULL) {
            fprintf(stderr, "can't create charm.gv\n");
        }
        else {
            fprintf(df, "digraph Harmony {\n");
            for (unsigned int i = 0; i < global.graph.size; i++) {
                fprintf(df, " s%u [label=\"%u\"]\n", i, i);
            }
            for (unsigned int i = 0; i < global.graph.size; i++) {
                struct node *node = global.graph.nodes[i];
                for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
                    struct state *state = node_state(node);
                    unsigned int j;
                    for (j = 0; j < state->bagsize; j++) {
                        if (state_contexts(state)[j] == edge_input(edge)->ctx) {
                            break;
                        }
                    }
                    assert(j < state->bagsize);
                    if (edge->failed) {
                        fprintf(df, " s%u -> s%u [style=%s label=\"F %u\"]\n",
                            node->id, edge->dst->id,
                            node_to_parent(edge->dst) == edge ? "solid" : "dashed",
                            multiplicities(state)[j]);
                    }
                    else {
                        fprintf(df, " s%u -> s%u [style=%s label=\"%u\"]\n",
                            node->id, edge->dst->id,
                            node_to_parent(edge->dst) == edge ? "solid" : "dashed",
                            multiplicities(state)[j]);
                    }
                }
            }
            fprintf(df, "}\n");
            fclose(df);
        }

        df = fopen("charm.dump", "w");
        if (df == NULL) {
            fprintf(stderr, "Can't create charm.dump\n");
        }
        else {
            // setbuf(df, NULL);
            for (unsigned int i = 0; i < global.graph.size; i++) {
                struct node *node = global.graph.nodes[i];
                assert(node->id == i);
                fprintf(df, "\nNode %d:\n", node->id);
                if (computed_components) {
                    fprintf(df, "    component: %d\n", scc[i].component);
                }
                fprintf(df, "    len to parent: %d\n", node->len);
                if (node_to_parent(node) != NULL) {
                    fprintf(df, "    ancestors:");
                    for (struct node *n = node_to_parent(node)->src;; n = node_to_parent(n)->src) {
                        fprintf(df, " %u", n->id);
                        if (node_to_parent(n) == NULL) {
                            break;
                        }
                    }
                    fprintf(df, "\n");
                }
                struct state *state = node_state(node);
                fprintf(df, "    vars: %s\n", value_string(state->vars));
                fprintf(df, "    contexts:\n");
                for (unsigned int i = 0; i < state->bagsize; i++) {
                    fprintf(df, "      %"PRI_HVAL": %u\n", state_contexts(state)[i], multiplicities(state)[i]);
                }
                if (state->stopbag != VALUE_DICT) {
                    fprintf(df, "    stopbag:\n");
                    unsigned int size;
                    hvalue_t *vals = value_get(state->stopbag, &size);
                    size /= 2 * sizeof(hvalue_t);
                    for (unsigned int i = 0; i < size; i++) {
                        fprintf(df, "      %"PRI_HVAL": %d\n", vals[2*i], (int) VALUE_FROM_INT(vals[2*i+1]));;
                    }
                }
                // fprintf(df, "    len: %u %u\n", node->len, node->steps);
                if (node->failed) {
                    fprintf(df, "    failed\n");
                }
                fprintf(df, "    fwd:\n");
                int eno = 0;
                for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext, eno++) {
                    fprintf(df, "        %d:\n", eno);
                    struct context *ctx = value_get(edge_input(edge)->ctx, NULL);
                    fprintf(df, "            node: %d (%d)\n", edge->dst->id, scc[edge->dst->id].component);
                    fprintf(df, "            context before: %"PRIx64" pc=%d\n", edge_input(edge)->ctx, ctx->pc);
                    ctx = value_get(edge_output(edge)->after, NULL);
                    fprintf(df, "            context after:  %"PRIx64" pc=%d\n", edge_output(edge)->after, ctx->pc);
                    if (edge->failed != 0) {
                        fprintf(df, "            failed\n");
                    }
                    if (edge_input(edge)->choice != 0) {
                        fprintf(df, "            choice: %s\n",
                                value_string(edge_input(edge)->choice));
                    }
                    if (edge_output(edge)->nlog > 0) {
                        fprintf(df, "            log:");
                        for (unsigned int j = 0; j < edge_output(edge)->nlog; j++) {
                            char *p = value_string(step_log(edge_output(edge))[j]);
                            fprintf(df, " %s", p);
                            free(p);
                        }
                        fprintf(df, "\n");
                    }
                    if (edge_output(edge)->ai != NULL) {
                        fprintf(df, "            ai:\n");
                        for (struct access_info *ai = edge_output(edge)->ai; ai != NULL; ai = ai->next) {
                            char *p = indices_string(ai->indices, ai->n);
                            if (ai->load) {
                                fprintf(df, "              load %s\n", p);
                            }
                            else {
                                fprintf(df, "              store %s\n", p);
                            }
                            free(p);
                        }
                    }
                }
            }
            fclose(df);
        }
    }

    // Look for data races
    // TODO.  Could be parallelized
    if (!Rflag && global.failures == NULL) {
        printf("    * Check for data races\n");
        for (unsigned int i = 0; i < global.graph.size; i++) {
            struct node *node = global.graph.nodes[i];
            graph_check_for_data_race(&global.failures, node, NULL);
            if (global.failures != NULL) {
                break;
            }
        }
    }

    if (global.failures == NULL) {
        printf("    * **No issues found**\n");
    }

    // Start creating the output (.hco) file.
    FILE *out = fopen(outfile, "w");
    if (out == NULL) {
        fprintf(stderr, "charm: can't create %s\n", outfile);
        exit(1);
    }

    global.pretty = dict_lookup(jv->u.map, "pretty", 6);
    assert(global.pretty->type == JV_LIST);

    fprintf(out, "{\n");
    fprintf(out, "  \"nstates\": %d,\n", global.graph.size);

    // In case no issues were found, we output a summary of the Kripke structure
    // with the 'print' outputs.
    if (global.failures == NULL) {
        printf("* Phase 4: write results to %s\n", outfile);
        fflush(stdout);

        fprintf(out, "  \"issue\": \"No issues\",\n");
        fprintf(out, "  \"hvm\": ");
        json_dump(jv, out, 2);
        fprintf(out, ",\n");

        // Reduce the output graph by removing nodes with only
        // one incoming edge that is an epsilon edge
        //
        destutter1();

        // Output the symbols;
        struct dict *symbols = collect_symbols(&global.graph);
        fprintf(out, "  \"symbols\": {\n");
        struct symbol_env se = { .out = out, .first = true };
        dict_iter(symbols, print_symbol, &se);
        fprintf(out, "\n");
        fprintf(out, "  },\n");

        // Only output nodes if there are symbols
        fprintf(out, "  \"nodes\": [\n");
        bool first = true;
        for (unsigned int i = 0; i < global.graph.size; i++) {
            struct node *node = global.graph.nodes[i];
            assert(node->id == i);
            if (node->reachable) {
                if (first) {
                    first = false;
                }
                else {
                    fprintf(out, ",\n");
                }
                fprintf(out, "    {\n");
                fprintf(out, "      \"idx\": %d,\n", node->id);
                if (computed_components) {
                    fprintf(out, "      \"component\": %d,\n", scc[node->id].component);
                }
#ifdef notdef
                if (node->parent != NULL) {
                    fprintf(out, "      \"parent\": %d,\n", node->parent->id);
                }
                char *val = json_escape_value(node_state(node)->vars);
                fprintf(out, "      \"value\": \"%s:%d\",\n", val, node_state(node)->choosing != 0);
                free(val);
#endif
                print_transitions(out, symbols, node->fwd);
                if (i == 0) {
                    fprintf(out, "      \"type\": \"initial\"\n");
                }
                else if (node->final) {
                    fprintf(out, "      \"type\": \"terminal\"\n");
                }
                else {
                    fprintf(out, "      \"type\": \"normal\"\n");
                }
                fprintf(out, "    }");
            }
        }
        fprintf(out, "\n");
        fprintf(out, "  ],\n");

        fprintf(out, "  \"profile\": [\n");
        for (unsigned int pc = 0; pc < global.code.len; pc++) {
            unsigned int count = 0;
            for (unsigned int i = 0; i < global.nworkers; i++) {
                struct worker *w = &workers[i];
                count += w->profile[pc];
            }
            if (pc > 0) {
                fprintf(out, ",\n");
            }
            fprintf(out, "    %u", count);
        }
        fprintf(out, "\n");
        fprintf(out, "  ]\n");
    }

    // Some error was detected.  Report the (approximately) shortest counter example.
    else {
        // Select some "bad path".  Here we do our first approximation, by picking
        // a state with the minimal distance to the initial state.  That does not
        // necessarily give us the best path, as the distance is not measured by
        // the number of steps but by the number of context switches.
        struct failure *bad = NULL;
        for (struct failure *f = global.failures; f != NULL; f = f->next) {
            if (bad == NULL || bad->edge->dst->len < f->edge->dst->len) {
                bad = f;
            }
        }

        switch (bad->type) {
        case FAIL_SAFETY:
            printf("    * **Safety Violation**\n");
            fprintf(out, "  \"issue\": \"Safety violation\",\n");
            break;
#ifdef notdef
        case FAIL_INVARIANT:
            printf("    * **Invariant Violation**\n");
            assert(VALUE_TYPE(bad->address) == VALUE_PC);
            fprintf(out, "  \"issue\": \"Invariant violation\",\n");
            fprintf(out, "  \"invpc\": %d,\n", (int) VALUE_FROM_PC(bad->address));
            break;
        case FAIL_FINALLY:
            printf("    * **Finally Predicate Violation**\n");
            assert(VALUE_TYPE(bad->address) == VALUE_PC);
            fprintf(out, "  \"issue\": \"Finally predicate violation\",\n");
            fprintf(out, "  \"finpc\": %d,\n", (int) VALUE_FROM_PC(bad->address));
            break;
#endif
        case FAIL_BEHAVIOR:
            printf("    * **Behavior Violation**: terminal state not final\n");
            fprintf(out, "  \"issue\": \"Behavior violation: terminal state not final\",\n");
            break;
        case FAIL_TERMINATION:
            printf("    * **Non-terminating state**\n");
            fprintf(out, "  \"issue\": \"Non-terminating state\",\n");
            break;
        case FAIL_BUSYWAIT:
            printf("    * **Active busy waiting**\n");
            fprintf(out, "  \"issue\": \"Active busy waiting\",\n");
            break;
        case FAIL_RACE:
            assert(VALUE_TYPE(bad->address) == VALUE_ADDRESS_SHARED);
            assert(bad->address != VALUE_ADDRESS_SHARED);
            char *addr = value_string(bad->address);
            char *json = json_string_encode(addr, strlen(addr));
            printf("    * **Data race** (%s)\n", json);
            fprintf(out, "  \"issue\": \"Data race (%s)\",\n", json);
            free(json);
            free(addr);
            break;
        default:
            panic("main: bad fail type");
        }

        printf("* Phase 4: write results to %s\n", outfile);
        fflush(stdout);

        fprintf(out, "  \"hvm\": ");
        json_dump(jv, out, 2);
        fprintf(out, ",\n");

        // This is where we actually output a path (shortest counter example).
        // Finding the shortest counter example is non-trivial and could be very
        // expensive.  Here we use a trick that seems to work well and is very
        // efficient.  Basically, we take any path

        fprintf(out, "  \"macrosteps\": [");

        // First copy the path to the bad state into an array for easier sorting
        path_serialize(bad->edge);

        // The optimal path minimizes the number of context switches.  Here we
        // reorder steps in the path to do so.
        path_optimize();

        // During model checking much information is removed for memory efficiency.
        // Here we recompute the path to reconstruct that information.
        path_recompute();

        // If this was a safety failure, we remove any unneeded steps to further
        // reduce the length of the counter-example.
        if (/* bad->type == FAIL_INVARIANT || */ bad->type == FAIL_SAFETY) {
            path_trim(NULL);
        }

        // Finally, we output the path.
        path_output(out);

        fprintf(out, "\n");
        fprintf(out, "  ]\n");
    }

    fprintf(out, "}\n");
    fclose(out);

    // iface_write_spec_graph_to_file("iface.gv");
    // iface_write_spec_graph_to_json_file("iface.json");

    return 0;
}

int run_model_checker(int argc, char **argv){
    return exec_model_checker(argc, argv);
}

int main(int argc, char** argv) {
    return exec_model_checker(argc, argv);
}
