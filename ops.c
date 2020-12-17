#define _GNU_SOURCE

#include <stdarg.h>
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
    int size, index;
    uint64_t *vals;
};

struct f_info {
    char *name;
    uint64_t (*f)(struct state *state, struct context *ctx, uint64_t *args, int n);
};

struct var_tree {
    // TODO.  Is VT_LIST really a thing?
    enum { VT_NAME, VT_TUPLE, VT_LIST } type;
    union {
        uint64_t name;
        struct {
            int n;
            struct var_tree **elements;
        } tuple;
    } u;
};

static struct dict *ops_map, *f_map;
extern struct code *code;

struct env_DelVar {
    uint64_t name;
};

struct env_Frame {
    uint64_t name;
    struct var_tree *args;
};

struct env_Invariant {
    int cnt;
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

struct env_Move {
    int offset;
};

struct env_Nary {
    int arity;
    struct f_info *fi;
};

struct env_Push {
    uint64_t value;
};

struct env_Split {
    int count;
};

struct env_Store {
    uint64_t *indices;
    int n;
};

struct env_StoreVar {
    struct var_tree *args;
};

uint64_t ctx_failure(struct context *ctx, char *fmt, ...){
    char *r;
    va_list args;

    assert(ctx->failure == 0);

    va_start(args, fmt);
    vasprintf(&r, fmt, args);
    va_end(args);

    ctx->failure = value_put_atom(r, strlen(r));
    free(r);

    return 0;
}

uint64_t var_match_rec(struct context *ctx, struct var_tree *vt,
                            uint64_t arg, uint64_t vars){
    switch (vt->type) {
    case VT_NAME:
        return dict_store(vars, vt->u.name, arg);
    case VT_TUPLE:
        if ((arg & VALUE_MASK) != VALUE_DICT) {
            return ctx_failure(ctx, "match: expected a tuple");
        }
        if (arg == VALUE_DICT) {
            if (vt->u.tuple.n != 0) {
                return ctx_failure(ctx, "match: expected a non-empty tuple");
            }
            return vars;
        }
        if (vt->u.tuple.n == 0) {
            return ctx_failure(ctx, "match: expected an empty tuple");
        }
        int size;
        uint64_t *vals = value_get(arg, &size);
        size /= 2 * sizeof(uint64_t);
        if (vt->u.tuple.n != size) {
            return ctx_failure(ctx, "match: tuple size mismatch");
        }
        for (int i = 0; i < size; i++) {
            if (vals[2*i] != ((i << VALUE_BITS) | VALUE_INT)) {
                return ctx_failure(ctx, "match: not a tuple");
            }
            vars = var_match_rec(ctx, vt->u.tuple.elements[i], vals[2*i+1], vars);
        }
        return vars;
    default:
        assert(false);
    }
}

void var_match(struct context *ctx, struct var_tree *vt, uint64_t arg){
    uint64_t vars = var_match_rec(ctx, vt, arg, ctx->vars);
    if (ctx->failure == 0) {
        ctx->vars = vars;
    }
}

// for debugging only
void var_dump(struct var_tree *vt){
    switch (vt->type) {
    case VT_NAME:
        printf("%"PRIx64"", vt->u.name);
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
        assert(false);
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
    else if (s[*index] == '[') {
        vt->type = VT_TUPLE;
        (*index)++;
        assert(false);      // TODO
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
	assert(*pctx != NULL);
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

	printf("CAN'T FIND %s in %s\n", value_string(key), value_string(dict));

    assert(false);
}

uint64_t dict_remove(uint64_t dict, uint64_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        assert(false);
    }
    vals = value_get(dict & ~VALUE_MASK, &size);
    size /= sizeof(uint64_t);
    assert(size % 2 == 0);

    if (size == 2) {
        return vals[0] == key ? VALUE_DICT : dict;
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
                assert(false);
            }
        */
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
                    assert(false);
                }
            */
        }

        assert(false);
    }
}

uint64_t ind_remove(uint64_t dict, uint64_t *indices, int n){
    assert((dict & VALUE_MASK) == VALUE_DICT);
    assert(n > 0);

    if (n == 1) {
        return dict_remove(dict, indices[0]);
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
                uint64_t nd = ind_remove(d, indices + 1, n - 1);
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
                    assert(false);
                }
            */
        }

        assert(false);
    }
}

void op_Address(const void *env, struct state *state, struct context **pctx){
    uint64_t index = ctx_pop(pctx);
    uint64_t av = ctx_pop(pctx);
    if ((av & VALUE_MASK) != VALUE_ADDRESS) {
        ctx_failure(*pctx, "not an address");
        return;
    }
    if (av == VALUE_ADDRESS) {
        ctx_failure(*pctx, "None unexpected");
        return;
    }
    if (false) {
        printf("ADDRESS %"PRIx64"\n", index);
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
        ctx_failure(*pctx, "Can only apply to methods or dictionaries");
    }
}

void op_Assert(const void *env, struct state *state, struct context **pctx){
    uint64_t v = ctx_pop(pctx);
    if ((v & VALUE_MASK) != VALUE_BOOL) {
        ctx_failure(*pctx, "assert can only be applied to bool values");
    }
    if (v == VALUE_FALSE) {
        printf("HARMONY ASSERTION FAILED\n");
        ctx_failure(*pctx, "Harmony assertion failed");
    }
    else {
        (*pctx)->pc++;
    }
}

void op_Assert2(const void *env, struct state *state, struct context **pctx){
    uint64_t e = ctx_pop(pctx);
    uint64_t v = ctx_pop(pctx);
    if ((v & VALUE_MASK) != VALUE_BOOL) {
        ctx_failure(*pctx, "assert2 can only be applied to bool values");
    }
    if (v == VALUE_FALSE) {
        char *p = value_string(e);
        printf("HARMONY ASSERTION FAILED: %s\n", p);
        ctx_failure(*pctx, "Harmony assertion failed: %s", p);
        free(p);
    }
    else {
        (*pctx)->pc++;
    }
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
    assert(false);
}

void op_Cut(const void *env, struct state *state, struct context **pctx){
    uint64_t v = ctx_pop(pctx);
    if ((v & VALUE_MASK) == VALUE_SET) {
        assert(v != VALUE_SET);
        void *p = (void *) (v & ~VALUE_MASK);

        int size;
        uint64_t *vals = dict_retrieve(p, &size);
        assert(size > 0);

        ctx_push(pctx, vals[0]);
        ctx_push(pctx, value_put_set(&vals[1], size - sizeof(uint64_t)));
        (*pctx)->pc++;
        return;
    }
    if ((v & VALUE_MASK) == VALUE_DICT) {
        assert(v != VALUE_DICT);
        assert(false);
        return;
    }
    assert(false);
}

void op_Del(const void *env, struct state *state, struct context **pctx){
    assert((state->vars & VALUE_MASK) == VALUE_DICT);
    uint64_t av = ctx_pop(pctx);
    assert((av & VALUE_MASK) == VALUE_ADDRESS);
    assert(av != VALUE_ADDRESS);

    int size;
    uint64_t *indices = value_get(av, &size);
    size /= sizeof(uint64_t);
    state->vars = ind_remove(state->vars, indices, size);

    (*pctx)->pc++;
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
    n >>= VALUE_BITS;
	if (n == 0) {
		ctx_push(pctx, VALUE_DICT);
		(*pctx)->pc++;
		return;
	}

    // TODO.  Fail if there's a duplicate key
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
        printf("FRAME %d %d %"PRIx64" ", (*pctx)->pc, (*pctx)->sp, ef->name);
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

    var_match(*pctx, ef->args, arg);
    if ((*pctx)->failure == 0) {
        ctx->pc += 1;
    }
}

void op_Invariant(const void *env, struct state *state, struct context **pctx){
    const struct env_Invariant *ei = env;

    assert((state->invariants & VALUE_MASK) == VALUE_SET);
    int size;
    uint64_t *vals;
    if (state->invariants == VALUE_SET) {
        size = 0;
        vals = NULL;
    }
    else {
        vals = value_get(state->invariants, &size);
    }
    vals = realloc(vals, size + sizeof(uint64_t));
    * (uint64_t *) ((char *) vals + size) = ((*pctx)->pc << VALUE_BITS) | VALUE_PC;
    state->invariants = value_put_set(vals, size + sizeof(uint64_t));
    (*pctx)->pc += ei->cnt + 1;
}

int invariant_cnt(const void *env){
    const struct env_Invariant *ei = env;

    return ei->cnt;
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
        assert(av != VALUE_ADDRESS);

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
        ctx_push(pctx, ind_load(state->vars, el->indices, el->n));
    }
    (*pctx)->pc++;
}

void op_LoadVar(const void *env, struct state *state, struct context **pctx){
    const struct env_LoadVar *el = env;
    assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);

    if (el == NULL) {
        uint64_t av = ctx_pop(pctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);

        ctx_push(pctx, ind_load((*pctx)->vars, indices, size));
    }
    else {
        ctx_push(pctx, dict_load((*pctx)->vars, el->name));
    }
    (*pctx)->pc++;
}

void op_Move(const void *env, struct state *state, struct context **pctx){
    const struct env_Move *em = env;
    struct context *ctx = *pctx;
    int offset = ctx->sp - em->offset;

    uint64_t v = ctx->stack[offset];
    memmove(&ctx->stack[offset], &ctx->stack[offset + 1],
                (em->offset - 1) * sizeof(uint64_t));
    ctx->stack[ctx->sp - 1] = v;
    ctx->pc++;
}

void op_Nary(const void *env, struct state *state, struct context **pctx){
    const struct env_Nary *en = env;
    uint64_t args[MAX_ARITY];

    for (int i = 0; i < en->arity; i++) {
        args[i] = ctx_pop(pctx);
    }
    uint64_t result = (*en->fi->f)(state, *pctx, args, en->arity);
    if ((*pctx)->failure == 0) {
        ctx_push(pctx, result);
        (*pctx)->pc++;
    }
}

void op_Pop(const void *env, struct state *state, struct context **pctx){
    assert((*pctx)->sp > 0);
    (*pctx)->sp--;
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
        (*pctx)->phase = CTX_END;
        if (false) {
            printf("RETURN INIT\n");
        }
    }
    else {
        uint64_t result = dict_load((*pctx)->vars, value_put_atom("result", 6));
        uint64_t fp = ctx_pop(pctx);
        if ((fp & VALUE_MASK) != VALUE_INT) {
            printf("XXX %d %d %s", (*pctx)->pc, (*pctx)->sp, value_string(fp));
            exit(0);
        }
        assert((fp & VALUE_MASK) == VALUE_INT);
        (*pctx)->fp = fp >> VALUE_BITS;
        (*pctx)->vars = ctx_pop(pctx);
        assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);
        (void) ctx_pop(pctx);   // argument saved for stack trace
        uint64_t calltype = ctx_pop(pctx);
        assert((calltype & VALUE_MASK) == VALUE_INT);
        switch (calltype >> VALUE_BITS) {
        case CALLTYPE_PROCESS:
            (*pctx)->phase = CTX_END;
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
            assert(false);
        }
    }
}

static int q_value_cmp(const void *v1, const void *v2){
    return value_cmp(* (const uint64_t *) v1, * (const uint64_t *) v2);
}

// Sort the resulting set and remove duplicates
static int sort(uint64_t *vals, int n){
    qsort(vals, n, sizeof(uint64_t), q_value_cmp);

    uint64_t *p = vals, *q = vals + 1;
    for (int i = 1; i < n; i++, q++) {
        if (*q != *p) {
            *++p = *q;
        }
    }
    p++;
    return p - vals;
}

void op_Set(const void *env, struct state *state, struct context **pctx){
    uint64_t n = ctx_pop(pctx);
    assert((n & VALUE_MASK) == VALUE_INT);
    n >>= VALUE_BITS;
	if (n == 0) {
		ctx_push(pctx, VALUE_SET);
		(*pctx)->pc++;
		return;
	}

    uint64_t *vals = malloc(n * sizeof(uint64_t));
    for (int i = 0; i < n; i++) {
        vals[i] = ctx_pop(pctx);
    }

    n = sort(vals, n);
    ctx_push(pctx, value_put_set(vals, n * sizeof(uint64_t)));
    free(vals);
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
    extern int code_len;

    uint64_t pc = ctx_pop(pctx);
    assert((pc & VALUE_MASK) == VALUE_PC);
    pc >>= VALUE_BITS;

    assert(pc < code_len);
    assert(strcmp(code[pc].oi->name, "Frame") == 0);
    uint64_t arg = ctx_pop(pctx);
    uint64_t tag = ctx_pop(pctx);
    if (false) {
        printf("SPAWN %"PRIx64" %"PRIx64" %"PRIx64"\n", pc, arg, tag);
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

void op_Split(const void *env, struct state *state, struct context **pctx){
    const struct env_Split *es = env;

    uint64_t v = ctx_pop(pctx);
    uint64_t type = v & VALUE_MASK;
    assert(type == VALUE_DICT || type == VALUE_SET);
    if (v == VALUE_DICT || v == VALUE_SET) {
        assert(es->count == 0);
        (*pctx)->pc++;
        return;
    }

    int size;
    uint64_t *vals = value_get(v, &size);

    // TODO.  Should items be pushed in this order???
    if (type == VALUE_DICT) {
        size /= 2 * sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            ctx_push(pctx, vals[2*i + 1]);
        }
        (*pctx)->pc++;
        return;
    }
    if (type == VALUE_SET) {
        size /= sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            ctx_push(pctx, vals[i]);
        }
        (*pctx)->pc++;
        return;
    }
    assert(false);
}

void op_Store(const void *env, struct state *state, struct context **pctx){
    const struct env_Store *es = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);
    uint64_t v = ctx_pop(pctx);

    if (es == 0) {
        uint64_t av = ctx_pop(pctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);

        if (false) {
            printf("STORE IND %d %d %d %"PRIx64" %s %s\n", (*pctx)->pc, (*pctx)->sp, size, v,
                    value_string((*pctx)->stack[(*pctx)->sp - 1]),
                    value_string(av));
            for (int i = 0; i < size; i++) {
                char *index = value_string(indices[i]);
                printf(">> %s\n", index);
                free(index);
            }
        }

        state->vars = ind_store(state->vars, indices, size, v);
    }
    else {
        state->vars = ind_store(state->vars, es->indices, es->n, v);
    }
    (*pctx)->pc++;
}

void op_StoreVar(const void *env, struct state *state, struct context **pctx){
    const struct env_StoreVar *es = env;
    uint64_t v = ctx_pop(pctx);

    assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);
    if (es == NULL) {
        uint64_t av = ctx_pop(pctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);

        (*pctx)->vars = ind_store((*pctx)->vars, indices, size, v);
        (*pctx)->pc++;
    }
    else {
        var_match(*pctx, es->args, v);
        if ((*pctx)->failure == 0) {
            (*pctx)->pc++;
        }
    }
}

void *init_Address(struct dict *map){ return NULL; }
void *init_Apply(struct dict *map){ return NULL; }
void *init_Assert(struct dict *map){ return NULL; }
void *init_Assert2(struct dict *map){ return NULL; }
void *init_AtomicDec(struct dict *map){ return NULL; }
void *init_AtomicInc(struct dict *map){ return NULL; }
void *init_Choose(struct dict *map){ return NULL; }
void *init_Cut(struct dict *map){ return NULL; }
void *init_Del(struct dict *map){ return NULL; }
void *init_Dict(struct dict *map){ return NULL; }
void *init_Dup(struct dict *map){ return NULL; }
void *init_Pop(struct dict *map){ return NULL; }
void *init_ReadonlyDec(struct dict *map){ return NULL; }
void *init_ReadonlyInc(struct dict *map){ return NULL; }
void *init_Return(struct dict *map){ return NULL; }
void *init_Set(struct dict *map){ return NULL; }
void *init_Spawn(struct dict *map){ return NULL; }

void *init_DelVar(struct dict *map){
    struct env_DelVar *env = new_alloc(struct env_DelVar);
    struct json_value *name = dict_lookup(map, "value", 5);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(name->u.atom.base, name->u.atom.len);
    return env;
}

void *init_Frame(struct dict *map){
    struct env_Frame *env = new_alloc(struct env_Frame);

    struct json_value *name = dict_lookup(map, "name", 4);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(name->u.atom.base, name->u.atom.len);

    struct json_value *args = dict_lookup(map, "args", 4);
    assert(args->type == JV_ATOM);
    int index = 0;
    env->args = var_parse(args->u.atom.base, args->u.atom.len, &index);

    return env;
}

void *init_Load(struct dict *map){
    struct json_value *jv = dict_lookup(map, "value", 5);
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

void *init_LoadVar(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
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

void *init_Move(struct dict *map){
    struct env_Move *env = new_alloc(struct env_Move);

    struct json_value *offset = dict_lookup(map, "offset", 6);
    assert(offset->type == JV_ATOM);
    char *copy = malloc(offset->u.atom.len + 1);
    memcpy(copy, offset->u.atom.base, offset->u.atom.len);
    copy[offset->u.atom.len] = 0;
    env->offset = atoi(copy);
    free(copy);

    return env;
}

void *init_Nary(struct dict *map){
    struct env_Nary *env = new_alloc(struct env_Nary);

    struct json_value *arity = dict_lookup(map, "arity", 5);
    assert(arity->type == JV_ATOM);
    char *copy = malloc(arity->u.atom.len + 1);
    memcpy(copy, arity->u.atom.base, arity->u.atom.len);
    copy[arity->u.atom.len] = 0;
    env->arity = atoi(copy);
    free(copy);

    struct json_value *op = dict_lookup(map, "value", 5);
    assert(op->type == JV_ATOM);
    struct f_info *fi = dict_lookup(f_map, op->u.atom.base, op->u.atom.len);
    if (fi == NULL) {
        fprintf(stderr, "Nary: unknown function '%.*s'\n", op->u.atom.len, op->u.atom.base);
        exit(1);
    }
    env->fi = fi;

    return env;
}

void *init_Invariant(struct dict *map){
    struct env_Invariant *env = new_alloc(struct env_Invariant);

    struct json_value *cnt = dict_lookup(map, "cnt", 3);
    assert(cnt->type == JV_ATOM);
    char *copy = malloc(cnt->u.atom.len + 1);
    memcpy(copy, cnt->u.atom.base, cnt->u.atom.len);
    copy[cnt->u.atom.len] = 0;
    env->cnt = atoi(copy);
    free(copy);
    return env;
}

void *init_Jump(struct dict *map){
    struct env_Jump *env = new_alloc(struct env_Jump);

    struct json_value *pc = dict_lookup(map, "pc", 2);
    assert(pc->type == JV_ATOM);
    char *copy = malloc(pc->u.atom.len + 1);
    memcpy(copy, pc->u.atom.base, pc->u.atom.len);
    copy[pc->u.atom.len] = 0;
    env->pc = atoi(copy);
    free(copy);
    return env;
}

void *init_JumpCond(struct dict *map){
    struct env_JumpCond *env = new_alloc(struct env_JumpCond);

    struct json_value *pc = dict_lookup(map, "pc", 2);
    assert(pc->type == JV_ATOM);
    char *copy = malloc(pc->u.atom.len + 1);
    memcpy(copy, pc->u.atom.base, pc->u.atom.len);
    copy[pc->u.atom.len] = 0;
    env->pc = atoi(copy);
    free(copy);

    struct json_value *cond = dict_lookup(map, "cond", 4);
    assert(cond->type == JV_MAP);
    env->cond = value_from_json(cond->u.map);

    return env;
}

void *init_Push(struct dict *map){
    struct json_value *jv = dict_lookup(map, "value", 5);
    assert(jv->type == JV_MAP);
    struct env_Push *env = new_alloc(struct env_Push);
    env->value = value_from_json(jv->u.map);
    return env;
}

void *init_Split(struct dict *map){
    struct env_Split *env = new_alloc(struct env_Split);

    struct json_value *count = dict_lookup(map, "count", 5);
    assert(count->type == JV_ATOM);
    char *copy = malloc(count->u.atom.len + 1);
    memcpy(copy, count->u.atom.base, count->u.atom.len);
    copy[count->u.atom.len] = 0;
    env->count = atoi(copy);
    free(copy);
    return env;
}

void *init_Store(struct dict *map){
    struct json_value *jv = dict_lookup(map, "value", 5);
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

void *init_StoreVar(struct dict *map){
    struct json_value *jv = dict_lookup(map, "value", 5);
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

uint64_t f_abs(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    int64_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "abs() can only be applied to integers");
    }
    e >>= VALUE_BITS;
    return e >= 0 ? args[0] : (((-e) << VALUE_BITS) | VALUE_INT);
}

uint64_t f_all(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
	if (e == VALUE_SET || e == VALUE_DICT) {
		return VALUE_TRUE;
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            if ((v[i] & VALUE_MASK) != VALUE_BOOL) {
                return ctx_failure(ctx, "set.all() can only be applied to booleans");
            }
            if (v[i] == VALUE_FALSE) {
                return VALUE_FALSE;
            }
        }
		return VALUE_TRUE;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= 2 * sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            if ((v[2*i+1] & VALUE_MASK) != VALUE_BOOL) {
                return ctx_failure(ctx, "dict.all() can only be applied to booleans");
            }
            if (v[2*i+1] == VALUE_FALSE) {
                return VALUE_FALSE;
            }
        }
		return VALUE_TRUE;
    }
    return ctx_failure(ctx, "all() can only be applied to sets or dictionaries");
}

uint64_t f_any(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
	if (e == VALUE_SET || e == VALUE_DICT) {
		return VALUE_FALSE;
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            if ((v[i] & VALUE_MASK) != VALUE_BOOL) {
                return ctx_failure(ctx, "set.any() can only be applied to booleans");
            }
            if (v[i] != VALUE_FALSE) {
                return VALUE_TRUE;
            }
        }
		return VALUE_FALSE;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= 2 * sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            if ((v[2*i+1] & VALUE_MASK) != VALUE_BOOL) {
                return ctx_failure(ctx, "dict.any() can only be applied to booleans");
            }
            if (v[2*i+1] != VALUE_FALSE) {
                return VALUE_TRUE;
            }
        }
		return VALUE_FALSE;
    }
    return ctx_failure(ctx, "any() can only be applied to sets or dictionaries");
}

uint64_t f_atLabel(struct state *state, struct context *ctx, uint64_t *args, int n){
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

uint64_t f_div(struct state *state, struct context *ctx, uint64_t *args, int n){
    int64_t e1 = args[0], e2 = args[1];
    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "right argument to / not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "left argument to / not an integer");
    }
    int64_t result = (e2 >> VALUE_BITS) / (e1 >> VALUE_BITS);
    return (result << VALUE_BITS) | VALUE_INT;
}

uint64_t f_eq(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    return ((args[0] == args[1]) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_ge(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp >= 0) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_gt(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp > 0) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_ne(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    return ((args[0] != args[1]) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_in(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    uint64_t s = args[0], e = args[1];
	if (s == VALUE_SET || s == VALUE_DICT) {
		return VALUE_FALSE;
	}
    if ((s & VALUE_MASK) == VALUE_SET) {
        int size;
        uint64_t *v = value_get(s, &size);
        size /= sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            if (v[i] == e) {
                return VALUE_TRUE;
            }
        }
        return VALUE_FALSE;
    }
    if ((s & VALUE_MASK) == VALUE_DICT) {
        int size;
        uint64_t *v = value_get(s, &size);
        size /= 2 * sizeof(uint64_t);
        for (int i = 0; i < size; i++) {
            if (v[2*i+1] == e) {
                return VALUE_TRUE;
            }
        }
        return VALUE_FALSE;
    }
    return ctx_failure(ctx, "'in' can only be applied to sets or dictionaries");
}

uint64_t f_intersection(struct state *state, struct context *ctx, uint64_t *args, int n){
    uint64_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            uint64_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return ctx_failure(ctx, "'&' applied to mix of ints and other types");
            }
            e1 &= e2;
        }
        return e1;
    }

    // get all the sets
    struct val_info *vi = malloc(n * sizeof(*vi));
    int min_size = -1;      // minimum set size
    uint64_t max_val;       // maximum value over the minima of all sets
    bool some_empty = false;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_SET) {
            return ctx_failure(ctx, "'&' applied to mix of sets and other types");
        }
        if (args[i] == VALUE_SET) {
            min_size = 0;
        }
        else {
            vi[i].vals = value_get(args[i], &vi[i].size); 
            vi[i].index = 0;
            if (min_size < 0) {
                min_size = vi[i].size;
                max_val = vi[i].vals[0];
            }
            else {
                if (vi[i].size < min_size) {
                    min_size = vi[i].size;
                }
                if (value_cmp(vi[i].vals[0], max_val) > 0) {
                    max_val = vi[i].vals[0];
                }
            }
        }
    }

    // If any are empty lists, we're done.
    if (min_size == 0) {
        return VALUE_SET;
    }

    // Allocate sufficient memory.
    uint64_t *vals = malloc(min_size), *v = vals;

    bool done = false;
    for (int i = 0; i < min_size; i++) {
        uint64_t old_max = max_val;
        for (int j = 0; j < n; j++) {
            int k, size = vi[j].size / sizeof(uint64_t);
            while ((k = vi[j].index) < size) {
                uint64_t v = vi[j].vals[k];
                int cmp = value_cmp(v, max_val);
                if (cmp > 0) {
                    max_val = v;
				}
				if (cmp >= 0) {
					break;
				}
				vi[j].index++;
            }
            if (vi[j].index == vi[j].size) {
                done = true;
				break;
            }
        }
		if (done) {
			break;
		}
        if (old_max == max_val) {
            *v++ = max_val;
			for (int j = 0; j < n; j++) {
				assert(vi[j].index < vi[j].size);
				vi[j].index++;
				int k, size = vi[j].size / sizeof(uint64_t);
				if ((k = vi[j].index) == size) {
					done = true;
					break;
				}
				if (value_cmp(vi[j].vals[k], max_val) > 0) {
					max_val = vi[j].vals[k];
				}
			}
        }
		if (done) {
			break;
		}
    }

    uint64_t result = value_put_set(vals, (char *) v - (char *) vals);
    free(vi);
    free(vals);
    return result;
}

uint64_t f_invert(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    int64_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "~ can only be applied to ints");
    }
    e >>= VALUE_BITS;
    return ((~e) << VALUE_BITS) | VALUE_INT;
}

uint64_t f_isEmpty(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
    if ((e & VALUE_MASK) == VALUE_DICT) {
        return ((e == VALUE_DICT) << VALUE_BITS) | VALUE_BOOL;
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        return ((e == VALUE_SET) << VALUE_BITS) | VALUE_BOOL;
    }
    assert(false);
}

uint64_t f_keys(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t v = args[0];
    if ((v & VALUE_MASK) != VALUE_DICT) {
        return ctx_failure(ctx, "keys() can only be applied to dictionaries");
    }
    if (v == VALUE_DICT) {
        return VALUE_SET;
    }

    int size;
    uint64_t *vals = value_get(v, &size);
    uint64_t *keys = malloc(size / 2);
    size /= 2 * sizeof(uint64_t);
    for (int i = 0; i < size; i++) {
        keys[i] = vals[2*i];
    }
    uint64_t result = value_put_set(keys, size * sizeof(uint64_t));
    free(keys);
    return result;
}

uint64_t f_len(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
	if (e == VALUE_SET || e == VALUE_DICT) {
		return 0;
	}
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
    return ctx_failure(ctx, "len() can only be applied to sets or dictionaries");
}

uint64_t f_le(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp <= 0) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_lt(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp < 0) << VALUE_BITS) | VALUE_BOOL;
}

uint64_t f_max(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
	if (e == VALUE_SET) {
        return ctx_failure(ctx, "can't apply max() to empty set");
    }
    if (e == VALUE_DICT) {
        return ctx_failure(ctx, "can't apply max() to empty list");
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= sizeof(uint64_t);
        uint64_t max = v[0];
        for (int i = 1; i < size; i++) {
            if (value_cmp(v[i], max) > 0) {
                max = v[i];
            }
        }
		return max;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= 2 * sizeof(uint64_t);
        uint64_t max = v[0];
        for (int i = 0; i < size; i++) {
            if (v[2*i] != ((i << VALUE_BITS) | VALUE_INT)) {
                return ctx_failure(ctx, "max() cannot be applied to a dictionary");
            }
            if (value_cmp(v[2*i+1], max) > 0) {
                max = v[i];
            }
        }
		return max;
    }
    return ctx_failure(ctx, "max() can only be applied to sets or lists");
}

uint64_t f_min(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
	if (e == VALUE_SET) {
        return ctx_failure(ctx, "can't apply min() to empty set");
    }
    if (e == VALUE_DICT) {
        return ctx_failure(ctx, "can't apply min() to empty list");
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= sizeof(uint64_t);
        uint64_t min = v[0];
        for (int i = 1; i < size; i++) {
            if (value_cmp(v[i], min) < 0) {
                min = v[i];
            }
        }
		return min;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        uint64_t *v = value_get(e, &size);
        size /= 2 * sizeof(uint64_t);
        uint64_t min = v[0];
        for (int i = 0; i < size; i++) {
            if (v[2*i] != ((i << VALUE_BITS) | VALUE_INT)) {
                return ctx_failure(ctx, "min() cannot be applied to a dictionary");
            }
            if (value_cmp(v[2*i+1], min) < 0) {
                min = v[i];
            }
        }
		return min;
    }
    return ctx_failure(ctx, "min() can only be applied to sets or lists");
}

uint64_t f_minus(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1 || n == 2);
    if (n == 1) {
        int64_t e = args[0];
        if ((e & VALUE_MASK) != VALUE_INT) {
            return ctx_failure(ctx, "unary minus can only be applied to ints");
        }
        e >>= VALUE_BITS;
        return ((-e) << VALUE_BITS) | VALUE_INT;
    }
    else {
        if ((args[0] & VALUE_MASK) == VALUE_INT) {
            int64_t e1 = args[0], e2 = args[1];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return ctx_failure(ctx, "minus applied to int and non-int");
            }
            e1 >>= VALUE_BITS;
            e2 >>= VALUE_BITS;
            return ((e2 - e1) << VALUE_BITS) | VALUE_INT;
        }

        uint64_t e1 = args[0], e2 = args[1];
        if ((e1 & VALUE_MASK) != VALUE_SET || (e2 & VALUE_MASK) != VALUE_SET) {
            return ctx_failure(ctx, "minus can only be applied to ints or sets");
        }
        int size1, size2;
        uint64_t *vals1, *vals2;
        if (e1 == VALUE_SET) {
            size1 = 0;
            vals1 = NULL;
        }
        else {
            vals1 = value_get(e1, &size1);
        }
        if (e2 == VALUE_SET) {
            size2 = 0;
            vals2 = NULL;
        }
        else {
            vals2 = value_get(e2, &size2);
        }
        uint64_t *vals = malloc(size2);
        size1 /= sizeof(uint64_t);
        size2 /= sizeof(uint64_t);

        uint64_t *p1 = vals1, *p2 = vals2, *q = vals;
        while (size1 > 0 && size2 > 0) {
            if (*p1 == *p2) {
                p1++; size1--;
                p2++; size2--;
            }
            else {
                int cmp = value_cmp(*p1, *p2);
                if (cmp < 0) {
                    p1++; size1--;
                }
                else {
                    assert(cmp > 0);
                    *q++ = *p2++; size2--;
                }
            }
        }
        while (size2 > 0) {
            *q++ = *p2++; size2--;
        }
        uint64_t result = value_put_set(vals, (char *) q - (char *) vals);
        free(vals);
        return result;
    }
}

uint64_t f_mod(struct state *state, struct context *ctx, uint64_t *args, int n){
    int64_t e1 = args[0], e2 = args[1];
    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "right argument to mod not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "left argument to mod not an integer");
    }
    int64_t result = (e2 >> VALUE_BITS) % (e1 >> VALUE_BITS);
    return (result << VALUE_BITS) | VALUE_INT;
}

uint64_t f_nametag(struct state *state, struct context *ctx, uint64_t *args, int n){
    return ctx->nametag;
}

uint64_t f_not(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    uint64_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_BOOL) {
        return ctx_failure(ctx, "not can only be applied to booleans");
    }
    return e ^ (1 << VALUE_BITS);
}

uint64_t f_plus(struct state *state, struct context *ctx, uint64_t *args, int n){
    if ((args[0] & VALUE_MASK) == VALUE_INT) {
        int64_t e1 = args[0];
        for (int i = 1; i < n; i++) {
            int64_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return ctx_failure(ctx,
                    "+: applied to mix of integers and other values");
            }
            e1 += e2 & ~VALUE_MASK;
        }
        return e1;
    }

    // get all the lists
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_DICT) {
            ctx_failure(ctx, "+: applied to mix of dictionaries and other values");
            free(vi);
            return 0;
        }
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

uint64_t f_power(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "right argument to ** not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "left argument to ** not an integer");
    }
    int64_t base = e2 >> VALUE_BITS;
    int64_t exp = e1 >> VALUE_BITS;

    int64_t result = 1;
    for (;;) {
        if (exp & 1) {
            result *= base;
        }
        exp >>= 1;
        if (exp == 0) {
            break;
        }
        base *= base;
    }

    return (result << VALUE_BITS) | VALUE_INT;
}

uint64_t f_range(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "right argument to .. not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "left argument to .. not an integer");
    }
    int64_t start = e2 >> VALUE_BITS;
    int64_t finish = e1 >> VALUE_BITS;
	if (finish < start) {
		return VALUE_SET;
	}
    int cnt = (finish - start) + 1;
	assert(cnt > 0);
	assert(cnt < 1000);		// seems unlikely...
    uint64_t *v = malloc(cnt * sizeof(uint64_t));
    for (int i = 0; i < cnt; i++) {
        v[i] = ((start + i) << VALUE_BITS) | VALUE_INT;
    }
    uint64_t result = value_put_set(v, cnt * sizeof(uint64_t));
    free(v);
    return result;
}

uint64_t f_shiftleft(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "right argument to << not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "left argument to << not an integer");
    }
    e1 >>= VALUE_BITS;
    e2 >>= VALUE_BITS;
    return ((e2 << e1) << VALUE_BITS) | VALUE_INT;
}

uint64_t f_shiftright(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "right argument to >> not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return ctx_failure(ctx, "left argument to >> not an integer");
    }
    e1 >>= VALUE_BITS;
    e2 >>= VALUE_BITS;
    return ((e2 >> e1) << VALUE_BITS) | VALUE_INT;
}

uint64_t f_times(struct state *state, struct context *ctx, uint64_t *args, int n){
    int64_t result = 1;
    int list = -1;
    for (int i = 0; i < n; i++) {
        int64_t e = args[i];
        if ((e & VALUE_MASK) == VALUE_DICT) {
            if (list >= 0) {
                return ctx_failure(ctx, "* can only have at most one list");
            }
            list = i;
        }
        else {
            if ((e & VALUE_MASK) != VALUE_INT) {
                return ctx_failure(ctx,
                    "* can only be applied to integers and at most one list");
            }
            result *= e >> VALUE_BITS;
        }
    }
    if (list < 0) {
        return (result << VALUE_BITS) | VALUE_INT;
    }
    int size;
    uint64_t *vals = value_get(args[list], &size);
    if (size == 0) {
        return VALUE_DICT;
    }
    uint64_t *r = malloc(result * size);
    unsigned int cnt = size / (2 * sizeof(uint64_t));
    int index = 0;
    for (int i = 0; i < result; i++) {
        for (int j = 0; j < cnt; j++) {
            r[2*index] = (index << VALUE_BITS) | VALUE_INT;
            r[2*index+1] = vals[2*j+1];
            index++;
        }
    }
    uint64_t v = value_put_dict(r, result * size);
    free(r);
    return v;
}

uint64_t f_union(struct state *state, struct context *ctx, uint64_t *args, int n){
    uint64_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            uint64_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return ctx_failure(ctx, "'|' applied to mix of ints and other types");
            }
            e1 |= e2;
        }
        return e1;
    }

    // get all the sets
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_SET) {
            return ctx_failure(ctx, "'|' applied to mix of sets and other types");
        }
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

    n = sort(vals, total / sizeof(uint64_t));
    uint64_t result = value_put_set(vals, n * sizeof(uint64_t));
    free(vi);
    free(vals);
    return result;
}

uint64_t f_xor(struct state *state, struct context *ctx, uint64_t *args, int n){
    uint64_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            uint64_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return ctx_failure(ctx, "'^' applied to mix of ints and other types");
            }
            e1 ^= e2;
        }
        return e1 | VALUE_INT;
    }

    // get all the sets
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_SET) {
            return ctx_failure(ctx, "'^' applied to mix of sets and other types");
        }
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

    // sort the values, but retain duplicates
    int cnt = total / sizeof(uint64_t);
    qsort(vals, cnt, sizeof(uint64_t), q_value_cmp);

    // Now remove the values that have an even number
    int i = 0, j = 0, k = 0;
    while (i < cnt) {
        while (i < cnt && vals[i] == vals[j]) {
            i++;
        }
        if ((i - j) % 2 != 0) {
            vals[k++] = vals[j];
        }
        j = i;
    }

    uint64_t result = value_put_set(vals, k * sizeof(uint64_t));
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
	{ "Invariant", init_Invariant, op_Invariant },
	{ "Jump", init_Jump, op_Jump },
	{ "JumpCond", init_JumpCond, op_JumpCond },
	{ "Load", init_Load, op_Load },
	{ "LoadVar", init_LoadVar, op_LoadVar },
	{ "Move", init_Move, op_Move },
	{ "Nary", init_Nary, op_Nary },
	{ "Pop", init_Pop, op_Pop },
	{ "Push", init_Push, op_Push },
	{ "ReadonlyDec", init_ReadonlyDec, op_ReadonlyDec },
	{ "ReadonlyInc", init_ReadonlyInc, op_ReadonlyInc },
	{ "Return", init_Return, op_Return },
	{ "Set", init_Set, op_Set },
	{ "Spawn", init_Spawn, op_Spawn },
	{ "Split", init_Split, op_Split },
	{ "Store", init_Store, op_Store },
	{ "StoreVar", init_StoreVar, op_StoreVar },
    { NULL, NULL, NULL }
};

struct f_info f_table[] = {
	{ "+", f_plus },
	{ "-", f_minus },
	{ "~", f_invert },
	{ "*", f_times },
	{ "/", f_div },
	{ "//", f_div },
	{ "%", f_mod },
	{ "**", f_power },
	{ "<<", f_shiftleft },
	{ ">>", f_shiftright },
    { "<", f_lt },
    { "<=", f_le },
    { ">=", f_ge },
    { ">", f_gt },
    { "|", f_union },
    { "&", f_intersection },
    { "^", f_xor },
    { "..", f_range },
    { "==", f_eq },
    { "!=", f_ne },
    { "abs", f_abs },
    { "all", f_all },
    { "any", f_any },
    { "atLabel", f_atLabel },
    { "in", f_in },
    { "IsEmpty", f_isEmpty },
    { "keys", f_keys },
    { "len", f_len },
    { "max", f_max },
    { "min", f_min },
	{ "mod", f_mod },
    { "nametag", f_nametag },
    { "not", f_not },
    { NULL, NULL }
};

struct op_info *ops_get(char *opname, int size){
    return dict_lookup(ops_map, opname, size);
}

void ops_init(){
    ops_map = dict_new(0);
    f_map = dict_new(0);

    for (struct op_info *oi = op_table; oi->name != NULL; oi++) {
        void **p = dict_insert(ops_map, oi->name, strlen(oi->name));
        *p = oi;
    }
    for (struct f_info *fi = f_table; fi->name != NULL; fi++) {
        void **p = dict_insert(f_map, fi->name, strlen(fi->name));
        *p = fi;
    }
}
