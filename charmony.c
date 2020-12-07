#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "json.h"
#include "global.h"

#define CHUNKSIZE   (1 << 12)

struct edge {
    struct edge *next;
    uint64_t ctx, choice;
    struct node *node;
    int weight;
};

struct node {
    struct node *parent;
    struct state *state;
    int id;                 // starting from 0
    uint64_t before;        // context before state change
    uint64_t after;         // context after state change
    uint64_t choice;        // choice made if any
    int len;                // length of path to initial state
    struct edge *fwd;       // forward edges
    struct edge *bwd;       // backward edges
    bool visited;           // for Kosaraju algorithm
};

struct failure {
    struct node *node;      // starting state
    uint64_t ctx;           // context that failed (before it failed)
    uint64_t choice;        // choice if any
};

struct code *code;
int code_len;

static struct node **graph;        // vector of all nodes
static int graph_size;             // to create node identifiers
static int graph_alloc;            // size allocated
static struct queue *failures;     // queue of "struct failure"

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
    struct json_value *op = map_lookup(jv->u.map, "op", 2);
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

void onestep(struct node *node, uint64_t ctx, uint64_t choice,
        struct map **pvisited, struct queue *todo){
    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    memcpy(sc, node->state, sizeof(*sc));
    sc->choosing = 0;

    if (false) {
        printf("ONESTEP %llx %llx\n", ctx, sc->ctxbag);
    }

    // Make a copy of the context
    struct context *cc = value_copy(ctx, NULL);
    assert(!cc->terminated);
    assert(!cc->failure);

    bool choosing = false;
    for (int loopcnt = 0;; loopcnt++) {
        int pc = cc->pc;

        if (false) {
            char *p = value_string(sc->vars);
            char *q = value_string(sc->ctxbag);
            printf("%d -> %s %s %s\n", pc, code[pc].oi->name, p, q);
            free(p);
            free(q);
        }

        struct op_info *oi = code[pc].oi;

        if (code[pc].choose) {
            cc->stack[cc->sp - 1] = choice;
            cc->pc++;
        }
        else {
            (*oi->op)(code[pc].env, sc, &cc);
            if (cc->terminated || cc->failure) {
                break;
            }
            if (cc->pc == pc) {
                fprintf(stderr, ">>> %s\n", oi->name);
            }
            assert(cc->pc != pc);
        }

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
            assert(size > 1);       // TODO
            choosing = true;
            break;
        }

        if (cc->atomic == 0 && sc->ctxbag != VALUE_DICT &&
                code[cc->pc].breakable) {
            break;
        }
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
        assert(!cc->terminated);
        sc->choosing = after;
    }

    // Add new context to state unless it's terminated
    if (!cc->terminated) {
        sc->ctxbag = bag_add(sc->ctxbag, after);
    }

    // Weight of this step
    int weight = ctx == node->after ? 0 : 1;

    // See if this new state was already seen before.
    void **p = map_insert(pvisited, sc, sizeof(*sc));
    struct node *next;
    if ((next = *p) == NULL) {
        *p = next = new_alloc(struct node);
        next->parent = node;
        next->state = sc;               // TODO: duplicate value
        next->before = ctx;
        next->choice = choice;
        next->after = after;
        next->len = node->len + weight;
        graph_add(next);

        if (sc->ctxbag != VALUE_DICT && !cc->failure &&
                queue_empty(failures)) {
            if (weight == 0) {
                queue_prepend(todo, next);
            }
            else {
                queue_enqueue(todo, next);
            }
        }
    }
    else {
        free(sc);

        if (next->len > node->len + weight) {
            next->before = ctx;
            next->after = after;
            next->choice = choice;
            next->len = node->len + weight;
        }
    }

    // Add a forward edge from node to next.
    struct edge *fwd = new_alloc(struct edge);
    fwd->ctx = ctx;
    fwd->choice = choice;
    fwd->node = next;
    fwd->weight = weight;
    fwd->next = node->fwd;
    node->fwd = fwd;

    // Add a backward edge from next to node.
    struct edge *bwd = new_alloc(struct edge);
    bwd->ctx = ctx;
    bwd->choice = choice;
    bwd->node = node;
    bwd->weight = weight;
    bwd->next = next->bwd;
    next->bwd = bwd;

    if (cc->failure) {
        struct failure *f = new_alloc(struct failure);
        f->ctx = ctx;
        f->choice = choice;
        f->node = node;
        queue_enqueue(failures, f);
    }

    free(cc);
}

// similar to onestep.  TODO.  Use flag to onestep?
void twostep(struct node *node, uint64_t ctx, uint64_t choice){
    // Make a copy of the state
    struct state *sc = new_alloc(struct state);
    memcpy(sc, node->state, sizeof(*sc));
    sc->choosing = 0;

    // Make a copy of the context
    struct context *cc = value_copy(ctx, NULL);
    assert(!cc->terminated);
    assert(!cc->failure);

    bool choosing = false;
    for (int loopcnt = 0;; loopcnt++) {
        int pc = cc->pc;

        struct op_info *oi = code[pc].oi;
        if (code[pc].choose) {
            char *p = value_string(choice);
            printf("--- %d: CHOOSE %s\n", pc, p);
            free(p);
            cc->stack[cc->sp - 1] = choice;
            cc->pc++;
        }
        else {
            printf("--- %d: %s\n", pc, oi->name);
            (*oi->op)(code[pc].env, sc, &cc);
            if (cc->terminated || cc->failure) {
                break;
            }
            if (cc->pc == pc) {
                fprintf(stderr, ">>> %s\n", oi->name);
            }
            assert(cc->pc != pc);
        }

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
            assert(size > 1);       // TODO
            choosing = true;
            break;
        }

        if (cc->atomic == 0 && sc->ctxbag != VALUE_DICT &&
                code[cc->pc].breakable) {
            break;
        }
    }

    free(sc);
    free(cc);
}

void label_upcall(void *env,
        const void *key, unsigned int key_size, void *value){
    uint64_t *labels = env;
    struct json_value *jv = value;

    assert(jv->type == JV_ATOM);
    char *copy = malloc(jv->u.atom.len + 1);
    strncpy(copy, jv->u.atom.base, jv->u.atom.len);
    copy[jv->u.atom.len] = 0;
    int64_t pc = atoi(copy);
    free(copy);
    printf("LABEL %.*s: %lld\n", key_size, key, pc);
    uint64_t k = value_put_atom(key, key_size);
    uint64_t v = (pc << VALUE_BITS) | VALUE_INT;
    *labels = dict_store(*labels, k, v);
}

void path_dump(struct node *last, uint64_t ctx, uint64_t choice){
    if (last == NULL) {
        return;
    }

    path_dump(last->parent, last->before, last->choice);

    char *before = value_string(ctx);
    char *c = value_string(choice);
    char *vars = value_string(last->state->vars);
    printf(">> before: %s choice: %s var: %s\n",
            before, c, vars);
    free(before);
    free(c);
    free(vars);

    twostep(last, ctx, choice);
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

static void kosaraju_assign(struct node *node){
    if (node->visited) {
        return;
    }
    node->visited = true;
    printf(" %d", node->id);
    for (struct edge *edge = node->bwd; edge != NULL; edge = edge->next) {
        kosaraju_assign(edge->node);
    }
}

static void find_scc(void){
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
            printf("SCC %d:", ++count); fflush(stdout);
            kosaraju_assign(next);
            printf(" //\n");
        }
    }
    for (int i = 0; i < graph_size; i++) {
        assert(graph[i]->visited);
    }

    printf("%d nodes, %d components\n", graph_size, count);
}

int main(){
    printf("Hello World\n");

    failures = queue_init();

    // initialize modules
    ops_init();
    value_init();

    // open the file
    FILE *fp = fopen("x.json", "r");
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

    // extract the labels
    struct json_value *labels = map_lookup(jv->u.map, "labels", 6);
    assert(labels->type == JV_MAP);
    uint64_t label_map = VALUE_DICT;
    map_iter(&label_map, labels->u.map, label_upcall);

    // travel through the json code contents to create the code array
    struct json_value *jc = map_lookup(jv->u.map, "code", 4);
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
    uint64_t name = value_put_atom("__init__", 8);
    init_ctx.nametag = dict_store(VALUE_DICT, nv, name);
    init_ctx.nametag = dict_store(init_ctx.nametag, tv, VALUE_DICT);
    init_ctx.vars = VALUE_DICT;
    init_ctx.atomic = 1;
    struct state *state = new_alloc(struct state);
    state->vars = VALUE_DICT;
    state->labels = label_map;
    state->ctxbag = dict_store(VALUE_DICT, 
            value_put_context(&init_ctx), (1 << VALUE_BITS) | VALUE_INT);

    // Put the initial state in the visited map
    struct map *visited = map_init();
    struct node *node = new_alloc(struct node);
    node->state = state;
    graph_add(node);
    void **p = map_insert(&visited, state, sizeof(*state));
    assert(*p == NULL);
    *p = node;

    // Put the initial state on the queue
    struct queue *todo = queue_init();
    queue_enqueue(todo, node);

    void *next;
    int state_counter = 1;
    while (queue_dequeue(todo, &next)) {
        state_counter++;

        node = next;
        state = node->state;

        if (state->choosing != 0) {
            assert((state->choosing & VALUE_MASK) == VALUE_CONTEXT);
            if (false) {
                printf("CHOOSING %llx\n", state->choosing);
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
                    printf("NEXT CHOICE %d %d %llx\n", i, size, vals[i]);
                }
                onestep(node, state->choosing, vals[i], &visited, todo);
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
                    printf("NEXT CONTEXT %d %llx\n", i, ctxs[i]);
                }
                assert((ctxs[i] & VALUE_MASK) == VALUE_CONTEXT);
                assert((ctxs[i+1] & VALUE_MASK) == VALUE_INT);
                onestep(node, ctxs[i], 0, &visited, todo);
                if (false) {
                    printf("NEXT CONTEXT DONE\n");
                }
            }
        }
    }

    printf("#states %d (%d)\n", state_counter, graph_size);

    find_scc();     // find the strongly connected components

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

    path_dump(bad->node, bad->ctx, bad->choice);

    return 0;
}
