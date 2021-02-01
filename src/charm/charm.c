#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <assert.h>

#ifndef HARMONY_COMBINE
#include "global.h"
#endif

#define CHUNKSIZE   (1 << 12)

struct combined {           // combination of current state and current context
    struct state state;
    struct context context;
};

struct component {
    bool good;          // terminating or out-going edge
};

struct edge {
    struct edge *next;      // linked list maintenance
    uint64_t ctx, choice;   // ctx that made the microstep, choice if any
    bool interrupt;         // set if state change is an interrupt
    struct node *node;      // resulting node (state)
    int weight;
};

struct node {
    // Information about state
    struct state *state;    // state corresponding to this node
    int id;                 // nodes are numbered starting from 0
    struct edge *fwd;       // forward edges
    struct edge *bwd;       // backward edges

    // How to get here from parent node
    struct node *parent;    // shortest path to initial state
    int len;                // length of path to initial state
    uint64_t before;        // context before state change
    uint64_t after;         // context after state change (current context)
    uint64_t choice;        // choice made if any
    bool interrupt;         // set if gotten here by interrupt

    // SCC
    bool visited;           // for Kosaraju algorithm
    unsigned int component; // strongly connected component id
};

struct failure {
    enum { FAIL_SAFETY, FAIL_INVARIANT, FAIL_TERMINATION } type;
    struct node *node;      // failed state
    uint64_t ctx;           // context that failed (before it failed)
    uint64_t choice;        // choice if any
};

struct code *code;
int code_len;

static struct node **graph;        // vector of all nodes
static int graph_size;             // to create node identifiers
static int graph_alloc;            // size allocated
static struct queue *failures;     // queue of "struct failure"  (TODO: make part of struct node "issues")
static uint64_t *processes;        // list of contexts of processes
static int nprocesses;             // the number of processes in the list
static double lasttime;            // since last report printed
static int timecnt;                // to reduce time overhead
static int enqueued;               // #states enqueued
static int dequeued;               // #states dequeued
static bool dumpfirst;             // for json dumping

static void graph_add(struct node *node){
    node->id = graph_size;
    if (graph_size >= graph_alloc) {
        graph_alloc = (graph_alloc + 1) * 2;
        graph = realloc(graph, (graph_alloc * sizeof(struct node *)));
    }
    graph[graph_size++] = node;
}

static void code_get(struct json_value *jv){
    assert(jv->type == JV_MAP);
    struct json_value *op = dict_lookup(jv->u.map, "op", 2);
    assert(op->type == JV_ATOM);
    struct op_info *oi = ops_get(op->u.atom.base, op->u.atom.len);
    if (oi == NULL) {
        fprintf(stderr, "Unknown HVM instruction: %.*s\n", op->u.atom.len, op->u.atom.base);
        exit(1);
    }
    code = realloc(code, (code_len + 1) * 2 * sizeof(struct code));
    struct code *c = &code[code_len++];
    c->oi = oi;
    c->env = (*oi->init)(jv->u.map);
    c->choose = strcmp(oi->name, "Choose") == 0;
    c->breakable = strcmp(oi->name, "Load") == 0 ||
        strcmp(oi->name, "Store") == 0 ||
        strcmp(oi->name, "AtomicInc") == 0;
}

bool invariant_check(struct state *state, struct context **pctx, int end){
    assert((*pctx)->sp == 0);
    assert((*pctx)->failure == 0);
    (*pctx)->pc++;
    while ((*pctx)->pc != end) {
        struct op_info *oi = code[(*pctx)->pc].oi;
        int oldpc = (*pctx)->pc;
        (*oi->op)(code[oldpc].env, state, pctx);
        if ((*pctx)->failure != 0) {
            (*pctx)->sp = 0;
            return false;
        }
        assert((*pctx)->pc != oldpc);
        assert((*pctx)->phase != CTX_END);
    }
    assert((*pctx)->sp == 1);
    (*pctx)->sp = 0;
    uint64_t b = (*pctx)->stack[0];
    assert((b & VALUE_MASK) == VALUE_BOOL);
    return b >> VALUE_BITS;
}

void check_invariants(struct node *node, struct context **pctx){
    struct state *state = node->state;
    extern int invariant_cnt(const void *env);

    assert((state->invariants & VALUE_MASK) == VALUE_SET);
    assert((*pctx)->sp == 0);
    int size;
    uint64_t *vals = value_get(state->invariants, &size);
    size /= sizeof(uint64_t);
    for (int i = 0; i < size; i++) {
        assert((vals[i] & VALUE_MASK) == VALUE_PC);
        (*pctx)->pc = vals[i] >> VALUE_BITS;
        assert(strcmp(code[(*pctx)->pc].oi->name, "Invariant") == 0);
        int cnt = invariant_cnt(code[(*pctx)->pc].env);
        bool b = invariant_check(state, pctx, (*pctx)->pc + cnt);
        if ((*pctx)->failure != 0) {
            printf("IC FAIL %s\n", value_string((*pctx)->failure));
            b = false;
        }
        if (!b) {
            struct failure *f = new_alloc(struct failure);
            f->type = FAIL_INVARIANT;
            f->ctx = node->before;
            f->choice = node->choice;
            f->node = node;
            queue_enqueue(failures, f);
        }
    }
}

void onestep(struct node *node, uint64_t ctx, uint64_t choice, bool interrupt,
        struct dict *visited, struct queue *todo, struct context **pinv_ctx,
        bool infloop_detect){
    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    memcpy(sc, node->state, sizeof(*sc));
    sc->choosing = 0;

    // Make a copy of the context
    struct context *cc = value_copy(ctx, NULL);
    assert(cc->phase != CTX_END);
    assert(cc->failure == 0);

    if (false) {
        printf("ONESTEP %"PRIx64" %"PRIx64"\n", ctx, sc->ctxbag);
    }

    // See if we should also try an interrupt.
    if (interrupt) {
        extern void interrupt_invoke(struct context **pctx);
		assert(cc->trap_pc != 0);
        interrupt_invoke(&cc);
    }
    else if (sc->choosing == 0 && cc->trap_pc != 0 && !cc->interruptlevel) {
        onestep(node, ctx, choice, true, visited, todo, pinv_ctx, infloop_detect);
    }

    // Copy the choice
    uint64_t choice_copy = choice;

    bool choosing = false, infinite_loop = false;;
    struct dict *infloop = NULL;        // infinite loop detector
    for (int loopcnt = 0;; loopcnt++) {
        int pc = cc->pc;

        if (timecnt-- == 0) {
            struct timeval tv;
            gettimeofday(&tv, NULL);
            double now = tv.tv_sec + (double) tv.tv_usec / 1000000;
            if (now - lasttime > 1) {
                if (lasttime != 0) {
                    char *p = value_string(cc->name);
                    printf("%s pc=%d states=%d queue=%d\n",
                            p, cc->pc, enqueued, enqueued - dequeued);
                    free(p);
                }
                lasttime = now;
            }
            timecnt = 1;
        }

        struct op_info *oi = code[pc].oi;
        if (code[pc].choose) {
            cc->stack[cc->sp - 1] = choice;
            cc->pc++;
        }
        else {
            if (code[pc].breakable) {
                assert(cc->phase != CTX_END);
                cc->phase = CTX_MIDDLE;
            }
            (*oi->op)(code[pc].env, sc, &cc);
        }

        if (cc->phase != CTX_END && cc->failure == 0 && (infloop_detect || loopcnt > 1000)) {
            if (infloop == NULL) {
                infloop = dict_new(0);
            }

            int stacksize = cc->sp * sizeof(uint64_t);
            int combosize = sizeof(struct combined) + stacksize;
            struct combined *combo = calloc(1, combosize);
            combo->state = *sc;
            memcpy(&combo->context, cc, sizeof(*cc) + stacksize);
            void **p = dict_insert(infloop, combo, combosize);
            free(combo);
            if (*p == (void *) 0) {
                *p = (void *) 1;
            }
            else if (infloop_detect) {
                cc->failure = value_put_atom("infinite loop", 13);
                infinite_loop = true;
            }
            else {
                // start over, as twostep does not have loopcnt optimization
                onestep(node, ctx, choice_copy, interrupt, visited, todo, pinv_ctx, true);
                free(cc);
                free(sc);
                return;
            }
        }

        if (cc->phase == CTX_END || cc->failure != 0 || cc->stopped) {
            break;
        }
        if (cc->pc == pc) {
            fprintf(stderr, ">>> %s\n", oi->name);
        }
        assert(cc->pc != pc);

        /* Peek at the next instruction.
         */
        oi = code[cc->pc].oi;
        if (code[cc->pc].choose) {
            assert(cc->sp > 0);
            if (cc->readonly > 0) {
                ctx_failure(cc, "can't choose in assertion or invariant");
                break;
            }
            uint64_t s = cc->stack[cc->sp - 1];
            if ((s & VALUE_MASK) != VALUE_SET) {
                ctx_failure(cc, "choose operation requires a set");
                break;
            }
            int size;
            uint64_t *vals = value_get(s, &size);
            size /= sizeof(uint64_t);
            if (size == 0) {
                ctx_failure(cc, "choose operation requires a non-empty set");
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

        if (cc->phase != CTX_START && cc->atomic == 0 && sc->ctxbag != VALUE_DICT &&
                code[cc->pc].breakable) {
            break;
        }
    }
    
    if (infloop != NULL) {
        dict_delete(infloop);
    }

    // Remove old context from the bag
    uint64_t count = dict_load(sc->ctxbag, ctx);
    assert((count & VALUE_MASK) == VALUE_INT);
    count -= 1 << VALUE_BITS;
    if (count == VALUE_INT) {
        sc->ctxbag = dict_remove(sc->ctxbag, ctx);
    }
    else {
        sc->ctxbag = dict_store(sc->ctxbag, ctx, count);
    }

    // Store new context in value directory.  Must be immutable now.
    uint64_t after = value_put_context(cc);

    // If choosing, save in state
    if (choosing) {
        assert(cc->phase != CTX_END);
        sc->choosing = after;
    }

    // Add new context to state unless it's terminated or stopped
    if (cc->stopped) {
        sc->stopbag = bag_add(sc->stopbag, after);
    }
    else if (cc->phase != CTX_END) {
        sc->ctxbag = bag_add(sc->ctxbag, after);
    }

    // Weight of this step
    int weight = ctx == node->after ? 0 : 1;

    // See if this new state was already seen before.
    void **p = dict_insert(visited, sc, sizeof(*sc));
    struct node *next;
    if ((next = *p) == NULL) {
        *p = next = new_alloc(struct node);
        next->parent = node;
        next->state = sc;               // TODO: duplicate value
        next->before = ctx;
        next->choice = choice_copy;
        next->interrupt = interrupt;
        next->after = after;
        next->len = node->len + weight;
        graph_add(next);

        if (sc->choosing == 0 && sc->invariants != VALUE_SET) {
            check_invariants(next, pinv_ctx);
        }

        if (sc->ctxbag != VALUE_DICT && cc->failure == 0 &&
                queue_empty(failures)) {
            if (weight == 0) {
                queue_prepend(todo, next);
            }
            else {
                queue_enqueue(todo, next);
            }
            enqueued++;
        }
    }
    else {
        free(sc);

        if (next->len > node->len + weight) {
            next->parent = node;
            next->before = ctx;
            next->after = after;
            next->choice = choice_copy;
            next->len = node->len + weight;
        }
    }

    // Add a forward edge from node to next.
    struct edge *fwd = new_alloc(struct edge);
    fwd->ctx = ctx;
    fwd->choice = choice_copy;
    fwd->interrupt = interrupt;
    fwd->node = next;
    fwd->weight = weight;
    fwd->next = node->fwd;
    node->fwd = fwd;

    // Add a backward edge from next to node.
    struct edge *bwd = new_alloc(struct edge);
    bwd->ctx = ctx;
    bwd->choice = choice_copy;
    fwd->interrupt = interrupt;
    bwd->node = node;
    bwd->weight = weight;
    bwd->next = next->bwd;
    next->bwd = bwd;

    if (cc->failure != 0) {
        struct failure *f = new_alloc(struct failure);
        f->type = infinite_loop ? FAIL_TERMINATION : FAIL_SAFETY;
        f->ctx = ctx;
        f->choice = choice_copy;
        f->node = next;
        queue_enqueue(failures, f);
    }

    free(cc);
}

void print_vars(FILE *file, uint64_t v){
    assert((v & VALUE_MASK) == VALUE_DICT);
    int size;
    uint64_t *vars = value_get(v, &size);
    size /= sizeof(uint64_t);
    fprintf(file, "{");
    for (int i = 0; i < size; i += 2) {
        if (i > 0) {
            fprintf(file, ",");
        }
        char *k = value_string(vars[i]);
        char *v = value_json(vars[i+1]);
        fprintf(file, " \"%s\": %s", k+1, v);
        free(k);
        free(v);
    }
    fprintf(file, " }");
}

bool print_trace(FILE *file, struct context *ctx, int pc, int fp, uint64_t vars){
    if (fp == 0) {
        return false;
    }
    assert(fp >= 4);

	int level = 0, orig_pc = pc;
    if (strcmp(code[pc].oi->name, "Frame") == 0) {
        uint64_t ct = ctx->stack[ctx->sp - 2];
        assert((ct & VALUE_MASK) == VALUE_INT);
        switch (ct >> VALUE_BITS) {
        case CALLTYPE_PROCESS:
            pc++;
            break;
        case CALLTYPE_INTERRUPT:
        case CALLTYPE_NORMAL:
            {
                uint64_t retaddr = ctx->stack[ctx->sp - 3];
                assert((retaddr & VALUE_MASK) == VALUE_PC);
                pc = retaddr >> VALUE_BITS;
            }
            break;
        default:
            panic("print_trace: bad call type 1");
        }
    }
    while (--pc >= 0) {
        if (strcmp(code[pc].oi->name, "Return") == 0) {
			level++;
		}
        else if (strcmp(code[pc].oi->name, "Frame") == 0) {
			if (level == 0) {
				if (fp >= 5) {
                    assert((ctx->stack[fp - 5] & VALUE_MASK) == VALUE_PC);
					int npc = ctx->stack[fp - 5] >> VALUE_BITS;
					uint64_t nvars = ctx->stack[fp - 2];
					int nfp = ctx->stack[fp - 1] >> VALUE_BITS;
					if (print_trace(file, ctx, npc, nfp, nvars)) {
                        fprintf(file, ",\n");
                    }
				}
				fprintf(file, "            {\n");
				fprintf(file, "              \"pc\": \"%d\",\n", orig_pc);

				const struct env_Frame *ef = code[pc].env;
				char *s = value_string(ef->name), *a = NULL;
                a = value_string(ctx->stack[fp - 3]);
				if (*a == '(') {
					fprintf(file, "              \"method\": \"%s%s\",\n", s + 1, a);
				}
				else {
					fprintf(file, "              \"method\": \"%s(%s)\",\n", s + 1, a);
				}

                uint64_t ct = ctx->stack[fp - 4];
                assert((ct & VALUE_MASK) == VALUE_INT);
                switch (ct >> VALUE_BITS) {
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

char *ctx_status(struct node *node, uint64_t ctx) {
    if (node->state->choosing == ctx) {
        return "choosing";
    }
    while (node->state->choosing != 0) {
        node = node->parent;
    }
    struct edge *edge;
    for (edge = node->fwd; edge != NULL; edge = edge->next) {
        if (edge->ctx == ctx) {
            break;
        }
    };
    if (edge != NULL && edge->node == node) {
        return "blocked";
    }
    return "runnable";
}

void print_context(FILE *file, uint64_t ctx, int tid, struct node *node){
    char *s, *a;

    fprintf(file, "        {\n");
    fprintf(file, "          \"tid\": \"%d\",\n", tid);

    struct context *c = value_get(ctx, NULL);

    s = value_string(c->name);
    a = value_string(c->arg);
    if (*a == '(') {
        fprintf(file, "          \"name\": \"%s%s\",\n", s + 1, a);
    }
    else {
        fprintf(file, "          \"name\": \"%s(%s)\",\n", s + 1, a);
    }
    free(s);
    free(a);

    // assert((c->entry & VALUE_MASK) == VALUE_PC);   TODO
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
    print_trace(file, c, c->pc, c->fp, c->vars);
    fprintf(file, "\n");
    fprintf(file, "          ],\n");

    if (c->failure != 0) {
        s = value_string(c->failure);
        fprintf(file, "          \"failure\": \"%s\",\n", s + 1);
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

    if (c->phase == CTX_END) {
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

void print_state(FILE *file, struct node *node){
#ifdef notdef
    fprintf(file, "      \"shared\": ");
    print_vars(file, node->state->vars);
    fprintf(file, ",\n");
#endif

    struct state *state = node->state;
    extern int invariant_cnt(const void *env);
    struct context *inv_ctx = new_alloc(struct context);
    uint64_t inv_nv = value_put_atom("name", 4);
    uint64_t inv_tv = value_put_atom("tag", 3);
    inv_ctx->name = value_put_atom("__invariant__", 13);
    inv_ctx->arg = VALUE_DICT;
    inv_ctx->this = VALUE_DICT;
    inv_ctx->vars = VALUE_DICT;
    inv_ctx->atomic = inv_ctx->readonly = 1;
    inv_ctx->interruptlevel = false;

    fprintf(file, "      \"invfails\": [");
    assert((state->invariants & VALUE_MASK) == VALUE_SET);
    int size;
    uint64_t *vals = value_get(state->invariants, &size);
    size /= sizeof(uint64_t);
    int nfailures = 0;
    for (int i = 0; i < size; i++) {
        assert((vals[i] & VALUE_MASK) == VALUE_PC);
        inv_ctx->pc = vals[i] >> VALUE_BITS;
        assert(strcmp(code[inv_ctx->pc].oi->name, "Invariant") == 0);
        int cnt = invariant_cnt(code[inv_ctx->pc].env);
        bool b = invariant_check(state, &inv_ctx, inv_ctx->pc + cnt);
        if (inv_ctx->failure != 0) {
            b = false;
        }
        if (!b) {
            if (nfailures != 0) {
                fprintf(file, ",");
            }
            fprintf(file, "\n        {\n");
            fprintf(file, "          \"pc\": \"%"PRIu64"\",\n", vals[i] >> VALUE_BITS);
            if (inv_ctx->failure == 0) {
                fprintf(file, "          \"reason\": \"invariant violated\"\n");
            }
            else {
                char *val = value_string(inv_ctx->failure);
                fprintf(file, "          \"reason\": \"%s\"\n", val + 1);
                free(val);
            }
            nfailures++;
            fprintf(file, "        }");
        }
    }
    fprintf(file, "\n      ],\n");
    free(inv_ctx);

    fprintf(file, "      \"contexts\": [\n");
    for (int i = 0; i < nprocesses; i++) {
        print_context(file, processes[i], i, node);
        if (i < nprocesses - 1) {
            fprintf(file, ",");
        }
        fprintf(file, "\n");
    }
    fprintf(file, "      ]\n");
}

void diff_state(FILE *file, struct state *oldstate, struct state *newstate,
                struct context *oldctx, struct context *newctx,
                bool interrupt, bool choose, uint64_t choice){
    if (dumpfirst) {
        dumpfirst = false;
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
    fprintf(file, "          \"npc\": \"%d\",\n", newctx->pc);
    if (newctx->fp != oldctx->fp) {
        fprintf(file, "          \"fp\": \"%d\",\n", newctx->fp);
        fprintf(file, "          \"trace\": [\n");
        print_trace(file, newctx, newctx->pc, newctx->fp, newctx->vars);
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
        fprintf(file, "          \"failure\": \"%s\",\n", val + 1);
        fprintf(file, "          \"mode\": \"failed\",\n");
        free(val);
    }
    else if (newctx->phase == CTX_END) {
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

void diff_dump(FILE *file, struct state *oldstate, struct state *newstate,
                struct context **oldctx, struct context *newctx,
                bool interrupt, bool choose, uint64_t choice){
    int newsize = sizeof(*newctx) + (newctx->sp * sizeof(uint64_t));

    if (memcmp(oldstate, newstate, sizeof(struct state)) == 0 &&
            (*oldctx)->sp == newctx->sp &&
            memcmp(*oldctx, newctx, newsize) == 0) {
        return;
    }

    // Keep track of old state and context for taking diffs
    diff_state(file, oldstate, newstate, *oldctx, newctx, interrupt, choose, choice);
    *oldstate = *newstate;
    free(*oldctx);
    *oldctx = malloc(newsize);
    memcpy(*oldctx, newctx, newsize);
}

// similar to onestep.  TODO.  Use flag to onestep?
uint64_t twostep(FILE *file, struct node *node, uint64_t ctx, uint64_t choice,
        bool interrupt, struct state *oldstate, struct context **oldctx){
    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    memcpy(sc, node->state, sizeof(*sc));
    sc->choosing = 0;

    // Make a copy of the context
    struct context *cc = value_copy(ctx, NULL);
    // diff_dump(file, oldstate, sc, oldctx, cc, node->interrupt);
    if (cc->phase == CTX_END || cc->failure != 0) {
        free(cc);
        return ctx;
    }

    if (interrupt) {
        extern void interrupt_invoke(struct context **pctx);
		assert(cc->trap_pc != 0);
        interrupt_invoke(&cc);
        diff_dump(file, oldstate, sc, oldctx, cc, true, false, 0);
    }

    bool choosing = false;
    struct dict *infloop = NULL;        // infinite loop detector
    for (int loopcnt = 0;; loopcnt++) {
        int pc = cc->pc;

        struct op_info *oi = code[pc].oi;
        if (code[pc].choose) {
            cc->stack[cc->sp - 1] = choice;
            cc->pc++;
        }
        else {
            if (code[pc].breakable) {
                assert(cc->phase != CTX_END);
                cc->phase = CTX_MIDDLE;
            }
            (*oi->op)(code[pc].env, sc, &cc);
        }

        if (cc->phase != CTX_END && cc->failure == 0) {
            if (infloop == NULL) {
                infloop = dict_new(0);
            }

            int stacksize = cc->sp * sizeof(uint64_t);
            int combosize = sizeof(struct combined) + stacksize;
            struct combined *combo = calloc(1, combosize);
            combo->state = *sc;
            memcpy(&combo->context, cc, sizeof(*cc) + stacksize);
            void **p = dict_insert(infloop, combo, combosize);
            if (*p == (void *) 0) {
                *p = (void *) 1;
            }
            else {
                cc->failure = value_put_atom("infinite loop", 13);
            }
            free(combo);
        }

        diff_dump(file, oldstate, sc, oldctx, cc, false, code[pc].choose, choice);
        if (cc->phase == CTX_END || cc->failure != 0 || cc->stopped) {
            break;
        }
        if (cc->pc == pc) {
            fprintf(stderr, ">>> %s\n", oi->name);
        }
        assert(cc->pc != pc);

        /* Peek at the next instruction.
         */
        oi = code[cc->pc].oi;
        if (code[cc->pc].choose) {
            assert(cc->sp > 0);
            if (cc->readonly > 0) {
                ctx_failure(cc, "can't choose in assertion or invariant");
                diff_dump(file, oldstate, sc, oldctx, cc, false, code[pc].choose, choice);
                break;
            }
            uint64_t s = cc->stack[cc->sp - 1];
            if ((s & VALUE_MASK) != VALUE_SET) {
                ctx_failure(cc, "choose operation requires a set");
                diff_dump(file, oldstate, sc, oldctx, cc, false, code[pc].choose, choice);
                break;
            }
            int size;
            uint64_t *vals = value_get(s, &size);
            size /= sizeof(uint64_t);
            if (size == 0) {
                ctx_failure(cc, "choose operation requires a non-empty set");
                diff_dump(file, oldstate, sc, oldctx, cc, false, code[pc].choose, choice);
                break;
            }
            if (size == 1) {
                choice = vals[0];
            }
            else {
                choosing = true;
                break;
            }
        }

        if (cc->phase != CTX_START && cc->atomic == 0 && sc->ctxbag != VALUE_DICT &&
                code[cc->pc].breakable) {
            break;
        }
    }

    ctx = value_put_context(cc);

    free(sc);
    free(cc);

    return ctx;
}

void path_dump(FILE *file, struct node *last, uint64_t ctx, uint64_t choice,
            struct state *oldstate, struct context **oldctx, bool interrupt){
    struct node *node = last;

    last = last->parent;
    if (last->parent == NULL) {
        fprintf(file, "\n");
    }
    else {
        path_dump(file, last, last->before, last->choice, oldstate, oldctx, last->interrupt);
        fprintf(file, ",\n");
    }

    fprintf(file, "    {\n");
    fprintf(file, "      \"id\": \"%d\",\n", node->id);

    /* Find this context in the list of processes.
     */
    int pid;
    for (pid = 0; pid < nprocesses; pid++) {
        if (processes[pid] == ctx) {
            break;
        }
    }
    assert(pid < nprocesses);

    struct context *context = value_get(ctx, NULL);
    assert(context->phase != CTX_END);
    char *name = value_string(context->name);
    char *arg = value_string(context->arg);
    // char *c = value_string(choice);
    fprintf(file, "      \"tid\": \"%d\",\n", pid);
    if (*arg == '(') {
        fprintf(file, "      \"name\": \"%s%s\",\n", name + 1, arg);
    }
    else {
        fprintf(file, "      \"name\": \"%s(%s)\",\n", name + 1, arg);
    }
    // fprintf(file, "      \"choice\": \"%s\",\n", c);
    dumpfirst = true;
    fprintf(file, "      \"microsteps\": [");
    free(name);
    free(arg);
    // free(c);
    memset(*oldctx, 0, sizeof(**oldctx));
    (*oldctx)->pc = context->pc;

    // Recreate the steps
    processes[pid] = twostep(file, last, ctx, choice, interrupt, oldstate, oldctx);
    fprintf(file, "\n      ],\n");

    /* Match each context to a process.
     */
    bool *matched = calloc(nprocesses, sizeof(bool));
    int nctxs;
    uint64_t *ctxs = value_get(node->state->ctxbag, &nctxs);
    nctxs /= sizeof(uint64_t);
    for (int i = 0; i < nctxs; i += 2) {
        assert((ctxs[i] & VALUE_MASK) == VALUE_CONTEXT);
        assert((ctxs[i+1] & VALUE_MASK) == VALUE_INT);
        int cnt = ctxs[i+1] >> VALUE_BITS;
        for (int j = 0; j < cnt; j++) {
            int k;
            for (k = 0; k < nprocesses; k++) {
                if (!matched[k] && processes[k] == ctxs[i]) {
                    matched[k] = true;
                    break;
                }
            }
            if (k == nprocesses) {
                processes = realloc(processes, (nprocesses + 1) * sizeof(uint64_t));
                matched = realloc(matched, (nprocesses + 1) * sizeof(bool));
                processes[nprocesses] = ctxs[i];
                matched[nprocesses] = true;
                nprocesses++;
            }
        }
    }
    free(matched);
  
    print_state(file, node);
    fprintf(file, "    }");
}

static struct stack {
    struct stack *next;
    struct node *node;
} *stack;

static void kosaraju_visit(struct node *node) {
    if (node->visited) {
        return;
    }
    node->visited = true;

    for (struct edge *edge = node->fwd; edge != NULL; edge = edge->next) {
        kosaraju_visit(edge->node);
    }

    // Push node
    struct stack *s = new_alloc(struct stack);
    s->node = node;
    s->next = stack;
    stack = s;
}

static void kosaraju_assign(struct node *node, int component){
    if (node->visited) {
        return;
    }
    node->visited = true;
    node->component = component;
    for (struct edge *edge = node->bwd; edge != NULL; edge = edge->next) {
        kosaraju_assign(edge->node, component);
    }
}

static int find_scc(void){
    for (int i = 0; i < graph_size; i++) {
        kosaraju_visit(graph[i]);
    }

    // make sure all nodes are marked and on the stack
    // while at it clear all the visited flags
    int count = 0;
    for (struct stack *s = stack; s != NULL; s = s->next) {
        assert(s->node->visited);
        s->node->visited = false;
        count++;
    }
    assert(count == graph_size);

    count = 0;
    while (stack != NULL) {
        // Pop
        struct stack *top = stack;
        stack = top->next;
        struct node *next = top->node;
        free(top);

        if (!next->visited) {
            kosaraju_assign(next, count++);
        }
    }
    for (int i = 0; i < graph_size; i++) {
        assert(graph[i]->visited);
    }

    return count;
}

static void enum_loc(void *env, const void *key, unsigned int key_size,
                                HASHDICT_VALUE_TYPE value){
    static bool notfirst = false;
    FILE *out = env;

    if (notfirst) {
        fprintf(out, ",\n");
    }
    else {
        notfirst = true;
        fprintf(out, "\n");
    }
    fprintf(out, "    \"%.*s\": { ", key_size, (char *) key);

    struct json_value *jv = value;
    assert(jv->type == JV_MAP);

    struct json_value *file = dict_lookup(jv->u.map, "file", 4);
    assert(file->type == JV_ATOM);
    fprintf(out, "\"file\": \"%.*s\", ", file->u.atom.len, file->u.atom.base);

    struct json_value *line = dict_lookup(jv->u.map, "line", 4);
    assert(line->type == JV_ATOM);
    fprintf(out, "\"line\": \"%.*s\"", line->u.atom.len, line->u.atom.base);

    // parse the line number
    char *cline = malloc(line->u.atom.len + 1);
    strncpy(cline, line->u.atom.base, line->u.atom.len);
    cline[line->u.atom.len] = 0;
    int lineno = atoi(cline);
    free(cline);

    // copy the file name
    char *cfile = malloc(file->u.atom.len + 1);
    strncpy(cfile, file->u.atom.base, file->u.atom.len);
    cfile[file->u.atom.len] = 0;

    // TODO.  Should cache the contents of the file
    FILE *fp = fopen(cfile, "r");
    assert(fp != NULL);
    char buf[1024];
    while (fgets(buf, 1024, fp) != NULL) {
        if (--lineno == 0) {
            buf[1023] = 0;
            int len = strlen(buf);
            if (len > 0 && buf[len - 1] == '\n') {
                buf[len - 1] = 0;
            }
            fprintf(out, ", \"code\": \"%s\"", buf);
            break;
        }
    }
    fclose(fp);
    fprintf(out, " }");
}

int main(int argc, char **argv){
    // printf("Charm v1\n");

    failures = queue_init();

    // initialize modules
    ops_init();
    value_init();

    // open the file
    char *fname = argc == 1 ? "harmony.json" : argv[1];
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
    for (int i = 0; i < jc->u.list.nvals; i++) {
        // printf("Line %d\n", i);
        code_get(jc->u.list.vals[i]);
    }

    // Create an initial state
    struct context *init_ctx = new_alloc(struct context);;
    uint64_t nv = value_put_atom("name", 4);
    uint64_t tv = value_put_atom("tag", 3);
    init_ctx->name = value_put_atom("__init__", 8);
    init_ctx->arg = VALUE_DICT;
    init_ctx->this = VALUE_DICT;
    init_ctx->vars = VALUE_DICT;
    init_ctx->atomic = 1;
    ctx_push(&init_ctx, (CALLTYPE_PROCESS << VALUE_BITS) | VALUE_INT);
    ctx_push(&init_ctx, VALUE_DICT);
    struct state *state = new_alloc(struct state);
    state->vars = VALUE_DICT;
    uint64_t ictx = value_put_context(init_ctx);
    state->ctxbag = dict_store(VALUE_DICT, ictx, (1 << VALUE_BITS) | VALUE_INT);
    state->stopbag = VALUE_DICT;
    state->invariants = VALUE_SET;
    processes = new_alloc(uint64_t);
    *processes = ictx;
    nprocesses = 1;

    // Put the initial state in the visited map
    struct dict *visited = dict_new(0);
    struct node *node = new_alloc(struct node);
    node->state = state;
    node->after = ictx;
    graph_add(node);
    void **p = dict_insert(visited, state, sizeof(*state));
    assert(*p == NULL);
    *p = node;

    // Put the initial state on the queue
    struct queue *todo = queue_init();
    queue_enqueue(todo, node);
    enqueued++;

    // Create a context for evaluating invariants
    struct context *inv_ctx = new_alloc(struct context);
    uint64_t inv_nv = value_put_atom("name", 4);
    uint64_t inv_tv = value_put_atom("tag", 3);
    inv_ctx->name = value_put_atom("__invariant__", 13);
    inv_ctx->arg = VALUE_DICT;
    inv_ctx->this = VALUE_DICT;
    inv_ctx->vars = VALUE_DICT;
    inv_ctx->atomic = inv_ctx->readonly = 1;
    inv_ctx->interruptlevel = false;

    void *next;
    int state_counter = 1;
    while (queue_dequeue(todo, &next)) {
        state_counter++;
        dequeued++;

        node = next;
        state = node->state;

        if (state->choosing != 0) {
            assert((state->choosing & VALUE_MASK) == VALUE_CONTEXT);
            if (false) {
                printf("CHOOSING %"PRIx64"\n", state->choosing);
            }

            struct context *cc = value_get(state->choosing, NULL);
            assert(cc != NULL);
            assert(cc->sp > 0);
            uint64_t s = cc->stack[cc->sp - 1];
            assert((s & VALUE_MASK) == VALUE_SET);
            int size;
            uint64_t *vals = value_get(s, &size);
            size /= sizeof(uint64_t);
            assert(size > 0);
            for (int i = 0; i < size; i++) {
                if (false) {
                    printf("NEXT CHOICE %d %d %"PRIx64"\n", i, size, vals[i]);
                }
                onestep(node, state->choosing, vals[i], false, visited, todo, &inv_ctx, false);
                if (false) {
                    printf("NEXT CHOICE DONE\n");
                }
            }
        }
        else {
            int size;
            uint64_t *ctxs = value_get(state->ctxbag, &size);
            size /= sizeof(uint64_t);
            assert(size > 0);
            for (int i = 0; i < size; i += 2) {
                if (false) {
                    printf("NEXT CONTEXT %d %"PRIx64"\n", i, ctxs[i]);
                }
                assert((ctxs[i] & VALUE_MASK) == VALUE_CONTEXT);
                assert((ctxs[i+1] & VALUE_MASK) == VALUE_INT);
                onestep(node, ctxs[i], 0, false, visited, todo, &inv_ctx, false);
                if (false) {
                    printf("NEXT CONTEXT DONE\n");
                }
            }
        }
    }

    printf("#states %d\n", graph_size);

    if (queue_empty(failures)) {
        // find the strongly connected components
        int ncomponents = find_scc();

        // mark the ones that are good
        struct component *components = calloc(ncomponents, sizeof(*components));
        for (int i = 0; i < graph_size; i++) {
            struct node *node = graph[i];
			assert(node->component < ncomponents);
            struct component *comp = &components[node->component];
            if (comp->good) {
                continue;
            }
            if (node->state->ctxbag == VALUE_DICT && node->state->stopbag == VALUE_DICT) {
                comp->good = true;
                continue;
            }
            for (struct edge *edge = node->fwd;
                            edge != NULL && !comp->good; edge = edge->next) {
                if (edge->node->component != node->component) {
                    comp->good = true;
                }
            }
        }

        // now count the nodes that are in bad components
        int nbad = 0;
        for (int i = 0; i < graph_size; i++) {
            struct node *node = graph[i];
            if (!components[node->component].good) {
                nbad++;
                struct failure *f = new_alloc(struct failure);
                f->type = FAIL_TERMINATION;
                f->ctx = node->before;
                f->choice = node->choice;
                f->node = node;
                queue_enqueue(failures, f);
            }
        }

        printf("%d components, %d bad states\n", ncomponents, nbad);
    }

    FILE *out = fopen("charm.json", "w");
    assert(out != NULL);
    fprintf(out, "{\n");

    if (queue_empty(failures)) {
        printf("No issues\n");
        fprintf(out, "  \"issue\": \"No issues\"\n");
        fprintf(out, "}\n");
        exit(0);
    }

    struct failure *bad = NULL;
    while (queue_dequeue(failures, &next)) {
        struct failure *f = next;

        if (bad == NULL || f->node->len < bad->node->len) {
            bad = f;
        }
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
    case FAIL_TERMINATION:
        printf("Non-terminating state\n");
        fprintf(out, "  \"issue\": \"Non-terminating state\",\n");
        break;
    default:
        panic("main: bad fail type");
    }

    fprintf(out, "  \"macrosteps\": [");
    struct state oldstate;
	memset(&oldstate, 0, sizeof(oldstate));
    struct context *oldctx = calloc(1, sizeof(*oldctx));
    dumpfirst = true;
    path_dump(out, bad->node, bad->ctx, bad->choice, &oldstate, &oldctx, false);
    fprintf(out, "\n");
    free(oldctx);
    fprintf(out, "  ],\n");

    fprintf(out, "  \"code\": [\n");
    jc = dict_lookup(jv->u.map, "pretty", 6);
    assert(jc->type == JV_LIST);
    for (int i = 0; i < jc->u.list.nvals; i++) {
        struct json_value *next = jc->u.list.vals[i];
        assert(next->type == JV_LIST);
        assert(next->u.list.nvals == 2);
        struct json_value *codestr = next->u.list.vals[0];
        assert(codestr->type == JV_ATOM);
        fprintf(out, "    \"%.*s\"", codestr->u.atom.len, codestr->u.atom.base);
        if (i < jc->u.list.nvals - 1) {
            fprintf(out, ",");
        }
        fprintf(out, "\n");
    }
    fprintf(out, "  ],\n");

    fprintf(out, "  \"explain\": [\n");
    for (int i = 0; i < jc->u.list.nvals; i++) {
        struct json_value *next = jc->u.list.vals[i];
        assert(next->type == JV_LIST);
        assert(next->u.list.nvals == 2);
        struct json_value *codestr = next->u.list.vals[1];
        assert(codestr->type == JV_ATOM);
        fprintf(out, "    \"%.*s\"", codestr->u.atom.len, codestr->u.atom.base);
        if (i < jc->u.list.nvals - 1) {
            fprintf(out, ",");
        }
        fprintf(out, "\n");
    }
    fprintf(out, "  ],\n");

    fprintf(out, "  \"locations\": {");
    jc = dict_lookup(jv->u.map, "locations", 9);
    assert(jc->type == JV_MAP);
    dict_iter(jc->u.map, enum_loc, out);
    fprintf(out, "\n  }\n");

    fprintf(out, "}\n");

    return 0;
}
