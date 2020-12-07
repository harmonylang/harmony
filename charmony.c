#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "json.h"
#include "global.h"

#define CHUNKSIZE   (1 << 12)

struct code *code;
int code_len;

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

struct node *onestep(struct node *node, uint64_t ctx, uint64_t choice,
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
    else if (false) {
        printf("TERMINATED\n");
    }

    // See if this new state was already seen before.
    void **p = map_insert(pvisited, sc, sizeof(*sc));
    struct node *next;
    if ((next = *p) == NULL) {
        *p = next = new_alloc(struct node);
        next->parent = node;
        next->state = sc;               // TODO: duplicate value
        next->before = ctx;
        next->after = after;
        next->choice = choice;
        next->failure = cc->failure;
        if (sc->ctxbag != VALUE_DICT) {
            queue_enqueue(todo, next);
        }
    }
    else {
        assert(!cc->failure);
        assert(!next->failure);
        free(sc);
    }

    free(cc);
    return next;
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

int main(){
    printf("Hello World\n");

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
    void **p = map_insert(&visited, state, sizeof(*state));
    assert(*p == NULL);
    *p = node;

    // Put the initial state on the queue
    struct queue *todo = queue_init();
    queue_enqueue(todo, node);

    void *next;
    int state_counter = 0;
    struct node *last = NULL;
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
                last = onestep(node, state->choosing, vals[i], &visited, todo);
                if (false) {
                    printf("NEXT CHOICE DONE\n");
                }
                if (last->failure) {
                    break;
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
                last = onestep(node, ctxs[i], 0, &visited, todo);
                if (last->failure) {
                    break;
                }
                if (false) {
                    printf("NEXT CONTEXT DONE\n");
                }
            }
        }
        if (last->failure) {
            break;
        }
    }

    assert(last != NULL);
    printf("#states %d %d\n", state_counter, last->failure);

    while (last != NULL) {
        char *before = value_string(last->before);
        char *after = value_string(last->after);
        char *choice = value_string(last->choice);
        char *vars = value_string(last->state->vars);
        printf(">> before: %s after: %s choice: %s var: %s\n",
            before, after, choice, vars);
        free(before);
        free(after);
        free(choice);
        free(vars);
        last = last->parent;
    }

    return 0;
}
