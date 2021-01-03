#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <assert.h>
#include "global.h"
#include "json.h"

#define CHUNKSIZE   (1 << 12)

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
        assert((*pctx)->pc != oldpc);
        assert((*pctx)->phase != CTX_END);
        if ((*pctx)->failure != 0) {
            (*pctx)->sp = 0;
            return false;
        }
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
        bool b = invariant_check(node->state, pctx, (*pctx)->pc + cnt);
        if ((*pctx)->failure != 0) {
            printf("IC FAIL %llx\n", (*pctx)->failure);
            printf("IC FAIL %s\n", value_string((*pctx)->failure));
        }
        if (!b) {
            printf("INVARIANT FAILED\n");
            struct failure *f = new_alloc(struct failure);
            f->type = FAIL_INVARIANT;
            f->ctx = node->after;
            f->choice = 0;
            f->node = node;
            queue_enqueue(failures, f);
        }
    }
}

void onestep(struct node *node, uint64_t ctx, uint64_t choice, bool interrupt,
        struct dict *visited, struct queue *todo, struct context **pinv_ctx){
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
        onestep(node, ctx, 0, true, visited, todo, pinv_ctx);
    }

    // Copy the choice
    uint64_t choice_copy = choice;

    bool choosing = false;
    struct dict *infloop = NULL;        // infinite loop detector
    for (int loopcnt = 0;; loopcnt++) {
        int pc = cc->pc;

        if (timecnt-- == 0) {
            struct timeval tv;
            gettimeofday(&tv, NULL);
            double now = tv.tv_sec + (double) tv.tv_usec / 1000000;
            if (now - lasttime > 1) {
                char *p = value_string(cc->name);
                printf("%s pc=%d states=%d queue=%d\n", p, cc->pc, enqueued, enqueued - dequeued);
                free(p);
                lasttime = now;
            }
            timecnt = 1000;
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

        if ((cc->phase != CTX_END && cc->failure == 0) && loopcnt > 1000) {
            if (infloop == NULL) {
                infloop = dict_new(0);
            }
            // TODO.  Also add global state?
            void **p = dict_insert(infloop, cc,
                            sizeof(*cc) + (cc->sp * sizeof(uint64_t)));
            if (*p != (void *) 0) {
                cc->failure = value_put_atom("infinite loop", 13);
            }
            *p = (void *) 1;
        }

        if (cc->phase == CTX_END || cc->failure != 0) {
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
            uint64_t s = cc->stack[cc->sp - 1];
            assert((s & VALUE_MASK) == VALUE_SET);
            int size;
            uint64_t *vals = value_get(s, &size);
            size /= sizeof(uint64_t);
            assert(size > 0);
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

    // Add new context to state unless it's terminated
    if (cc->phase != CTX_END) {
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

        if (sc->invariants != VALUE_SET) {
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
        f->type = FAIL_SAFETY;
        f->ctx = after;
        f->choice = choice_copy;
        f->node = next;
        queue_enqueue(failures, f);
    }

    free(cc);
}

void print_vars(uint64_t v){
    assert((v & VALUE_MASK) == VALUE_DICT);
    int size;
    uint64_t *vars = value_get(v, &size);
    size /= sizeof(uint64_t);
    printf("{");
    for (int i = 0; i < size; i += 2) {
        if (i > 0) {
            printf(",");
        }
        char *k = value_string(vars[i]);
        char *v = value_string(vars[i+1]);
        printf(" \"%s\": \"%s\"", k+1, v);
        free(k);
        free(v);
    }
    printf(" }");
}

void print_method(struct context *ctx, int pc, int fp, uint64_t vars){
	int level = 0;
    while (pc > 0) {
        if (strcmp(code[pc].oi->name, "Return") == 0) {
			level++;
		}
        else if (strcmp(code[pc].oi->name, "Frame") == 0) {
			if (level == 0) {
				if (fp > 0) {
					int npc = ctx->stack[fp - 5] >> VALUE_BITS;
					uint64_t nvars = ctx->stack[fp - 2];
					int nfp = ctx->stack[fp - 1] >> VALUE_BITS;
					// printf("RECURS %d %d\n", fp, pc);
					print_method(ctx, npc, nfp, nvars);
				}
				printf("            {\n");
				const struct env_Frame *ef = code[pc].env;
				char *s = value_string(ef->name), *a = NULL;
				if (fp == 0) {
					if (ctx->sp > 1) {
						a = value_string(ctx->stack[1]);
					}
				}
				else {
					a = value_string(ctx->stack[fp - 3]);
				}
				if (a == NULL) {
					printf("              \"method\": \"%s()\",\n", s + 1);
				}
				else if (*a == '(') {
					printf("              \"method\": \"%s%s\",\n", s + 1, a);
				}
				else {
					printf("              \"method\": \"%s(%s)\",\n", s + 1, a);
				}
				free(s);
				free(a);
				printf("              \"vars\": ");
				print_vars(vars);
				printf(",\n");
				printf("            },\n");
				break;
			}
		}
		else {
			level--;
		}
        pc--;
    }
}

void print_context(uint64_t ctx, int tid, struct node *node){
    char *s, *a;

    printf("        {\n");
    printf("          \"tid\": \"%d\",\n", tid);

    struct context *c = value_get(ctx, NULL);

    s = value_string(c->name);
    a = value_string(c->arg);
    if (*a == '(') {
        printf("          \"name\": \"%s%s\",\n", s + 1, a);
    }
    else {
        printf("          \"name\": \"%s(%s)\",\n", s + 1, a);
    }
    free(s);
    free(a);

    // assert((c->entry & VALUE_MASK) == VALUE_PC);   TODO
    printf("          \"entry\": \"%d\",\n", (int) (c->entry >> VALUE_BITS));

    printf("          \"pc\": \"%d\",\n", c->pc);
    printf("          \"fp\": \"%d\",\n", c->fp);

    printf("          \"trace\": [\n");
    print_method(c, c->pc, c->fp, c->vars);
    printf("          ],\n");

    s = value_string(c->this);
    printf("          \"this\": \"%s\",\n", s);
    free(s);

    if (c->failure != 0) {
        s = value_string(c->failure);
        printf("          \"failure\": \"%s\",\n", s + 1);
        free(s);
    }

    if (c->trap_pc != 0) {
        s = value_string(c->trap_pc);
        a = value_string(c->trap_arg);
        if (*a == '(') {
            printf("          \"trap\": \"%s%s\",\n", s, a);
        }
        else {
            printf("          \"trap\": \"%s(%s)\",\n", s, a);
        }
        free(s);
    }

    if (c->interruptlevel) {
        printf("          \"interruptlevel\": \"True\",\n");
    }

    if (c->atomic != 0) {
        printf("          \"atomic\": \"%d\",\n", c->atomic);
    }
    if (c->readonly != 0) {
        printf("          \"readonly\": \"%d\",\n", c->readonly);
    }

    if (c->phase == CTX_END) {
        printf("          \"mode\": \"terminated\",\n");
    }
    else if (c->failure != 0) {
        printf("          \"mode\": \"failed\",\n");
    }
    else {
        struct edge *edge;
        for (edge = node->fwd; edge != NULL; edge = edge->next) {
            if (edge->ctx == ctx) {
                break;
            }
        };
        if (edge == NULL || edge->node != node) {
            printf("          \"mode\": \"running\",\n");
        }
        else {
            printf("          \"mode\": \"blocked\",\n");
        }
    }

    printf("          \"stack\": [\n");
    for (int i = 0; i < c->sp; i++) {
        s = value_string(c->stack[i]);
        printf("            \"%s\",\n", s);
        free(s);
    }
    printf("          ]\n");

    printf("        },\n");
}

void print_state(struct node *node){
    printf("      \"shared\": ");
    print_vars(node->state->vars);
    printf(",\n");

    printf("      \"contexts\": [\n");
    for (int i = 0; i < nprocesses; i++) {
        print_context(processes[i], i, node);
    }
    printf("      ]\n");
}

void diff_state(struct state *oldstate, struct state *newstate,
                struct context *oldctx, struct context *newctx,
                bool interrupt){
    printf("        {\n");
    if (newstate->vars != oldstate->vars) {
        printf("          \"shared\": ");
        print_vars(newstate->vars);
        printf(",\n");
    }
    if (interrupt) {
        printf("          \"interrupt\": \"True\",\n");
    }
    if (false && newstate->ctxbag != oldstate->ctxbag) {
        char *val = value_string(newstate->ctxbag);
        printf("NEW RUNNING CONTEXTS %s\n", val);
        free(val);
    }
    if (newctx->pc != oldctx->pc) {
        printf("          \"pc\": \"%d\",\n", newctx->pc);
    }
    if (newctx->fp != oldctx->fp) {
        printf("          \"fp\": \"%d\",\n", newctx->fp);
    }
    if (newctx->this != oldctx->this) {
        char *val = value_string(newctx->this);
        printf("          \"this\": \"%s\",\n", val);
        free(val);
    }
    if (newctx->vars != oldctx->vars) {
        printf("          \"local\": ");
        print_vars(newctx->vars);
        printf(",\n");
    }
    if (newctx->atomic != oldctx->atomic) {
        printf("          \"atomic\": \"%d\",\n", newctx->atomic);
    }
    if (newctx->readonly != oldctx->readonly) {
        printf("          \"readonly\": \"%d\",\n", newctx->readonly);
    }
    if (newctx->failure != 0) {
        char *val = value_string(newctx->failure);
        printf("          \"failure\": \"%s\",\n", val + 1);
        printf("          \"mode\": \"failed\",\n");
        free(val);
    }
    else if (newctx->phase == CTX_END) {
        printf("          \"mode\": \"terminated\",\n");
    }

    int common;
    for (common = 0; common < newctx->sp && common < oldctx->sp; common++) {
        if (newctx->stack[common] != oldctx->stack[common]) {
            break;
        }
    }
    if (common < oldctx->sp) {
        printf("          \"pop\": \"%d\",\n", oldctx->sp - common);
    }
    printf("          \"push\": [");
    for (int i = common; i < newctx->sp; i++) {
        if (i > common) {
            printf(",");
        }
        char *val = value_string(newctx->stack[i]);
        printf(" \"%s\"", val);
        free(val);
    }
    printf(" ]\n");
    printf("        },\n");
}

void diff_dump(struct state *oldstate, struct state *newstate,
                struct context **oldctx, struct context *newctx,
                bool interrupt){
    int newsize = sizeof(*newctx) + (newctx->sp * sizeof(uint64_t));

    if (memcmp(oldstate, newstate, sizeof(struct state)) == 0 &&
            (*oldctx)->sp == newctx->sp &&
            memcmp(*oldctx, newctx, newsize) == 0) {
        return;
    }

    // Keep track of old state and context for taking diffs
    diff_state(oldstate, newstate, *oldctx, newctx, interrupt);
    *oldstate = *newstate;
    free(*oldctx);
    *oldctx = malloc(newsize);
    memcpy(*oldctx, newctx, newsize);
}

// similar to onestep.  TODO.  Use flag to onestep?
uint64_t twostep(struct node *node, uint64_t ctx, uint64_t choice,
        bool interrupt, struct state *oldstate, struct context **oldctx){
    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    memcpy(sc, node->state, sizeof(*sc));
    sc->choosing = 0;

    // Make a copy of the context
    struct context *cc = value_copy(ctx, NULL);
    diff_dump(oldstate, sc, oldctx, cc, node->interrupt);
    if (cc->phase == CTX_END || cc->failure != 0) {
        free(cc);
        return ctx;
    }

    bool choosing = false;
    struct dict *infloop = NULL;        // infinite loop detector
    for (int loopcnt = 0;; loopcnt++) {
        int pc = cc->pc;

        struct op_info *oi = code[pc].oi;
        if (code[pc].choose) {
            char *p = value_string(choice);
            // printf("--- %d: CHOOSE %s\n", pc, p);
            free(p);
            cc->stack[cc->sp - 1] = choice;
            cc->pc++;
        }
        else {
            // printf("--- %d: %s\n", pc, oi->name);
            if (code[pc].breakable) {
                cc->phase = CTX_MIDDLE;
            }
            (*oi->op)(code[pc].env, sc, &cc);
        }

        if (cc->phase != CTX_END && cc->failure == 0) {
            if (infloop == NULL) {
                infloop = dict_new(0);
            }
            // TODO.  Also add global state?
            void **p = dict_insert(infloop, cc,
                            sizeof(*cc) + (cc->sp * sizeof(uint64_t)));
            if (*p != (void *) 0) {
                cc->failure = value_put_atom("infinite loop", 13);
            }
            *p = (void *) 1;
        }

        diff_dump(oldstate, sc, oldctx, cc, false);
        if (cc->phase == CTX_END || cc->failure != 0) {
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
            uint64_t s = cc->stack[cc->sp - 1];
            assert((s & VALUE_MASK) == VALUE_SET);
            int size;
            uint64_t *vals = value_get(s, &size);
            size /= sizeof(uint64_t);
            assert(size > 0);
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

    if (false && cc->failure != 0) {
        char *r = value_string(cc->failure);
        printf("Safety violation: %s\n", r + 1);
        free(r);
    }

    ctx = value_put_context(cc);

    free(sc);
    free(cc);

    return ctx;
}

void path_dump(struct node *last, uint64_t ctx, uint64_t choice,
                struct state *oldstate, struct context **oldctx){
    if (last == NULL) {
        return;
    }
    path_dump(last->parent, last->before, last->choice, oldstate, oldctx);


    /* Match each context to a process.
     */
    bool *matched = calloc(nprocesses, sizeof(bool));
    int nctxs;
    uint64_t *ctxs = value_get(last->state->ctxbag, &nctxs);
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

    /* See if we can find this context in the list of processes.  If not
     * add it.
     */
    int pid;
    for (pid = 0; pid < nprocesses; pid++) {
        if (processes[pid] == ctx) {
            break;
        }
    }
    assert(pid < nprocesses);

    bool interrupt = false;
    if (last->parent == NULL || last->after != ctx || last->interrupt) {
        if (last->parent != NULL) {
            printf("      ],\n");
            print_state(last);
            printf("    },\n");
        }

        interrupt = last->interrupt;
        struct context *context = value_get(ctx, NULL);
        assert(context->phase != CTX_END);
        char *name = value_string(context->name);
        char *arg = value_string(context->arg);
        // char *c = value_string(choice);
        printf("    \"switch\": {\n");
        printf("      \"tid\": \"%d\",\n", pid);
        if (*arg == '(') {
            printf("      \"name\": \"%s%s\",\n", name + 1, arg);
        }
        else {
            printf("      \"name\": \"%s(%s)\",\n", name + 1, arg);
        }
        // printf("      \"choice\": \"%s\",\n", c);
        printf("      \"microsteps\": [\n");
        free(name);
        free(arg);
        // free(c);
        memset(*oldctx, 0, sizeof(**oldctx));
    }

    // Recreate the steps
    processes[pid] = twostep(last, ctx, choice, interrupt, oldstate, oldctx);
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

int main(int argc, char **argv){
    printf("Charm v1\n");

    failures = queue_init();

    // initialize modules
    ops_init();
    value_init();

    // open the file
    FILE *fp = fopen(argc == 1 ? "harmony.json" : argv[1], "r");
    assert(fp != NULL);

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
    struct context init_ctx;
    memset(&init_ctx, 0, sizeof(init_ctx));
    uint64_t nv = value_put_atom("name", 4);
    uint64_t tv = value_put_atom("tag", 3);
    init_ctx.name = value_put_atom("__init__", 8);
    init_ctx.arg = VALUE_DICT;
    init_ctx.this = VALUE_DICT;
    init_ctx.vars = VALUE_DICT;
    init_ctx.atomic = 1;
    struct state *state = new_alloc(struct state);
    state->vars = VALUE_DICT;
    uint64_t ictx = value_put_context(&init_ctx);
    state->ctxbag = dict_store(VALUE_DICT, ictx, (1 << VALUE_BITS) | VALUE_INT);
    state->invariants = VALUE_SET;

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
                onestep(node, state->choosing, vals[i], false, visited, todo, &inv_ctx);
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
                onestep(node, ctxs[i], 0, false, visited, todo, &inv_ctx);
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
            if (node->state->ctxbag == VALUE_DICT) {
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
                f->ctx = node->after;
                f->choice = 0;          // TODO
                f->node = node;
                queue_enqueue(failures, f);
            }
        }

        printf("%d components, %d bad nodes\n", ncomponents, nbad);
    }

    if (queue_empty(failures)) {
        printf("no issues\n");
        exit(0);
    }

    struct failure *bad = NULL;
    while (queue_dequeue(failures, &next)) {
        struct failure *f = next;

        if (bad == NULL || f->node->len < bad->node->len) {
            bad = f;
        }
    }

    printf("{\n");

    switch (bad->type) {
    case FAIL_SAFETY:
        printf("  \"issue\": \"Safety violation\",\n");
        break;
    case FAIL_INVARIANT:
        printf("  \"issue\": \"Invariant violation\",\n");
        break;
    case FAIL_TERMINATION:
        printf("  \"issue\": \"Non-terminating state\",\n");
        break;
    default:
        assert(0);
    }

    printf("  \"megasteps\": [\n");
    struct state oldstate;
	memset(&oldstate, 0, sizeof(oldstate));
    struct context *oldctx = calloc(1, sizeof(*oldctx));
    path_dump(bad->node, bad->ctx, bad->choice, &oldstate, &oldctx);
    free(oldctx);
    printf("      ],\n");
    print_state(bad->node);
    printf("    },\n");
    printf("  ]\n");
    printf("}\n");

    return 0;
}
