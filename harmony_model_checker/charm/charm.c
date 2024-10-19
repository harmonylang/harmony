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

// Newly discovered nodes are kept in arrays of this size
#define NRESULTS        (4 * 4096)

// Convenient constant
#define MAX_STATE_SIZE (sizeof(struct state) + MAX_CONTEXT_BAG * (sizeof(hvalue_t) + 1))

// Important performance parameter that represents the number of states that
// each worker produces for each other worker before going to the barrier.
// TODO.  How to tune this thing?
#define STATE_BUFFER_HWM    50

// All global variables should be here
struct global global;

// Immediately followed by a state
struct state_header {
    struct state_header *next;  // linked list
    // bool garbage;               // returned to sender
    // unsigned int source;        // for return to sender and free-ing
    unsigned int nctxs;         // for free list maintenance
    struct node *node;          // old state
    int edge_index;             // index of edge in the old state (-1 is invarinat)
    unsigned int noutgoing;     // number of outgoing edges of new state
    uint32_t hash;              // to speed up hash lookup
};

extern bool has_countLabel;     // TODO.  Hack for backward compatibility

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

struct state_queue {
    struct state_header *first, **last;
};

// TODO.  Is this a problem?
#define MAX_THREADS 100

// One of these per worker thread
struct worker {
    // Putting the more-or-less constant fields here at the beginning
    // in the hope of better cache performance
    unsigned int index;          // index of worker
    double timeout;              // deadline for model checker (-t option)

    // Shard of the Kripke structure.  There is an array of shards.  Each shard
    // holds the states that hash onto the index into the array.
    struct shard {
        struct dict *states;          // maps states to nodes
        struct state_queue *peers;    // peers[nshards]

        struct results_block *todo_buffer, *tb_head, *tb_tail;
        unsigned int tb_size, tb_index;
    } shard;

    // free lists of state_headers for various numbers of threads
    struct state_header *state_header_free[MAX_THREADS];

    unsigned int vproc;          // virtual processor for pinning
    struct failure *failures;    // list of discovered failures (not data races)
    bool found_failures;         // some worker found failures

    // Each worker keeps track of how often it executes a particular
    // instruction for profiling purposes.
    unsigned int *profile;      // one for each instruction in the HVM code

    //
    // Below are the things that are likely to change more often
    //

    unsigned int si_total, si_hits;
    struct edge_list *el_free;
    bool loops_possible;         // loops in Kripke structure are possible
    bool printed_something;      // worker executed Print op

    // Statistics about the three phases for optimization purposes
    double start_wait, middle_wait, end_wait;
    unsigned int start_count, middle_count, end_count;
    double phase1, phase2a, phase2b, phase3;

    // State maintained while evaluating invariants
    struct step inv_step;        // for evaluating invariants

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

    // These need to be next to one another.  When a worker performs a
    // "step", it's on behalf of a particular thread with a particular
    // context (state of the thread).  The context structure is immediately
    // followed by its stack of Harmony values.
    struct context ctx;
    hvalue_t stack[MAX_CONTEXT_STACK];

    // We also keep space for an optimization for atomic sections
    char as_state[MAX_STATE_SIZE];
    struct context as_ctx;
    hvalue_t as_stack[MAX_CONTEXT_STACK];

    unsigned int sb_index;

    // Some cached info from global to reduce contention
    unsigned int nworkers;
    struct dfa *dfa;
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
        // w->align_waste += asize - size;
        if (w->alloc_ptr + asize > w->alloc_buf + WALLOC_CHUNK) {
            // w->frag_waste += WALLOC_CHUNK - (w->alloc_ptr - w->alloc_buf);
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

// Per thread one-time memory allocator (no free(), although the last
// thing allocated can be freed with wfree()).
static inline void *walloc_fast(struct worker *w, unsigned int size){
    assert(size % 8 == 0);
    if (w->alloc_ptr + size > w->alloc_buf + WALLOC_CHUNK) {
        w->alloc_buf = malloc(WALLOC_CHUNK);
        w->alloc_ptr = w->alloc_buf;
        w->allocated += WALLOC_CHUNK;
    }
    void *result = w->alloc_ptr;
    w->alloc_ptr += size;
    return result;
}

// Allocate a "state_header", copy in s, and make sure there's room for
// at least n contexts.
static inline struct state_header *state_header_alloc(struct worker *w,
                        struct state *s, unsigned int nctxs){
    if (nctxs < s->total) {
        nctxs = s->total;
    }
    assert(nctxs < MAX_THREADS);
    struct state_header *sh = w->state_header_free[nctxs];
    if (sh == NULL) {
        sh = walloc_fast(w, sizeof(*sh) + state_size_nctx(nctxs));
        sh->nctxs = nctxs;
    }
    else {
        assert(sh->nctxs == nctxs);
        w->state_header_free[nctxs] = sh->next;
    }
    memcpy(sh + 1, s, state_size(s));
    return sh;
}

// Put a state_header on the freelist of the right size
static void state_header_free(struct worker *w, struct state_header *sh){
    assert(sh->nctxs < MAX_THREADS);
    sh->next = w->state_header_free[sh->nctxs];
    w->state_header_free[sh->nctxs] = sh;
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

// Remove context 'ctx' from the state by index.
static inline void context_remove_by_index(struct state *state, int i){
    hvalue_t *ctxlist = state_ctxlist(state);
    if ((ctxlist[i] & STATE_MULTIPLICITY) > ((hvalue_t) 1 << STATE_M_SHIFT)) {
        ctxlist[i] -= (hvalue_t) 1 << STATE_M_SHIFT;
    }
    else {
        state->bagsize--;
        state->total--;
        memmove(&ctxlist[i], &ctxlist[i+1], (state->total - i) * sizeof(hvalue_t));
    }
}

// Copy of value::context_add
static inline int local_context_add(struct state *state, hvalue_t ctx){
    hvalue_t *ctxlist = state_ctxlist(state);

    unsigned int i;
    for (i = 0; i < state->bagsize; i++) {
        hvalue_t ctxi = ctxlist[i] & ~STATE_MULTIPLICITY;
        if (ctxi == ctx) {
            ctxlist[i] += (hvalue_t) 1 << STATE_M_SHIFT;
            return i;
        }
        if (ctxi > ctx) {
            break;
        }
    }

    if (state->total >= MAX_CONTEXT_BAG) {
        return -1;
    }
 
    // Move the last contexts
    memmove(&ctxlist[i+1], &ctxlist[i],
                    (state->total - i) * sizeof(hvalue_t));

    state->bagsize++;
    state->total++;
    ctxlist[i] = ctx | ((hvalue_t) 1 << STATE_M_SHIFT);
    return i;
}

// Part of experimental -d option, running Harmony programs "for real".
static void direct_run(struct state *state, unsigned int id){
    struct worker w;
    struct step step;

    memset(&w, 0, sizeof(w));
    w.alloc_buf = malloc(WALLOC_CHUNK);
    w.alloc_ptr = w.alloc_buf;
    w.alloc_buf16 = malloc(WALLOC_CHUNK);
    w.alloc_ptr16 = w.alloc_buf16;
    w.allocator.alloc = walloc;
    w.allocator.free = wfree;
    w.allocator.ctx = &w;

    memset(&step, 0, sizeof(step));
    step.allocator = &w.allocator;
    step.ctx = &w.ctx;
    unsigned int interrupt_count = 1;

    setbuf(stdout, NULL);

    while (state->total > 0) {
        direct_check(state, &step);
        if (state->bagsize == 0) {
            continue;
        }

        // Collect info about the various possible
        // contexts to run next
        struct ctx_info {
            hvalue_t ctx;
            struct context *cc;
            enum {
                CI_NO_TRANSITION,
                CI_OLD_TRANSITION,
                CI_NEW_TRANSITION,
                CI_POT_TRANSITION,
            } trans;
        } *ci = calloc( state->bagsize, sizeof(*ci));
        unsigned int no_trans = 0;
        unsigned int old_trans = 0;
        unsigned int new_trans = 0;
        unsigned int pot_trans = 0;
        for (int i = 0; i < state->bagsize; i++) {
            ci[i].ctx = state_ctx(state, i);
            unsigned int size;
            ci[i].cc = value_get(ci[i].ctx, &size);
            assert(ctx_size(ci[i].cc) == size);
            assert(!ci[i].cc->terminated);
            assert(!ci[i].cc->failed);

            // See if it's about to print something
            struct instr *instrs = global.code.instrs;
            if (instrs[ci[i].cc->pc].print) {
                assert(ci[i].cc->sp > 0);
                hvalue_t symbol = ctx_stack(ci[i].cc)[ci[i].cc->sp - 1];
                int cnt = dfa_visited(global.dfa, state->dfa_state, symbol);
                if (cnt == 0) {
                    ci[i].trans = CI_NEW_TRANSITION;
                    new_trans++;
                }
                else if (cnt < 0) {
                    char *v = value_string(symbol);
                    printf("%u: about to print '%s'\n", id, v);
                    panic("bad transition");
                }
                else if (dfa_potential(global.dfa, state->dfa_state, symbol) < 0) {
                    ci[i].trans = CI_OLD_TRANSITION;
                    old_trans++;
                }
                else {
                    ci[i].trans = CI_POT_TRANSITION;
                    pot_trans++;
                }
            }
            else {
                ci[i].trans = CI_NO_TRANSITION;
                no_trans++;
            }
        }
        assert(no_trans + old_trans + new_trans + pot_trans== state->bagsize);

        int ctx_index = -1;
        if (ctx_index < 0) {    // random selection
            ctx_index = 0;
            unsigned int total = 0;
            for (int i = 0; i < state->bagsize; i++) {
                total += state_multiplicity(state, i);
            }
            unsigned int select = rand() % total;
            // printf("--> %u %u\n", total, select);
            for (int i = 0; i < state->bagsize; i++) {
                if (state_multiplicity(state, i) > select) {
                    ctx_index = i;
                    break;
                }
                select -= state_multiplicity(state, i);
            }
        }

#ifdef notdef
        if (no_trans + new_trans > 0) {
            unsigned int r = rand() % (no_trans + new_trans);
            for (unsigned int i = 0; i < state->bagsize; i++) {
                if (ci[i].trans == CI_NO_TRANSITION || ci[i].trans == CI_NEW_TRANSITION) {
                    if (r == 0) {
                        ctx_index = i;
                        break;
                    }
                    r--;
                }
            }
        }
        else if (pot_trans > 0) {
            unsigned int r = rand() % pot_trans;
            for (unsigned int i = 0; i < state->bagsize; i++) {
                if (ci[i].trans == CI_POT_TRANSITION) {
                    if (r == 0) {
                        ctx_index = i;
                        break;
                    }
                    r--;
                }
            }
        }
        else {
            assert(old_trans > 0);
            unsigned int r = rand() % old_trans;
            for (unsigned int i = 0; i < state->bagsize; i++) {
                if (ci[i].trans == CI_OLD_TRANSITION) {
                    if (r == 0) {
                        ctx_index = i;
                        break;
                    }
                    r--;
                }
            }
        }
 #endif
        free(ci);
        assert(ctx_index >= 0);
        hvalue_t pick = state_ctx(state, ctx_index);

        // Remove the original context from the state
        // assert(state_ctx(state, ctx_index) == ctx);
        context_remove_by_index(state, ctx_index);

        // printf("RUN %p\n", (void *) pick);

        // Get and copy the context
        unsigned int size;
        struct context *cc = value_get(pick, &size);
        assert(ctx_size(cc) == size);
        assert(!cc->terminated);
        assert(!cc->failed);
        memcpy(&w.ctx, cc, ctx_size(cc));

        // Check if an interrupt is in order
        if (pick & VALUE_CONTEXT_INTERRUPTABLE) {
        // if (cc->extended && ctx_trap_pc(cc) != 0 && !cc->interruptlevel) {
            interrupt_count += 1;
            if (rand() % interrupt_count == 0) {
                interrupt_invoke(&step);
            }
        }

        for (int i = 0; i < 100; i++) {     // Limit partial order reduction
            int pc = step.ctx->pc;
            struct instr *instrs = global.code.instrs;
            struct op_info *oi = instrs[pc].oi;
            step.vars = state->vars;       // NEW
            (*oi->op)(instrs[pc].env, state, &step);
            state->vars = step.vars;       // NEW
            if (step.ctx->terminated || step.ctx->stopped) {
                break;
            }
            if (step.ctx->failed) {
                char *s = value_string(ctx_failure(step.ctx));
                printf("Failure: %s\n", s);
                printf("pc = %d\n", (int) step.ctx->pc);
                free(s);
                break;
            }
            if (step.ctx->stopped) {
                break;
            }

            if (step.ctx->pc == pc) {
                fprintf(stderr, ">>> %s\n", oi->name);
            }
            assert(step.ctx->pc != pc);
            assert(step.ctx->pc >= 0);
            assert(step.ctx->pc < global.code.len);

            // If not in atomic mode, see if we should give another
            // context a shot
            if (step.ctx->atomic == 0) {
                struct instr *next_instr = &global.code.instrs[step.ctx->pc];
                bool breakable = next_instr->breakable;

                // If this is a Load operation, it's only breakable if it
                // accesses a global variable
                // TODO.  Can this be made more efficient?
                if (next_instr->load && next_instr->env == NULL) {
                    hvalue_t addr = ctx_stack(step.ctx)[step.ctx->sp - 1];
                    if (VALUE_TYPE(addr) != VALUE_ADDRESS_SHARED && VALUE_TYPE(addr) != VALUE_ADDRESS_PRIVATE) {
                        value_ctx_failure(step.ctx, step.allocator, "Load: not an address");
                        break;
                    }
                    if ((VALUE_TYPE(addr)) == VALUE_ADDRESS_PRIVATE) {
                        breakable = false;
                    }
                }

                if (breakable) {
                    break;
                }
            }
        }

        // If context has failed, we're done
        if (step.ctx->failed) {
            return;
        }

        // Add updated context to state unless terminated or stopped
        if (step.ctx->stopped) {
            hvalue_t after = value_put_context(step.allocator, step.ctx);
            stopped_context_add(state, after);
        }
        else if (!step.ctx->terminated) {
            hvalue_t after = value_put_context(step.allocator, step.ctx);
            local_context_add(state, after);
        }
    }

    if (global.dfa != NULL && !dfa_is_final(global.dfa, state->dfa_state)) {
        printf("Error: not in the final DFA state\n");
    }
}

// Specialized hash function for states
static inline uint32_t meiyan2(const struct state *s){
	typedef uint32_t *P;
    unsigned int count = sizeof(*s) / 8 + s->total;
    P key = (P) s;

	uint32_t h = 0x811c9dc5;
	while (count > 0) {
		h = (h ^ ((((*key) << 5) | ((*key) >> 27)) ^ *(key + 1))) * 0xad3e7;
		count--;
		key += 2;
	}
	return h ^ (h >> 16);
}

// Apply the effect of evaluating a context (for a particular assignment
// of shared variables and possibly some choice) to a state.  This leads
// to a new edge in the Kripke structure, possibly to a new state.
static inline void process_step(
    struct worker *w,
    struct step_condition *stc,
    struct state_header *sh
) {
    struct step_output *so = stc->u.completed;

    if (sh->edge_index < 0) { // invariant
        assert(stc->completed);
        assert(stc->invariant_chk);
        if (so->failed || so->infinite_loop) {
            struct failure *f = new_alloc(struct failure);
            f->type = so->failed ? FAIL_SAFETY : FAIL_INFLOOP;
            f->node = sh->node;
            f->edge = walloc_fast(w, sizeof(struct edge));
#ifdef SHORT_PTR
            f->edge->dest = (int64_t *) node - (int64_t *) f->edge;
            printf("SET DST 1: %p\n", node);
#else
            f->edge->dst = sh->node;
#endif
            assert(f->edge->dst != NULL);
            f->edge->stc_id = (uint64_t) stc;
            f->edge->failed = true;
            f->edge->invariant_chk = true;
            add_failure(&w->failures, f);
        }
        state_header_free(w, sh);
        return;
    }

    struct state *sc = (struct state *) &sh[1];
    sc->vars = so->vars;

    // Update state with spawned and resumed threads.
    for (unsigned int i = 0; i < so->nspawned; i++) {
        if (local_context_add(sc, step_spawned(so)[i]) < 0) {
            panic("too many threads 1");
        }
    }
    for (unsigned int i = 0; i < so->nunstopped; i++) {
        hvalue_t ctx = step_unstopped(so)[i];
        hvalue_t *ctxlist = state_ctxlist(sc);
        for (unsigned int i = sc->bagsize; i < sc->total; i++) {
            hvalue_t ctxi = ctxlist[i] & ~STATE_MULTIPLICITY;
            if (ctxi == ctx) {
                if ((ctxlist[i] & STATE_MULTIPLICITY) > ((hvalue_t) 1 << STATE_M_SHIFT)) {
                    ctxlist[i] -= ((hvalue_t) 1 << STATE_M_SHIFT);
                }
                else {
                    assert(sc->total > sc->bagsize);
                    sc->total--;
                    memmove(&ctxlist[i], &ctxlist[i+1], (sc->total - i) * sizeof(hvalue_t));
                }
                break;
            }
        }
    }

    // Add new context to state unless it's terminated or stopped
    int new_index = -1;
    if (so->stopped) {
        stopped_context_add(sc, so->after);
    }
    else if (!so->terminated) {
        new_index = local_context_add(sc, so->after);
        if (new_index < 0) {
            panic("too many threads 0");
        }
    }

    // Determine the number of outgoing edges of the new state below
    unsigned int noutgoing;

    if (so->printing) {
        assert(so->choose_count == 0);
        sc->type = STATE_PRINT;
        sc->chooser = new_index;
        noutgoing = 1;
    }
    else if (so->choose_count > 0) {
        sc->type = STATE_CHOOSE;
        sc->chooser = new_index;
        // sc->pre = global.inv_pre ? node_state(sh->node)->pre : sc->vars;
        noutgoing = so->choose_count;
    }
    else {
        assert(so->choose_count == 0);
        sc->type = STATE_NORMAL;
        sc->chooser = 0;
        // sc->pre = sc->vars;
        hvalue_t *choices = state_ctxlist(sc);
        noutgoing = sc->bagsize;
        for (unsigned int i = 0; i < sc->bagsize; i++) {
            if (choices[i] & VALUE_CONTEXT_INTERRUPTABLE) {
                noutgoing++;
            }
        }
    }

    // If a failure has occurred, keep track of that too.
    assert(sh->edge_index >= 0);
    assert(sh->edge_index < 256);
    // assert(edge->dst != NULL);
    if (so->failed || so->infinite_loop) {
        struct edge *edge = &node_edges(sh->node)[sh->edge_index];
        edge->failed = true;
        noutgoing = 0;
        struct failure *f = new_alloc(struct failure);
        f->type = so->infinite_loop ? FAIL_INFLOOP : FAIL_SAFETY;
        f->node = sh->node;
        f->edge = edge;
        f->next = w->failures;
        w->failures = f;
    }

    if (w->dfa != NULL) {
        for (unsigned int i = 0; i < so->nlog; i++) {
            int nstate = dfa_step(w->dfa, sc->dfa_state, step_log(so)[i]);
            if (nstate < 0) {
                struct edge *edge = &node_edges(sh->node)[sh->edge_index];
                struct failure *f = new_alloc(struct failure);
                f->type = FAIL_BEHAVIOR_BAD;
                f->node = sh->node;
                f->edge = edge;
                edge->failed = true;
                add_failure(&w->failures, f);
                break;
            }
            sc->dfa_state = nstate;
        }
    }

    sh->noutgoing = noutgoing;
    sh->hash = meiyan2(sc);

    // Add to the linked list of the responsible peer shard
    struct shard *shard = &w->shard;
    unsigned int responsible = (sh->hash >> 16) % w->nworkers;
    struct state_queue *sq = &shard->peers[responsible];
    *sq->last = sh;
    sq->last = &sh->next;
    sh->next = NULL;

    w->sb_index++;
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
//
// NEW: sc is read-only in onestep.  All the effects are returned, and process_step
//      must be invoked to apply them.
static struct step_output *onestep(
    struct worker *w,       // thread info
    struct node *node,      // starting node
    struct state *sc,       // actual state
    hvalue_t ctx,           // context identifier
    struct step *step,      // step info
    hvalue_t choice,        // if about to make a choice, which choice?
    bool infloop_detect     // try to detect infloop from the start
) {
    assert(state_size(sc) == state_size(node_state(node)));
    assert(!step->ctx->terminated);
    assert(!step->ctx->failed);

    struct instr *instrs = global.code.instrs;
    bool infinite_loop = false;
    unsigned int instrcnt = 0;          // keeps track of #instruction executed
    bool must_break = true;
    unsigned int choose_count = 0;      // number of choices
    struct dict *infloop = NULL;        // infinite loop detector
    unsigned int as_instrcnt = 0;       // for rollback
    bool stopped = false;
    bool terminated = false;
    bool rollback = false;
    bool printing = false;

    // See if we should first try an interrupt or make a choice.
    if (choice == (hvalue_t) -1) {
        assert(step->ctx->extended);
        assert(ctx_trap_pc(step->ctx) != 0);
        interrupt_invoke(step);
    }
    else if (choice != 0) {
        assert(instrs[step->ctx->pc].choose);
        assert(sc->type == STATE_CHOOSE);
        assert(step->ctx->sp > 0);
        ctx_stack(step->ctx)[step->ctx->sp - 1] = choice;
        w->profile[step->ctx->pc]++;
        instrcnt++;
        step->ctx->pc++;
    }
    else {
        must_break = false;
    }

    for (;;) {
        assert(!step->ctx->terminated);
        assert(!step->ctx->failed);

        // See what kind of instruction is next
        int pc = step->ctx->pc;
        struct op_info *oi = instrs[pc].oi;
        // printf("--> %u %s %u %u\n", pc, oi->name, step->ctx->sp, instrcnt);

        // If it's a Choose instruction, we should break no matter what.
        if (instrs[pc].choose) {
            assert(step->ctx->sp > 0);

            // Check that the top of the stack contains a set.
            hvalue_t s = ctx_stack(step->ctx)[step->ctx->sp - 1];
            if (s == VALUE_SET) {
                value_ctx_failure(step->ctx, step->allocator, "choose operation requires a non-empty set");
                instrcnt++;
                break;
            }
            if (VALUE_TYPE(s) != VALUE_SET) {
                value_ctx_failure(step->ctx, step->allocator, "choose operation requires a set");
                instrcnt++;
                break;
            }

            if (as_instrcnt == 0) {
                unsigned int size;
                (void) value_get(s, &size);
                choose_count = size / sizeof(hvalue_t);
                assert(choose_count > 0);
            }
            else {
                rollback = true;
            }
            break;
        }

        if (instrs[pc].atomicinc && step->ctx->atomic == 0) {
            if (must_break) {
                memcpy(w->as_state, sc, state_size(sc));
                memcpy(&w->as_ctx, step->ctx, ctx_size(step->ctx));
                as_instrcnt = instrcnt;
            }
            else if (!instrs[pc].is_assert) {
                must_break = true;
            }
        }

        // Possibly break unless it's in atomic mode.
        else if (step->ctx->atomic == 0 || as_instrcnt != 0) {
            // If it's a Load instruction, it's breakable if it accesses a global variable.
            // TODO.  Can this check be made more efficient?
            if (instrs[pc].load && instrs[pc].env == NULL) {
                hvalue_t addr = ctx_stack(step->ctx)[step->ctx->sp - 1];
                if (VALUE_TYPE(addr) != VALUE_ADDRESS_SHARED && VALUE_TYPE(addr) != VALUE_ADDRESS_PRIVATE) {
                    value_ctx_failure(step->ctx, step->allocator, "Load: not an address");
                    instrcnt++;
                    break;
                }
                if ((VALUE_TYPE(addr)) != VALUE_ADDRESS_PRIVATE) {
                    if (must_break) {
                        if (as_instrcnt != 0) {
                            rollback = true;
                        }
                        break;
                    }
                    else {
                        must_break = true;
                    }
                }
            }
            else if (instrs[pc].load || instrs[pc].store || instrs[pc].del || instrs[pc].print) {
                if (must_break) {
                    if (as_instrcnt != 0) {
                        rollback = true;
                    }
                    break;
                }
                else {
                    must_break = true;
                }
            }

            // Deal with interrupts if enabled
            else if (step->ctx->extended && ctx_trap_pc(step->ctx) != 0 &&
                                !step->ctx->interruptlevel) {
                // If this is a thread exit, break so we can invoke the
                // interrupt handler one more time (just before its exit)
                if (instrs[pc].retop && step->ctx->sp == 1) {
                    if (instrcnt > 0) {
                        break;
                    }
                }

                // If this is a setintlevel(True), should try interrupt
                // For simplicity, always try when SetIntLevel is about to
                // be executed.
                else if (instrs[pc].setintlevel && instrcnt > 0) {
                    break;
                }
            }
        }
        // If it's a Print instruction in atomic mode, we should break if it's not the
        // first instruction.
        else if (instrcnt > 0 && instrs[pc].print) {
            printing = true;
            break;
        }

        // Execute the instruction
        w->profile[pc]++;
        (*oi->op)(instrs[pc].env, sc, step);
        if (step->nlog > 0) {
            w->printed_something = true;
        }
        instrcnt++;
        // printf("<-- %u %s %u %u %u\n", pc, oi->name, step->ctx->atomic, as_instrcnt, must_break);

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

        assert(step->ctx->pc >= 0);
        assert(step->ctx->pc != pc);
        assert(step->ctx->pc < global.code.len);

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
                                                0, 0, false, false);
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
                    break;
                }

                // Otherwise start over to create the shortest counterexample.
                else {
                    return NULL;
                }
            }
        }

        assert(step->ctx->pc != pc);
        assert(step->ctx->pc >= 0);
        assert(step->ctx->pc < global.code.len);

        // If we're not in atomic mode, we limit the number of steps to MAX_STEPS.
        // TODO.  Not sure why.
        if (step->ctx->atomic == 0 && instrcnt > MAX_STEPS) {
            break;
        }
    }

    assert(step->nlog == 0 || step->nlog == 1);

    // No longer need 'infloop' state.
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
    struct step_output *so = walloc_fast(w, sizeof(struct step_output) +
            (step->nlog + step->nspawned + step->nunstopped) * sizeof(hvalue_t));
    so->vars = step->vars;  // NEW
    so->after = value_put_context(step->allocator, step->ctx);
    so->ai = step->ai;     step->ai = NULL;
    so->nsteps = instrcnt;

    assert(choose_count <= 255);
    so->choose_count = choose_count;
    so->printing = printing;
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
    struct worker *w,         // thread info
    struct node *node,        // starting node
    int edge_index,           // edge index (-1 if an invariant)
    struct state *state,      // actual state
    hvalue_t ctx,             // context identifier
    struct step *step,        // step info
    hvalue_t choice,          // if about to make a choice, which choice?
    int ctx_index             // -1 if not in the context bag (i.e., invariant)
) {
    assert(ctx_index == -1 || state_ctx(state, ctx_index) == ctx);
    assert(edge_index >= -1);
    assert(edge_index < 256);
    struct step_condition *stc;
    bool si_new;
    mutex_t *si_lock;

    w->si_total++;          // counts the number of edges

    // Key to find (vars, choice, ctx) pair in hash table.
    struct step_input si = {
        .vars = state->vars,
        .choice = choice,
        .ctx = ctx
    };

    // See if we did this already (or are doing this already)
    struct dict_assoc *da = dict_find_lock(global.computations,
        &w->allocator, &si, sizeof(si), &si_new, &si_lock);
    stc = (struct step_condition *) &da[1];

    if (si_new) {
        stc->invariant_chk = edge_index < 0;
        stc->completed = false;
        stc->u.in_progress = NULL;
    }

    // edge_index < 0 ==> invariant check
    if (edge_index >= 0) {
        struct edge *edge = &node_edges(node)[edge_index];
        edge->stc_id = (uint64_t) stc;
        edge->multiple = ctx_index >= 0 &&
                            state_multiplicity(state, ctx_index) > 1;
        edge->failed = false;
    }

    if (!si_new) {
        w->si_hits++;
        if (!stc->completed) {
            struct edge_list *el;
            if ((el = w->el_free) == NULL) {
                el = walloc_fast(w, sizeof(struct edge_list));
            }
            else {
                w->el_free = el->next;
            }
            el->node = node;
            el->ctx_index = ctx_index;
            el->edge_index = edge_index;
            el->next = stc->u.in_progress;
            stc->u.in_progress = el;
            mutex_release(si_lock);
            return;
        }
        assert(stc->completed);
    }

    mutex_release(si_lock);

    // If this is a new step, perform it
    struct edge_list *el = NULL;
    if (si_new) {
        // Get the context
        unsigned int size;
        struct context *cc = value_get(ctx, &size);
        assert(ctx_size(cc) == size);

        // Make a copy of the context
        assert(!cc->terminated);
        assert(!cc->failed);
        memcpy(&w->ctx, cc, ctx_size(cc));
        step->ctx = &w->ctx;
        step->vars = state->vars; // NEW

        // This will first attempt to run onestep() with delayed detection
        // of infinite loops (for efficiency).  If an infinite loop is
        // detected, it will run again immediately looking for infinite
        // loops to find the shortest counterexample.
        struct step_output *so =
            onestep(w, node, state, ctx, step, choice, false);
        if (so == NULL) {        // ran into an infinite loop
            // TODO.  Need probably more cleanup of step, like ai
            step->nlog = step->nspawned = step->nunstopped = 0;
            memcpy(&w->ctx, cc, ctx_size(cc));
            step->vars = state->vars; // NEW
            so = onestep(w, node, state, ctx, step, choice, true);
        }

        // Mark as completed
        mutex_acquire(si_lock);
        assert(!stc->completed);
        el = stc->u.in_progress;
        stc->completed = true;
        stc->u.completed = so;
        mutex_release(si_lock);
    }

    assert(stc->completed);

    // Conservative size.  Actual size hard to estimate because of
    // multiplicities.
    struct step_output *so2 = stc->u.completed;

    // If there was no change, then we don't need to look up the state.
    // We can simply create a self-edge.
    if (so2->vars == state->vars && so2->after == ctx &&
            so2->nlog == 0 && so2->nspawned == 0 && so2->nunstopped == 0 &&
            !so2->failed && !so2->infinite_loop) {
        if (edge_index >= 0) {
            node_edges(node)[edge_index].dst = node;
        }
        while (el != NULL) {
            node = el->node;
            if (el->edge_index >= 0) {
                node_edges(node)[el->edge_index].dst = node;
            }
            struct edge_list *next = el->next;
            el->next = w->el_free;
            w->el_free = el;
            el = next;
        }
        return;
    }

    // Allocate a state_header, essentially a message to another worker
    unsigned int est_total_ctxs = state->total + so2->nspawned + 1;
    struct state_header *sh = state_header_alloc(w, state, est_total_ctxs);
    sh->node = node;
    sh->edge_index = edge_index;
    assert(sh->edge_index >= -1);
    assert(sh->edge_index < 256);
    struct state *sc = (struct state *) &sh[1];

    // Remove original context from context bag
    if (ctx_index >= 0) {
        assert(state_ctx(sc, ctx_index) == ctx);
        context_remove_by_index(sc, ctx_index);
    }

    // Process the effect of the step
    process_step(w, stc, sh);
    assert(sc->total <= est_total_ctxs);

    // See if any other edges were waiting for the result of this
    // computation as well.
    while (el != NULL) {
        node = el->node;
        state = node_state(node);
        est_total_ctxs = state->total + so2->nspawned + 1;
        sh = state_header_alloc(w, state, est_total_ctxs);
        sh->node = node;
        sh->edge_index = el->edge_index;
        assert(sh->edge_index >= -1);
        assert(sh->edge_index < 256);
        sc = (struct state *) &sh[1];
        if (el->ctx_index >= 0) {
            assert(state_ctx(sc, el->ctx_index) == ctx);
            context_remove_by_index(sc, el->ctx_index);
        }
        process_step(w, stc, sh);
        assert(sc->total <= est_total_ctxs);

        // Put edge_list node back on the free list
        struct edge_list *next = el->next;
        el->next = w->el_free;
        w->el_free = el;
        el = next;
    }
}

static char *ctx_status(struct node *node, hvalue_t ctx) {
    struct state *state = node_state(node);

    // if (state->chooser >= 0 && state_ctx(state, state->chooser) == ctx) {
    if (state->type == STATE_CHOOSE && state_ctx(state, state->chooser) == ctx) {
        return "choosing";
    }
    while (state->type == STATE_CHOOSE) {
        node = node->parent;
        state = node_state(node);
    }
    struct edge *edge = node_edges(node);
    for (unsigned int i = 0; i < node->nedges; i++, edge++) {
        if (edge_input(edge)->ctx == ctx) {
            if (edge_dst(edge) == node) {
                return "blocked";
            }
            break;
        }
    }
    return "runnable";
}

static void print_context(
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
    unsigned int nsteps,
    unsigned int pid,
    struct macrostep *macro
){
    sc->type = STATE_NORMAL;
    sc->chooser = 0;

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
        else if (instrs[pc].print) {
            print = ctx_stack(step.ctx)[step.ctx->sp - 1];
            step.vars = sc->vars;        // NEW
            (*oi->op)(instrs[pc].env, sc, &step);
            sc->vars = step.vars;        // NEW
        }
        else {
            step.vars = sc->vars;        // NEW
            (*oi->op)(instrs[pc].env, sc, &step);
            sc->vars = step.vars;        // NEW
        }

        // Infinite loop detection
        if (!step.ctx->terminated && !step.ctx->failed) {
            if (infloop == NULL) {
                infloop = dict_new("infloop2", 0, 0, 0, false, false);
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
        (void) stopped_context_add(sc, after);
    }
    else if (!step.ctx->terminated) {
        // TODO.  Check failure of context_add
        (void) local_context_add(sc, after);
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
static void path_serialize(struct node *parent, struct edge *e){
    // First recurse to the previous step
    assert(parent != NULL);
    struct edge *to_grandparent = node_to_parent(parent);
    if (to_grandparent != NULL) {
        assert(parent->parent != NULL);
        path_serialize(parent->parent, to_grandparent);
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

static void path_recompute(){
    struct node *node = global.graph.nodes[0];
    struct state *sc = calloc(1, MAX_STATE_SIZE);
    memcpy(sc, node_state(node), state_size(node_state(node)));

    for (unsigned int i = 0; i < global.nmacrosteps; i++) {
        struct macrostep *macro = global.macrosteps[i];
        struct edge *e = macro->edge;
        // assert(e->dst != NULL);
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

    fprintf(file, "          \"pc\": \"%d\"\n", oldctx->pc);
    fprintf(file, "        }");
}

static void path_output_macrostep(FILE *file, struct macrostep *macro, struct state *oldstate){
    fprintf(file, "    {\n");
    fprintf(file, "      \"id\": \"%d\",\n", edge_dst(macro->edge)->id);
    // fprintf(file, "      \"len\": \"%d\",\n", edge_dst(macro->edge)->len);
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
    print_context(file, edge_input(macro->edge)->ctx, macro->cs, macro->tid, edge_dst(macro->edge), "        ");
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
    struct state *state = node_state(edge_dst(macro->edge));
    for (unsigned int i = 0; i < state->bagsize; i++) {
        if (i > 0) {
            fprintf(file, ",\n");
        }
        assert(VALUE_TYPE(state_ctx(state, i)) == VALUE_CONTEXT);
        fprintf(file, "          \"%"PRIx64"\": \"%u\"", state_ctx(state, i),
                state_multiplicity(state, i));
    }
    fprintf(file, "\n      },\n");

    fprintf(file, "      \"contexts\": [\n");
    for (unsigned int i = 0; i < macro->nprocesses; i++) {
        fprintf(file, "        {\n");
        print_context(file, macro->processes[i], macro->callstacks[i], i, edge_dst(macro->edge), "          ");
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
static bool path_edge_conflict(
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
        struct edge *e = node_edges(node);
        bool found = false;
        for (unsigned int j = 0; j < node->nedges; j++, e++) {
            if (edge_input(e)->ctx == ctx && edge_input(e)->choice == choice) {
                found = true;
                break;
            }
        }

        // TODO.  This should generally never happen, but it can
        //        happen for the fake edges that are added at the
        //        end in the case of invariant or finally violations.
        if (!found) {
            if (i != global.nmacrosteps - 1) {
                printf("KLUDGE %d %d\n", i, global.nmacrosteps - 1);
            }
            assert(i == global.nmacrosteps - 1);
            break;
        }
        global.macrosteps[i]->edge = e;
        node = edge_dst(e);
    }
}

// Output the macrosteps
static void path_output(FILE *file){
    fprintf(file, "\n");
    struct state *oldstate = calloc(1, MAX_STATE_SIZE);
    oldstate->vars = VALUE_DICT;
    for (unsigned int i = 0; i < global.nmacrosteps; i++) {
        // assert(global.macrosteps[i]->edge->dst != NULL);
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

enum busywait { BW_ESCAPE, BW_RETURN, BW_VISITED };
static enum busywait is_stuck(
    struct node *start,
    struct node *node,
    hvalue_t ctx,
    bool change
) {
    if (global.scc[node->id].component != global.scc[start->id].component) {
        return BW_ESCAPE;
    }
    if (node->visited) {
        return BW_VISITED;
    }
    change = change || (node_state(node)->vars != node_state(start)->vars);
    node->visited = true;
    enum busywait result = BW_ESCAPE;
    struct edge *edge = node_edges(node);
    for (unsigned int i = 0; i < node->nedges; i++, edge++) {
        if (edge_input(edge)->ctx == ctx) {
            if (edge_dst(edge) == node) {
                node->visited = false;
                return BW_ESCAPE;
            }
            if (edge_dst(edge) == start) {
                if (!change) {
                    node->visited = false;
                    return BW_ESCAPE;
                }
                result = BW_RETURN;
            }
            else {
                enum busywait bw = is_stuck(start, edge_dst(edge), edge_output(edge)->after, change);
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
    struct state *state = node_state(node);
    hvalue_t *ctxlist = state_ctxlist(state);
    for (unsigned int i = 0; i < state->bagsize; i++) {
        hvalue_t ctxi = ctxlist[i] & ~STATE_MULTIPLICITY;
        if (is_stuck(node, node, ctxi, false) == BW_RETURN) {
            struct failure *f = new_alloc(struct failure);
            f->type = FAIL_BUSYWAIT;
            f->node = node->parent;
            f->edge = node_to_parent(node);
            add_failure(&global.failures, f);
            // break;
        }
    }
}

// Initialize the given step
static inline void step_init(struct worker *w, struct step *step){
    step->ctx = NULL;
    step->ai = NULL;
    step->nlog = step->nspawned = step->nunstopped = 0;
    step->allocator = &w->allocator;
    step->keep_callstack = false;
}

// This function explores the non-deterministic choices of a node just
// taken from the todo list by the worker. Any new nodes that are found are
// kept in w->results and not yet added to the todo list or the graph.
static void do_work1(struct worker *w, struct node *node){
    struct step step;
    struct state *state = node_state(node);
    switch (state->type) {
    case STATE_CHOOSE:
        {
            // The actual set of choices is on top of its stack
            hvalue_t chooser = state_ctx(state, state->chooser);
            struct context *cc = value_get(chooser, NULL);
            assert(cc != NULL);
            assert(cc->sp > 0);
            hvalue_t s = ctx_stack(cc)[cc->sp - 1];
            assert(VALUE_TYPE(s) == VALUE_SET);
            unsigned int size;
            hvalue_t *vals = value_get(s, &size);
            size /= sizeof(hvalue_t);
            assert(size > 0);
            assert(size == node->nedges);

            // Explore each choice.
            for (unsigned int i = 0; i < size; i++) {
                step_init(w, &step);
                trystep(w, node, i, state, chooser, &step, vals[i], state->chooser);
            }
        }
        break;
    case STATE_PRINT:
        assert(node->nedges == 1);
        hvalue_t chooser = state_ctx(state, state->chooser);
        step_init(w, &step);
        trystep(w, node, 0, state, chooser, &step, 0, state->chooser);
        break;
    default:
        assert(state->type == STATE_NORMAL);

        // Explore each thread that can make a step.
        for (unsigned int i = 0; i < state->bagsize; i++) {
            step_init(w, &step);
            trystep(w, node, i, state, state_ctx(state, i), &step, 0, i);
        }
        unsigned int j = state->bagsize;
        for (unsigned int i = 0; i < state->bagsize; i++) {
            hvalue_t ctx = state_ctx(state, i);
            if (ctx & VALUE_CONTEXT_INTERRUPTABLE) {
                step_init(w, &step);
                trystep(w, node, j, state, state_ctx(state, i), &step, (hvalue_t) -1, i);
                j++;
            }
        }
        assert(j == node->nedges);
    }

    // About to check invariants etc.
    if (node->initial || state->type != STATE_NORMAL) {
        return;
    }

    // Check invariants.
	if (global.ninvs > 0) {
        step_init(w, &step);

        // Check each invariant
        for (unsigned int i = 0; i < global.ninvs; i++) {
            trystep(w, node, -1, state, global.invs[i].context, &step, 0, -1);
        }
    }

    // See if this is a final state.  It's a final state if all threads
    // are eternal and all outgoing edges are self-edges.
    bool dead_end = true;
    struct edge *e = node_edges(node);
    for (unsigned int j = 0; j < node->nedges; j++, e++) {
        if (edge_dst(e) != node) {
            dead_end = false;
            break;
        }
    }
    if (dead_end) {
        bool final = value_state_all_eternal(state);
        if (final) {
            // If an input dfa was specified, it should also be in the
            // final state.
            if (global.dfa != NULL &&
                    !dfa_is_final(global.dfa, state->dfa_state)) {
                struct failure *f = new_alloc(struct failure);
                f->type = FAIL_BEHAVIOR_FINAL;
                f->node = node->parent;
                f->edge = node_to_parent(node);
                add_failure(&w->failures, f);
            }
            else {
                node->final = true;
            }

            // Check the finally predicates
            if (global.nfinals > 0) {
                struct step step;
                step_init(w, &step);

                // Check each "finally" predicate
                for (unsigned int i = 0; i < global.nfinals; i++) {
                    trystep(w, node, -1, state, global.finals[i], &step, 0, -1);
                }
            }
        }
        else {
            struct failure *f = new_alloc(struct failure);
            f->type = FAIL_DEADLOCK;
            f->node = node->parent;
            f->edge = node_to_parent(node);
            assert(f->edge != NULL);
            add_failure(&w->failures, f);
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
static void do_work(struct worker *w){
    // double start = gettime(), now;
    struct shard *shard = &w->shard;

    // Put any messages from the prior round on the appropriate free lists
    for (unsigned int i = 0; i < w->nworkers; i++) {
        struct state_queue *sq = &shard->peers[i];
        struct state_header *sh;
        while ((sh = sq->first) != NULL) {
            sq->first = sh->next;
            state_header_free(w, sh);
        }
        sq->last = &sq->first;
    }

    // See if there's anything on my TODO list.
    w->sb_index = 0;
    while (shard->tb_index < shard->tb_size) {
        struct node *n = shard->tb_head->results[shard->tb_index % NRESULTS];
        if (!w->found_failures && !n->failed) {
            do_work1(w, n);
        }
        shard->tb_index++;
        if (shard->tb_index % NRESULTS == 0) {
            shard->tb_head = shard->tb_head->next;
        }

        // Stop if about to run out of state buffer space
        if (w->sb_index > STATE_BUFFER_HWM * w->nworkers) {
            break;
        }
    }
}

static void do_work2(struct worker *w){
    struct shard *shard = &w->shard; 

    // printf("WORK 2: %u: %u %lu\n", w->index, shard->sb_index, sizeof(shard->state_buffer));

    for (unsigned int i = 0; i < w->nworkers; i++) {
        struct shard *s2 = &global.workers[i].shard;
        for (struct state_header *sh = s2->peers[w->index].first;
                                    sh != NULL; sh = sh->next) {
            struct state *sc = (struct state *) &sh[1];
            unsigned int size = state_size(sc);

            // See if this state has been computed before by looking up the node,
            // or allocate if not.
            bool new;
            struct dict_assoc *hn = dict_find_new(shard->states, &w->allocator,
                        sc, size, sh->noutgoing * sizeof(struct edge), &new, sh->hash);
            struct node *next = (struct node *) &hn[1];
            struct edge *edge = &node_edges(sh->node)[sh->edge_index];
            edge->dst = next;

            if (new) {
                next->failed = edge->failed;
                next->initial = false;
                next->parent = sh->node;
                next->len = sh->node->len + 1;
                next->nedges = sh->noutgoing;

                assert(shard->tb_tail->nresults == shard->tb_size % NRESULTS);
                assert(shard->tb_tail->next == NULL);
                shard->tb_size++;
                shard->tb_tail->results[shard->tb_tail->nresults++] = next;
                if (shard->tb_tail->nresults == NRESULTS) {
                    struct results_block *rb = walloc_fast(w, sizeof(*shard->tb_tail));
                    rb->nresults = 0;
                    rb->next = NULL;
                    shard->tb_tail->next = rb;
                    shard->tb_tail = rb;
                }
                assert(shard->tb_tail->nresults == shard->tb_size % NRESULTS);
            }

            // See if the node points sideways or backwards, in which
            // case cycles in the graph are possible
            else if (next != sh->node && next->len <= sh->node->len) {
                w->loops_possible = true;
            }
        }
    }

    assert(shard->tb_index <= shard->tb_size);
    // printf("WORK 2: %u DONE\n", w->index);
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
static int my_getline(char **buf, size_t *cap, FILE *fp) {
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
static void vproc_tree_alloc(struct vproc_tree *vt, struct worker *workers, unsigned int *index, unsigned int n){
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

    // Spread them evenly over the children
    unsigned int over_capacity = vt->n_vprocessors - n;
    for (unsigned int i = 0; i < vt->nchildren; i++) {
        struct vproc_tree *child = vt->children[i].child;
        if (n <= child->n_vprocessors) {
            vproc_tree_alloc(child, workers, index, n);
            break;
        }
        unsigned int assign = child->n_vprocessors - (over_capacity / vt->nchildren);
        vproc_tree_alloc(child, workers, index, assign);
        n -= assign;
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

    // printf("WORKER %u\n", w->index);

    // Pin the thread to its virtual processor.
#ifdef __linux__
    if (!global.do_not_pin) {
        if (w->index == 0) {
            printf("pinning cores\n");
        }
        // Pin worker to a core
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(w->vproc, &cpuset);
        sched_setaffinity(0, sizeof(cpuset), &cpuset);
    }
#endif // __linux__

    // The worker now goes into a loop.  Each iteration consists of three phases.
    // Only worker 0 ever breaks out of this loop.
    double before = gettime();
    unsigned int nrounds = 0;
    bool done = false;
    for (;; nrounds++) {
        // Wait for the first barrier (and keep stats)
        // This is where the worker is waiting for stabilizing hash tables
        barrier_wait(&global.start_barrier);
        double after = gettime();
        w->start_wait += after - before;
        w->start_count++;

        // See if we're done
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
        // Here we are waiting for everybody's todo list processing
        before = after;
        // printf("WAIT FOR MIDDLE %u\n", w->index);
        barrier_wait(&global.middle_barrier);
        // printf("DONE WITH MIDDLE %u\n", w->index);
        after = gettime();
        w->middle_wait += after - before;
        w->middle_count++;

        // Nobody's doing work.  Great time to see if we are done
        // by looking at all peers.
        unsigned int nstates = 0, local_node_id = 0;
        done = true;
        for (unsigned int i = 0; i < w->nworkers; i++) {
            if (i == w->index) {
                local_node_id = nstates;
            }

            // Keep track of the total number of states
            nstates += global.workers[i].shard.tb_size;

            // See if the worker found a failure.
            if (global.workers[i].failures != NULL) {
                w->found_failures = true;
            }

            // If the worker has outgoing messages, we're not done.
            if (global.workers[i].sb_index != 0) {
                done = false;
            }

            // TODO.  Should we also check for outgoing messages?

            // If the worker has anything on its todo list, we're not done.
            struct shard *shard = &global.workers[i].shard;
            if (shard->tb_index != shard->tb_size) {
                done = false;
            }
        }

        before = after;
        do_work2(w);
        after = gettime();
        w->phase2a += after - before;
        before = after;

        // If we're done, allocate an array of nodes, which is easier
        // for graph analysis than a linked list.  The entriews themselves
        // are filled in parallel later, while also assigning ids to each
        // of the nodes.
        if (w->index == 0 % w->nworkers) {
            if (done) {
                // Compute how much memory was used, approximately
                unsigned long allocated = global.allocated;
#define REPORT_WORKERS
#ifdef REPORT_WORKERS
                double phase1 = 0, phase2a = 0, phase2b = 0, phase3 = 0, start_wait = 0, middle_wait = 0, end_wait = 0;
                for (unsigned int i = 0; i < global.nworkers; i++) {
                    struct worker *w = &global.workers[i];
                    allocated += w->allocated;
                    phase1 += w->phase1;
                    phase2a += w->phase2a;
                    phase2b += w->phase2b;
                    phase3 += w->phase3;
                    start_wait += w->start_wait;
                    middle_wait += w->middle_wait;
                    end_wait += w->end_wait;
#ifdef notdef
                    printf("W%2u: %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf %u\n", i,
                            w->phase1,
                            w->phase2a,
                            w->phase2b,
                            w->phase3,
                            w->start_wait/w->start_count,
                            w->middle_wait/w->middle_count,
                            w->end_wait/w->end_count,
                            w->shard.tb_size);
#endif
                }
#else
                for (unsigned int i = 0; i < global.nworkers; i++) {
                    struct worker *w = &workers[i];
                    allocated += w->allocated;
                }
#endif // REPORT_WORKERS
#ifndef notdef
                // printf("computing: %lf %lf %lf %lf (%lf %lf %lf %lf); waiting: %lf %lf %lf\n",
                printf("computing: %lf %lf %lf %lf; waiting: %lf %lf %lf\n",
                    phase1 / global.nworkers,
                    phase2a / global.nworkers,
                    phase2b / global.nworkers,
                    phase3 / global.nworkers,
                    // phase1,
                    // phase2a,
                    // phase2b,
                    // phase3,
                    start_wait / global.nworkers,
                    middle_wait / global.nworkers,
                    end_wait / global.nworkers);
#endif

                printf("    * %u states (time %.2lfs, mem=%.3lfGB)\n", nstates, gettime() - global.starttime, (double) allocated / (1L << 30));
                unsigned int si_hits = 0, si_total = 0;
                for (unsigned int i = 0; i < global.nworkers; i++) {
                    struct worker *w = &global.workers[i];
                    si_hits += w->si_hits;
                    si_total += w->si_total;
                }

                printf("    * %u/%u computations/edges\n", (si_total - si_hits), si_total);
                printf("    * %u rounds\n", nrounds);
                printf("    * %u values\n", global.values->count);
                printf("* Phase 3a: Scan states\n");

                // Allocate an array for all the nodes.
                graph_add_multiple(&global.graph, nstates);
            }

            // Worker 0 periodically prints some stats for long runs.
            else if (after - global.lasttime > 3) {
                if (global.lasttime != 0) {
                    unsigned int enqueued = 0, dequeued = 0;
                    unsigned long allocated = global.allocated;
                    for (unsigned int i = 0; i < w->nworkers; i++) {
                        struct worker *w2 = &global.workers[i];
                        enqueued += w2->shard.tb_size;
                        dequeued += w2->shard.tb_index;
                        allocated += w2->allocated;
                    }
                    double gigs = (double) allocated / (1 << 30);
                    fprintf(stderr, "    states=%u diam=%u q=%d mem=%.3lfGB\n",
                            enqueued, global.diameter,
                            enqueued - dequeued,
                            gigs);
                    global.last_nstates = enqueued;
                }
                global.lasttime = after;
                if (after > w->timeout) {
                    fprintf(stderr, "charm: timeout exceeded\n");
                    exit(1);
                }
            }
        }

        // Prepare the grow the hash tables (but the actual work of
        // rehashing is distributed among the threads in the next phase
        // The only parallelism here is that workers 1 and 2 grow different
        // hash tables, while worker 0 deals with the graph table
        if (w->index == 1 % w->nworkers) {
            dict_grow_prepare(global.values);
        }
        if (w->index == 2 % w->nworkers) {
            dict_grow_prepare(global.computations);
        }

        // Start the final phase (and keep stats).
        // Here we're waiting for all workers to process the generated
        // states and put new states on their todo lists
        after = gettime();
        w->phase2b += after - before;
        before = after;
        // printf("WAIT FOR END %u\n", w->index);
        barrier_wait(&global.end_barrier);
        // printf("DONE WITH END %u\n", w->index);
        after = gettime();
        w->end_wait += after - before;
        w->end_count++;
        before = after;

        assert(global.graph.size == nstates);

        // In parallel, the workers copy the old hash table entries into the
        // new buckets.
        dict_make_stable(global.values, w->index);
        dict_make_stable(global.computations, w->index);

        after = gettime();
        w->phase3 += after - before;
        before = after;

        // If done, fill in the graph table
        // TODO: check for race condition here?
        if (done) {
            unsigned int total = 0;
            for (struct results_block *rb = w->shard.todo_buffer;
                                            rb != NULL; rb = rb->next) {
                assert(rb->nresults <= nstates);
                assert(rb->nresults <= w->shard.tb_size);
                for (unsigned int k = 0; k < rb->nresults; k++) {
                    total += 1;
                    struct node *node = rb->results[k];
                    node->id = local_node_id;
                    assert(local_node_id < global.graph.size);
                    global.graph.nodes[local_node_id++] = node;

                    // Pacifier
                    if (w->index == 0 && gettime() - before > 3) {
                        printf("  Progress %.1f%%\n", 100.0 * total / w->shard.tb_size);
                        before = gettime();
                    }

                    // Check for deadlock and data races.
                    // TODO.  Should check -R flag
                    if (!w->found_failures && w->failures == NULL && !global.no_race_detect) {
                        graph_check_for_data_race(&w->failures, node, NULL);
                    }
                }
            }
        }
    }
}

// To simplify running Tarjan's algorithm, reorganize all the edges so that
// the epsilon edges go first.  Also count the number of epsilon edges of
// each node.
static void epsilon_closure_prep(){
    global.neps = malloc(sizeof(*global.neps) * global.graph.size);
    for (unsigned int i = 0; i < global.graph.size; i++) {
        struct node *n = global.graph.nodes[i];
        struct edge *edges = node_edges(n);
        unsigned int neps = 0;
        bool must_reorg = false;
        int first_noneps = -1;
        for (unsigned int j = 0; j < n->nedges; j++) {
            struct step_output *so = edge_output(&edges[j]);
            if (so->nlog == 0) {
                if (first_noneps >= 0) {
                    must_reorg = true;
                }
                neps++;
            }
            else {
                if (first_noneps < 0) {
                    first_noneps = j;
                }
            }
        }
        if (must_reorg) {
            struct edge eps_edges[256], noneps_edges[256];
            unsigned int ei = 0, nei = 0;
            // Copy out the edges into the respective arrays
            for (unsigned int j = first_noneps; j < n->nedges; j++) {
                struct step_output *so = edge_output(&edges[j]);
                if (so->nlog == 0) {
                    eps_edges[ei++] = edges[j];
                }
                else {
                    noneps_edges[nei++] = edges[j];
                }
            }
            // Copy them back in in the right order
            memcpy(&edges[first_noneps], eps_edges, ei * sizeof(struct edge));
            memcpy(&edges[first_noneps + ei], noneps_edges, nei * sizeof(struct edge));
        }
        global.neps[i] = neps;
    }
}

#define STACK_CHUNK 4096

struct node_edge {
    struct node *node;
    unsigned int edge_index;
};

// The stack contains pointers to nodes and, possibly, edges.
struct stack {
    struct stack *next, *prev;
    struct node_edge ptrs[STACK_CHUNK];
    unsigned int sp;
};

static void stack_push(struct stack **sp, struct node *n, unsigned int ei) {
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
    s->ptrs[s->sp].edge_index = ei;
    s->ptrs[s->sp].node = n;
    s->sp++;
}

static struct node *stack_pop(struct stack **sp, unsigned int *pei) {
    // If the current chunk is empty, go to the previous one
    struct stack *s = *sp;
    if (s->sp == 0) {
        assert(s->prev->next == s);
        s = s->prev;
        assert(s->sp == STACK_CHUNK);
        *sp = s;
    }

    struct node_edge *ptr = &s->ptrs[--s->sp];
    if (pei != NULL) {
        *pei = ptr->edge_index;
    }
    return ptr->node;
}

static inline bool stack_empty(struct stack *s) {
    return s->prev == NULL && s->sp == 0;
}

// Tarjan non-recursive SCC algorithm
/* Python code:
    i = 0
    stack = []
    call_stack = []
    comps = []
    for v in vs:        # vertices
        if v.index is None:
            call_stack.append((v,0))
            while call_stack:
                v, pi = call_stack.pop()
                # If this is first time we see v
                if pi == 0:
                    v.index = i
                    v.lowlink = i
                    i += 1
                    stack.append(v)
                    v.on_stack = True
                # If we just recursed on something
                if pi > 0:
                    prev = v.adj[pi-1]
                    v.lowlink = min(v.lowlink, prev.lowlink)
                # Find the next thing to recurse on
                while pi < len(v.adj) and v.adj[pi].index is not None:
                    w = v.adj[pi]
                    if w.on_stack:
                        v.lowlink = min(v.lowlink, w.index)
                    pi += 1
                # If we found something with index=None, recurse
                if pi < len(v.adj):
                    w = v.adj[pi]
                    call_stack.append((v,pi+1))
                    call_stack.append((w,0))
                    continue
                # If v is the root of a connected component
                if v.lowlink == v.index:
                    comp = []
                    while True:
                        w = stack.pop()
                        w.on_stack = False
                        comp.append(w.name)
                        if w is v:
                            break
                    comps.append(comp)
*/
static void tarjan(){
    struct scc *scc = malloc(global.graph.size * sizeof(*scc));
    for (unsigned int v = 0; v < global.graph.size; v++) {
        scc[v].index = -1;
    }

    unsigned int i = 0, comp_id = 0;
    struct stack *stack = calloc(1, sizeof(*stack));
    struct stack *call_stack = calloc(1, sizeof(*call_stack));
    double now = gettime();
    unsigned int ndone = 0, lastdone = 0;

    // Only need to iterate once as the graph is connected
    for (unsigned int v = 0; v < 1 /*global.graph.size*/; v++) {
        struct node *n = global.graph.nodes[v];
        if (scc[v].index == -1) {
            stack_push(&call_stack, n, 0);
            while (!stack_empty(call_stack)) {
                unsigned int pi;
                n = stack_pop(&call_stack, &pi);
                if (pi == 0) {
                    scc[n->id].index = i;
                    scc[n->id].lowlink = i;
                    i++;
                    stack_push(&stack, n, 0);
                    n->on_stack = true;
                }
                else {
                    assert(pi > 0);
                    struct edge *e = &node_edges(n)[pi - 1];
                    struct node *prev = edge_dst(e);
                    if (scc[prev->id].lowlink < scc[n->id].lowlink) {
                        scc[n->id].lowlink = scc[prev->id].lowlink;
                    }
                }
                while (pi < n->nedges) {
                    struct edge *e = &node_edges(n)[pi];
                    struct node *w = edge_dst(e);
                    if (scc[w->id].index < 0) {
                        break;
                    }
                    if (w->on_stack && scc[w->id].index < scc[n->id].lowlink) {
                        scc[n->id].lowlink = scc[w->id].index;
                    }
                    pi += 1;
                }
                if (pi < n->nedges) {
                    struct edge *e = &node_edges(n)[pi];
                    stack_push(&call_stack, n, pi + 1);
                    stack_push(&call_stack, edge_dst(e), 0);
                }
                else if (scc[n->id].lowlink == scc[n->id].index) {
                    for (;;) {
                        ndone++;
                        if (ndone - lastdone >= 10000000 && gettime() - now > 3) {
                            printf("        completed %u/%u states (%.2f%%)\n", ndone, global.graph.size, 100.0 * ndone / global.graph.size);
                            now = gettime();
                            lastdone = ndone;
                        }
                        struct node *n2 = stack_pop(&stack, NULL);
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

    global.scc = scc;
    global.ncomponents = comp_id;
}

// Add a single node to the given node set
static void node_set_add(struct node_set *ns, uint32_t node){
    // Use binary search to try to find the entry.
    unsigned int b = 0, e = ns->nnodes, m = 0;
    while (b < e) {
        m = (b + e) / 2;
        if (ns->list[m] == node) {
            return;
        }
        if (ns->list[m] < node) {
            b = m + 1;
        }
        else {
            e = m;
        }
    }

    // Make sure we have enough memory
    if (ns->nnodes == ns->nallocated) {
        ns->nallocated = (ns->nallocated + 8) * 2;
        ns->list = realloc(ns->list, ns->nallocated * sizeof(*ns->list));
    }

    // Make space
    if (b < ns->nnodes) {
        memmove(&ns->list[b+1], &ns->list[b], (ns->nnodes - b) * sizeof(*ns->list));
    }

    ns->list[b] = node;
    ns->nnodes += 1;
}

// Check if ns is a subset of ns2
// TODO.  Should probably use binary search for efficiency
static inline bool node_set_issubset(struct node_set *ns, struct node_set *ns2){
    for (unsigned int i = 0, j = 0; i < ns->nnodes; j++) {
        if (j == ns2->nnodes) {
            return false;
        }
        if (ns->list[i] < ns2->list[j]) {
            return false;
        }
        if (ns->list[i] == ns2->list[j]) {
            i++;
        }
    }
    return true;
}

// Compute the union of ns and ns2 and store in ns.
static inline void node_set_union(struct node_set *ns, struct node_set *ns2){
    // If there's just one node in ns2, node_set_add is more efficient.
    // TODO.  Maybe true for two or three nodes too...
    if (ns2->nnodes == 1) {
        node_set_add(ns, ns2->list[0]);
        return;
    }

    // If ns2 is a subset of ns we're done.
    // TODO.  Might not be worth the overhead.
    if (node_set_issubset(ns2, ns)) {
        return;
    }

    // Allocate enough space for the union
    uint32_t *list = malloc((ns->nnodes + ns2->nnodes) * sizeof(uint32_t));

    unsigned int i = 0, j = 0, k = 0;
    for (; i < ns->nnodes && j < ns2->nnodes; k++) {
        if (ns->list[i] < ns2->list[j]) {
            list[k] = ns->list[i++];
        }
        else if (ns->list[i] > ns2->list[j]) {
            list[k] = ns2->list[j++];
        }
        else {
            assert(ns->list[i] == ns2->list[j]);
            list[k] = ns->list[i++];
            j++;
        }
    }
    unsigned int todo = (ns->nnodes - i);
    memcpy(&list[k], &ns->list[i], todo * sizeof(uint32_t));
    k += todo;
    todo = (ns2->nnodes - j);
    memcpy(&list[k], &ns2->list[j], todo * sizeof(uint32_t));
    k += todo;

    free(ns->list);
    ns->list = list;
    ns->nallocated = ns->nnodes + ns2->nnodes;
    ns->nnodes = k;
}

// This is the same as tarjan(), except that it only considers
// epsilon edges in the graph.
static void tarjan_epsclosure(){
    struct eps_scc *scc = malloc(global.graph.size * sizeof(*scc));
    for (unsigned int v = 0; v < global.graph.size; v++) {
        scc[v].index = -1;
    }

    unsigned int i = 0, comp_id = 0;
    struct stack *stack = calloc(1, sizeof(*stack));
    struct stack *call_stack = calloc(1, sizeof(*call_stack));
    double now = gettime();
    unsigned int ndone = 0, lastdone = 0;

    for (unsigned int v = 0; v < global.graph.size; v++) {
        struct node *n = global.graph.nodes[v];
        if (scc[v].index == -1) {
            stack_push(&call_stack, n, 0);
            while (!stack_empty(call_stack)) {
                unsigned int pi;
                n = stack_pop(&call_stack, &pi);
                if (pi == 0) {
                    scc[n->id].index = i;
                    scc[n->id].lowlink = i;
                    i++;
                    stack_push(&stack, n, 0);
                    n->eps_on_stack = true;
                }
                else {
                    assert(pi > 0);
                    struct edge *e = &node_edges(n)[pi - 1];
                    struct node *prev = edge_dst(e);
                    if (scc[prev->id].lowlink < scc[n->id].lowlink) {
                        scc[n->id].lowlink = scc[prev->id].lowlink;
                    }
                }
                while (pi < global.neps[n->id]) {
                    struct edge *e = &node_edges(n)[pi];
                    struct node *w = edge_dst(e);
                    if (scc[w->id].index < 0) {
                        break;
                    }
                    if (w->eps_on_stack && scc[w->id].index < scc[n->id].lowlink) {
                        scc[n->id].lowlink = scc[w->id].index;
                    }
                    pi += 1;
                }
                if (pi < global.neps[n->id]) {
                    struct edge *e = &node_edges(n)[pi];
                    stack_push(&call_stack, n, pi + 1);
                    stack_push(&call_stack, edge_dst(e), 0);
                }
                else if (scc[n->id].lowlink == scc[n->id].index) {
                    struct eps_component *ec = new_alloc(struct eps_component);
                    for (;;) {
                        ndone++;
                        if (ndone - lastdone >= 10000000 && gettime() - now > 3) {
                            printf("        completed %u/%u states (%.2f%%)\n", ndone, global.graph.size, 100.0 * ndone / global.graph.size);
                            now = gettime();
                            lastdone = ndone;
                        }
                        struct node *n2 = stack_pop(&stack, NULL);
                        n2->eps_on_stack = false;
                        node_set_add(&ec->ns, n2->id);
                        scc[n2->id].component = ec;
                        struct edge *e = node_edges(n2);
                        for (unsigned int i = 0; i < global.neps[n2->id]; i++, e++) {
                            struct node *n3 = edge_dst(e);
                            struct eps_component *ec2 = scc[n3->id].component;
                            // If the following fails, this means that n3 is in the
                            // current component but hasn't been "popped" yet.
                            if (ec2 != NULL) {
#ifdef notdef
                                for (unsigned int j = 0; j < ec2->ns.nnodes; j++) {
                                    node_set_add(&ec->ns, ec2->ns.list[j]);
                                }
#else
                                node_set_union(&ec->ns, &ec2->ns);
#endif
                            }
                        }
                        if (n2 == n) {
                            ec->ns.list = realloc(ec->ns.list,
                                    ec->ns.nnodes * sizeof(*ec->ns.list));
                            ec->ns.nallocated = ec->ns.nnodes;
                            break;
                        }
                    }
                    comp_id++;
                }
            }
        }
    }

    global.eps_scc = scc;
    global.eps_ncomponents = comp_id;
}

struct dfa_node {
    unsigned int id;            // DFA state id
    struct dict *transitions;   // map of symbol to dfa_node
    bool final;                 // final state
};

struct dfa_env {
    struct dict *dfa;           // map of node set to dfa state index
    struct dict_assoc **todo;   // queue of dfa nodes that need to be considered
    unsigned int allocated;     // current allocated size of queue
    uint32_t next_id;           // id of next dfa node to be created
    struct dfa_node *current;
    FILE *hfa;                  // .hfa output file
    struct dict *symbols;       // maps symbols to symbol ids
    bool first;                 // for "last comma problem"
};

static struct dfa_node *nfa2dfa_add_node(struct dfa_env *de, struct node_set *ns){
    bool new;
    struct dict_assoc *da = dict_find(de->dfa, &global.workers[0].allocator,
                    ns->list, ns->nnodes * sizeof(uint32_t), &new);
    struct dfa_node *dn = (struct dfa_node *) &da[1];
    if (new) {
        dn->id = de->next_id;
        dn->transitions = dict_new("nfa2dfa trans", sizeof(uint32_t), 10, 0, false, false);
        for (unsigned int i = 0; i < ns->nnodes; i++) {
            struct node *n = global.graph.nodes[ns->list[i]];
            if (n->final) {
                dn->final = true;
                break;
            }
        }
        if (de->next_id == de->allocated) {
            de->allocated = (de->allocated + 1) * 2;
            de->todo = realloc(de->todo, de->allocated * sizeof(*de->todo));
        }
        de->todo[de->next_id++] = da;
    }

    return dn;
}

static void nfa2dfa_helper(void *env, const void *key, unsigned int key_size, void *value){
    assert(key_size == sizeof(hvalue_t));       // should be a symbol
    struct dfa_env *de = env;
    struct node_set *ns = value;

    // Compute the nodes in this dfa state using precomputed closures
    struct node_set uni;
    memset(&uni, 0, sizeof(uni));
    for (unsigned int i = 0; i < ns->nnodes; i++) {
        struct node_set *clos = &global.eps_scc[ns->list[i]].component->ns;

        // TODO.  Curiously, adding a node at a time is often more efficient
        //        than computing the union.  In fact, it seems that computing
        //        the union is never worth it here in the few experiments that
        //        I've tried.  Surprising to me...
        if (clos->nnodes <= 5) {
            for (unsigned int j = 0; j < clos->nnodes; j++) {
                node_set_add(&uni, clos->list[j]);
            }
        }
        else {
            node_set_union(&uni, clos);
        }
    }
    free(ns->list);

    // Find or insert "state" in the dfa state table.
    struct dfa_node *dn = nfa2dfa_add_node(de, &uni);
    free(uni.list);

    // Add to the transitions.
    bool new;
    struct dict_assoc *da = dict_find(de->current->transitions,
                    &global.workers[0].allocator, key, key_size, &new);
    assert(new);
    uint32_t *pid = (uint32_t *) &da[1];
    *pid = dn->id;
}

static void nfa2dfa_dumper(void *env, const void *key, unsigned int key_size, void *value){
    assert(key_size == sizeof(hvalue_t));       // should be a symbol
    struct dfa_env *de = env;
    uint32_t *pid = value;

    bool new;
    unsigned int *symbol = dict_insert(de->symbols, &global.workers[0].allocator,
                                key, key_size, &new);
    assert(!new);
    if (de->first) {
        de->first = false;
    }
    else {
        fprintf(de->hfa, ",");
    }
    fprintf(de->hfa, "\n");
    fprintf(de->hfa, "     { \"src\": \"%u\", \"dst\": \"%u\", \"sym\": %u }",
                        de->current->id, *pid, *symbol - 1);
}

static unsigned int nfa2dfa(FILE *hfa, struct dict *symbols){
    struct dfa_env de;
    double start = gettime();

    de.dfa = dict_new("nfa2dfa", sizeof(struct dfa_node), global.graph.size, 0, false, false);
    de.next_id = 0;
    de.allocated = global.graph.size;   // decent initial estimate
    de.todo = malloc(de.allocated * sizeof(*de.todo));
    de.hfa = hfa;
    de.symbols = symbols;

    // Find the initial state.
    nfa2dfa_add_node(&de, &global.eps_scc[0].component->ns);

    // Go through the todo list
    unsigned int todo_index = 0;
    while (todo_index < de.next_id) {
        // Pacifier
        if (gettime() - start > 3) {
            printf("  NFA to DFA progress %u/%u=%.1f%%\n", todo_index, de.next_id, 100.0 * todo_index / de.next_id);
            start = gettime();
        }

        // The next dfa state to consider
        struct dict_assoc *da = de.todo[todo_index];
        de.current = (struct dfa_node *) &da[1];

        // Create a "symbol" table for this dfa state
        struct dict *d = dict_new("nfa2dfa symbols", sizeof(struct node_set), 10, 0, false, false);

        // Iterate of the nodes in the dfa state
        uint32_t *nodes = (uint32_t *) &de.current[1];
        unsigned int nnodes = da->len / sizeof(uint32_t);
        for (unsigned int i = 0; i < nnodes; i++) {
            unsigned int ni = nodes[i];                 // node index
            struct node *n = global.graph.nodes[ni];    // node pointer

            // Iterate of the edges in the node
            unsigned int neps = global.neps[ni];
            struct edge *e = node_edges(n) + neps;
            for (unsigned int j = neps; j < n->nedges; j++, e++) {
                struct step_output *so = edge_output(e);
                assert(so->nlog == 1);
                hvalue_t symbol = *step_log(so);

                // Lookup or create a node set for this symbol
                bool new;
                struct node_set *ns = dict_insert(d, &global.workers[0].allocator,
                                            &symbol, sizeof(symbol), &new);
                node_set_add(ns, edge_dst(e)->id);
            }
        }

        // d now contains, for each valid symbol, a node set that still needs to
        // be epsilon closed and then added to mapping.
        dict_iter(d, nfa2dfa_helper, &de);

        todo_index += 1;
    }

    printf("* Phase 4d: output the DFA (%u states)\n", de.next_id);

    // Now dump the whole thing
    fprintf(hfa, "  \"nodes\": [\n");
    for (unsigned int i = 0; i < de.next_id; i++) {
        struct dict_assoc *da = de.todo[i];
        struct dfa_node *dn = (struct dfa_node *) &da[1];
        fprintf(hfa, "    { \"idx\": \"%u\", \"type\": \"%s\" }", i,
                    dn->final ? "final" : "normal");
        if (i + 1 < de.next_id) {
            fprintf(hfa, ",\n");
        }
        else {
            fprintf(hfa, "\n");
        }
    }
    fprintf(hfa, "  ],\n");
    fprintf(hfa, "  \"edges\": [");
    de.first = true;
    for (unsigned int i = 0; i < de.next_id; i++) {
        struct dict_assoc *da = de.todo[i];
        de.current = (struct dfa_node *) &da[1];
        dict_iter(de.current->transitions, nfa2dfa_dumper, &de);
    }
    fprintf(hfa, "\n");
    fprintf(hfa, "  ]\n");

    return de.next_id;
}

// This routine removes all nodes that have a single incoming edge and it's
// an "epsilon" edge (empty print log).  These are essentially useless nodes.
static void destutter1(FILE *out, bool suppress){
    struct graph *graph = &global.graph;

    // If nothing got printed, we can just return a single node
    if (!global.printed_something) {
        graph->size = 1;
        struct node *n = global.graph.nodes[0] = calloc(1, sizeof(*n));
        n->final = true;
        return;
    }

    // Also suppress very large outputs when checking behaviors.
    if (suppress && graph->size > 100000) {
        graph->size = 1;
        struct node *n = global.graph.nodes[0] = calloc(1, sizeof(*n));
        n->final = true;
        fprintf(out, "  \"suppressed\": \"True\",\n");
        return;
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

// This function finds all the printed symbols in the Kripke structure and
// assigns a small unique identifier to each.
// TODO.  Perhaps should replace hvalue_t with this id in the graph while at it
static struct dict *collect_symbols(struct graph *graph){
    struct dict *symbols = dict_new("symbols", sizeof(unsigned int), 0, 0, false, false);
    unsigned int symbol_id = 0;

    // Also make a global list
    unsigned int allocated = 10;
    global.symbols = malloc(allocated * sizeof(*global.symbols));

    for (unsigned int i = 0; i < graph->size; i++) {
        struct node *n = graph->nodes[i];
        struct edge *e = node_edges(n);
        for (unsigned int k = 0; k < n->nedges; k++, e++) {
            for (unsigned int j = 0; j < edge_output(e)->nlog; j++) {
                hvalue_t symbol = step_log(edge_output(e))[j];
                bool new;
                unsigned int *p = dict_insert(symbols, NULL, &symbol, sizeof(symbol), &new);
                if (new) {
                    *p = ++symbol_id;
                    if (global.nsymbols == allocated) {
                        allocated = (allocated + 1) * 2;
                        global.symbols = realloc(global.symbols,
                                            allocated * sizeof(*global.symbols));
                    }
                    global.symbols[global.nsymbols++] = symbol;
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

// Split s into components separated by sep.  Returns #components.
// Return the components themselves into *parts.  All is malloc'd.
static unsigned int str_split(const char *s, char sep, char ***parts){
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

static void charm_dump(bool computed_components){
    FILE *df = fopen("charm.dump", "w");
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
                fprintf(df, "    component: %d\n", global.scc[i].component);
            }
            if (node->final) {
                fprintf(df, "    final\n");
            }
            fprintf(df, "    len to parent: %d\n", node->len);
            if (node_to_parent(node) != NULL) {
                fprintf(df, "    ancestors:");
                for (struct node *n = node->parent;; n = n->parent) {
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
                fprintf(df, "      %"PRI_HVAL": %u\n", state_ctx(state, i), state_multiplicity(state, i));
            }
#ifdef TODO
            if (state->stopbag != VALUE_DICT) {
                fprintf(df, "    stopbag:\n");
                unsigned int size;
                hvalue_t *vals = value_get(state->stopbag, &size);
                size /= 2 * sizeof(hvalue_t);
                for (unsigned int i = 0; i < size; i++) {
                    fprintf(df, "      %"PRI_HVAL": %d\n", vals[2*i], (int) VALUE_FROM_INT(vals[2*i+1]));;
                }
            }
#endif
            // fprintf(df, "    len: %u %u\n", node->len, node->steps);
            if (node->failed) {
                fprintf(df, "    failed\n");
            }
            fprintf(df, "    fwd:\n");
            int eno = 0;
            struct edge *edge = node_edges(node);
            for (unsigned int i = 0; i < node->nedges; i++, edge++) {
                fprintf(df, "        %d:\n", eno);
                struct context *ctx = value_get(edge_input(edge)->ctx, NULL);
                struct node *dst = edge_dst(edge);
                if (computed_components) {
                    fprintf(df, "            node: %d (%d)\n", dst->id, global.scc[dst->id].component);
                }
                else {
                    fprintf(df, "            node: %d\n", dst->id);
                }
                fprintf(df, "            context before: %"PRIx64" pc=%d\n", edge_input(edge)->ctx, ctx->pc);
                ctx = value_get(edge_output(edge)->after, NULL);
                fprintf(df, "            context after:  %"PRIx64" pc=%d\n", edge_output(edge)->after, ctx->pc);
                if (edge->failed) {
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

#ifndef _WIN32
static void inthandler(int sig){
    printf("Caught interrupt\n");
    fflush(stdout);
    fflush(stderr);
    _exit(1);
}

static void alrmhandler(int sig){
    printf("Timeout exceeded\n");
    fflush(stdout);
    fflush(stderr);
    _exit(1);
}
#endif

// Error in arguments.  Print a "usage" message and exit
static void usage(char *prog){
    fprintf(stderr, "Usage: %s [-c] [-t<maxtime>] [-B<dfafile>] -o<outfile> file.json\n", prog);
    exit(1);
}

static bool endsWith(char *s, char *suffix){
    unsigned int n = strlen(s);
    unsigned int m = strlen(suffix);
    if (n < m) {
        return false;
    }
    return strcmp(s + n - m, suffix) == 0;
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
    bool cflag = false, dflag = false, Dflag = false, bflag = false;
    int i, maxtime = 300000000 /* about 10 years */;
    char *outfile = NULL, *hfaout = NULL, *dfafile = NULL, *worker_flag = NULL;
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
            global.no_race_detect = true;
            break;
        case 'U':
            global.do_not_pin = true;
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
        case 'b':
            bflag = true;
            break;
        case 'o':
            {
                char *name = &argv[i][2];
                if (endsWith(name, ".hco")) {
                    outfile = name;
                }
                else if (endsWith(name, ".hfa")) {
                    hfaout = name;
                }
                else {
                    fprintf(stderr, "%s: unknown suffix in %s\n", argv[0], argv[i]);
                    exit(1);
                }
            }
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
    bool print_vproc_info = false;
    if (worker_flag == NULL) {
        global.nworkers = n_vproc_info;
        for (unsigned int i = 0; i < n_vproc_info; i++) {
            vproc_info[i].selected = true;
        }
    }
    else {
        // -w/... causes virtual processors to be printed.
        if (*worker_flag == '/') {
            print_vproc_info = true;
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

    if (print_vproc_info) {
        vproc_info_dump();
    }

    if (dflag) {
        printf("* Phase 2: execute directly\n");
    }
    else {
        printf("* Phase 2: run the model checker (nworkers = %d)\n", global.nworkers);
    }

    // Initialize barriers for the three phases (see struct worker definition)
    barrier_init(&global.start_barrier, global.nworkers);
    barrier_init(&global.middle_barrier, global.nworkers);
    barrier_init(&global.end_barrier, global.nworkers);

    // initialize modules
    mutex_init(&global.inv_lock);
    global.values = dict_new("values", 0, 4096, global.nworkers, true, true);

    graph_init(&global.graph);
    global.failures = NULL;
    global.seqs = VALUE_SET;

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
    if (jv == NULL || jv->type != JV_MAP) {
        fprintf(stderr, "%s: bad input file: %s\n", argv[0], fname);
        exit(1);
    }
    free(buf_orig);

    // Allocate space for worker info
    struct worker *workers = calloc(global.nworkers, sizeof(*workers));
    global.workers = workers;
    for (unsigned int i = 0; i < global.nworkers; i++) {
        struct worker *w = &workers[i];

        w->timeout = timeout;
        w->index = i;

        // Create a context for evaluating invariants
        w->inv_step.ctx = calloc(1, sizeof(struct context) +
                                MAX_CONTEXT_STACK * sizeof(hvalue_t));
        // w->inv_step.ctx->name = value_put_atom(&allocator, "__invariant__", 13);
        w->inv_step.ctx->vars = VALUE_DICT;
        w->inv_step.ctx->atomic = w->inv_step.ctx->readonly = 1;
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

        struct shard *shard = &w->shard;
        shard->states = dict_new("shard states", sizeof(struct node), 0, 0, false, false);
        shard->peers = calloc(global.nworkers, sizeof(*shard->peers));
        for (unsigned int si2 = 0; si2 < global.nworkers; si2++) {
            shard->peers[si2].last = &shard->peers[si2].first;
        }
        shard->todo_buffer = shard->tb_head = shard->tb_tail = walloc_fast(w, sizeof(*shard->tb_tail));
        shard->todo_buffer->nresults = 0;
        shard->todo_buffer->next = NULL;
    }

    // Pin workers to particular virtual processors
    unsigned int worker_index = 0;
    vproc_tree_alloc(vproc_root, workers, &worker_index, global.nworkers);

    if (print_vproc_info) {
        printf("Assignment:");
        for (unsigned int i = 0; i < global.nworkers; i++) {
            struct worker *w = &workers[i];
            printf(" %u", w->vproc);
        }
        printf("\n");
    }

    // Prefer to allocate memory at the memory bank attached to the first worker.
    // The main advantage of this is that if the entire Kripke structure is stored
    // there, the Tarjan SCC algorithm (executed by worker 0) will run significantly
    // faster.
#ifdef __linux__
#ifdef xxxNUMA
    numa_available();
    numa_set_preferred(vproc_info[workers[0].vproc].ids[0]);
#endif
#endif

    ops_init(&workers[0].allocator);

    // Read and parse the DFA if any
    if (dfafile != NULL) {
        global.dfa = dfa_read(&workers[0].allocator, dfafile);
        if (global.dfa == NULL) {
            exit(1);
        }
    }

    // travel through the json code contents to create the code array
    struct json_value *jc = dict_lookup(jv->u.map, "code", 4);
    assert(jc->type == JV_LIST);
    global.code = code_init_parse(&workers[0].allocator, jc);

    if (has_countLabel) {
        fprintf(stderr, "countLabel no longer supported\n");
        exit(1);
    }

    // Initialize some more of the worker info.
    for (unsigned int i = 0; i < global.nworkers; i++) {
        struct worker *w = &workers[i];
        w->profile = calloc(global.code.len, sizeof(*w->profile));
        w->nworkers = global.nworkers;
        w->dfa = global.dfa;
    }

    // Create an initial state.  Start with the initial context.
    struct context *init_ctx = calloc(1, sizeof(struct context) + MAX_CONTEXT_STACK * sizeof(hvalue_t));
    init_ctx->vars = VALUE_DICT;
    init_ctx->atomic = 1;
    init_ctx->initial = true;
    value_ctx_push(init_ctx, VALUE_LIST);

    // Now create the state.  If running direct, keep room to grow.
    struct state *state = calloc(1, sizeof(struct state) +
            (dflag ? 256 : 1) * (sizeof(hvalue_t) + 1));
    state->vars = VALUE_DICT;
    hvalue_t ictx = value_put_context(&workers[0].allocator, init_ctx);
    state->type = STATE_NORMAL;
    state->bagsize = state->total = 1;
    state_ctxlist(state)[0] = ictx | ((hvalue_t) 1 << STATE_M_SHIFT);
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
        srand((unsigned) gettime());

#ifndef _WIN32
        signal(SIGALRM, alrmhandler);
        alarm((int) maxtime);
#endif

        struct state *sc = calloc(1, sizeof(struct state) +
                    256 * (sizeof(hvalue_t) + 1));
        for (unsigned int i = 0; i < 1; i++) {
            if (i > 0 && i % 100 == 0) {
                printf("TIME %d\n", i);
            }
            memcpy(sc, state, state_size(state));
            direct_run(sc, i);
        }
        if (global.dfa != NULL) {
            dfa_dump(global.dfa);
        }
        exit(0);
    }

    global.computations = dict_new("computations", sizeof(struct step_condition), 16 * 1024, global.nworkers, false, true);

    bool new;
    struct dict_assoc *hn = dict_find_new(global.workers[0].shard.states, &workers[0].allocator, state, state_size(state), sizeof(struct edge), &new, meiyan2(state));
    struct node *node = (struct node *) &hn[1];
    memset(node, 0, sizeof(*node));
    node->initial = true;
    node->nedges = 1;
    memset(node_edges(node), 0, sizeof(struct edge));

    // Add node to the todo list of shard 0
    // TODO.  Should probably just add the state, not the node
    global.workers[0].shard.todo_buffer->results[0] = node;
    global.workers[0].shard.todo_buffer->nresults = 1;
    global.workers[0].shard.tb_size = 1;

    // Compute how much table space is allocated
    // TODO.  Add per worker stuff
    global.allocated = global.graph.size * sizeof(struct node *) +
                             dict_allocated(global.values);

    // Start all but one of the workers. All will wait on the start barrier
    for (unsigned int i = 1; i < global.nworkers; i++) {
        thread_create(worker, &workers[i]);
    }

    global.starttime = gettime();

    // Run the last worker.  When it terminates the model checking is done.
    worker(&workers[0]);

    // Collect the failures of all the workers.  Also keep track if
    // any of the workers printed something
    for (unsigned int i = 0; i < global.nworkers; i++) {
        if (workers[i].printed_something) {
            global.printed_something = true;
        }
        collect_failures(&workers[i]);
    }

    // If no output file is desired, we're done.
    if (outfile == NULL) {
        exit(0);
    }

    // Put the hashtables into "sequential mode" to avoid locking overhead.
    dict_set_sequential(global.values);
    dict_set_sequential(global.computations);

    printf("* Phase 3b: Further analysis\n");

    bool computed_components = false;

    // charm_dump(computed_components);

#ifdef OBSOLETE
    // Do a cheap check for deadlock if no other errors have been detected
    // TODO.  Could be parallelized
    if (global.failures == NULL) {
        if (global.graph.size > 10000) {
            printf("    * Check for deadlock\n");
            fflush(stdout);
        }
        for (unsigned int i = 0; i < global.graph.size; i++) {
            struct node *node = global.graph.nodes[i];
            struct state *state = node_state(node);
            bool dead_end = true;
            struct edge *e = node_edges(node);
            for (unsigned int j = 0; j < node->nedges; j++, e++) {
                if (edge_dst(e) != node) {
                    dead_end = false;
                    break;
                }
            }
            if (dead_end) {
                bool final = value_state_all_eternal(state);
                if (final) {
                    // If an input dfa was specified, it should also be in the
                    // final state.
                    if (global.dfa != NULL &&
                            !dfa_is_final(global.dfa, state->dfa_state)) {
                        struct failure *f = new_alloc(struct failure);
                        f->type = FAIL_BEHAVIOR_FINAL;
                        f->node = node->parent;
                        f->edge = node_to_parent(node);
                        add_failure(&global.failures, f);
                    }
                    else {
                        node->final = true;
                    }
                }
                else {
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_DEADLOCK;
                    f->node = node->parent;
                    f->edge = node_to_parent(node);
                    assert(f->edge != NULL);
                    add_failure(&global.failures, f);
                }
            }
        }
    }
#endif

    // If no failures were detected (yet), look for deadlock and busy
    // waiting.
    // TODO.  Also look for other final states and evaluate more finally
    //        clauses.  This can happen if an eternal thread sits in
    //        a loop like:  await x and y
    if (global.failures == NULL /* && loops_possible */) {
        if (global.graph.size > 10000) {
            printf("    * Determine strongly connected components\n");
            fflush(stdout);
        }
        double now = gettime();
        tarjan();
        computed_components = true;
        printf("        * %u components (%.2lf seconds)\n", global.ncomponents, gettime() - now);

#ifdef DUMP_GRAPH
        printf("digraph Harmony {\n");
        for (unsigned int i = 0; i < global.graph.size; i++) {
            printf(" s%u [label=\"%u/%u\"]\n", i, i, global.scc[i].component);
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
            assert(global.scc[i].component < global.ncomponents);
            struct component *comp = &components[global.scc[i].component];
            struct node *node = global.graph.nodes[i];

            // See if this is the first state that we are looking at for
            // this component, make this state the 'representative' for
            // this component.
            if (comp->size == 0) {
                comp->rep = node;
                comp->all_same = value_state_all_eternal(node_state(node));
            }
            else if (node_state(node)->vars != node_state(comp->rep)->vars
                        || !value_state_all_eternal(node_state(node))) {
                comp->all_same = false;
            }
            comp->size++;

            // If we already determined that this component has a way out,
            // we're done.
            if (comp->good) {
                continue;
            }

            // If this component has a way out, it is good
            struct edge *edge = node_edges(node);
            for (unsigned int i = 0; i < node->nedges && !comp->good; i++, edge++) {
                if (global.scc[edge_dst(edge)->id].component != global.scc[node->id].component) {
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

        // If we haven't found any failures yet, look for states in bad components.
        // If there are none, look for busy waiting states.
        if (global.failures == NULL) {
            // Report the states in bad components as non-terminating.
            int nbad = 0;
            for (unsigned int i = 0; i < global.graph.size; i++) {
                struct node *node = global.graph.nodes[i];
                if (!components[global.scc[i].component].good) {
                    nbad++;
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_TERMINATION;
                    if (node->nedges == 1) {
                        f->node = node;
                        f->edge = node_edges(node);
                    }
                    else {
                        f->node = node->parent;
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
                    if (components[global.scc[i].component].size > 1) {
                        detect_busywait(global.graph.nodes[i]);
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
                struct edge *edge = node_edges(node);
                for (unsigned int k = 0; k < node->nedges; k++, edge++) {
                    struct state *state = node_state(node);
                    unsigned int j;
                    for (j = 0; j < state->bagsize; j++) {
                        if (state_ctx(state, j) == edge_input(edge)->ctx) {
                            break;
                        }
                    }
                    assert(j < state->bagsize);
                    if (edge->failed) {
                        fprintf(df, " s%u -> s%u [style=%s label=\"F %u\"]\n",
                            node->id, edge_dst(edge)->id,
                            node_to_parent(edge_dst(edge)) == edge ? "solid" : "dashed",
                            state_multiplicity(state, j));
                    }
                    else {
                        fprintf(df, " s%u -> s%u [style=%s label=\"%u\"]\n",
                            node->id, edge_dst(edge)->id,
                            node_to_parent(edge_dst(edge)) == edge ? "solid" : "dashed",
                            state_multiplicity(state, j));
                    }
                }
            }
            fprintf(df, "}\n");
            fclose(df);
        }

        charm_dump(computed_components);
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
        destutter1(out, dfafile != NULL && !bflag);

        // Output the symbols
        // TODO.  This can probably be done more efficiently (and in parallel if needed)
        struct dict *symbols = collect_symbols(&global.graph);
        fprintf(out, "  \"symbols\": {\n");
        struct symbol_env se = { .out = out, .first = true };
        dict_iter(symbols, print_symbol, &se);
        fprintf(out, "\n");
        fprintf(out, "  },\n");

        if (hfaout != NULL) {
            FILE *hfa = fopen(hfaout, "w");
            if (hfa == NULL) {
                fprintf(stderr, "%s: can't create %s\n", argv[0], hfaout);
                exit(1);
            }
            fprintf(hfa, "{\n");
            fprintf(hfa, "  \"initial\": \"0\",\n");
            fprintf(hfa, "  \"symbols\": [\n");
            for (unsigned int i = 0; i < global.nsymbols; i++) {
                char *p = value_json(global.symbols[i]);
                fprintf(hfa, "    %s", p);
                if (i + 1 < global.nsymbols) {
                    fprintf(hfa, ",\n");
                }
                else {
                    fprintf(hfa, "\n");
                }
                free(p);
            }
            fprintf(hfa, "  ],\n");
            printf("* Phase 4b: epsilon closure\n");
            epsilon_closure_prep();     // move epsilon edges to start of each node
            tarjan_epsclosure();
            printf("* Phase 4c: convert NFA to DFA\n");
            unsigned int size = nfa2dfa(hfa, symbols);
            fprintf(hfa, "}\n");
            fclose(hfa);
            fprintf(out, "  \"dfasize\": %u,\n", size);
        }

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
            if (bad == NULL || edge_dst(bad->edge)->len < edge_dst(f->edge)->len) {
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
        case FAIL_BEHAVIOR_BAD:
            printf("    * **Behavior Violation**: unexpected output\n");
            fprintf(out, "  \"issue\": \"Behavior violation: unexpected output\",\n");
            break;
        case FAIL_BEHAVIOR_FINAL:
            printf("    * **Behavior Violation**: terminal state not final\n");
            fprintf(out, "  \"issue\": \"Behavior violation: terminal state not final\",\n");
            break;
        case FAIL_INFLOOP:
            printf("    * **Infinite Loop**\n");
            fprintf(out, "  \"issue\": \"Non-terminating state\",\n");
            break;
        case FAIL_DEADLOCK:
            printf("    * **Non-terminating state (possibly deadlock)**\n");
            fprintf(out, "  \"issue\": \"Non-terminating state\",\n");
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
        assert(bad->node != NULL);
        // assert(bad->edge->dst != NULL);
        path_serialize(bad->node, bad->edge);

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
