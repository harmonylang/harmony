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

// One of these per worker thread
struct worker {
    struct global_t *global;     // global state
    double timeout;
    barrier_t *start_barrier, *middle_barrier, *end_barrier;

    struct dict *visited;

    int index;                   // index of worker
    int nworkers;                // total number of workers
    struct node *todo;           // set of states to evaluate
    int timecnt;                 // to reduce gettime() overhead
    struct step inv_step;        // for evaluating invariants

    struct node *results;        // list of resulting states
    struct failure *failures;   // list of failures
};

bool invariant_check(struct global_t *global, struct state *state, struct step *step, int end){
    assert(step->ctx->sp == 0);
    assert(step->ctx->failure == 0);
    step->ctx->pc++;
    while (step->ctx->pc != end) {
        struct op_info *oi = global->code.instrs[step->ctx->pc].oi;
        int oldpc = step->ctx->pc;
        (*oi->op)(global->code.instrs[oldpc].env, state, step, global);
        if (step->ctx->failure != 0) {
            step->ctx->sp = 0;
            return false;
        }
        assert(step->ctx->pc != oldpc);
        assert(!step->ctx->terminated);
    }
    assert(step->ctx->sp == 1);
    step->ctx->sp = 0;
    assert(step->ctx->fp == 0);
    hvalue_t b = step->ctx->stack[0];
    assert(VALUE_TYPE(b) == VALUE_BOOL);
    return VALUE_FROM_BOOL(b);
}

void check_invariants(struct worker *w, struct node *node, struct step *step){
    struct global_t *global = w->global;
    struct state *state = node->state;
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
        if (step->ctx->failure != 0) {
            printf("Invariant failed: %s\n", value_string(step->ctx->failure));
            b = false;
        }
        if (!b) {
            node->ftype = FAIL_INVARIANT;
            break;
        }
    }
}

static void *node_alloc(void){
    struct node *node = new_alloc(struct node);
    mutex_init(&node->lock);
    return node;
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
    assert(step->ctx->failure == 0);

    struct global_t *global = w->global;

    // See if we should also try an interrupt.
    if (interrupt) {
		assert(step->ctx->trap_pc != 0);
        interrupt_invoke(step);
    }

    // Copy the choice
    hvalue_t choice_copy = choice;

    bool choosing = false, infinite_loop = false;
    struct dict *infloop = NULL;        // infinite loop detector
    int instrcnt = 0;
    struct state *as_state = NULL;
    hvalue_t as_context = 0;
    int as_instrcnt = 0;
    bool rollback = false, failure = false, stopped = false;
    bool terminated = false;
    for (;;) {
        int pc = step->ctx->pc;

        // If I'm pthread 0 and it's time, print some stats
        if (w->index == 0 && w->timecnt-- == 0) {
            double now = gettime();
            if (now - global->lasttime > 1) {
                if (global->lasttime != 0) {
                    char *p = value_string(step->ctx->name);
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
            step->ctx->stack[step->ctx->sp - 1] = choice;
            step->ctx->pc++;
        }
        else if (instrs[pc].atomicinc) {
            if (instrcnt == 0) {
                step->ctx->atomicFlag = true;
            }
            else if (step->ctx->atomic == 0) {
                // Save the current state in case it needs restoring
                as_state = new_alloc(struct state);
                memcpy(as_state, sc, sizeof(*sc));
                as_context = value_put_context(&global->values, step->ctx);
                as_instrcnt = instrcnt;
            }
            (*oi->op)(instrs[pc].env, sc, step, global);
        }
        else if (instrs[pc].atomicdec) {
            (*oi->op)(instrs[pc].env, sc, step, global);
            if (step->ctx->atomic == 0) {
                free(as_state);
                as_state = NULL;
                as_context = 0;
                as_instrcnt = 0;
            }
        }
        else {
            // Keep track of access for data race detection
            if (instrs[pc].load || instrs[pc].store || instrs[pc].del) {
                struct access_info *ai = graph_ai_alloc(multiplicity, step->ctx->atomic, pc);
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
        if (step->ctx->failure != 0) {
            failure = true;
            break;
        }
        if (step->ctx->stopped) {
            stopped = true;
            break;
        }

        if (infloop_detect || instrcnt > 1000) {
            if (infloop == NULL) {
                infloop = dict_new(0, NULL, NULL);
            }

            int stacksize = step->ctx->sp * sizeof(hvalue_t);
            int combosize = sizeof(struct combined) + stacksize;
            struct combined *combo = calloc(1, combosize);
            combo->state = *sc;
            memcpy(&combo->context, step->ctx, sizeof(*step->ctx) + stacksize);
            void **p = dict_insert(infloop, combo, combosize);
            free(combo);
            if (*p == (void *) 0) {
                *p = (void *) 1;
            }
            else if (infloop_detect) {
                step->ctx->failure = value_put_atom(&global->values, "infinite loop", 13);
                failure = infinite_loop = true;
                break;
            }
            else {
                // start over, as twostep does not have instrcnt optimization
                return false;
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
                value_ctx_failure(step->ctx, &global->values, "can't choose in assertion or invariant");
                failure = true;
                break;
            }
#endif
            hvalue_t s = step->ctx->stack[step->ctx->sp - 1];
            if (VALUE_TYPE(s) != VALUE_SET) {
                value_ctx_failure(step->ctx, &global->values, "choose operation requires a set");
                failure = true;
                break;
            }
            unsigned int size;
            hvalue_t *vals = value_get(s, &size);
            size /= sizeof(hvalue_t);
            if (size == 0) {
                value_ctx_failure(step->ctx, &global->values, "choose operation requires a non-empty set");
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
            if (step->ctx->trap_pc != 0 && !step->ctx->interruptlevel) {
                // If this is a thread exit, break so we can invoke the
                // interrupt handler one more time
                if (next_instr->retop) {
                    hvalue_t ct = step->ctx->stack[step->ctx->sp - 4];
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
                    assert(as_state != NULL);
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
        assert(as_state != NULL);
        memcpy(sc, as_state, sizeof(*sc));
        after = as_context;
        instrcnt = as_instrcnt;
    }
    else {
        // Store new context in value directory.  Must be immutable now.
        after = value_put_context(&global->values, step->ctx);
    }
    free(as_state);

    // Remove old context from the bag
    hvalue_t count = value_dict_load(sc->ctxbag, ctx);
    assert(VALUE_TYPE(count) == VALUE_INT);
    count -= 1 << VALUE_BITS;
    if (count == VALUE_INT) {
        sc->ctxbag = value_dict_remove(&global->values, sc->ctxbag, ctx);
    }
    else {
        sc->ctxbag = value_dict_store(&global->values, sc->ctxbag, ctx, count);
    }

    // If choosing, save in state
    if (choosing) {
        sc->choosing = after;
    }

    // Add new context to state unless it's terminated or stopped
    if (stopped) {
        sc->stopbag = value_bag_add(&global->values, sc->stopbag, after, 1);
    }
    else if (!terminated) {
        sc->ctxbag = value_bag_add(&global->values, sc->ctxbag, after, 1);
    }

    // Weight of this step
    int weight = ctx == node->after ? 0 : 1;

    // Allocate edge now
    struct edge *edge = new_alloc(struct edge);
    edge->ctx = ctx;
    edge->choice = choice_copy;
    edge->interrupt = interrupt;
    edge->weight = weight;
    edge->after = after;
    edge->ai = step->ai;
    edge->log = step->log;
    edge->nlog = step->nlog;

    // See if this state has been computed before
    void **p = dict_insert_alloc(w->visited, sc, sizeof(struct state), node_alloc);
    struct node *next = *p;
    mutex_acquire(&next->lock);
    if (next->initialized) {
        int len = node->len + weight;
        int steps = node->steps + instrcnt;
        if (len < next->len || (len == next->len && steps < next->steps)) {
            next->len = len;
            next->parent = node;
            next->weight = weight;
            next->steps = steps;
            next->before = ctx;
            next->after = after;
            next->choice = choice_copy;
            next->interrupt = interrupt;
        }
    }
    else {
        next->parent = node;
        next->state = sc;
        next->before = ctx;
        next->choice = choice_copy;
        next->interrupt = interrupt;
        next->after = after;
        next->len = node->len + weight;
        next->steps = node->steps + instrcnt;
        next->weight = weight;

        next->ai = step->ai;
        next->log = step->log;
        next->nlog = step->nlog;

        next->initialized = true;
        next->next = w->results;
        w->results = next;
    }

    if (failure) {
        struct failure *f = new_alloc(struct failure);
        f->type = infinite_loop ? FAIL_TERMINATION : FAIL_SAFETY;
        f->choice = choice_copy;
        f->interrupt = interrupt;
        f->parent = node;
        f->node = next;
        f->next = w->failures;
        w->failures = f;
    }
    else if (sc->choosing == 0 && sc->invariants != VALUE_SET) {
        check_invariants(w, next, &w->inv_step);
    }

    // Backward edge from node to parent.
    edge->src = node;
    edge->bwdnext = next->bwd;
    next->bwd = edge;

    mutex_release(&next->lock);

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

    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    memcpy(sc, node->state, sizeof(*sc));

    // Make a copy of the context
    step.ctx = value_copy(ctx, NULL);

    // See if we need to interrupt
    if (sc->choosing == 0 && step.ctx->trap_pc != 0 && !step.ctx->interruptlevel) {
        bool succ = onestep(w, node, sc, ctx, &step, choice, true, false, multiplicity);
        if (!succ) {        // ran into an infinite loop
            (void) onestep(w, node, sc, ctx, &step, choice, true, true, multiplicity);
        }

        // Allocate another state
        sc = new_alloc(struct state);
        memcpy(sc, node->state, sizeof(*sc));
        free(step.ctx);
        step.ctx = value_copy(ctx, NULL);
    }

    sc->choosing = 0;
    bool succ = onestep(w, node, sc, ctx, &step, choice, false, false, multiplicity);
    if (!succ) {        // ran into an infinite loop
        (void) onestep(w, node, sc, ctx, &step, choice, false, true, multiplicity);
    }

    free(step.ctx);
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
    char *r = json_escape(s, strlen(s));
    free(s);
    return r;
}

bool print_trace(
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
        hvalue_t ct = ctx->stack[ctx->sp - 2];
        assert(VALUE_TYPE(ct) == VALUE_INT);
        switch (VALUE_FROM_INT(ct)) {
        case CALLTYPE_PROCESS:
            pc++;
            break;
        case CALLTYPE_INTERRUPT:
        case CALLTYPE_NORMAL:
            {
                hvalue_t retaddr = ctx->stack[ctx->sp - 3];
                assert(VALUE_TYPE(retaddr) == VALUE_PC);
                pc = VALUE_FROM_PC(retaddr);
            }
            break;
        default:
            fprintf(stderr, "call type: %"PRI_HVAL" %d %d %d\n", ct, ctx->sp, ctx->fp, ctx->pc);
            // panic("print_trace: bad call type 1");
        }
    }
    while (--pc >= 0) {
        const char *name = global->code.instrs[pc].oi->name;

        if (strcmp(name, "Return") == 0) {
			level++;
		}
        else if (strcmp(name, "Frame") == 0) {
			if (level == 0) {
				if (fp >= 5) {
                    assert(VALUE_TYPE(ctx->stack[fp - 5]) == VALUE_PC);
					int npc = VALUE_FROM_PC(ctx->stack[fp - 5]);
					hvalue_t nvars = ctx->stack[fp - 2];
					int nfp = ctx->stack[fp - 1] >> VALUE_BITS;
					if (print_trace(global, file, ctx, npc, nfp, nvars)) {
                        fprintf(file, ",\n");
                    }
				}
				fprintf(file, "            {\n");
				fprintf(file, "              \"pc\": \"%d\",\n", orig_pc);
				fprintf(file, "              \"xpc\": \"%d\",\n", pc);

				const struct env_Frame *ef = global->code.instrs[pc].env;
				char *s = value_string(ef->name), *a = NULL;
				int len = strlen(s);
                a = json_escape_value(ctx->stack[fp - 3]);
				if (*a == '(') {
					fprintf(file, "              \"method\": \"%.*s%s\",\n", len - 2, s + 1, a);
				}
				else {
					fprintf(file, "              \"method\": \"%.*s(%s)\",\n", len - 2, s + 1, a);
				}

                hvalue_t ct = ctx->stack[fp - 4];
                assert(VALUE_TYPE(ct) == VALUE_INT);
                switch (VALUE_FROM_INT(ct)) {
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
    if (node->state->choosing == ctx) {
        return "choosing";
    }
    while (node->state->choosing != 0) {
        node = node->parent;
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
    char *s, *a;

    fprintf(file, "        {\n");
    fprintf(file, "          \"tid\": \"%d\",\n", tid);
    fprintf(file, "          \"yhash\": \"%"PRI_HVAL"\",\n", ctx);

    struct context *c = value_get(ctx, NULL);

    s = value_string(c->name);
	int len = strlen(s);
    a = json_escape_value(c->arg);
    if (*a == '(') {
        fprintf(file, "          \"name\": \"%.*s%s\",\n", len - 2, s + 1, a);
    }
    else {
        fprintf(file, "          \"name\": \"%.*s(%s)\",\n", len - 2, s + 1, a);
    }
    free(s);
    free(a);

    // assert(VALUE_TYPE(c->entry) == VALUE_PC);   TODO
    fprintf(file, "          \"entry\": \"%d\",\n", (int) (c->entry >> VALUE_BITS));

    fprintf(file, "          \"pc\": \"%d\",\n", c->pc);
    fprintf(file, "          \"fp\": \"%d\",\n", c->fp);

#ifdef notdef
    {
        fprintf(file, "STACK %d:\n", c->fp);
        for (int x = 0; x < c->sp; x++) {
            fprintf(file, "    %d: %s\n", x, value_string(c->stack[x]));
        }
    }
#endif

    fprintf(file, "          \"trace\": [\n");
    print_trace(global, file, c, c->pc, c->fp, c->vars);
    fprintf(file, "\n");
    fprintf(file, "          ],\n");

    if (c->failure != 0) {
        s = value_string(c->failure);
        fprintf(file, "          \"failure\": %s,\n", s);
        free(s);
    }

    if (c->trap_pc != 0) {
        s = value_string(c->trap_pc);
        a = value_string(c->trap_arg);
        if (*a == '(') {
            fprintf(file, "          \"trap\": \"%s%s\",\n", s, a);
        }
        else {
            fprintf(file, "          \"trap\": \"%s(%s)\",\n", s, a);
        }
        free(s);
    }

    if (c->interruptlevel) {
        fprintf(file, "          \"interruptlevel\": \"1\",\n");
    }

    if (c->atomic != 0) {
        fprintf(file, "          \"atomic\": \"%d\",\n", c->atomic);
    }
    if (c->readonly != 0) {
        fprintf(file, "          \"readonly\": \"%d\",\n", c->readonly);
    }

    if (c->terminated) {
        fprintf(file, "          \"mode\": \"terminated\",\n");
    }
    else if (c->failure != 0) {
        fprintf(file, "          \"mode\": \"failed\",\n");
    }
    else if (c->stopped) {
        fprintf(file, "          \"mode\": \"stopped\",\n");
    }
    else {
        fprintf(file, "          \"mode\": \"%s\",\n", ctx_status(node, ctx));
    }

#ifdef notdef
    fprintf(file, "          \"stack\": [\n");
    for (int i = 0; i < c->sp; i++) {
        s = value_string(c->stack[i]);
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

    s = value_json(c->this);
    fprintf(file, "          \"this\": %s\n", s);
    free(s);

    fprintf(file, "        }");
}

void print_state(
    struct global_t *global,
    FILE *file,
    struct node *node
) {

#ifdef notdef
    fprintf(file, "      \"shared\": ");
    print_vars(file, node->state->vars);
    fprintf(file, ",\n");
#endif

    struct state *state = node->state;
    extern int invariant_cnt(const void *env);
    struct step inv_step;
    memset(&inv_step, 0, sizeof(inv_step));
    inv_step.ctx = new_alloc(struct context);

    // hvalue_t inv_nv = value_put_atom("name", 4);
    // hvalue_t inv_tv = value_put_atom("tag", 3);
    inv_step.ctx->name = value_put_atom(&global->values, "__invariant__", 13);
    inv_step.ctx->arg = VALUE_LIST;
    inv_step.ctx->this = VALUE_DICT;
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
        inv_step.ctx->pc = VALUE_FROM_PC(vals[i]);
        assert(strcmp(global->code.instrs[inv_step.ctx->pc].oi->name, "Invariant") == 0);
        int end = invariant_cnt(global->code.instrs[inv_step.ctx->pc].env);
        bool b = invariant_check(global, state, &inv_step, end);
        if (inv_step.ctx->failure != 0) {
            b = false;
        }
        if (!b) {
            if (nfailures != 0) {
                fprintf(file, ",");
            }
            fprintf(file, "\n        {\n");
            fprintf(file, "          \"pc\": \"%u\",\n", (unsigned int) VALUE_FROM_PC(vals[i]));
            if (inv_step.ctx->failure == 0) {
                fprintf(file, "          \"reason\": \"invariant violated\"\n");
            }
            else {
                char *val = value_string(inv_step.ctx->failure);
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
        fprintf(file, "          \"trace\": [\n");
        print_trace(global, file, newctx, newctx->pc, newctx->fp, newctx->vars);
        fprintf(file, "\n");
        fprintf(file, "          ],\n");
    }
    if (newctx->this != oldctx->this) {
        char *val = value_json(newctx->this);
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
    if (newctx->failure != 0) {
        char *val = value_string(newctx->failure);
        fprintf(file, "          \"failure\": %s,\n", val);
        fprintf(file, "          \"mode\": \"failed\",\n");
        free(val);
    }
    else if (newctx->terminated) {
        fprintf(file, "          \"mode\": \"terminated\",\n");
    }

    int common;
    for (common = 0; common < newctx->sp && common < oldctx->sp; common++) {
        if (newctx->stack[common] != oldctx->stack[common]) {
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
        char *val = value_json(newctx->stack[i]);
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
    int nsteps
){
    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    memcpy(sc, node->state, sizeof(*sc));
    sc->choosing = 0;

    struct step step;
    memset(&step, 0, sizeof(step));
    step.ctx = value_copy(ctx, NULL);
    if (step.ctx->terminated || step.ctx->failure != 0) {
        free(step.ctx);
        return ctx;
    }

    if (interrupt) {
		assert(step.ctx->trap_pc != 0);
        interrupt_invoke(&step);
        diff_dump(global, file, oldstate, sc, oldctx, step.ctx, true, false, 0, NULL);
    }

    struct dict *infloop = NULL;        // infinite loop detector
    int instrcnt = 0;
    for (;;) {
        int pc = step.ctx->pc;

        char *print = NULL;
        struct instr_t *instrs = global->code.instrs;
        struct op_info *oi = instrs[pc].oi;
        if (instrs[pc].choose) {
            step.ctx->stack[step.ctx->sp - 1] = choice;
            step.ctx->pc++;
        }
        else if (instrs[pc].print) {
            print = value_json(step.ctx->stack[step.ctx->sp - 1]);
            (*oi->op)(instrs[pc].env, sc, &step, global);
        }
        else {
            (*oi->op)(instrs[pc].env, sc, &step, global);
        }

        // Infinite loop detection
        if (!step.ctx->terminated && step.ctx->failure == 0) {
            if (infloop == NULL) {
                infloop = dict_new(0, NULL, NULL);
            }

            int stacksize = step.ctx->sp * sizeof(hvalue_t);
            int combosize = sizeof(struct combined) + stacksize;
            struct combined *combo = calloc(1, combosize);
            combo->state = *sc;
            memcpy(&combo->context, step.ctx, sizeof(*step.ctx) + stacksize);
            void **p = dict_insert(infloop, combo, combosize);
            free(combo);
            if (*p == (void *) 0) {
                *p = (void *) 1;
            }
            else {
                step.ctx->failure = value_put_atom(&global->values, "infinite loop", 13);
            }
        }

        diff_dump(global, file, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, print);
        free(print);
        if (step.ctx->terminated || step.ctx->failure != 0 || step.ctx->stopped) {
            break;
        }
        instrcnt++;
        if (instrcnt >= nsteps - node->steps) {
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
                value_ctx_failure(step.ctx, &global->values, "can't choose in assertion or invariant");
                diff_dump(global, file, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
                break;
            }
#endif
            hvalue_t s = step.ctx->stack[step.ctx->sp - 1];
            if (VALUE_TYPE(s) != VALUE_SET) {
                value_ctx_failure(step.ctx, &global->values, "choose operation requires a set");
                diff_dump(global, file, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
                break;
            }
            unsigned int size;
            hvalue_t *vals = value_get(s, &size);
            size /= sizeof(hvalue_t);
            if (size == 0) {
                value_ctx_failure(step.ctx, &global->values, "choose operation requires a non-empty set");
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
        sc->ctxbag = value_dict_remove(&global->values, sc->ctxbag, ctx);
    }
    else {
        sc->ctxbag = value_dict_store(&global->values, sc->ctxbag, ctx, count);
    }

    hvalue_t after = value_put_context(&global->values, step.ctx);

    // Add new context to state unless it's terminated or stopped
    if (step.ctx->stopped) {
        sc->stopbag = value_bag_add(&global->values, sc->stopbag, after, 1);
    }
    else if (!step.ctx->terminated) {
        sc->ctxbag = value_bag_add(&global->values, sc->ctxbag, after, 1);
    }

    // assert(sc->vars == nextvars);
    ctx = value_put_context(&global->values, step.ctx);

    free(sc);
    free(step.ctx);
    free(step.log);

    return ctx;
}

void path_dump(
    struct global_t *global,
    FILE *file,
    struct node *last,
    struct node *parent,
    hvalue_t choice,
    struct state *oldstate,
    struct context **oldctx,
    bool interrupt,
    int nsteps
) {
    struct node *node = last;

    last = parent == NULL ? last->parent : parent;
    if (last->parent == NULL) {
        fprintf(file, "\n");
    }
    else {
        path_dump(global, file, last, last->parent, last->choice, oldstate, oldctx, last->interrupt, last->steps);
        fprintf(file, ",\n");
    }

    fprintf(file, "    {\n");
    fprintf(file, "      \"id\": \"%d\",\n", node->id);
    fprintf(file, "      \"len\": \"%d\",\n", node->len);

    /* Find the starting context in the list of processes.
     */
    hvalue_t ctx = node->before;
    int pid;
    for (pid = 0; pid < global->nprocesses; pid++) {
        if (global->processes[pid] == ctx) {
            break;
        }
    }

    struct context *context = value_get(ctx, NULL);
    assert(!context->terminated);
    char *name = value_string(context->name);
	int len = strlen(name);
    char *arg = json_escape_value(context->arg);
    // char *c = value_string(choice);
    fprintf(file, "      \"tid\": \"%d\",\n", pid);
    fprintf(file, "      \"xhash\": \"%"PRI_HVAL"\",\n", ctx);
    if (*arg == '(') {
        fprintf(file, "      \"name\": \"%.*s%s\",\n", len - 2, name + 1, arg);
    }
    else {
        fprintf(file, "      \"name\": \"%.*s(%s)\",\n", len - 2, name + 1, arg);
    }
    // fprintf(file, "      \"choice\": \"%s\",\n", c);
    global->dumpfirst = true;
    fprintf(file, "      \"microsteps\": [");
    free(name);
    free(arg);
    // free(c);
    memset(*oldctx, 0, sizeof(**oldctx));
    (*oldctx)->pc = context->pc;

    // Recreate the steps
    assert(pid < global->nprocesses);
    global->processes[pid] = twostep(
        global,
        file,
        last,
        ctx,
        choice,
        interrupt,
        oldstate,
        oldctx,
        node->state->vars,
        nsteps
    );
    fprintf(file, "\n      ],\n");

    /* Match each context to a process.
     */
    bool *matched = calloc(global->nprocesses, sizeof(bool));
    unsigned int nctxs;
    hvalue_t *ctxs = value_get(node->state->ctxbag, &nctxs);
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
    HASHDICT_VALUE_TYPE value
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

    struct json_value *jv = value;
    assert(jv->type == JV_MAP);

    struct json_value *file = dict_lookup(jv->u.map, "file", 4);
    assert(file->type == JV_ATOM);
    fprintf(out, "\"file\": \"%s\", ", json_string_encode(file->u.atom.base, file->u.atom.len));

    struct json_value *line = dict_lookup(jv->u.map, "line", 4);
    assert(line->type == JV_ATOM);
    fprintf(out, "\"line\": \"%.*s\", ", line->u.atom.len, line->u.atom.base);

    void **p = dict_insert(code_map, &pc, sizeof(pc));
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
    change = change || (node->state->vars != start->state->vars);
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
	hvalue_t *ctxs = value_get(node->state->ctxbag, &size);
	size /= sizeof(hvalue_t);

	for (unsigned int i = 0; i < size; i += 2) {
		if (is_stuck(node, node, ctxs[i], false) == BW_RETURN) {
			struct failure *f = new_alloc(struct failure);
			f->type = FAIL_BUSYWAIT;
			f->choice = node->choice;
			f->node = node;
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

    return node_cmp(fail1->node, fail2->node);
}

static void do_work(struct worker *w){
	struct node *node;
	while ((node = w->todo) != NULL) {
		w->todo = node->next;
		struct state *state = node->state;
		w->global->dequeued++; // TODO race condition

		if (state->choosing != 0) {
			assert(VALUE_TYPE(state->choosing) == VALUE_CONTEXT);

			struct context *cc = value_get(state->choosing, NULL);
			assert(cc != NULL);
			assert(cc->sp > 0);
			hvalue_t s = cc->stack[cc->sp - 1];
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
	}
}

static void worker(void *arg){
    struct worker *w = arg;
    double work_time = 0, wait_time = 0, start, now;

    for (int epoch = 0;; epoch++) {
        // start of sequential phase
        barrier_wait(w->start_barrier);
        // parallel phase starts now
        start = gettime();
		// printf("WORKER %d starting epoch %d\n", w->index, epoch);
		do_work(w);
        now = gettime();
        work_time += now - start;
        // wait for others to finish
        start = now;
		// printf("WORKER %d finished epoch %d %f %f\n", w->index, epoch, work_time, wait_time);
        barrier_wait(w->middle_barrier);
		// printf("WORKER %d make stable %d %f %f\n", w->index, epoch, work_time, wait_time);
        value_make_stable(&w->global->values, w->nworkers, w->index);
        dict_make_stable(w->visited, w->nworkers, w->index);
        barrier_wait(w->end_barrier);
        // start of sequential phase
        now = gettime();
        wait_time += now - start;
    }
}

int process_results(
    struct global_t *global,
    struct worker *w,
    struct worker *workers,
    int nworkers,
    int count
) {
	struct node *node;
    int next = count % nworkers;
    struct node *results = w->results;

    while ((node = results) != NULL) {
		results = node->next;
        graph_add(&global->graph, node);   // sets node->id
        assert(node->id != 0);
        struct node **todo = &workers[next].todo;
        node->next = *todo;
        *todo = node;
        count++;
        if (++next == nworkers) {
            next = 0;
        }
        global->enqueued++;
    }
    w->results = NULL;

    struct failure *f;
    while ((f = w->failures) != NULL) {
        w->failures = f->next;
        minheap_insert(global->failures, f);
    }

    return count;
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
                    free(e);
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
    struct dict *symbols = dict_new(0, NULL, NULL);
    hvalue_t symbol_id = 0;

    for (unsigned int i = 0; i < graph->size; i++) {
        struct node *n = graph->nodes[i];
        if (!n->reachable) {
            continue;
        }
        for (struct edge *e = n->fwd; e != NULL; e = e->fwdnext) {
            for (unsigned int j = 0; j < e->nlog; j++) {
                void **p = dict_insert(symbols, &e->log[j], sizeof(e->log[j]));
                if (*p == NULL) {
                    *p = (void *) ++symbol_id;
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
    fprintf(se->out, "     \"%"PRIu64"\": %s", (uint64_t) value, p);
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
        void *p = dict_lookup(pte->symbols, &log[i], sizeof(log[i]));
        assert(p != NULL);
        if (i != 0) {
            fprintf(pte->out, ",");
        }
        fprintf(pte->out, "%"PRIu64, (uint64_t) p);
    }
    fprintf(pte->out, "],[%s]]", strbuf_getstr(sb));
    strbuf_deinit(sb);
    free(sb);
}

static void print_transitions(FILE *out, struct dict *symbols, struct edge *edges){
    struct dict *d = dict_new(0, NULL, NULL);

    fprintf(out, "      \"transitions\": [\n");
    for (struct edge *e = edges; e != NULL; e = e->fwdnext) {
        void **p = dict_insert(d, e->log, e->nlog * sizeof(*e->log));
        struct strbuf *sb = *p;
        if (sb == NULL) {
            *p = sb = malloc(sizeof(struct strbuf));
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
    if (argc - i != 1 || outfile == NULL) {
        usage(argv[0]);
    }
    char *fname = argv[i];
    double timeout = gettime() + maxtime;

    // initialize modules
    struct global_t *global = new_alloc(struct global_t);
    value_init(&global->values);
    ops_init(global);
    graph_init(&global->graph, 1024*1024);
    global->failures = minheap_create(fail_cmp);
    global->processes = NULL;
    global->nprocesses = 0;
    global->lasttime = 0;
    global->enqueued = 0;
    global->dequeued = 0;
    global->dumpfirst = false;
    global->init_name = value_put_atom(&global->values, "__init__", 8);

    // First read and parse the DFA if any
    if (dfafile != NULL) {
        global->dfa = dfa_read(&global->values, dfafile);
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
    struct json_value *jv = json_parse_value(&buf);
    assert(jv->type == JV_MAP);

    // travel through the json code contents to create the code array
    struct json_value *jc = dict_lookup(jv->u.map, "code", 4);
    assert(jc->type == JV_LIST);
    global->code = code_init_parse(&global->values, jc);

    // Create an initial state
    struct context *init_ctx = new_alloc(struct context);
    init_ctx->name = global->init_name;
    init_ctx->arg = VALUE_LIST;
    init_ctx->this = VALUE_DICT;
    init_ctx->vars = VALUE_DICT;
    init_ctx->atomic = 1;
    init_ctx->atomicFlag = true;
    value_ctx_push(&init_ctx, VALUE_TO_INT(CALLTYPE_PROCESS));
    value_ctx_push(&init_ctx, VALUE_LIST);
    struct state *state = new_alloc(struct state);
    state->vars = VALUE_DICT;
    state->seqs = VALUE_SET;
    hvalue_t ictx = value_put_context(&global->values, init_ctx);
    state->ctxbag = value_dict_store(&global->values, VALUE_DICT, ictx, VALUE_TO_INT(1));
    state->stopbag = VALUE_DICT;
    state->invariants = VALUE_SET;
    state->dfa_state = global->dfa == NULL ? 0 : dfa_initial(global->dfa);
    global->processes = new_alloc(hvalue_t);
    *global->processes = ictx;
    global->nprocesses = 1;

    // Put the initial state in the visited map
    struct dict *visited = dict_new(0, NULL, NULL);
    struct node *node = node_alloc();
    node->state = state;
    node->after = ictx;
    graph_add(&global->graph, node);
    void **p = dict_insert(visited, state, sizeof(*state));
    assert(*p == NULL);
    *p = node;

    // Determine how many worker threads to use
    int nworkers = getNumCores();
	printf("nworkers = %d\n", nworkers);
    barrier_t start_barrier, middle_barrier, end_barrier;
    barrier_init(&start_barrier, nworkers + 1);
    barrier_init(&middle_barrier, nworkers + 1);
    barrier_init(&end_barrier, nworkers + 1);

    // Allocate space for worker info
    struct worker *workers = calloc(nworkers, sizeof(*workers));
    for (int i = 0; i < nworkers; i++) {
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
        w->inv_step.ctx = new_alloc(struct context);
        w->inv_step.ctx->name = value_put_atom(&global->values, "__invariant__", 13);
        w->inv_step.ctx->arg = VALUE_LIST;
        w->inv_step.ctx->this = VALUE_DICT;
        w->inv_step.ctx->vars = VALUE_DICT;
        w->inv_step.ctx->atomic = w->inv_step.ctx->readonly = 1;
        w->inv_step.ctx->interruptlevel = false;
    }

    // Start the workers, who'll wait on the start barrier
    for (int i = 0; i < nworkers; i++) {
        thread_create(worker, &workers[i]);
    }

    // Give the initial state to worker 0
	workers[0].todo = node;
    global->enqueued++;

    double before = gettime(), postproc = 0;
    while (minheap_empty(global->failures)) {
        // Put the value dictionaries in concurrent mode
        value_set_concurrent(&global->values);
        dict_set_concurrent(visited);

        // make the threads work
        barrier_wait(&start_barrier);
        barrier_wait(&middle_barrier);
        barrier_wait(&end_barrier);
        // printf("Diameter %d\n", global->diameter);
        global->diameter++;

        double before_postproc = gettime();

        // Deal with the unstable values
        value_set_sequential(&global->values);
        dict_set_sequential(visited);

        int count = 0;

        // Collect the results of all the workers
        for (int i = 0; i < nworkers; i++) {
            struct worker *w = &workers[i];
			count = process_results(global, w, workers, nworkers, count);
        }

        if (count == 0) {
            break;
        }

        postproc += gettime() - before_postproc;
    }

    printf("#states %d (time %.3lf+%.3lf=%.3lf)\n", global->graph.size, gettime() - before - postproc, postproc, gettime() - before);

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
                comp->all_same = value_ctx_all_eternal(node->state->ctxbag)
                    && value_ctx_all_eternal(node->state->stopbag);
            }
            else if (node->state->vars != comp->rep->state->vars ||
                        !value_ctx_all_eternal(node->state->ctxbag) ||
                        !value_ctx_all_eternal(node->state->stopbag)) {
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
						!dfa_is_final(global->dfa, node->state->dfa_state)) {
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_BEHAVIOR;
                    f->choice = node->choice;
                    f->node = node;
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
                    f->choice = node->choice;
                    f->node = node;
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
            if (node->parent != NULL) {
                fprintf(df, "    parent: %d\n", node->parent->id);
            }
            fprintf(df, "    vars: %s\n", value_string(node->state->vars));
            fprintf(df, "    fwd:\n");
            int eno = 0;
            for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext, eno++) {
                fprintf(df, "        %d:\n", eno);
                struct context *ctx = value_get(edge->ctx, NULL);
                fprintf(df, "            context: %s %s %d\n", value_string(ctx->name), value_string(ctx->arg), ctx->pc);
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
                fprintf(df, "            context: %s %s %d\n", value_string(ctx->name), value_string(ctx->arg), ctx->pc);
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
            graph_check_for_data_race(node, warnings, &global->values);
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
                char *val = json_escape_value(node->state->vars);
                fprintf(out, "      \"value\": \"%s:%d\",\n", val, node->state->choosing != 0);
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
        path_dump(global, out, bad->node, bad->parent, bad->choice, &oldstate, &oldctx, bad->interrupt, bad->node->steps);
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
