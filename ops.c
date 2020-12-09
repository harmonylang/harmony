#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <ctype.h>
#include <assert.h>
#include "global.h"
#include "json.h"

#define MAX_ARITY   10

#define CALLTYPE_PROCESS       1
#define CALLTYPE_NORMAL        2

struct val_info {
    int size;
    uint64_t *vals;
};

struct f_info {
    char *name;
    uint64_t (*f)(struct state *state, struct context **pctx, uint64_t *args, int n);
};

struct var_tree {
    enum { VT_NAME, VT_TUPLE } type;
    union {
        uint64_t name;
        struct {
            int n;
            struct var_tree **elements;
        } tuple;
    } u;
};

static struct map *ops_map, *f_map;

struct env_DelVar {
    uint64_t name;
};

struct env_Frame {
    uint64_t name;
    struct var_tree *args;
};

struct env_Jump {
    int pc;
};

struct env_JumpCond {
    uint64_t cond;
    int pc;
};

struct env_Load {
    uint64_t *indices;
    int n;
};

struct env_LoadVar {
    uint64_t name;
};

struct env_Nary {
    int arity;
    struct f_info *fi;
};

struct env_Push {
    uint64_t value;
};

struct env_Store {
    uint64_t *indices;
    int n;
};

struct env_StoreVar {
    struct var_tree *args;
};

uint64_t var_match(struct var_tree *vt, uint64_t arg, uint64_t vars){
    switch (vt->type) {
    case VT_NAME:
        return dict_store(vars, vt->u.name, arg);
    case VT_TUPLE:
        assert((arg & VALUE_MASK) == VALUE_DICT);
        if (arg == VALUE_DICT) {
            assert(vt->u.tuple.n == 0);
            return vars;
        }
        assert(vt->u.tuple.n > 0);
        int size;
        uint64_t *vals = value_get(arg, &size);
        size /= 2 * sizeof(uint64_t);
        assert(vt->u.tuple.n == size);
        for (int i = 0; i < size; i++) {
            assert(vals[2*i] == ((i << VALUE_BITS) | VALUE_INT));
            vars = var_match(vt->u.tuple.elements[i], vals[2*i+1], vars);
        }
        return vars;
    default:
        assert(0);
    }
}

void var_dump(struct var_tree *vt){
    switch (vt->type) {
    case VT_NAME:
        printf("%llx", vt->u.name);
        break;
    case VT_TUPLE:
        printf("(");
        for (int i = 0; i < vt->u.tuple.n; i++) {
            printf(" ");
            var_dump(vt->u.tuple.elements[i]);
        }
        printf(" )");
        break;
    default:
        assert(0);
    }
}

static void skip_blanks(char *s, int len, int *index){
    while (*index < len && s[*index] == ' ') {
        (*index)++;
    }
}

struct var_tree *var_parse(char *s, int len, int *index){
    assert(*index < len);
    struct var_tree *vt = new_alloc(struct var_tree);

    skip_blanks(s, len, index);
    if (s[*index] == '(') {
        vt->type = VT_TUPLE;
        (*index)++;
        skip_blanks(s, len, index);
        assert(*index < len);
        if (s[*index] == ')') {
            (*index)++;
        }
        else {
            while (true) {
                struct var_tree *elt = var_parse(s, len, index);
                vt->u.tuple.elements = realloc(vt->u.tuple.elements,
                        (vt->u.tuple.n + 1) * sizeof(elt));
                vt->u.tuple.elements[vt->u.tuple.n++] = elt;
                skip_blanks(s, len, index);
                assert(*index < len);
                if (s[*index] == ')') {
                    (*index)++;
                    break;
                }
                assert(s[*index] == ',');
                (*index)++;
            }
        }
    }
    else {
        vt->type = VT_NAME;
        int i = *index;
        assert(isalpha(s[i]) || s[i] == '_');
        i++;
        while (i < len && (isalpha(s[i]) || s[i] == '_' || isdigit(s[i]))) {
            i++;
        }
        vt->u.name = value_put_atom(&s[*index], i - *index);
        *index = i;
    }
    return vt;
}

void ctx_push(struct context **pctx, uint64_t v){
    struct context *ctx = realloc(*pctx, sizeof(struct context) + 
                ((*pctx)->sp + 1) * sizeof(uint64_t));

    ctx->stack[ctx->sp++] = v;
    *pctx = ctx;
}

uint64_t ctx_pop(struct context **pctx){
    struct context *ctx = *pctx;

    assert(ctx->sp > 0);
    return ctx->stack[--ctx->sp];
}

uint64_t dict_load(uint64_t dict, uint64_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        assert(size % 2 == 0);
        size /= sizeof(uint64_t);
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            return vals[i + 1];
        }
        /* 
            if (value_cmp(vals[i], key) > 0) {
                break;
            }
        */
    }

    assert(0);
}

uint64_t dict_remove(uint64_t dict, uint64_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        assert(0);
    }
    vals = value_get(dict & ~VALUE_MASK, &size);
    size /= sizeof(uint64_t);
    assert(size % 2 == 0);

    if (size == 2) {
        assert(vals[0] == key);
        return VALUE_DICT;
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            int n = (size - 2) * sizeof(uint64_t);
            uint64_t *copy = malloc(n);
            memcpy(copy, vals, i * sizeof(uint64_t));
            memcpy(&copy[i], &vals[i+2],
                (size - i - 2) * sizeof(uint64_t));
            uint64_t v = value_put_dict(copy, n);
            free(copy);
            return v;
        }
        /* 
            if (value_cmp(vals[i], key) > 0) {
                assert(0);
            }
        */
    }

    if (false) {
        char *p = value_string(key);
        char *q = value_string(dict);
        fprintf(stderr, "DICT_REMOVE: '%s' from %s\n", p, q);
        assert(0);
    }

    return dict;
}

bool dict_tryload(uint64_t dict, uint64_t key, uint64_t *result){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(uint64_t);
        assert(size % 2 == 0);
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            *result = vals[i + 1];
            return true;
        }
        /* 
            if (value_cmp(vals[i], key) > 0) {
                break;
            }
        */
    }
    return false;
}

// Store key:value in the given dictionary and returns its value code
uint64_t dict_store(uint64_t dict, uint64_t key, uint64_t value){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    if (false) {
        char *p = value_string(value);
        char *q = value_string(dict);
        char *r = value_string(key);
        printf("DICT_STORE %s %s %s\n", p, q, r);
        free(p);
        free(q);
        free(r);
    }

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(uint64_t);
        assert(size % 2 == 0);
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            if (vals[i + 1] == value) {
                return dict;
            }
            int n = size * sizeof(uint64_t);
            uint64_t *copy = malloc(n);
            memcpy(copy, vals, n);
            copy[i + 1] = value;
            uint64_t v = value_put_dict(copy, n);
            free(copy);
            return v;
        }
        if (value_cmp(vals[i], key) > 0) {
            break;
        }
    }

    int n = (size + 2) * sizeof(uint64_t);
    uint64_t *nvals = malloc(n);
    memcpy(nvals, vals, i * sizeof(uint64_t));
    nvals[i] = key;
    nvals[i+1] = value;
    memcpy(&nvals[i+2], &vals[i], (size - i) * sizeof(uint64_t));
    uint64_t v = value_put_dict(nvals, n);
    free(nvals);
    return v;
}

uint64_t ind_load(uint64_t dict, uint64_t *indices, int n){
    uint64_t d = dict;
    for (int i = 0; i < n; i++) {
        d = dict_load(d, indices[i]);
    }
    return d;
}

uint64_t ind_store(uint64_t dict, uint64_t *indices, int n, uint64_t value){
    assert((dict & VALUE_MASK) == VALUE_DICT);
    assert(n > 0);

    if (n == 1) {
        return dict_store(dict, indices[0], value);
    }
    else {
        uint64_t *vals;
        int size;
        if (dict == VALUE_DICT) {
            vals = NULL;
            size = 0;
        }
        else {
            vals = value_get(dict & ~VALUE_MASK, &size);
            assert(size % 2 == 0);
            size /= sizeof(uint64_t);
        }

        int i;
        for (i = 0; i < size; i += 2) {
            if (vals[i] == indices[0]) {
                uint64_t d = vals[i+1];
                assert((d & VALUE_MASK) == VALUE_DICT);
                uint64_t nd = ind_store(d, indices + 1, n - 1, value);
                if (d == nd) {
                    return dict;
                }
                int n = size * sizeof(uint64_t);
                uint64_t *copy = malloc(n);
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                uint64_t v = value_put_dict(copy, n);
                free(copy);
                return v;
            }
            /* 
                if (value_cmp(vals[i], key) > 0) {
                    assert(0);
                }
            */
        }

        assert(0);
    }
}

void op_Assert2(const void *env, struct state *state, struct context **pctx){}
void op_Del(const void *env, struct state *state, struct context **pctx){}

void op_Address(const void *env, struct state *state, struct context **pctx){
    uint64_t index = ctx_pop(pctx);
    uint64_t av = ctx_pop(pctx);
    assert((av & VALUE_MASK) == VALUE_ADDRESS);
    if (false) {
        printf("ADDRESS %llx\n", index);
    }

    int size;
    uint64_t *indices = value_copy(av, &size);
    indices = realloc(indices, size + sizeof(index));
    indices[size / sizeof(uint64_t)] = index;
    ctx_push(pctx, value_put_address(indices, size + sizeof(index)));
    free(indices);
    (*pctx)->pc++;
}

void op_Apply(const void *env, struct state *state, struct context **pctx){
    uint64_t method = ctx_pop(pctx);
    uint64_t e = ctx_pop(pctx);

    uint64_t type = method & VALUE_MASK;
    switch (type) {
    case VALUE_DICT:
        ctx_push(pctx, dict_load(method, e));
        (*pctx)->pc++;
        return;
    case VALUE_PC:
        ctx_push(pctx, (((*pctx)->pc + 1) << VALUE_BITS) | VALUE_PC);
        ctx_push(pctx, (CALLTYPE_NORMAL << VALUE_BITS) | VALUE_INT);
        ctx_push(pctx, e);
        assert((method >> VALUE_BITS) != (*pctx)->pc);
        (*pctx)->pc = method >> VALUE_BITS;
        return;
    default:
        assert(0);
    }
}

void op_Assert(const void *env, struct state *state, struct context **pctx){
    uint64_t v = ctx_pop(pctx);
    assert((v & VALUE_MASK) == VALUE_BOOL);
    if (false) {
        printf("ASSERT %lld\n", v >> VALUE_BITS);
    }
    if (v == VALUE_BOOL) {
        printf("HARMONY ASSERTION FAILED\n");
        (*pctx)->failure = true;
    }
    (*pctx)->pc++;
}

void op_AtomicDec(const void *env, struct state *state, struct context **pctx){
    struct context *ctx = *pctx;

    assert(ctx->atomic > 0);
    ctx->atomic--;
    ctx->pc++;
}

void op_AtomicInc(const void *env, struct state *state, struct context **pctx){
    struct context *ctx = *pctx;

    ctx->atomic++;
    ctx->pc++;
}

void op_Choose(const void *env, struct state *state, struct context **pctx){
#ifdef notdef
    uint64_t s = ctx_pop(pctx);
    assert((s & VALUE_MASK) == VALUE_SET);
    void *p = (void *) (s & ~VALUE_MASK);

    int size;
    uint64_t *vals = map_retrieve(p, &size);
    size /= sizeof(uint64_t);
    assert(size > 0);

    printf("CHOOSE %llx %llx %d\n", vals[0], vals[1], size);

    ctx_push(pctx, vals[0]);
    (*pctx)->pc++;
#endif
    assert(0);
}

void op_Cut(const void *env, struct state *state, struct context **pctx){
    uint64_t v = ctx_pop(pctx);
    if ((v & VALUE_MASK) == VALUE_SET) {
        assert(v != VALUE_SET);
        void *p = (void *) (v & ~VALUE_MASK);

        int size;
        uint64_t *vals = map_retrieve(p, &size);
        assert(size > 0);

        ctx_push(pctx, vals[0]);
        ctx_push(pctx, value_put_set(&vals[1], size - sizeof(uint64_t)));
        (*pctx)->pc++;
        return;
    }
    if ((v & VALUE_MASK) == VALUE_DICT) {
        assert(v != VALUE_DICT);
        assert(0);
        return;
    }
    assert(0);
}

void op_DelVar(const void *env, struct state *state, struct context **pctx){
    const struct env_DelVar *ed = env;
    if (false) {
        char *p = value_string(ed->name);
        char *q = value_string((*pctx)->vars);
        printf("DELVAR %s %s\n", p, q);
        free(p);
        free(q);
    }

    (*pctx)->vars = dict_remove((*pctx)->vars, ed->name);
    (*pctx)->pc++;
}

void op_Dict(const void *env, struct state *state, struct context **pctx){
    uint64_t n = ctx_pop(pctx);
    assert((n & VALUE_MASK) == VALUE_INT);
    if (false) {
        printf("DICT %lld\n", n >> VALUE_BITS);
    }
    n >>= VALUE_BITS;

    uint64_t d = VALUE_DICT;
    for (int i = 0; i < n; i++) {
        uint64_t v = ctx_pop(pctx);
        uint64_t k = ctx_pop(pctx);
        d = dict_store(d, k, v);
    }
    ctx_push(pctx, d);
    (*pctx)->pc++;
}

void op_Dup(const void *env, struct state *state, struct context **pctx){
    uint64_t v = ctx_pop(pctx);

    if (false) {
        char *p = value_string(v);
        printf("DUP %s\n", p);
        free(p);
    }

    ctx_push(pctx, v);
    ctx_push(pctx, v);
    (*pctx)->pc++;
}

void op_Frame(const void *env, struct state *state, struct context **pctx){
    const struct env_Frame *ef = env;
    if (false) {
        printf("FRAME %llx ", ef->name);
        var_dump(ef->args);
        printf("\n");
    }

    uint64_t arg = ctx_pop(pctx);
    ctx_push(pctx, arg);
    ctx_push(pctx, (*pctx)->vars);
    ctx_push(pctx, ((*pctx)->fp << VALUE_BITS) | VALUE_INT);

    struct context *ctx = *pctx;
    ctx->fp = ctx->sp;

    ctx->vars = dict_store(VALUE_DICT,
        value_put_atom("result", 6), VALUE_DICT);       // TODO "result" atom

    ctx->vars = var_match(ef->args, arg, ctx->vars);

    ctx->pc += 1;
}

void op_Jump(const void *env, struct state *state, struct context **pctx){
    const struct env_Jump *ej = env;

    if (false) {
        printf("JUMP %d\n", ej->pc);
    }
    (*pctx)->pc = ej->pc;
}

void op_JumpCond(const void *env, struct state *state, struct context **pctx){
    const struct env_JumpCond *ej = env;

    if (false) {
        printf("JUMPCOND %d\n", ej->pc);
    }
    uint64_t v = ctx_pop(pctx);
    if (v == ej->cond) {
        assert((*pctx)->pc != ej->pc);
        (*pctx)->pc = ej->pc;
    }
    else {
        (*pctx)->pc++;
    }
}

void op_Load(const void *env, struct state *state, struct context **pctx){
    const struct env_Load *el = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    if (el == 0) {
        uint64_t av = ctx_pop(pctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);

        if (false) {
            printf("LOAD IND %d\n", size);
            for (int i = 0; i < size; i++) {
                char *index = value_string(indices[i]);
                printf(">> %s\n", index);
                free(index);
            }
        }

        ctx_push(pctx, ind_load(state->vars, indices, size));
    }
    else {
        assert(el->n == 1);
        ctx_push(pctx, dict_load(state->vars, el->indices[0]));
    }
    (*pctx)->pc++;
}

void op_LoadVar(const void *env, struct state *state, struct context **pctx){
    const struct env_LoadVar *el = env;
    assert(el != NULL);
    assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);
    ctx_push(pctx, dict_load((*pctx)->vars, el->name));
    (*pctx)->pc++;
}

void op_Nary(const void *env, struct state *state, struct context **pctx){
    const struct env_Nary *en = env;
    uint64_t args[MAX_ARITY];

    for (int i = 0; i < en->arity; i++) {
        args[i] = ctx_pop(pctx);
    }
    ctx_push(pctx, (*en->fi->f)(state, pctx, args, en->arity));
    (*pctx)->pc++;
}

void op_Pop(const void *env, struct state *state, struct context **pctx){
    (void) ctx_pop(pctx);
    (*pctx)->pc++;
}

void op_Push(const void *env, struct state *state, struct context **pctx){
    const struct env_Push *ep = env;

    if (false) {
        char *p = value_string(ep->value);
        printf("PUSH %s\n", p);
        free(p);
    }

    ctx_push(pctx, ep->value);
    (*pctx)->pc++;
}

void op_ReadonlyDec(const void *env, struct state *state, struct context **pctx){
    struct context *ctx = *pctx;

    assert(ctx->readonly > 0);
    ctx->readonly--;
    ctx->pc++;
}

void op_ReadonlyInc(const void *env, struct state *state, struct context **pctx){
    struct context *ctx = *pctx;

    ctx->readonly++;
    ctx->pc++;
}

void op_Return(const void *env, struct state *state, struct context **pctx){
    if ((*pctx)->sp == 0) {     // __init__
        (*pctx)->terminated = true;
        if (false) {
            printf("RETURN INIT\n");
        }
    }
    else {
        uint64_t result = dict_load((*pctx)->vars, value_put_atom("result", 6));
        uint64_t fp = ctx_pop(pctx);
        assert((fp & VALUE_MASK) == VALUE_INT);
        (*pctx)->fp = fp >> VALUE_BITS;
        (*pctx)->vars = ctx_pop(pctx);
        assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);
        (void) ctx_pop(pctx);   // argument saved for stack trace
        uint64_t calltype = ctx_pop(pctx);
        assert((calltype & VALUE_MASK) == VALUE_INT);
        switch (calltype >> VALUE_BITS) {
        case CALLTYPE_PROCESS:
            (*pctx)->terminated = true;
            break;
        case CALLTYPE_NORMAL:
            {
                uint64_t pc = ctx_pop(pctx);
                assert((pc & VALUE_MASK) == VALUE_PC);
                pc >>= VALUE_BITS;
                assert(pc != (*pctx)->pc);
                ctx_push(pctx, result);
                (*pctx)->pc = pc;
            }
            break;
        default:
            assert(0);
        }
    }
}

void op_Set(const void *env, struct state *state, struct context **pctx){
    uint64_t n = ctx_pop(pctx);
    assert((n & VALUE_MASK) == VALUE_INT);
    n >>= VALUE_BITS;

    uint64_t *v = malloc(n * sizeof(uint64_t));
    for (int i = 0; i < n; i++) {
        v[i] = ctx_pop(pctx);
    }

    // TODO.  NEED TO SORT THE SET
    assert(0);

    ctx_push(pctx, value_put_set(v, n * sizeof(uint64_t)));
    free(v);
    (*pctx)->pc++;
}

uint64_t bag_add(uint64_t bag, uint64_t v){
    uint64_t count;
    if (dict_tryload(bag, v, &count)) {
        assert((count & VALUE_MASK) == VALUE_INT);
        assert(count != VALUE_INT);
        count += 1 << VALUE_BITS;
        return dict_store(bag, v, count);
    }
    else {
        return dict_store(bag, v, (1 << VALUE_BITS) | VALUE_INT);
    }
}

void op_Spawn(const void *env, struct state *state, struct context **pctx){
    extern struct code *code;
    extern int code_len;

    uint64_t pc = ctx_pop(pctx);
    assert((pc & VALUE_MASK) == VALUE_PC);
    pc >>= VALUE_BITS;

    assert(pc < code_len);
    assert(strcmp(code[pc].oi->name, "Frame") == 0);
    uint64_t arg = ctx_pop(pctx);
    uint64_t tag = ctx_pop(pctx);
    if (false) {
        printf("SPAWN %llx %llx %llx\n", pc, arg, tag);
    }

    struct context *ctx = new_alloc(struct context);

    // TODO.  Precompute the next two in init_Spawn
    uint64_t nv = value_put_atom("name", 4);
    uint64_t tv = value_put_atom("tag", 3);
    const struct env_Frame *ef = code[pc].env;
    ctx->nametag = dict_store(VALUE_DICT, nv, ef->name);
    ctx->nametag = dict_store(ctx->nametag, tv, tag);

    ctx->pc = pc;
    ctx->vars = VALUE_DICT;
    ctx_push(&ctx, (CALLTYPE_PROCESS << VALUE_BITS) | VALUE_INT);
    ctx_push(&ctx, arg);
    uint64_t v = value_put_context(ctx);

    state->ctxbag = bag_add(state->ctxbag, v);

    if (false) {
        char *p = value_string(state->ctxbag);
        printf("SPAWN --> %s\n", p);
        free(p);
    }

    (*pctx)->pc++;
}

void op_Store(const void *env, struct state *state, struct context **pctx){
    const struct env_Store *es = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);
    uint64_t v = ctx_pop(pctx);

    if (es == 0) {
        uint64_t av = ctx_pop(pctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);

        if (false) {
            printf("STORE IND %d %llx\n", size, v);
            for (int i = 0; i < size; i++) {
                char *index = value_string(indices[i]);
                printf(">> %s\n", index);
                free(index);
            }
        }

        state->vars = ind_store(state->vars, indices, size, v);
    }
    else {
        assert(es->n == 1);
        state->vars = dict_store(state->vars, es->indices[0], v);
    }
    (*pctx)->pc++;
}

void op_StoreVar(const void *env, struct state *state, struct context **pctx){
    const struct env_StoreVar *es = env;
    assert(es != NULL);
    assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);
    uint64_t v = ctx_pop(pctx);
    (*pctx)->vars = var_match(es->args, v, (*pctx)->vars);
    (*pctx)->pc++;
}

void *init_Address(struct map *map){ return NULL; }
void *init_Apply(struct map *map){ return NULL; }
void *init_Assert(struct map *map){ return NULL; }
void *init_Assert2(struct map *map){ return NULL; }
void *init_AtomicDec(struct map *map){ return NULL; }
void *init_AtomicInc(struct map *map){ return NULL; }
void *init_Choose(struct map *map){ return NULL; }
void *init_Cut(struct map *map){ return NULL; }
void *init_Del(struct map *map){ return NULL; }
void *init_Dict(struct map *map){ return NULL; }
void *init_Dup(struct map *map){ return NULL; }
void *init_Pop(struct map *map){ return NULL; }
void *init_ReadonlyDec(struct map *map){ return NULL; }
void *init_ReadonlyInc(struct map *map){ return NULL; }
void *init_Return(struct map *map){ return NULL; }
void *init_Set(struct map *map){ return NULL; }
void *init_Spawn(struct map *map){ return NULL; }

void *init_DelVar(struct map *map){
    struct env_DelVar *env = new_alloc(struct env_DelVar);
    struct json_value *name = map_lookup(map, "value", 5);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(name->u.atom.base, name->u.atom.len);
    return env;
}

void *init_Frame(struct map *map){
    struct env_Frame *env = new_alloc(struct env_Frame);

    struct json_value *name = map_lookup(map, "name", 4);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(name->u.atom.base, name->u.atom.len);

    struct json_value *args = map_lookup(map, "args", 4);
    assert(args->type == JV_ATOM);
    int index = 0;
    env->args = var_parse(args->u.atom.base, args->u.atom.len, &index);

    return env;
}

void *init_Load(struct map *map){
    struct json_value *jv = map_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Load *env = new_alloc(struct env_Load);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(uint64_t));
    for (int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(index->u.map);
    }
    return env;
}

void *init_LoadVar(struct map *map){
    struct json_value *value = map_lookup(map, "value", 5);
    if (value == NULL) {
        return NULL;
    }
    else {
        struct env_LoadVar *env = new_alloc(struct env_LoadVar);
        assert(value->type == JV_ATOM);
        env->name = value_put_atom(value->u.atom.base, value->u.atom.len);
        return env;
    }
}

void *init_Nary(struct map *map){
    struct env_Nary *env = new_alloc(struct env_Nary);

    struct json_value *arity = map_lookup(map, "arity", 5);
    assert(arity->type == JV_ATOM);
    char *copy = malloc(arity->u.atom.len + 1);
    memcpy(copy, arity->u.atom.base, arity->u.atom.len);
    copy[arity->u.atom.len] = 0;
    env->arity = atoi(copy);
    free(copy);

    struct json_value *op = map_lookup(map, "value", 5);
    assert(op->type == JV_ATOM);
    struct f_info *fi = map_lookup(f_map, op->u.atom.base, op->u.atom.len);
    if (fi == NULL) {
        fprintf(stderr, "Nary: unknown function '%.*s'\n", op->u.atom.len, op->u.atom.base);
        exit(1);
    }
    env->fi = fi;

    return env;
}

void *init_Push(struct map *map){
    struct json_value *jv = map_lookup(map, "value", 5);
    assert(jv->type == JV_MAP);
    struct env_Push *env = new_alloc(struct env_Push);
    env->value = value_from_json(jv->u.map);
    return env;
}

void *init_Store(struct map *map){
    struct json_value *jv = map_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Store *env = new_alloc(struct env_Store);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(uint64_t));
    for (int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(index->u.map);
    }
    return env;
}

void *init_StoreVar(struct map *map){
    struct json_value *jv = map_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    else {
        assert(jv->type == JV_ATOM);
        struct env_StoreVar *env = new_alloc(struct env_StoreVar);
        int index = 0;
        env->args = var_parse(jv->u.atom.base, jv->u.atom.len, &index);
        return env;
    }
}

void *init_Jump(struct map *map){
    struct env_Jump *env = new_alloc(struct env_Jump);

    struct json_value *pc = map_lookup(map, "pc", 2);
    assert(pc->type == JV_ATOM);
    char *copy = malloc(pc->u.atom.len + 1);
    memcpy(copy, pc->u.atom.base, pc->u.atom.len);
    copy[pc->u.atom.len] = 0;
    env->pc = atoi(copy);
    free(copy);
    return env;
}

void *init_JumpCond(struct map *map){
    struct env_JumpCond *env = new_alloc(struct env_JumpCond);

    struct json_value *pc = map_lookup(map, "pc", 2);
    assert(pc->type == JV_ATOM);
    char *copy = malloc(pc->u.atom.len + 1);
    memcpy(copy, pc->u.atom.base, pc->u.atom.len);
    copy[pc->u.atom.len] = 0;
    env->pc = atoi(copy);
    free(copy);

    struct json_value *cond = map_lookup(map, "cond", 4);
    assert(cond->type == JV_MAP);
    env->cond = value_from_json(cond->u.map);

    return env;
}

uint64_t f_atLabel(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
    assert((e & VALUE_MASK) == VALUE_ATOM);
    uint64_t pc = dict_load(state->labels, e);
    assert((pc & VALUE_MASK) == VALUE_INT);
    pc >>= 3;

    int size;
    uint64_t *vals = value_get(state->ctxbag, &size);
    size /= sizeof(uint64_t);
    assert(size > 0);
    assert(size % 2 == 0);
    uint64_t bag = VALUE_DICT;
    for (int i = 0; i < size; i += 2) {
        assert((vals[i] & VALUE_MASK) == VALUE_CONTEXT);
        assert((vals[i+1] & VALUE_MASK) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        if (ctx->pc == pc) {
            bag = bag_add(bag, ctx->nametag);
        }
    }
    return bag;
}

uint64_t f_eq(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    return ((args[0] == args[1]) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_ge(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp >= 0) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_gt(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp > 0) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_ne(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    return ((args[0] != args[1]) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_in(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    assert(0);
}

uint64_t f_isEmpty(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
    if ((e & VALUE_MASK) == VALUE_DICT) {
        return ((e == VALUE_DICT) << VALUE_BITS) | VALUE_BOOL;
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        return ((e == VALUE_SET) << VALUE_BITS) | VALUE_BOOL;
    }
    assert(0);
}

uint64_t f_keys(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(0);
}

uint64_t f_len(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= sizeof(uint64_t);
        return (size << VALUE_BITS) | VALUE_INT;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= 2 * sizeof(uint64_t);
        return (size << VALUE_BITS) | VALUE_INT;
    }
    assert(0);
}

uint64_t f_le(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    assert(0);
}

uint64_t f_lt(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    assert(0);
}

uint64_t f_minus(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 1 || n == 2);
    if (n == 1) {
        uint64_t e = args[0];
        assert((e & VALUE_MASK) == VALUE_INT);
        e >>= VALUE_BITS;
        return ((-e) << VALUE_BITS) | VALUE_INT;
    }
    else {
        uint64_t e1 = args[0], e2 = args[1];
        assert((e1 & VALUE_MASK) == VALUE_INT);
        assert((e2 & VALUE_MASK) == VALUE_INT);
        e1 >>= VALUE_BITS;
        e2 >>= VALUE_BITS;
        return ((e2 - e1) << VALUE_BITS) | VALUE_INT;
    }
}

uint64_t f_mod(struct state *state, struct context **pctx, uint64_t *args, int n){
    uint64_t e1 = args[0], e2 = args[1];
    assert((e1 & VALUE_MASK) == VALUE_INT);
    assert((e2 & VALUE_MASK) == VALUE_INT);
    uint64_t result = (e2 >> VALUE_BITS) % (e1 >> VALUE_BITS);
    return (result << VALUE_BITS) | VALUE_INT;
}

uint64_t f_nametag(struct state *state, struct context **pctx, uint64_t *args, int n){
    return (*pctx)->nametag;
}

uint64_t f_not(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
    assert((e & VALUE_MASK) == VALUE_BOOL);
    return e ^ (1 << VALUE_BITS);
}

uint64_t f_plus(struct state *state, struct context **pctx, uint64_t *args, int n){
    uint64_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            uint64_t e2 = args[i];
            assert((e2 & VALUE_MASK) == VALUE_INT);
            e1 += e2 & ~VALUE_MASK;
        }
        return e1;
    }

    // get all the lists
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        assert((args[i] & VALUE_MASK) == VALUE_DICT);
        if (args[i] == VALUE_DICT) {
            vi[i].vals = NULL;
            vi[i].size = 0;
        }
        else {
            vi[i].vals = value_get(args[i], &vi[i].size); 
            total += vi[i].size;
        }
    }

    // If all are empty lists, we're done.
    if (total == 0) {
        return VALUE_DICT;
    }

    // Concatenate the sets
    uint64_t *vals = malloc(total), *v;
    total = 0;
    for (int i = n; --i >= 0;) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // Update the indices
    n = total / (2 * sizeof(uint64_t));
    for (int i = 0; i < n; i++) {
        vals[2*i] = (i << VALUE_BITS) | VALUE_INT;
    }
    uint64_t result = value_put_dict(vals, total);

    free(vi);
    free(vals);
    return result;
}

uint64_t f_range(struct state *state, struct context **pctx, uint64_t *args, int n){
    assert(n == 2);
    uint64_t e1 = args[0], e2 = args[1];

    assert((e1 & VALUE_MASK) == VALUE_INT);
    assert((e2 & VALUE_MASK) == VALUE_INT);
    int64_t start = e2 >> VALUE_BITS;
    int64_t finish = e1 >> VALUE_BITS;
    int cnt = (finish - start) + 1;
    uint64_t *v = malloc(cnt * sizeof(uint64_t));
    for (int i = 0; i < cnt; i++) {
        v[i] = ((start + i) << VALUE_BITS) | VALUE_INT;
    }
    uint64_t result = value_put_set(v, cnt * sizeof(uint64_t));
    free(v);
    return result;
}

static int q_value_cmp(const void *v1, const void *v2){
    return value_cmp(* (const uint64_t *) v1, * (const uint64_t *) v2);
}

uint64_t f_union(struct state *state, struct context **pctx, uint64_t *args, int n){
    uint64_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            uint64_t e2 = args[i];
            assert((e2 & VALUE_MASK) == VALUE_INT);
            e1 |= e2;
        }
        return e1;
    }

    // get all the sets
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        assert((args[i] & VALUE_MASK) == VALUE_SET);
        if (args[i] == VALUE_SET) {
            vi[i].vals = NULL;
            vi[i].size = 0;
        }
        else {
            vi[i].vals = value_get(args[i], &vi[i].size); 
            total += vi[i].size;
        }
    }

    // If all are empty lists, we're done.
    if (total == 0) {
        return VALUE_SET;
    }

    // Concatenate the sets
    uint64_t *vals = malloc(total), *v;
    total = 0;
    for (int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // Sort the resulting set (with potential duplicates)
    qsort(vals, total / sizeof(uint64_t), sizeof(uint64_t), q_value_cmp);

    // Remove duplicates
    n = total / sizeof(uint64_t);
    uint64_t *p = vals, *q = vals + 1;
    for (int i = 1; i < n; i++, q++) {
        if (*q != *p) {
            *++p = *q;
        }
    }
    p++;

    uint64_t result = value_put_set(vals, (p - vals) * sizeof(uint64_t));

    free(vi);
    free(vals);
    return result;
}

struct op_info op_table[] = {
	{ "Address", init_Address, op_Address },
	{ "Apply", init_Apply, op_Apply },
	{ "Assert", init_Assert, op_Assert },
	{ "Assert2", init_Assert2, op_Assert2 },
	{ "AtomicDec", init_AtomicDec, op_AtomicDec },
	{ "AtomicInc", init_AtomicInc, op_AtomicInc },
	{ "Choose", init_Choose, op_Choose },
	{ "Cut", init_Cut, op_Cut },
	{ "Del", init_Del, op_Del },
	{ "DelVar", init_DelVar, op_DelVar },
	{ "Dict", init_Dict, op_Dict },
	{ "Dup", init_Dup, op_Dup },
	{ "Frame", init_Frame, op_Frame },
	{ "Jump", init_Jump, op_Jump },
	{ "JumpCond", init_JumpCond, op_JumpCond },
	{ "Load", init_Load, op_Load },
	{ "LoadVar", init_LoadVar, op_LoadVar },
	{ "Nary", init_Nary, op_Nary },
	{ "Pop", init_Pop, op_Pop },
	{ "Push", init_Push, op_Push },
	{ "ReadonlyDec", init_ReadonlyDec, op_ReadonlyDec },
	{ "ReadonlyInc", init_ReadonlyInc, op_ReadonlyInc },
	{ "Return", init_Return, op_Return },
	{ "Set", init_Set, op_Set },
	{ "Spawn", init_Spawn, op_Spawn },
	{ "Store", init_Store, op_Store },
	{ "StoreVar", init_StoreVar, op_StoreVar },
    { NULL, NULL, NULL }
};

struct f_info f_table[] = {
	{ "+", f_plus },
	{ "-", f_minus },
	{ "%", f_mod },
    { "<", f_lt },
    { "<=", f_le },
    { ">=", f_ge },
    { ">", f_gt },
    { "|", f_union },
    { "..", f_range },
    { "==", f_eq },
    { "!=", f_ne },
    { "atLabel", f_atLabel },
    { "in", f_in },
    { "IsEmpty", f_isEmpty },
    { "keys", f_keys },
    { "len", f_len },
    { "nametag", f_nametag },
    { "not", f_not },
    { NULL, NULL }
};

struct op_info *ops_get(char *opname, int size){
    return map_lookup(ops_map, opname, size);
}

void ops_init(){
    ops_map = map_init();

    for (struct op_info *oi = op_table; oi->name != NULL; oi++) {
        void **p = map_insert(&ops_map, oi->name, strlen(oi->name));
        *p = oi;
    }
    for (struct f_info *fi = f_table; fi->name != NULL; fi++) {
        void **p = map_insert(&f_map, fi->name, strlen(fi->name));
        *p = fi;
    }
}
