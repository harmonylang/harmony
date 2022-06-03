#include "head.h"

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/param.h>
#include <unistd.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <errno.h>
#include <assert.h>
#include <time.h>

#include "global.h"
#include "global.h"
#include "thread.h"
#include "charm.h"
#include "ops.h"
#include "dot.h"
#include "strbuf.h"
#include "iface/iface.h"
#include "hashdict.h"
#include "dfa.h"
#include "thread.h"
#include "spawn.h"

#define WALLOC_CHUNK    (1024 * 1024)

// For -d option
unsigned int run_count;  // counter of #threads
mutex_t run_mutex;       // to protect count
mutex_t run_waiting;     // for main thread to wait on

// One of these per worker thread
struct worker {
    struct global_t *global;     // global state
    double timeout;
    barrier_t *start_barrier, *middle_barrier, *end_barrier;

    struct dict *visited;

    unsigned int index;          // index of worker
    unsigned int nworkers;       // total number of workers
    int timecnt;                 // to reduce gettime() overhead
    struct step inv_step;        // for evaluating invariants

    struct node *results;       // list of resulting states
    unsigned int count;         // number of resulting states
    unsigned int node_id;       // node_ids to use for resulting states
    struct failure *failures;   // list of failures

    char *alloc_buf;            // allocated buffer
    char *alloc_ptr;            // pointer into allocated buffer

    struct allocator allocator; // mostly for hashdict

    // These need to be next to one another
    struct context ctx;
    hvalue_t stack[MAX_CONTEXT_STACK];
};

// Per thread one-time memory allocator (no free)
static void *walloc(void *ctx, unsigned int size, bool zero){
    struct worker *w = ctx;

    if (size > WALLOC_CHUNK) {
        return zero ? calloc(1, size) : malloc(size);
    }
    size = (size + 0xF) & ~0xF;     // align to 16 bytes
    if (w->alloc_ptr + size > w->alloc_buf + WALLOC_CHUNK) {
        w->alloc_buf = malloc(WALLOC_CHUNK);
        w->alloc_ptr = w->alloc_buf;
    }
    void *result = w->alloc_ptr;
    w->alloc_ptr += size;
    if (zero) {
        memset(result, 0, size);
    }
    return result;
}

static void run_thread(struct global_t *global, struct state *state, struct context *ctx){
    struct step step;
    memset(&step, 0, sizeof(step));
    step.ctx = ctx;
    step.engine.values = &global->values;

    for (;;) {
        int pc = step.ctx->pc;
        struct instr_t *instrs = global->code.instrs;
        struct op_info *oi = instrs[pc].oi;
        (*oi->op)(instrs[pc].env, state, &step, global);
        if (step.ctx->terminated) {
            break;
        }
        if (step.ctx->failed) {
            char *s = value_string(step.ctx->ctx_failure);
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
		assert(step.ctx->pc < global->code.len);
    }

    mutex_acquire(&run_mutex);
    if (--run_count == 0) {
        mutex_release(&run_waiting);
    }
    mutex_release(&run_mutex);
}

static void wrap_thread(void *arg){
    struct spawn_info *si = arg;
    run_thread(si->global, si->state, si->ctx);
}

void spawn_thread(struct global_t *global, struct state *state, struct context *ctx){
    mutex_acquire(&run_mutex);
    run_count++;
    mutex_release(&run_mutex);

    struct spawn_info *si = new_alloc(struct spawn_info);
    si->global = global;
    si->state = state;
    si->ctx = ctx;
    thread_create(wrap_thread, si);
}

bool invariant_check(struct global_t *global, struct state *state, struct step *step, int end){
    assert(step->ctx->sp == 0);
    assert(!step->ctx->failed);
    step->ctx->pc++;
    while (step->ctx->pc != end) {
        struct op_info *oi = global->code.instrs[step->ctx->pc].oi;
        int oldpc = step->ctx->pc;
        (*oi->op)(global->code.instrs[oldpc].env, state, step, global);
        if (step->ctx->failed) {
            step->ctx->sp = 0;
            return false;
        }
        assert(step->ctx->pc != oldpc);
        assert(!step->ctx->terminated);
    }
    assert(step->ctx->sp == 1);
    step->ctx->sp = 0;
    assert(step->ctx->fp == 0);
    hvalue_t b = ctx_stack(step->ctx)[0];
    assert(VALUE_TYPE(b) == VALUE_BOOL);
    return VALUE_FROM_BOOL(b);
}

bool check_invariants(struct worker *w, struct node *node, struct step *step){
    struct global_t *global = w->global;
    struct state *state = &node->state;
    extern int invariant_cnt(const void *env);

    assert(VALUE_TYPE(state->invariants) == VALUE_SET);
    assert(step->ctx->sp == 0);
    unsigned int size;
    hvalue_t *vals = value_get(state->invariants, &size);
    size /= sizeof(hvalue_t);
    for (unsigned int i = 0; i < size; i++) {
        assert(VALUE_TYPE(vals[i]) == VALUE_PC);
        step->ctx->pc = VALUE_FROM_PC(vals[i]);
        assert(strcmp(global->code.instrs[step->ctx->pc].oi->name, "Invariant") == 0);
        int end = invariant_cnt(global->code.instrs[step->ctx->pc].env);
        bool b = invariant_check(global, state, step, end);
        if (step->ctx->failed) {
            printf("Invariant failed: %s\n", value_string(step->ctx->ctx_failure));
            b = false;
        }
        if (!b) {
            return false;
        }
    }
    return true;
}

// For tracking data races
static struct access_info *ai_alloc(struct worker *w, int multiplicity,
                        int atomic, int pc) {
    struct access_info *ai = walloc(w, sizeof(*ai), true);
    ai->multiplicity = multiplicity;
    ai->atomic = atomic;
    ai->pc = pc;
    return ai;
}

static bool onestep(
    struct worker *w,       // thread info
    struct node *node,      // starting node
    struct state *sc,       // actual state
    hvalue_t ctx,           // context identifier
    struct step *step,      // step info
    hvalue_t choice,        // if about to make a choice, which choice?
    bool interrupt,         // start with invoking interrupt handler
    bool infloop_detect,    // try to detect infloop from the start
    int multiplicity        // #contexts that are in the current state
) {
    assert(!step->ctx->terminated);
    assert(!step->ctx->failed);

    struct global_t *global = w->global;

    // See if we should also try an interrupt.
    if (interrupt) {
        assert(step->ctx->extended);
		assert(step->ctx->ctx_trap_pc != 0);
        interrupt_invoke(step);
    }

    // Copy the choice
    hvalue_t choice_copy = choice;

    bool choosing = false, infinite_loop = false;
    struct dict *infloop = NULL;        // infinite loop detector
    unsigned int instrcnt = 0;
    struct state as_state;
    hvalue_t as_context = 0;
    unsigned int as_instrcnt = 0;
    bool rollback = false, failure = false, stopped = false;
    bool terminated = false;
    for (;;) {
        int pc = step->ctx->pc;

        // If I'm pthread 0 and it's time, print some stats
        if (w->index == 0 && w->timecnt-- == 0) {
            double now = gettime();
            if (now - global->lasttime > 1) {
                if (global->lasttime != 0) {
                    assert(strcmp(global->code.instrs[step->ctx->entry].oi->name, "Frame") == 0);
                    const struct env_Frame *ef = global->code.instrs[step->ctx->entry].env;
                    char *p = value_string(ef->name);
                    fprintf(stderr, "%s pc=%d states=%d diameter=%u queue=%d\n",
                            p, step->ctx->pc, global->enqueued, global->diameter, global->enqueued - global->dequeued);
                    free(p);
                }
                global->lasttime = now;
                if (now > w->timeout) {
                    fprintf(stderr, "charm: timeout exceeded\n");
                    exit(1);
                }
            }
            w->timecnt = 100;
        }

        struct instr_t *instrs = global->code.instrs;
        struct op_info *oi = instrs[pc].oi;
        if (instrs[pc].choose) {
            assert(step->ctx->sp > 0);
            assert(choice != 0);
            ctx_stack(step->ctx)[step->ctx->sp - 1] = choice;
            step->ctx->pc++;
        }
        else if (instrs[pc].atomicinc) {
            if (instrcnt == 0) {
                step->ctx->atomicFlag = true;
            }
            else if (step->ctx->atomic == 0) {
                // Save the current state in case it needs restoring
                as_state = *sc;
                as_context = value_put_context(&step->engine, step->ctx);
                as_instrcnt = instrcnt;
            }
            (*oi->op)(instrs[pc].env, sc, step, global);
        }
        else if (instrs[pc].atomicdec) {
            (*oi->op)(instrs[pc].env, sc, step, global);
            if (step->ctx->atomic == 0) {
                as_context = 0;
                as_instrcnt = 0;
            }
        }
        else {
            // Keep track of access for data race detection
            if (instrs[pc].load || instrs[pc].store || instrs[pc].del) {
                struct access_info *ai = ai_alloc(w, multiplicity, step->ctx->atomic, pc);
                ai->next = step->ai;
                step->ai = ai;
            }
            (*oi->op)(instrs[pc].env, sc, step, global);
        }
		assert(step->ctx->pc >= 0);
		assert(step->ctx->pc < global->code.len);

        instrcnt++;

        if (step->ctx->terminated) {
            terminated = true;
            break;
        }
        if (step->ctx->failed) {
            failure = true;
            break;
        }
        if (step->ctx->stopped) {
            stopped = true;
            break;
        }

        if (infloop_detect || instrcnt > 1000) {
            if (infloop == NULL) {
                infloop = dict_new("infloop1", 0, 0, 0, NULL, NULL);
            }

            int stacksize = step->ctx->sp * sizeof(hvalue_t);
            int combosize = sizeof(struct combined) + stacksize;
            struct combined *combo = calloc(1, combosize);
            combo->state = *sc;
            memcpy(&combo->context, step->ctx, sizeof(*step->ctx) + stacksize);
            bool new;
            dict_insert(infloop, NULL, combo, combosize, &new);
            free(combo);
            if (!new) {
                if (infloop_detect) {
                    value_ctx_failure(step->ctx, &step->engine, "infinite loop");
                    failure = infinite_loop = true;
                    break;
                }
                else {
                    // start over, as twostep does not have instrcnt optimization
                    return false;
                }
            }
        }

        if (step->ctx->pc == pc) {
            fprintf(stderr, ">>> %s\n", oi->name);
        }
        assert(step->ctx->pc != pc);
		assert(step->ctx->pc >= 0);
		assert(step->ctx->pc < global->code.len);

        /* Peek at the next instruction.
         */
        struct instr_t *next_instr = &global->code.instrs[step->ctx->pc];
        if (next_instr->choose) {
            assert(step->ctx->sp > 0);
#ifdef TODO
            if (0 && step->ctx->readonly > 0) {    // TODO
                value_ctx_failure(step->ctx, &step->engine, "can't choose in assertion or invariant");
                instrcnt++;
                failure = true;
                break;
            }
#endif
            hvalue_t s = ctx_stack(step->ctx)[step->ctx->sp - 1];
            if (VALUE_TYPE(s) != VALUE_SET) {
                value_ctx_failure(step->ctx, &step->engine, "choose operation requires a set");
                instrcnt++;
                failure = true;
                break;
            }
            unsigned int size;
            hvalue_t *vals = value_get(s, &size);
            size /= sizeof(hvalue_t);
            if (size == 0) {
                value_ctx_failure(step->ctx, &step->engine, "choose operation requires a non-empty set");
                instrcnt++;
                failure = true;
                break;
            }
            if (size == 1) {            // TODO.  This optimization is probably not worth it
                choice = vals[0];
            }
            else {
                choosing = true;
                break;
            }
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

            // Deal with interrupts if enabled
            if (step->ctx->extended && step->ctx->ctx_trap_pc != 0 &&
                                !step->ctx->interruptlevel) {
                // If this is a thread exit, break so we can invoke the
                // interrupt handler one more time
                if (next_instr->retop) {
                    hvalue_t ct = ctx_stack(step->ctx)[step->ctx->sp - 4];
                    assert(VALUE_TYPE(ct) == VALUE_INT);
                    if (VALUE_FROM_INT(ct) == CALLTYPE_PROCESS) {
                        breakable = true;
                    }
                }

                // If this is a setintlevel(True), should try interrupt
                // For simplicity, always try when setintlevel
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

    if (infloop != NULL) {
        dict_delete(infloop);
    }

    hvalue_t after;
    if (rollback) {
        *sc = as_state;
        after = as_context;
        instrcnt = as_instrcnt;
    }
    else {
        // Store new context in value directory.  Must be immutable now.
        after = value_put_context(&step->engine, step->ctx);
    }

    // Remove old context from the bag
    hvalue_t count = value_dict_load(sc->ctxbag, ctx);
    assert(VALUE_TYPE(count) == VALUE_INT);
    count -= 1 << VALUE_BITS;
    if (count == VALUE_INT) {
        sc->ctxbag = value_dict_remove(&step->engine, sc->ctxbag, ctx);
    }
    else {
        sc->ctxbag = value_dict_store(&step->engine, sc->ctxbag, ctx, count);
    }

    // If choosing, save in state
    if (choosing) {
        sc->choosing = after;
    }

    // Add new context to state unless it's terminated or stopped
    if (stopped) {
        sc->stopbag = value_bag_add(&step->engine, sc->stopbag, after, 1);
    }
    else if (!terminated) {
        sc->ctxbag = value_bag_add(&step->engine, sc->ctxbag, after, 1);
    }

    // Weight of this step
    int weight = (node->to_parent != NULL && ctx == node->to_parent->after) ? 0 : 1;

    // Allocate edge now
    struct edge *edge = walloc(w, sizeof(struct edge), false);
    edge->src = node;
    edge->ctx = ctx;
    edge->choice = choice_copy;
    edge->interrupt = interrupt;
    edge->after = after;
    edge->ai = step->ai;
    edge->log = step->log;
    edge->nlog = step->nlog;
    edge->nsteps = instrcnt;

    // See if this state has been computed before
    bool new;
    struct node *next = dict_insert_lock(w->visited, &w->allocator,
                sc, sizeof(struct state), &new);
    if (new) {
        memset(next, 0, sizeof(*next));
        next->len = node->len + weight;
        next->steps = node->steps + instrcnt;
        next->to_parent = edge;
        next->state = *sc;
        next->next = w->results;
        w->results = next;
        w->count++;
    }
    else {
        int len = node->len + weight;
        int steps = node->steps + instrcnt;
        if (len < next->len || (len == next->len && steps < next->steps)) {
            next->len = len;
            next->steps = steps;
            next->to_parent = edge;
        }
    }
    edge->dst = next;

    if (failure) {
        struct failure *f = new_alloc(struct failure);
        f->type = infinite_loop ? FAIL_TERMINATION : FAIL_SAFETY;
        f->edge = edge;
        f->next = w->failures;
        w->failures = f;
    }
    else if (sc->choosing == 0 && sc->invariants != VALUE_SET) {
        if (!check_invariants(w, next, &w->inv_step)) {
            struct failure *f = new_alloc(struct failure);
            f->type = FAIL_INVARIANT;
            f->edge = edge;
            f->next = w->failures;
            w->failures = f;
        }
    }

    // Backward edge from node to parent.
    edge->bwdnext = next->bwd;
    next->bwd = edge;

    dict_insert_release(w->visited, sc, sizeof(struct state));

    // We stole the access info and log
    step->ai = NULL;
    step->log = NULL;
    step->nlog = 0;

    return true;
}

static void make_step(
    struct worker *w,
    struct node *node,
    hvalue_t ctx,
    hvalue_t choice,       // if about to make a choice, which choice?
    int multiplicity       // #contexts that are in the current state
) {
    struct step step;
    memset(&step, 0, sizeof(step));
    step.engine.allocator = &w->allocator;
    step.engine.values = &w->global->values;

    // Make a copy of the state
    struct state sc = node->state;

    // Make a copy of the context
    unsigned int size;
    struct context *cc = value_get(ctx, &size);
    memcpy(&w->ctx, cc, size);
    step.ctx = &w->ctx;

    // See if we need to interrupt
    if (sc.choosing == 0 && cc->extended && cc->ctx_trap_pc != 0 && !cc->interruptlevel) {
        bool succ = onestep(w, node, &sc, ctx, &step, choice, true, false, multiplicity);
        if (!succ) {        // ran into an infinite loop
            (void) onestep(w, node, &sc, ctx, &step, choice, true, true, multiplicity);
        }

        sc = node->state;
        memcpy(&w->ctx, cc, size);
    }

    sc.choosing = 0;
    bool succ = onestep(w, node, &sc, ctx, &step, choice, false, false, multiplicity);
    if (!succ) {        // ran into an infinite loop
        (void) onestep(w, node, &sc, ctx, &step, choice, false, true, multiplicity);
    }
}

void print_vars(FILE *file, hvalue_t v){
    assert(VALUE_TYPE(v) == VALUE_DICT);
    unsigned int size;
    hvalue_t *vars = value_get(v, &size);
    size /= sizeof(hvalue_t);
    fprintf(file, "{");
    for (unsigned int i = 0; i < size; i += 2) {
        if (i > 0) {
            fprintf(file, ",");
        }
        char *k = value_string(vars[i]);
		int len = strlen(k);
        char *v = value_json(vars[i+1]);
        fprintf(file, " \"%.*s\": %s", len - 2, k + 1, v);
        free(k);
        free(v);
    }
    fprintf(file, " }");
}

char *json_escape_value(hvalue_t v){
    char *s = value_string(v);
    int len = strlen(s);
    if (*s == '[') {
        *s = '(';
        s[len-1] = ')';
    }
    char *r = json_escape(s, len);
    free(s);
    return r;
}

static bool print_trace(
    struct global_t *global,
    FILE *file,
    struct context *ctx,
    int pc,
    int fp,
    hvalue_t vars
) {
    if (fp == 0) {
        return false;
    }
    assert(fp >= 4);

	int level = 0, orig_pc = pc;
    if (strcmp(global->code.instrs[pc].oi->name, "Frame") == 0) {
        hvalue_t callval = ctx_stack(ctx)[ctx->sp - 2];
        assert(VALUE_TYPE(callval) == VALUE_INT);
        unsigned int call = VALUE_FROM_INT(callval);
        switch (call & CALLTYPE_MASK) {
        case CALLTYPE_PROCESS:
            pc++;
            break;
        case CALLTYPE_INTERRUPT:
        case CALLTYPE_NORMAL:
            pc = call >> CALLTYPE_BITS;
            break;
        default:
            fprintf(stderr, "call type: %x %d %d %d\n", call, ctx->sp, ctx->fp, ctx->pc);
            panic("print_trace: bad call type 1");
        }
    }
    while (--pc >= 0) {
        const char *name = global->code.instrs[pc].oi->name;

        if (strcmp(name, "Return") == 0) {
			level++;
		}
        else if (strcmp(name, "Frame") == 0) {
			if (level == 0) {
				if (fp > 4) {
                    hvalue_t callval = ctx_stack(ctx)[fp - 4];
                    assert(VALUE_TYPE(callval) == VALUE_INT);
                    unsigned int call = VALUE_FROM_INT(callval);
                    switch (call & CALLTYPE_MASK) {
                    case CALLTYPE_PROCESS:
                        panic("XXX");
                    case CALLTYPE_INTERRUPT:
                    case CALLTYPE_NORMAL:
                        { 
                            unsigned int npc = call >>= CALLTYPE_BITS;
                            hvalue_t nvars = ctx_stack(ctx)[fp - 2];
                            int nfp = ctx_stack(ctx)[fp - 1] >> VALUE_BITS;
                            if (print_trace(global, file, ctx, npc, nfp, nvars)) {
                                fprintf(file, ",\n");
                            }
                        }
                        break;
                    default:
                        panic("YYY");
                    }
				}
				fprintf(file, "            {\n");
				fprintf(file, "              \"pc\": \"%d\",\n", orig_pc);
				fprintf(file, "              \"xpc\": \"%d\",\n", pc);

				const struct env_Frame *ef = global->code.instrs[pc].env;
				char *s = value_string(ef->name), *a = NULL;
				int len = strlen(s);
                a = json_escape_value(ctx_stack(ctx)[fp - 3]);
				if (*a == '(') {
					fprintf(file, "              \"method\": \"%.*s%s\",\n", len - 2, s + 1, a);
				}
				else {
					fprintf(file, "              \"method\": \"%.*s(%s)\",\n", len - 2, s + 1, a);
				}

                hvalue_t callval = ctx_stack(ctx)[fp - 4];
                assert(VALUE_TYPE(callval) == VALUE_INT);
                unsigned int call = VALUE_FROM_INT(callval);
                switch (call & CALLTYPE_MASK) {
                case CALLTYPE_PROCESS:
                    fprintf(file, "              \"calltype\": \"process\",\n");
                    break;
                case CALLTYPE_NORMAL:
                    fprintf(file, "              \"calltype\": \"normal\",\n");
                    break;
                case CALLTYPE_INTERRUPT:
                    fprintf(file, "              \"calltype\": \"interrupt\",\n");
                    break;
                default:
                    printf(">>> %x\n", call);
                    panic("print_trace: bad call type 2");
                }

				free(s);
				free(a);
				fprintf(file, "              \"vars\": ");
				print_vars(file, vars);
				fprintf(file, "\n");
				fprintf(file, "            }");
				return true;
			}
            else {
                assert(level > 0);
                level--;
            }
        }
    }
    return false;
}

char *ctx_status(struct node *node, hvalue_t ctx) {
    if (node->state.choosing == ctx) {
        return "choosing";
    }
    while (node->state.choosing != 0) {
        node = node->to_parent->src;
    }
    struct edge *edge;
    for (edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
        if (edge->ctx == ctx) {
            break;
        }
    }
    if (edge != NULL && edge->dst == node) {
        return "blocked";
    }
    return "runnable";
}

void print_context(
    struct global_t *global,
    FILE *file,
    hvalue_t ctx,
    int tid,
    struct node *node
) {
    fprintf(file, "        {\n");
    fprintf(file, "          \"tid\": \"%d\",\n", tid);
    fprintf(file, "          \"yhash\": \"%"PRI_HVAL"\",\n", ctx);

    unsigned int size;
    struct context *c = value_get(ctx, &size);

#ifdef notdef
    fprintf(file, "          \"dump\": \"");
    unsigned char *p = (unsigned char *) c;
    for (unsigned i = 0; i < size; i++) {
        fprintf(file, "%02x", *p++);
    }
    fprintf(file, "\",\n");
#endif

    assert(strcmp(global->code.instrs[c->entry].oi->name, "Frame") == 0);
    const struct env_Frame *ef = global->code.instrs[c->entry].env;
    char *s = value_string(ef->name);
	int len = strlen(s);
    assert(c->sp > 1);
    char *a = json_escape_value(ctx_stack(c)[1]);
    if (*a == '(') {
        fprintf(file, "          \"name\": \"%.*s%s\",\n", len - 2, s + 1, a);
    }
    else {
        fprintf(file, "          \"name\": \"%.*s(%s)\",\n", len - 2, s + 1, a);
    }
    free(s);
    free(a);

    fprintf(file, "          \"entry\": \"%u\",\n", c->entry);

    fprintf(file, "          \"pc\": \"%d\",\n", c->pc);
    fprintf(file, "          \"fp\": \"%d\",\n", c->fp);

#ifdef notdef
    {
        fprintf(file, "STACK1 %d:\n", c->fp);
        for (int x = 0; x < c->sp; x++) {
            fprintf(file, "    %d: %s\n", x, value_string(ctx_stack(k)[x]));
        }
    }
#endif

    fprintf(file, "          \"trace\": [\n");
    print_trace(global, file, c, c->pc, c->fp, c->vars);
    fprintf(file, "\n");
    fprintf(file, "          ],\n");

    if (c->failed) {
        s = value_string(c->ctx_failure);
        fprintf(file, "          \"failure\": %s,\n", s);
        free(s);
    }

    if (c->extended && c->ctx_trap_pc != 0) {
        s = value_string(c->ctx_trap_pc);
        a = value_string(c->ctx_trap_arg);
        if (*a == '(') {
            fprintf(file, "          \"trap\": \"%s%s\",\n", s, a);
        }
        else {
            fprintf(file, "          \"trap\": \"%s(%s)\",\n", s, a);
        }
        free(a);
        free(s);
    }

    if (c->interruptlevel) {
        fprintf(file, "          \"interruptlevel\": \"1\",\n");
    }

    if (c->extended) {
        s = value_json(c->ctx_this);
        fprintf(file, "          \"this\": %s,\n", s);
        free(s);
    }

    if (c->atomic != 0) {
        fprintf(file, "          \"atomic\": \"%d\",\n", c->atomic);
    }
    if (c->readonly != 0) {
        fprintf(file, "          \"readonly\": \"%d\",\n", c->readonly);
    }

    if (c->terminated) {
        fprintf(file, "          \"mode\": \"terminated\"\n");
    }
    else if (c->failed) {
        fprintf(file, "          \"mode\": \"failed\"\n");
    }
    else if (c->stopped) {
        fprintf(file, "          \"mode\": \"stopped\"\n");
    }
    else {
        fprintf(file, "          \"mode\": \"%s\"\n", ctx_status(node, ctx));
    }

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

    fprintf(file, "        }");
}

void print_state(
    struct global_t *global,
    FILE *file,
    struct node *node
) {

#ifdef notdef
    fprintf(file, "      \"shared\": ");
    print_vars(file, node->state.vars);
    fprintf(file, ",\n");
#endif

    struct state *state = &node->state;
    extern int invariant_cnt(const void *env);
    struct step inv_step;
    memset(&inv_step, 0, sizeof(inv_step));
    inv_step.engine.values = &global->values;
    inv_step.ctx = calloc(1, sizeof(struct context) +
                        MAX_CONTEXT_STACK * sizeof(hvalue_t));

    // hvalue_t inv_nv = value_put_atom("name", 4);
    // hvalue_t inv_tv = value_put_atom("tag", 3);
    // inv_step.ctx->name = value_put_atom(&inv_step.engine, "__invariant__", 13);
    inv_step.ctx->vars = VALUE_DICT;
    inv_step.ctx->atomic = inv_step.ctx->readonly = 1;
    inv_step.ctx->interruptlevel = false;

    fprintf(file, "      \"invfails\": [");
    assert(VALUE_TYPE(state->invariants) == VALUE_SET);
    unsigned int size;
    hvalue_t *vals = value_get(state->invariants, &size);
    size /= sizeof(hvalue_t);
    int nfailures = 0;
    for (unsigned int i = 0; i < size; i++) {
        assert(VALUE_TYPE(vals[i]) == VALUE_PC);
        inv_step.ctx->entry = VALUE_FROM_PC(vals[i]);
        inv_step.ctx->pc = inv_step.ctx->entry;
        assert(strcmp(global->code.instrs[inv_step.ctx->pc].oi->name, "Invariant") == 0);
        int end = invariant_cnt(global->code.instrs[inv_step.ctx->pc].env);
        bool b = invariant_check(global, state, &inv_step, end);
        if (inv_step.ctx->failed) {
            b = false;
        }
        if (!b) {
            if (nfailures != 0) {
                fprintf(file, ",");
            }
            fprintf(file, "\n        {\n");
            fprintf(file, "          \"pc\": \"%u\",\n", (unsigned int) VALUE_FROM_PC(vals[i]));
            if (!inv_step.ctx->failed) {
                fprintf(file, "          \"reason\": \"invariant violated\"\n");
            }
            else {
                char *val = value_string(inv_step.ctx->ctx_failure);
				int len = strlen(val);
                fprintf(file, "          \"reason\": \"%.*s\"\n", len - 2, val + 1);
                free(val);
            }
            nfailures++;
            fprintf(file, "        }");
        }
    }
    fprintf(file, "\n      ],\n");
    free(inv_step.ctx);

    fprintf(file, "      \"ctxbag\": {\n");
    unsigned int nctxs;
    hvalue_t *ctxs = value_get(node->state.ctxbag, &nctxs);
    nctxs /= sizeof(hvalue_t);
    for (unsigned int i = 0; i < nctxs; i += 2) {
        if (i > 0) {
            fprintf(file, ",\n");
        }
        assert(VALUE_TYPE(ctxs[i]) == VALUE_CONTEXT);
        assert(VALUE_TYPE(ctxs[i+1]) == VALUE_INT);
        fprintf(file, "          \"%"PRIx64"\": \"%u\"", ctxs[i], (unsigned int) VALUE_FROM_INT(ctxs[i+1]));
    }
    fprintf(file, "\n      },\n");

    fprintf(file, "      \"contexts\": [\n");
    for (int i = 0; i < global->nprocesses; i++) {
        print_context(global, file, global->processes[i], i, node);
        if (i < global->nprocesses - 1) {
            fprintf(file, ",");
        }
        fprintf(file, "\n");
    }
    fprintf(file, "      ]\n");
}

void diff_state(
    struct global_t *global,
    FILE *file,
    struct state *oldstate,
    struct state *newstate,
    struct context *oldctx,
    struct context *newctx,
    bool interrupt,
    bool choose,
    hvalue_t choice,
    char *print
) {
    if (global->dumpfirst) {
        global->dumpfirst = false;
    }
    else {
        fprintf(file, ",");
    }
    fprintf(file, "\n        {\n");
    if (newstate->vars != oldstate->vars) {
        fprintf(file, "          \"shared\": ");
        print_vars(file, newstate->vars);
        fprintf(file, ",\n");
    }
    if (interrupt) {
        fprintf(file, "          \"interrupt\": \"True\",\n");
    }
    if (choose) {
        char *val = value_json(choice);
        fprintf(file, "          \"choose\": %s,\n", val);
        free(val);
    }
    if (print != NULL) {
        fprintf(file, "          \"print\": %s,\n", print);
    }
    fprintf(file, "          \"npc\": \"%d\",\n", newctx->pc);
    if (newctx->fp != oldctx->fp) {
        fprintf(file, "          \"fp\": \"%d\",\n", newctx->fp);
#ifdef notdef
        {
            fprintf(stderr, "STACK2 %d:\n", newctx->fp);
            for (int x = 0; x < newctx->sp; x++) {
                fprintf(stderr, "    %d: %s\n", x, value_string(ctx_stack(newctx)[x]));
            }
        }
#endif
        fprintf(file, "          \"trace\": [\n");
        print_trace(global, file, newctx, newctx->pc, newctx->fp, newctx->vars);
        fprintf(file, "\n");
        fprintf(file, "          ],\n");
    }
    if (newctx->extended && newctx->ctx_this != oldctx->ctx_this) {
        char *val = value_json(newctx->ctx_this);
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
        char *val = value_string(newctx->ctx_failure);
        fprintf(file, "          \"failure\": %s,\n", val);
        fprintf(file, "          \"mode\": \"failed\",\n");
        free(val);
    }
    else if (newctx->terminated) {
        fprintf(file, "          \"mode\": \"terminated\",\n");
    }

    int common;
    for (common = 0; common < newctx->sp && common < oldctx->sp; common++) {
        if (ctx_stack(newctx)[common] != ctx_stack(oldctx)[common]) {
            break;
        }
    }
    if (common < oldctx->sp) {
        fprintf(file, "          \"pop\": \"%d\",\n", oldctx->sp - common);
    }
    fprintf(file, "          \"push\": [");
    for (int i = common; i < newctx->sp; i++) {
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

void diff_dump(
    struct global_t *global,
    FILE *file,
    struct state *oldstate,
    struct state *newstate,
    struct context **oldctx,
    struct context *newctx,
    bool interrupt,
    bool choose,
    hvalue_t choice,
    char *print
) {
    int newsize = sizeof(*newctx) + (newctx->sp * sizeof(hvalue_t));

    if (memcmp(oldstate, newstate, sizeof(struct state)) == 0 &&
            (*oldctx)->sp == newctx->sp &&
            memcmp(*oldctx, newctx, newsize) == 0) {
        return;
    }

    // Keep track of old state and context for taking diffs
    diff_state(global, file, oldstate, newstate, *oldctx, newctx, interrupt, choose, choice, print);
    *oldstate = *newstate;
    free(*oldctx);
    *oldctx = malloc(newsize);
    memcpy(*oldctx, newctx, newsize);
}

// similar to onestep.
hvalue_t twostep(
    struct global_t *global,
    FILE *file,
    struct node *node,
    hvalue_t ctx,
    hvalue_t choice,
    bool interrupt,
    struct state *oldstate,
    struct context **oldctx,
    hvalue_t nextvars,
    unsigned int nsteps
){
    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    *sc = node->state;
    sc->choosing = 0;

    struct step step;
    memset(&step, 0, sizeof(step));
    step.engine.values = &global->values;

    unsigned int size;
    struct context *cc = value_get(ctx, &size);
    step.ctx = calloc(1, sizeof(struct context) +
                            MAX_CONTEXT_STACK * sizeof(hvalue_t));
    memcpy(step.ctx, cc, size);
    if (step.ctx->terminated || step.ctx->failed) {
        free(step.ctx);
        return ctx;
    }

    if (interrupt) {
        assert(step.ctx->extended);
		assert(step.ctx->ctx_trap_pc != 0);
        interrupt_invoke(&step);
        diff_dump(global, file, oldstate, sc, oldctx, step.ctx, true, false, 0, NULL);
    }

    struct dict *infloop = NULL;        // infinite loop detector
    unsigned int instrcnt = 0;
    for (;;) {
        int pc = step.ctx->pc;

        char *print = NULL;
        struct instr_t *instrs = global->code.instrs;
        struct op_info *oi = instrs[pc].oi;
        if (instrs[pc].choose) {
            assert(choice != 0);
            ctx_stack(step.ctx)[step.ctx->sp - 1] = choice;
            step.ctx->pc++;
        }
        else if (instrs[pc].atomicinc) {
            if (instrcnt == 0) {
                step.ctx->atomicFlag = true;
            }
            (*oi->op)(instrs[pc].env, sc, &step, global);
        }
        else if (instrs[pc].print) {
            print = value_json(ctx_stack(step.ctx)[step.ctx->sp - 1]);
            (*oi->op)(instrs[pc].env, sc, &step, global);
        }
        else {
            (*oi->op)(instrs[pc].env, sc, &step, global);
        }

        // Infinite loop detection
        if (!step.ctx->terminated && !step.ctx->failed) {
            if (infloop == NULL) {
                // TODO.  infloop should be deallocated
                infloop = dict_new("infloop2", 0, 0, 0, NULL, NULL);
            }

            int stacksize = step.ctx->sp * sizeof(hvalue_t);
            int combosize = sizeof(struct combined) + stacksize;
            struct combined *combo = calloc(1, combosize);
            combo->state = *sc;
            memcpy(&combo->context, step.ctx, sizeof(*step.ctx) + stacksize);
            bool new;
            dict_insert(infloop, NULL, combo, combosize, &new);
            free(combo);
            if (!new) {
                value_ctx_failure(step.ctx, &step.engine, "infinite loop");
            }
        }

        assert(!instrs[pc].choose || choice != 0);
        diff_dump(global, file, oldstate, sc, oldctx, step.ctx, false, instrs[pc].choose, choice, print);
        free(print);
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
        oi = global->code.instrs[step.ctx->pc].oi;
        if (global->code.instrs[step.ctx->pc].choose) {
            assert(step.ctx->sp > 0);
#ifdef TODO
            if (0 && step.ctx->readonly > 0) {    // TODO
                value_ctx_failure(step.ctx, &step.engine, "can't choose in assertion or invariant");
                diff_dump(global, file, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
                break;
            }
#endif
            hvalue_t s = ctx_stack(step.ctx)[step.ctx->sp - 1];
            if (VALUE_TYPE(s) != VALUE_SET) {
                value_ctx_failure(step.ctx, &step.engine, "choose operation requires a set");
                diff_dump(global, file, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
                break;
            }
            unsigned int size;
            hvalue_t *vals = value_get(s, &size);
            size /= sizeof(hvalue_t);
            if (size == 0) {
                value_ctx_failure(step.ctx, &step.engine, "choose operation requires a non-empty set");
                diff_dump(global, file, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
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
    hvalue_t count = value_dict_load(sc->ctxbag, ctx);
    assert(VALUE_TYPE(count) == VALUE_INT);
    count -= 1 << VALUE_BITS;
    if (count == VALUE_INT) {
        sc->ctxbag = value_dict_remove(&step.engine, sc->ctxbag, ctx);
    }
    else {
        sc->ctxbag = value_dict_store(&step.engine, sc->ctxbag, ctx, count);
    }

    hvalue_t after = value_put_context(&step.engine, step.ctx);

    // Add new context to state unless it's terminated or stopped
    if (step.ctx->stopped) {
        sc->stopbag = value_bag_add(&step.engine, sc->stopbag, after, 1);
    }
    else if (!step.ctx->terminated) {
        sc->ctxbag = value_bag_add(&step.engine, sc->ctxbag, after, 1);
    }

    // assert(sc->vars == nextvars);
    ctx = value_put_context(&step.engine, step.ctx);
    if ((ctx & 0xFFFF00000000) == 0x600000000000) {
        printf("YYYYYYY\n");
    }

    free(sc);
    free(step.ctx);
    free(step.log);

    return ctx;
}

void path_dump(
    struct global_t *global,
    FILE *file,
    struct edge *e,
    struct state *oldstate,
    struct context **oldctx
) {
    struct node *node = e->dst;
    struct node *parent = e->src;

    if (parent->to_parent == NULL) {
        fprintf(file, "\n");
    }
    else {
        path_dump(global, file, parent->to_parent, oldstate, oldctx);
        fprintf(file, ",\n");
    }

    fprintf(file, "    {\n");
    fprintf(file, "      \"id\": \"%d\",\n", node->id);
    fprintf(file, "      \"len\": \"%d\",\n", node->len);

    /* Find the starting context in the list of processes.
     */
    hvalue_t ctx = e->ctx;
    int pid;
    for (pid = 0; pid < global->nprocesses; pid++) {
        if (global->processes[pid] == ctx) {
            break;
        }
    }

    struct context *context = value_get(ctx, NULL);
    assert(!context->terminated);
    assert(strcmp(global->code.instrs[context->entry].oi->name, "Frame") == 0);
    const struct env_Frame *ef = global->code.instrs[context->entry].env;
    char *name = value_string(ef->name);
	int len = strlen(name);
    assert(context->sp > 1);
    char *arg = json_escape_value(ctx_stack(context)[1]);
    char *c = e->choice == 0 ? NULL : value_json(e->choice);
    fprintf(file, "      \"tid\": \"%d\",\n", pid);
    fprintf(file, "      \"xhash\": \"%"PRI_HVAL"\",\n", ctx);
    if (*arg == '(') {
        fprintf(file, "      \"name\": \"%.*s%s\",\n", len - 2, name + 1, arg);
    }
    else {
        fprintf(file, "      \"name\": \"%.*s(%s)\",\n", len - 2, name + 1, arg);
    }
    if (c != NULL) {
        fprintf(file, "      \"choice\": %s,\n", c);
    }
    global->dumpfirst = true;
    fprintf(file, "      \"microsteps\": [");
    free(name);
    free(arg);
    free(c);
    memset(*oldctx, 0, sizeof(**oldctx));
    (*oldctx)->pc = context->pc;

    // Recreate the steps
    assert(pid < global->nprocesses);
    global->processes[pid] = twostep(
        global,
        file,
        parent,
        ctx,
        e->choice,
        e->interrupt,
        oldstate,
        oldctx,
        node->state.vars,
        e->nsteps
    );
    fprintf(file, "\n      ],\n");

    /* Match each context to a process.
     */
    bool *matched = calloc(global->nprocesses, sizeof(bool));
    unsigned int nctxs;
    hvalue_t *ctxs = value_get(node->state.ctxbag, &nctxs);
    nctxs /= sizeof(hvalue_t);
    for (unsigned int i = 0; i < nctxs; i += 2) {
        assert(VALUE_TYPE(ctxs[i]) == VALUE_CONTEXT);
        assert(VALUE_TYPE(ctxs[i+1]) == VALUE_INT);
        int cnt = VALUE_FROM_INT(ctxs[i+1]);
        for (int j = 0; j < cnt; j++) {
            int k;
            for (k = 0; k < global->nprocesses; k++) {
                if (!matched[k] && global->processes[k] == ctxs[i]) {
                    matched[k] = true;
                    break;
                }
            }
            if (k == global->nprocesses) {
                global->processes = realloc(global->processes, (global->nprocesses + 1) * sizeof(hvalue_t));
                matched = realloc(matched, (global->nprocesses + 1) * sizeof(bool));
                global->processes[global->nprocesses] = ctxs[i];
                matched[global->nprocesses] = true;
                global->nprocesses++;
            }
        }
    }
    free(matched);
  
    print_state(global, file, node);
    fprintf(file, "    }");
}

static char *json_string_encode(char *s, int len){
    char *result = malloc(4 * len), *p = result;

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

enum busywait { BW_ESCAPE, BW_RETURN, BW_VISITED };
static enum busywait is_stuck(
    struct node *start,
    struct node *node,
    hvalue_t ctx,
    bool change
) {
	if (node->component != start->component) {
		return BW_ESCAPE;
	}
	if (node->visited) {
		return BW_VISITED;
	}
    change = change || (node->state.vars != start->state.vars);
	node->visited = true;
	enum busywait result = BW_ESCAPE;
    for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
        if (edge->ctx == ctx) {
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
				enum busywait bw = is_stuck(start, edge->dst, edge->after, change);
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

static void detect_busywait(struct minheap *failures, struct node *node){
	// Get the contexts
	unsigned int size;
	hvalue_t *ctxs = value_get(node->state.ctxbag, &size);
	size /= sizeof(hvalue_t);

	for (unsigned int i = 0; i < size; i += 2) {
		if (is_stuck(node, node, ctxs[i], false) == BW_RETURN) {
			struct failure *f = new_alloc(struct failure);
			f->type = FAIL_BUSYWAIT;
			f->edge = node->to_parent;
			minheap_insert(failures, f);
			// break;
		}
	}
}

static int node_cmp(void *n1, void *n2){
    struct node *node1 = n1, *node2 = n2;

    if (node1->len != node2->len) {
        return node1->len - node2->len;
    }
    if (node1->steps != node2->steps) {
        return node1->steps - node2->steps;
    }
    return node1->id - node2->id;
}

static int fail_cmp(void *f1, void *f2){
    struct failure *fail1 = f1, *fail2 = f2;

    return node_cmp(fail1->edge->dst, fail2->edge->dst);
}

static void do_work(struct worker *w){
    struct global_t *global = w->global;

    for (;;) {
        mutex_acquire(&global->todo_lock);
        unsigned int start = global->todo;
        unsigned int nleft = global->graph.size - start;
        if (nleft == 0) {
            mutex_release(&global->todo_lock);
            break;
        }

        unsigned int take = nleft / w->nworkers / 2;
        if (take < 100) {
            take = 100;
        }
        if (take > nleft) {
            take = nleft;
        }
        global->todo = start + take;
        mutex_release(&global->todo_lock);

        while (take > 0) {
            struct node *node = global->graph.nodes[start++];
            struct state *state = &node->state;

            if (state->choosing != 0) {
                assert(VALUE_TYPE(state->choosing) == VALUE_CONTEXT);

                struct context *cc = value_get(state->choosing, NULL);
                assert(cc != NULL);
                assert(cc->sp > 0);
                hvalue_t s = ctx_stack(cc)[cc->sp - 1];
                assert(VALUE_TYPE(s) == VALUE_SET);
                unsigned int size;
                hvalue_t *vals = value_get(s, &size);
                size /= sizeof(hvalue_t);
                assert(size > 0);
                for (unsigned int i = 0; i < size; i++) {
                    make_step(
                        w,
                        node,
                        state->choosing,
                        vals[i],
                        1
                    );
                }
            }
            else {
                unsigned int size;
                hvalue_t *ctxs = value_get(state->ctxbag, &size);
                size /= sizeof(hvalue_t);
                assert(size >= 0);
                for (unsigned int i = 0; i < size; i += 2) {
                    assert(VALUE_TYPE(ctxs[i]) == VALUE_CONTEXT);
                    assert(VALUE_TYPE(ctxs[i+1]) == VALUE_INT);
                    make_step(
                        w,
                        node,
                        ctxs[i],
                        0,
                        VALUE_FROM_INT(ctxs[i+1])
                    );
                }
            }
            take--;
        }
    }
}

static void worker(void *arg){
    struct worker *w = arg;
    struct global_t *global = w->global;

    for (int epoch = 0;; epoch++) {
        barrier_wait(w->start_barrier);

        // (first) parallel phase starts now
		// printf("WORKER %d starting epoch %d\n", w->index, epoch);
		do_work(w);

        // wait for others to finish
		// printf("WORKER %d finished epoch %d %u %u\n", w->index, epoch, w->count, w->node_id);
        barrier_wait(w->middle_barrier);

        // Wait for coordinator to have grown the graph table and hash tables

        barrier_wait(w->end_barrier);

		// printf("WORKER %d make stable %d %u %u\n", w->index, epoch, w->count, w->node_id);
        value_make_stable(&global->values, w->index);
        dict_make_stable(w->visited, w->index);

        // Fill the graph table
        for (unsigned int i = 0; w->count != 0; i++) {
            struct node *node = w->results;
			node->id = w->node_id;
            global->graph.nodes[w->node_id++] = node;
            w->results = node->next;
            w->count--;
        }
        assert(w->results == NULL);
    }
}

void process_results(struct global_t *global, struct worker *w){
    struct failure *f;
    while ((f = w->failures) != NULL) {
        w->failures = f->next;
        minheap_insert(global->failures, f);
    }
}

char *state_string(struct state *state){
    struct strbuf sb;
    strbuf_init(&sb);

    char *v;
    strbuf_printf(&sb, "{");
    v = value_string(state->vars);
    strbuf_printf(&sb, "%s", v); free(v);
    v = value_string(state->seqs);
    strbuf_printf(&sb, ",%s", v); free(v);
    v = value_string(state->choosing);
    strbuf_printf(&sb, ",%s", v); free(v);
    v = value_string(state->ctxbag);
    strbuf_printf(&sb, ",%s", v); free(v);
    v = value_string(state->stopbag);
    strbuf_printf(&sb, ",%s", v); free(v);
    v = value_string(state->termbag);
    strbuf_printf(&sb, ",%s", v); free(v);
    v = value_string(state->invariants);
    strbuf_printf(&sb, ",%s}", v); free(v);
    return strbuf_convert(&sb);
}

// This routine removes all node that have a single incoming edge and it's
// an "epsilon" edge (empty print log).  These are essentially useless nodes.
// Typically about half of the nodes can be removed this way.
static void destutter1(struct graph_t *graph){
    for (unsigned int i = 0; i < graph->size; i++) {
        struct node *n = graph->nodes[i];

        if (n->bwd != NULL && n->bwd->bwdnext == NULL && n->bwd->nlog == 0) {
            struct node *parent = n->bwd->src;

            if (n->final) {
                parent->final = true;
            }

            // Remove the edge from the parent
            struct edge **pe, *e;
            for (pe = &parent->fwd; (e = *pe) != NULL; pe = &e->fwdnext) {
                if (e->dst == n && e->nlog == 0) {
                    *pe = e->fwdnext;
                    // free(e);
                    break;
                }
            }

            struct edge *next;
            for (struct edge *e = n->fwd; e != NULL; e = next) {
                // Move the outgoing edge to the parent.
                next = e->fwdnext;
                e->fwdnext = parent->fwd;
                parent->fwd = e;

                // Fix the corresponding backwards edge
                for (struct edge *f = e->dst->bwd; f != NULL; f = f->bwdnext) {
                    if (f->src == n && f->nlog == e->nlog &&
                            memcmp(f->log, e->log, f->nlog * sizeof(*f->log)) == 0) {
                        f->src = parent;
                        break;
                    }
                }
            }
            n->reachable = false;
        }
        else {
            n->reachable = true;
        }
    }
}

static struct dict *collect_symbols(struct graph_t *graph){
    struct dict *symbols = dict_new("symbols", sizeof(unsigned int), 0, 0, NULL, NULL);
    unsigned int symbol_id = 0;

    for (unsigned int i = 0; i < graph->size; i++) {
        struct node *n = graph->nodes[i];
        if (!n->reachable) {
            continue;
        }
        for (struct edge *e = n->fwd; e != NULL; e = e->fwdnext) {
            for (unsigned int j = 0; j < e->nlog; j++) {
                bool new;
                unsigned int *p = dict_insert(symbols, NULL, &e->log[j], sizeof(e->log[j]), &new);
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
    struct dict *d = dict_new("transitions", sizeof(struct strbuf), 0, 0, NULL, NULL);

    fprintf(out, "      \"transitions\": [\n");
    for (struct edge *e = edges; e != NULL; e = e->fwdnext) {
        bool new;
        struct strbuf *sb = dict_insert(d, NULL, e->log, e->nlog * sizeof(*e->log), &new);
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

#ifdef OBSOLETE
static void pr_state(struct global_t *global, FILE *fp, struct state *state, int index){
    char *v = state_string(state);
    fprintf(fp, "%s\n", v);
    free(v);
}
#endif

static void usage(char *prog){
    fprintf(stderr, "Usage: %s [-c] [-t<maxtime>] [-B<dfafile>] -o<outfile> file.json\n", prog);
    exit(1);
}

int main(int argc, char **argv){
    bool cflag = false;
    int i, maxtime = 300000000 /* about 10 years */;
    char *outfile = NULL, *dfafile = NULL;
    for (i = 1; i < argc; i++) {
        if (*argv[i] != '-') {
            break;
        }
        switch (argv[i][1]) {
        case 'c':
            cflag = true;
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
        case 'x':
            printf("Charm model checker working\n");
            return 0;
        default:
            usage(argv[0]);
        }
    }
    if (argc - i != 1) {
        usage(argv[0]);
    }
    char *fname = argv[i];
    double timeout = gettime() + maxtime;

    // Determine how many worker threads to use
    unsigned int nworkers = getNumCores();
	printf("nworkers = %d\n", nworkers);
    barrier_t start_barrier, middle_barrier, end_barrier;
    barrier_init(&start_barrier, nworkers + 1);
    barrier_init(&middle_barrier, nworkers + 1);
    barrier_init(&end_barrier, nworkers + 1);

    // initialize modules
    struct global_t *global = new_alloc(struct global_t);
    mutex_init(&global->todo_lock);
    value_init(&global->values, nworkers);

    struct engine engine;
    engine.allocator = NULL;
    engine.values = &global->values;
    ops_init(&engine);

    graph_init(&global->graph, 1024*1024);
    global->failures = minheap_create(fail_cmp);
    global->processes = NULL;
    global->nprocesses = 0;
    global->lasttime = 0;
    global->enqueued = 0;
    global->dequeued = 0;
    global->dumpfirst = false;

    // First read and parse the DFA if any
    if (dfafile != NULL) {
        global->dfa = dfa_read(&engine, dfafile);
        if (global->dfa == NULL) {
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
    global->code = code_init_parse(&engine, jc);

    // Create an initial state
    struct context *init_ctx = calloc(1, sizeof(struct context) + MAX_CONTEXT_STACK * sizeof(hvalue_t));
    init_ctx->vars = VALUE_DICT;
    init_ctx->atomic = 1;
    init_ctx->atomicFlag = true;
    value_ctx_push(init_ctx, VALUE_TO_INT(CALLTYPE_PROCESS));
    value_ctx_push(init_ctx, VALUE_LIST);
    struct state *state = new_alloc(struct state);
    state->vars = VALUE_DICT;
    state->seqs = VALUE_SET;
    hvalue_t ictx = value_put_context(&engine, init_ctx);
    state->ctxbag = value_dict_store(&engine, VALUE_DICT, ictx, VALUE_TO_INT(1));
    state->stopbag = VALUE_DICT;
    state->invariants = VALUE_SET;
    state->dfa_state = global->dfa == NULL ? 0 : dfa_initial(global->dfa);
    global->processes = new_alloc(hvalue_t);
    *global->processes = ictx;
    global->nprocesses = 1;

    // Run direct
    if (outfile == NULL) {
        global->run_direct = true;
        mutex_init(&run_mutex);
        mutex_init(&run_waiting);
        mutex_acquire(&run_waiting);
        run_count = 1;

        // Run the initializing thread to completion
        // TODO.  spawned threads should wait...
        run_thread(global, state, init_ctx);

        // Wait for other threads
        mutex_acquire(&run_mutex);
        if (run_count > 0) {
            mutex_release(&run_mutex);
            mutex_acquire(&run_waiting);
        }
        mutex_release(&run_mutex);
        exit(0);
    }

    // Put the initial state in the visited map
    struct dict *visited = dict_new("visited", sizeof(struct node), 0, nworkers, NULL, NULL);
    struct node *node = dict_insert(visited, NULL, state, sizeof(*state), NULL);
    memset(node, 0, sizeof(*node));
    node->state = *state;
    graph_add(&global->graph, node);

    // Allocate space for worker info
    struct worker *workers = calloc(nworkers, sizeof(*workers));
    for (unsigned int i = 0; i < nworkers; i++) {
        struct worker *w = &workers[i];
        w->global = global;
        w->timeout = timeout;
        w->start_barrier = &start_barrier;
        w->middle_barrier = &middle_barrier;
        w->end_barrier = &end_barrier;
        w->index = i;
        w->nworkers = nworkers;
        w->visited = visited;

        // Create a context for evaluating invariants
        w->inv_step.ctx = calloc(1, sizeof(struct context) +
                                MAX_CONTEXT_STACK * sizeof(hvalue_t));
        // w->inv_step.ctx->name = value_put_atom(&engine, "__invariant__", 13);
        w->inv_step.ctx->vars = VALUE_DICT;
        w->inv_step.ctx->atomic = w->inv_step.ctx->readonly = 1;
        w->inv_step.ctx->interruptlevel = false;
        w->inv_step.engine.allocator = &w->allocator;
        w->inv_step.engine.values = &global->values;

        w->alloc_buf = malloc(WALLOC_CHUNK);
        w->alloc_ptr = w->alloc_buf;

        w->allocator.alloc = walloc;
        w->allocator.ctx = w;
        w->allocator.worker = i;
    }

    // Start the workers, who'll wait on the start barrier
    for (unsigned int i = 0; i < nworkers; i++) {
        thread_create(worker, &workers[i]);
    }

    // make sure first node gets process
    global->enqueued++;

    // Put the state and value dictionaries in concurrent mode
    value_set_concurrent(&global->values);
    dict_set_concurrent(visited);

    double before = gettime(), postproc = 0;
    for (;;) {
        barrier_wait(&start_barrier);

        // Threads are working to create the next layer of nodes.
        // Stay out of their way!

        barrier_wait(&middle_barrier);

        double before_postproc = gettime();

        // Back to sequential mode
        assert(global->todo == global->graph.size);

        global->diameter++;
        // printf("Diameter %d\n", global->diameter);

        // The threads completed producing the next layer of nodes in the graph.
        // Grow the graph table.
        unsigned int total = 0;
        for (unsigned int i = 0; i < nworkers; i++) {
            struct worker *w = &workers[i];
            w->node_id = global->todo + total;
            total += w->count;
        }
        graph_add_multiple(&global->graph, total);
        global->enqueued += total;

        // Prepare the grow the hash tables as well (but the actual work of
        // rehashing is distributed among the threads in the next phase
        dict_grow_prepare(visited);
        value_grow_prepare(&global->values);

        // Collect the failures of all the workers
        for (unsigned int i = 0; i < nworkers; i++) {
			process_results(global, &workers[i]);
        }

        postproc += gettime() - before_postproc;

        if (!minheap_empty(global->failures)) {
            global->todo = global->graph.size;
        }
        if (global->todo == global->graph.size) {
            break;
        }

        // printf("Coordinator back to workers (%d)\n", global->diameter);

        barrier_wait(&end_barrier);

        // The threads now update the hash tables and the graph table
    }

    // Get threads going on fixing hash tables
    barrier_wait(&end_barrier);
    // Wait for threads to fix up hash tables
    barrier_wait(&start_barrier);

    printf("#states %d (time %.3lf+%.3lf=%.3lf)\n", global->graph.size, gettime() - before - postproc, postproc, gettime() - before);

	dict_set_sequential(visited);
	value_set_sequential(&global->values);
 
    printf("Phase 3: analysis\n");
    if (minheap_empty(global->failures)) {
        // Link the forward edges
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            for (struct edge *edge = node->bwd; edge != NULL; edge = edge->bwdnext) {
                struct node *other = edge->src;
                edge->dst = node;
                edge->fwdnext = other->fwd;
                other->fwd = edge;
            }
        }

        // find the strongly connected components
        unsigned int ncomponents = graph_find_scc(&global->graph);
        printf("%u components\n", ncomponents);

        // mark the components that are "good" because they have a way out
        struct component *components = calloc(ncomponents, sizeof(*components));
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
			assert(node->component < ncomponents);
            struct component *comp = &components[node->component];
            if (comp->size == 0) {
                comp->rep = node;
                comp->all_same = value_ctx_all_eternal(node->state.ctxbag)
                    && value_ctx_all_eternal(node->state.stopbag);
            }
            else if (node->state.vars != comp->rep->state.vars ||
                        !value_ctx_all_eternal(node->state.ctxbag) ||
                        !value_ctx_all_eternal(node->state.stopbag)) {
                comp->all_same = false;
            }
            comp->size++;
            if (comp->good) {
                continue;
            }
            // if this component has a way out, it is good
            for (struct edge *edge = node->fwd;
                            edge != NULL && !comp->good; edge = edge->fwdnext) {
                if (edge->dst->component != node->component) {
                    comp->good = true;
                    break;
                }
            }
        }

        // components that have only one shared state and only eternal
        // threads are good because it means all its threads are blocked
        for (unsigned int i = 0; i < ncomponents; i++) {
            struct component *comp = &components[i];
            assert(comp->size > 0);
            if (!comp->good && comp->all_same) {
                comp->good = true;
                comp->final = true;
            }
        }

        // Look for states in final components
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
			assert(node->component < ncomponents);
            struct component *comp = &components[node->component];
            if (comp->final) {
                node->final = true;
                if (global->dfa != NULL &&
						!dfa_is_final(global->dfa, node->state.dfa_state)) {
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_BEHAVIOR;
                    f->edge = node->to_parent;
                    minheap_insert(global->failures, f);
                    // break;
                }
            }
        }

        if (minheap_empty(global->failures)) {
            // now count the nodes that are in bad components
            int nbad = 0;
            for (unsigned int i = 0; i < global->graph.size; i++) {
                struct node *node = global->graph.nodes[i];
                if (!components[node->component].good) {
                    nbad++;
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_TERMINATION;
                    f->edge = node->to_parent;
                    minheap_insert(global->failures, f);
                    // break;
                }
            }

            if (nbad == 0 && !cflag) {
                for (unsigned int i = 0; i < global->graph.size; i++) {
                    global->graph.nodes[i]->visited = false;
                }
                for (unsigned int i = 0; i < global->graph.size; i++) {
                    struct node *node = global->graph.nodes[i];
                    if (components[node->component].size > 1) {
                        detect_busywait(global->failures, node);
                    }
                }
            }
        }
    }

#ifdef OBSOLETE
    if (false) {
        FILE *df = fopen("charm.dump", "w");
        assert(df != NULL);
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            assert(node->id == i);
            fprintf(df, "\nNode %d:\n", node->id);
            fprintf(df, "    component: %d\n", node->component);
            if (node->to_parent != NULL) {
                fprintf(df, "    parent: %d\n", node->to_parent->src->id);
            }
            fprintf(df, "    vars: %s\n", value_string(node->state.vars));
            fprintf(df, "    fwd:\n");
            int eno = 0;
            for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext, eno++) {
                fprintf(df, "        %d:\n", eno);
                struct context *ctx = value_get(edge->ctx, NULL);
                // fprintf(df, "            context: %s %s %d\n", value_string(ctx->name), value_string(ctx->arg), ctx->pc);
                fprintf(df, "            choice: %s\n", value_string(edge->choice));
                fprintf(df, "            node: %d (%d)\n", edge->dst->id, edge->dst->component);
                fprintf(df, "            log:");
                for (unsigned int j = 0; j < edge->nlog; j++) {
                    char *p = value_string(edge->log[j]);
                    fprintf(df, " %s", p);
                    free(p);
                }
                fprintf(df, "\n");
            }
            fprintf(df, "    bwd:\n");
            eno = 0;
            for (struct edge *edge = node->bwd; edge != NULL; edge = edge->bwdnext, eno++) {
                fprintf(df, "        %d:\n", eno);
                struct context *ctx = value_get(edge->ctx, NULL);
                // fprintf(df, "            context: %s %s %d\n", value_string(ctx->name), value_string(ctx->arg), ctx->pc);
                fprintf(df, "            choice: %s\n", value_string(edge->choice));
                fprintf(df, "            node: %d (%d)\n", edge->src->id, edge->src->component);
                fprintf(df, "            log:");
                for (int j = 0; j < edge->nlog; j++) {
                    char *p = value_string(edge->log[j]);
                    fprintf(df, " %s", p);
                    free(p);
                }
                fprintf(df, "\n");
            }
        }
        fclose(df);
    }

    if (false) {
        FILE *df = fopen("charm.dump", "w");
        assert(df != NULL);
        char **table = malloc(global->graph.size * sizeof(char*));
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            table[i] = state_string(node->state);
            fprintf(df, "%s\n", table[i]);
        }
        fclose(df);
    }
#endif // OBSOLETE

    // Look for data races
    // TODO.  Can easily be parallelized
	// TODO.  Don't need failures/warnings distinction any more
    struct minheap *warnings = minheap_create(fail_cmp);
    if (minheap_empty(global->failures)) {
        printf("Check for data races\n");
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            graph_check_for_data_race(node, warnings, &engine);
            if (!minheap_empty(warnings)) {
                break;
            }
        }
    }

    bool no_issues = minheap_empty(global->failures) && minheap_empty(warnings);
    if (no_issues) {
        printf("No issues\n");
    }

    FILE *out = fopen(outfile, "w");
    if (out == NULL) {
        fprintf(stderr, "charm: can't create %s\n", outfile);
        exit(1);
    }

    printf("Phase 4: write results to %s\n", outfile);
    fflush(stdout);

    fprintf(out, "{\n");

    if (no_issues) {
        fprintf(out, "  \"issue\": \"No issues\",\n");

        destutter1(&global->graph);

        // Output the symbols;
        struct dict *symbols = collect_symbols(&global->graph);
        fprintf(out, "  \"symbols\": {\n");
        struct symbol_env se = { .out = out, .first = true };
        dict_iter(symbols, print_symbol, &se);
        fprintf(out, "\n");
        fprintf(out, "  },\n");

        fprintf(out, "  \"nodes\": [\n");
        bool first = true;
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
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
                fprintf(out, "      \"component\": %d,\n", node->component);
#ifdef notdef
                if (node->parent != NULL) {
                    fprintf(out, "      \"parent\": %d,\n", node->parent->id);
                }
                char *val = json_escape_value(node->state.vars);
                fprintf(out, "      \"value\": \"%s:%d\",\n", val, node->state.choosing != 0);
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
#ifdef notdef
        fprintf(out, "  \"edges\": [\n");
        first = true;
        bool first_log;
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            if (node->reachable) {
                for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
                    assert(edge->dst->reachable);
                    if (first) {
                        first = false;
                    }
                    else {
                        fprintf(out, ",\n");
                    }
                    fprintf(out, "    {\n");
                    fprintf(out, "      \"src\": %d,\n", node->id);
                    fprintf(out, "      \"dst\": %d,\n", edge->dst->id);
                    fprintf(out, "      \"print\": [");
                    first_log = true;
                    for (int j = 0; j < edge->nlog; j++) {
                        if (first_log) {
                            first_log = false;
                            fprintf(out, "\n");
                        }
                        else {
                            fprintf(out, ",\n");
                        }
                        char *p = value_json(edge->log[j]);
                        fprintf(out, "        %s", p);
                        free(p);
                    }
                    fprintf(out, "\n");
                    fprintf(out, "      ]\n");
                    fprintf(out, "    }");
                }
            }
        }
        fprintf(out, "\n");
        fprintf(out, "  ],\n");
#endif // notdef
    }
    else {
        // Find shortest "bad" path
        struct failure *bad = NULL;
        if (minheap_empty(global->failures)) {
            bad = minheap_getmin(warnings);
        }
        else {
            bad = minheap_getmin(global->failures);
        }

        switch (bad->type) {
        case FAIL_SAFETY:
            printf("Safety Violation\n");
            fprintf(out, "  \"issue\": \"Safety violation\",\n");
            break;
        case FAIL_INVARIANT:
            printf("Invariant Violation\n");
            fprintf(out, "  \"issue\": \"Invariant violation\",\n");
            break;
        case FAIL_BEHAVIOR:
            printf("Behavior Violation: terminal state not final\n");
            fprintf(out, "  \"issue\": \"Behavior violation: terminal state not final\",\n");
            break;
        case FAIL_TERMINATION:
            printf("Non-terminating state\n");
            fprintf(out, "  \"issue\": \"Non-terminating state\",\n");
            break;
        case FAIL_BUSYWAIT:
            printf("Active busy waiting\n");
            fprintf(out, "  \"issue\": \"Active busy waiting\",\n");
            break;
        case FAIL_RACE:
            assert(bad->address != VALUE_ADDRESS);
            char *addr = value_string(bad->address);
            char *json = json_string_encode(addr, strlen(addr));
            printf("Data race (%s)\n", json);
            fprintf(out, "  \"issue\": \"Data race (%s)\",\n", json);
            free(json);
            free(addr);
            break;
        default:
            panic("main: bad fail type");
        }

        fprintf(out, "  \"macrosteps\": [");
        struct state oldstate;
        memset(&oldstate, 0, sizeof(oldstate));
        struct context *oldctx = calloc(1, sizeof(*oldctx));
        global->dumpfirst = true;
        path_dump(global, out, bad->edge, &oldstate, &oldctx);
        fprintf(out, "\n");
        free(oldctx);
        fprintf(out, "  ],\n");
    }

    fprintf(out, "  \"code\": [\n");
    jc = dict_lookup(jv->u.map, "pretty", 6);
    assert(jc->type == JV_LIST);
    for (unsigned int i = 0; i < jc->u.list.nvals; i++) {
        struct json_value *next = jc->u.list.vals[i];
        assert(next->type == JV_LIST);
        assert(next->u.list.nvals == 2);
        struct json_value *codestr = next->u.list.vals[0];
        assert(codestr->type == JV_ATOM);
		char *v = json_escape(codestr->u.atom.base, codestr->u.atom.len);
        fprintf(out, "    \"%s\"", v);
		free(v);
        if (i < jc->u.list.nvals - 1) {
            fprintf(out, ",");
        }
        fprintf(out, "\n");
    }
    fprintf(out, "  ],\n");

    fprintf(out, "  \"explain\": [\n");
    for (unsigned int i = 0; i < jc->u.list.nvals; i++) {
        struct json_value *next = jc->u.list.vals[i];
        assert(next->type == JV_LIST);
        assert(next->u.list.nvals == 2);
        struct json_value *codestr = next->u.list.vals[1];
        assert(codestr->type == JV_ATOM);
		char *v = json_escape(codestr->u.atom.base, codestr->u.atom.len);
        fprintf(out, "    \"%s\"", v);
		free(v);
        if (i < jc->u.list.nvals - 1) {
            fprintf(out, ",");
        }
        fprintf(out, "\n");
    }
    fprintf(out, "  ],\n");

    fprintf(out, "  \"locations\": {");
    jc = dict_lookup(jv->u.map, "locations", 9);
    assert(jc->type == JV_MAP);
    struct enum_loc_env_t enum_loc_env;
    enum_loc_env.out = out;
    enum_loc_env.code_map = global->code.code_map;
    dict_iter(jc->u.map, enum_loc, &enum_loc_env);
    fprintf(out, "\n  }\n");

    fprintf(out, "}\n");
	fclose(out);

    iface_write_spec_graph_to_file(global, "iface.gv");
    iface_write_spec_graph_to_json_file(global, "iface.json");

    free(global);
    return 0;
}
