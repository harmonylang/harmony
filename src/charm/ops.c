#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <ctype.h>
#include <assert.h>

#ifndef HARMONY_COMBINE
#include "global.h"
#endif

#define MAX_ARITY   16

struct val_info {
    int size, index;
    uint64_t *vals;
};

struct f_info {
    char *name;
    uint64_t (*f)(struct state *state, struct context *ctx, uint64_t *args, int n);
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

static struct dict *ops_map, *f_map;
extern struct code *code;

bool is_sequential(uint64_t seqvars, uint64_t *indices, int n){
    assert((seqvars & VALUE_MASK) == VALUE_SET);
    int size;
    uint64_t *seqs = value_get(seqvars, &size);
    size /= sizeof(uint64_t);

    n *= sizeof(uint64_t);
    for (int i = 0; i < size; i++) {
        assert((seqs[i] & VALUE_MASK) == VALUE_ADDRESS);
        int sn;
        uint64_t *inds = value_get(seqs[i], &sn);
        if (n >= sn && memcmp(indices, inds, sn) == 0) {
            return true;
        }
    }
    return false;
}

uint64_t ctx_failure(struct context *ctx, char *fmt, ...){
    char *r;
    va_list args;

    assert(ctx->failure == 0);

    va_start(args, fmt);
    if (vasprintf(&r, fmt, args) < 0) {
		panic("ctx_failure: vasprintf");
	}
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
        panic("var_tree_rec: bad vartree type");
        return 0;
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
        panic("var_dump: bad vartree type");
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
        panic("var_parse: TODO");
    }
    else {
        vt->type = VT_NAME;
        int i = *index;
        assert(isalpha(s[i]) || s[i] == '_' || s[i] == '$');
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

void interrupt_invoke(struct context **pctx){
    assert(!(*pctx)->interruptlevel);
	assert(((*pctx)->trap_pc & VALUE_MASK) == VALUE_PC);
    ctx_push(pctx, ((*pctx)->pc << VALUE_BITS) | VALUE_PC);
    ctx_push(pctx, (CALLTYPE_INTERRUPT << VALUE_BITS) | VALUE_INT);
    ctx_push(pctx, (*pctx)->trap_arg);
    (*pctx)->pc = (*pctx)->trap_pc >> VALUE_BITS;
    (*pctx)->trap_pc = 0;
    (*pctx)->interruptlevel = true;
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
    panic("dict_load");
    return 0;
}

uint64_t dict_remove(uint64_t dict, uint64_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        return VALUE_DICT;
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

bool ind_tryload(uint64_t dict, uint64_t *indices, int n, uint64_t *result){
    uint64_t d = dict;
    for (int i = 0; i < n; i++) {
        if (!dict_tryload(d, indices[i], &d)) {
            return false;
        }
    }
    *result = d;
    return true;
}

bool ind_trystore(uint64_t dict, uint64_t *indices, int n, uint64_t value, uint64_t *result){
    assert((dict & VALUE_MASK) == VALUE_DICT);
    assert(n > 0);

    if (n == 1) {
        *result = dict_store(dict, indices[0], value);
        return true;
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
                uint64_t nd;
                if (!ind_trystore(d, indices + 1, n - 1, value, &nd)) {
                    return false;
                }
                if (d == nd) {
                    *result = dict;
                    return true;
                }
                int n = size * sizeof(uint64_t);
                uint64_t *copy = malloc(n);
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                uint64_t v = value_put_dict(copy, n);
                free(copy);
                *result = v;
                return true;
            }
            /* 
                if (value_cmp(vals[i], key) > 0) {
                    assert(false);
                }
            */
        }
    }
    return false;
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

        panic("ind_remove");        // TODO.  Should this return orig dict?
        return 0;
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
        {
            uint64_t v;
            if (!dict_tryload(method, e, &v)) {
                char *m = value_string(method);
                char *x = value_string(e);
                ctx_failure(*pctx, "Bad index %s: not in %s", x, m);
                free(m);
                free(x);
                return;
            }
            ctx_push(pctx, v);
            (*pctx)->pc++;
        }
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
    panic("op_Choose: should not be called");
}

void op_Continue(const void *env, struct state *state, struct context **pctx){
    (*pctx)->pc++;
}

void op_Cut(const void *env, struct state *state, struct context **pctx){
    const struct env_Cut *ec = env;
    struct context *ctx = *pctx;

    uint64_t v = dict_load(ctx->vars, ec->set);
    if ((v & VALUE_MASK) == VALUE_SET) {
        assert(v != VALUE_SET);
        void *p = (void *) (v & ~VALUE_MASK);

        int size;
        uint64_t *vals = dict_retrieve(p, &size);
        assert(size > 0);

        ctx->vars = dict_store(ctx->vars, ec->set, value_put_set(&vals[1], size - sizeof(uint64_t)));
        ctx->vars = dict_store(ctx->vars, ec->var, vals[0]);
        (*pctx)->pc++;
        return;
    }
    if ((v & VALUE_MASK) == VALUE_DICT) {
        assert(v != VALUE_DICT);
        void *p = (void *) (v & ~VALUE_MASK);

        int size;
        uint64_t *vals = dict_retrieve(p, &size);
        assert(size > 0);

        ctx->vars = dict_store(ctx->vars, ec->set, value_put_dict(&vals[2], size - 2 * sizeof(uint64_t)));
        ctx->vars = dict_store(ctx->vars, ec->var, vals[1]);
        (*pctx)->pc++;
        return;
    }
    panic("op_Cut: not a set or dict");
}

void ext_Del(const void *env, struct state *state, struct context **pctx,
                                                        struct access_info *ai){
    assert((state->vars & VALUE_MASK) == VALUE_DICT);
    uint64_t av = ctx_pop(pctx);
    assert((av & VALUE_MASK) == VALUE_ADDRESS);
    assert(av != VALUE_ADDRESS);

    int size;
    uint64_t *indices = value_get(av, &size);
    size /= sizeof(uint64_t);
    if (ai != NULL) {
        ai->indices = indices;
        ai->n = size;
        ai->load = false;
    }
    state->vars = ind_remove(state->vars, indices, size);

    (*pctx)->pc++;
}

void op_Del(const void *env, struct state *state, struct context **pctx){
    ext_Del(env, state, pctx, NULL);
}

void op_DelVar(const void *env, struct state *state, struct context **pctx){
    const struct env_DelVar *ed = env;
    (*pctx)->vars = dict_remove((*pctx)->vars, ed->name);
    (*pctx)->pc++;
}

void op_Dup(const void *env, struct state *state, struct context **pctx){
    uint64_t v = ctx_pop(pctx);
    ctx_push(pctx, v);
    ctx_push(pctx, v);
    (*pctx)->pc++;
}

void op_Frame(const void *env, struct state *state, struct context **pctx){
    static uint64_t result = 0;

    if (result == 0) {
        result = value_put_atom("result", 6);
    }

    const struct env_Frame *ef = env;
    if (false) {
        printf("FRAME %d %d %"PRIx64" ", (*pctx)->pc, (*pctx)->sp, ef->name);
        var_dump(ef->args);
        printf("\n");
    }

    // peek at argument
    uint64_t arg = ctx_pop(pctx);
    ctx_push(pctx, arg);

    uint64_t oldvars = (*pctx)->vars;

    // try to match against parameters
    (*pctx)->vars = dict_store(VALUE_DICT, result, VALUE_DICT);
    var_match(*pctx, ef->args, arg);
    if ((*pctx)->failure != 0) {
        return;
    }
 
    ctx_push(pctx, oldvars);
    ctx_push(pctx, ((*pctx)->fp << VALUE_BITS) | VALUE_INT);

    struct context *ctx = *pctx;
    ctx->fp = ctx->sp;
    ctx->pc += 1;
}

void op_Go(const void *env, struct state *state, struct context **pctx){
    uint64_t ctx = ctx_pop(pctx);
    if ((ctx & VALUE_MASK) != VALUE_CONTEXT) {
        ctx_failure(*pctx, "Go: not a context");
        return;
    }

    // Remove from stopbag if it's there
    uint64_t count;
    if (dict_tryload(state->stopbag, ctx, &count)) {
        assert((count & VALUE_MASK) == VALUE_INT);
        assert(count != VALUE_INT);
        count -= 1 << VALUE_BITS;
        if (count != VALUE_INT) {
            state->stopbag = dict_store(state->stopbag, ctx, count);
        }
        else {
            state->stopbag = dict_remove(state->stopbag, ctx);
        }
    }

    uint64_t result = ctx_pop(pctx);
    struct context *copy = value_copy(ctx, NULL);
    ctx_push(&copy, result);
    copy->stopped = false;
    uint64_t v = value_put_context(copy);
    free(copy);
    state->ctxbag = bag_add(state->ctxbag, v);
    (*pctx)->pc++;
}

void op_IncVar(const void *env, struct state *state, struct context **pctx){
    const struct env_IncVar *ei = env;
    struct context *ctx = *pctx;

    assert((ctx->vars & VALUE_MASK) == VALUE_DICT);

    uint64_t v = dict_load(ctx->vars, ei->name);
    assert((v & VALUE_MASK) == VALUE_INT);
    v += 1 << VALUE_BITS;
    ctx->vars = dict_store(ctx->vars, ei->name, v);
    (*pctx)->pc++;
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

void ext_Load(const void *env, struct state *state, struct context **pctx,
                                                        struct access_info *ai){
    const struct env_Load *el = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    uint64_t v;
    if (el == 0) {
        uint64_t av = ctx_pop(pctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);
        if (ai != NULL) {
            ai->indices = indices;
            ai->n = size;
            ai->load = true;
        }

        if (!ind_tryload(state->vars, indices, size, &v)) {
            char *x = indices_string(indices, size);
            ctx_failure(*pctx, "Load: unknown address %s", x);
            free(x);
            return;
        }
        ctx_push(pctx, v);
    }
    else {
        if (ai != NULL) {
            ai->indices = el->indices;
            ai->n = el->n;
            ai->load = true;
        }
        if (!ind_tryload(state->vars, el->indices, el->n, &v)) {
            char *x = indices_string(el->indices, el->n);
            ctx_failure(*pctx, "Load: unknown variable %s", x);
            free(x);
            return;
        }
        ctx_push(pctx, v);
    }
    (*pctx)->pc++;
}

void op_Load(const void *env, struct state *state, struct context **pctx){
    ext_Load(env, state, pctx, NULL);
}

void op_LoadVar(const void *env, struct state *state, struct context **pctx){
    const struct env_LoadVar *el = env;
    assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);

    uint64_t v;
    if (el == NULL) {
        uint64_t av = ctx_pop(pctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);

        if (!ind_tryload((*pctx)->vars, indices, size, &v)) {
            ctx_failure(*pctx, "Loadvar: unknown address");
            return;
        }
        ctx_push(pctx, v);
    }
    else {
        if (!dict_tryload((*pctx)->vars, el->name, &v)) {
            ctx_failure(*pctx, "Loadvar: unknown variable");
            return;
        }
        ctx_push(pctx, v);
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
    if ((*pctx)->sp == 0) {     // __init__    TODO: no longer the case
        assert(false);
        (*pctx)->terminated = true;
        if (false) {
            printf("RETURN INIT\n");
        }
    }
    else {
        uint64_t result = dict_load((*pctx)->vars, value_put_atom("result", 6));
        uint64_t fp = ctx_pop(pctx);
        if ((fp & VALUE_MASK) != VALUE_INT) {
            printf("XXX %d %d %s\n", (*pctx)->pc, (*pctx)->sp, value_string(fp));
            ctx_failure(*pctx, "XXX");
            return;
            // exit(1);
        }
        assert((fp & VALUE_MASK) == VALUE_INT);
        (*pctx)->fp = fp >> VALUE_BITS;
        (*pctx)->vars = ctx_pop(pctx);
        assert(((*pctx)->vars & VALUE_MASK) == VALUE_DICT);
        (void) ctx_pop(pctx);   // argument saved for stack trace
        if ((*pctx)->sp == 0) {     // __init__
            (*pctx)->terminated = true;
            if (false) {
                printf("RETURN INIT\n");
            }
            return;
        }
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
		case CALLTYPE_INTERRUPT:
			assert((*pctx)->interruptlevel);
			(*pctx)->interruptlevel = false;
			uint64_t pc = ctx_pop(pctx);
			assert((pc & VALUE_MASK) == VALUE_PC);
			pc >>= VALUE_BITS;
			assert(pc != (*pctx)->pc);
			(*pctx)->pc = pc;
			break;
        default:
            panic("op_Return: bad call type");
        }
    }
}

void op_Sequential(const void *env, struct state *state, struct context **pctx){
    uint64_t addr = ctx_pop(pctx);
    if ((addr & VALUE_MASK) != VALUE_ADDRESS) {
        ctx_failure(*pctx, "Sequential: not an address");
        return;
    }

    /* Insert in state's set of sequential variables.
     */
    int size;
    uint64_t *seqs = value_copy(state->seqs, &size);
    size /= sizeof(uint64_t);
    int i;
    for (i = 0; i < size; i++) {
        int k = value_cmp(seqs[i], addr);
        if (k == 0) {
            free(seqs);
            (*pctx)->pc++;
            return;
        }
        if (k > 0) {
            break;
        }
    }
    seqs = realloc(seqs, (size + 1) * sizeof(uint64_t));
    memmove(&seqs[i + 1], &seqs[i], (size - i) * sizeof(uint64_t));
    seqs[i] = addr;
    state->seqs = value_put_set(seqs, (size + 1) * sizeof(uint64_t));
    free(seqs);
    (*pctx)->pc++;
}

// sort two key/value pairs
static int q_kv_cmp(const void *e1, const void *e2){
    const uint64_t *kv1 = (const uint64_t *) e1;
    const uint64_t *kv2 = (const uint64_t *) e2;

    int k = value_cmp(kv1[0], kv2[0]);
    if (k != 0) {
        return k;
    }
    return value_cmp(kv1[1], kv2[1]);
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

void op_SetIntLevel(const void *env, struct state *state, struct context **pctx){
	bool oldlevel = (*pctx)->interruptlevel;
	uint64_t newlevel =  ctx_pop(pctx);
    if ((newlevel & VALUE_MASK) != VALUE_BOOL) {
        ctx_failure(*pctx, "setintlevel can only be set to a boolean");
        return;
    }
    (*pctx)->interruptlevel = newlevel >> VALUE_BITS;
	ctx_push(pctx, (oldlevel << VALUE_BITS) | VALUE_BOOL);
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
    if ((pc & VALUE_MASK) != VALUE_PC) {
        ctx_failure(*pctx, "spawn: not a method");
        return;
    }
    pc >>= VALUE_BITS;

    assert(pc < code_len);
    assert(strcmp(code[pc].oi->name, "Frame") == 0);
    uint64_t arg = ctx_pop(pctx);
    uint64_t this = ctx_pop(pctx);
    if (false) {
        printf("SPAWN %"PRIx64" %"PRIx64" %"PRIx64"\n", pc, arg, this);
    }

    struct context *ctx = new_alloc(struct context);

    const struct env_Frame *ef = code[pc].env;
    ctx->name = ef->name;
    ctx->arg = arg;
    ctx->this = this;
    ctx->entry = (pc << VALUE_BITS) | VALUE_PC;
    ctx->pc = pc;
    ctx->vars = VALUE_DICT;
    ctx->interruptlevel = VALUE_FALSE;
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
    if (type != VALUE_DICT && type != VALUE_SET) {
        ctx_failure(*pctx, "Can only split tuples or sets");
        return;
    }
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
    panic("op_Split: not a set or dict");
}

void op_Stop(const void *env, struct state *state, struct context **pctx){
    const struct env_Stop *es = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    if ((*pctx)->readonly > 0) {
        ctx_failure(*pctx, "Stop: in read-only mode");
        return;
    }

    if (es == 0) {
        uint64_t av = ctx_pop(pctx);
        if ((av & VALUE_MASK) != VALUE_ADDRESS) {
            ctx_failure(*pctx, "Stop: not an address");
            return;
        }
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);

        (*pctx)->stopped = true;
        (*pctx)->pc++;
        uint64_t v = value_put_context(*pctx);

        if (!ind_trystore(state->vars, indices, size, v, &state->vars)) {
            ctx_failure(*pctx, "Store: bad address");
            return;
        }
    }
    else {
        (*pctx)->stopped = true;
        (*pctx)->pc++;
        uint64_t v = value_put_context(*pctx);

        if (!ind_trystore(state->vars, es->indices, es->n, v, &state->vars)) {
            ctx_failure(*pctx, "Store: bad variable");
            return;
        }
    }
}

void ext_Store(const void *env, struct state *state, struct context **pctx,
                                                        struct access_info *ai){
    const struct env_Store *es = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    if ((*pctx)->readonly > 0) {
        ctx_failure(*pctx, "Store: in read-only mode");
        return;
    }

    uint64_t v = ctx_pop(pctx);

    if (es == 0) {
        uint64_t av = ctx_pop(pctx);
        if ((av & VALUE_MASK) != VALUE_ADDRESS) {
            ctx_failure(*pctx, "Store: not an address");
            return;
        }
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        uint64_t *indices = value_get(av, &size);
        size /= sizeof(uint64_t);
        if (ai != NULL) {
            ai->indices = indices;
            ai->n = size;
            ai->load = is_sequential(state->seqs, ai->indices, ai->n);
        }

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

        if (!ind_trystore(state->vars, indices, size, v, &state->vars)) {
            ctx_failure(*pctx, "Store: bad address");
            return;
        }
    }
    else {
        if (ai != NULL) {
            ai->indices = es->indices;
            ai->n = es->n;
            ai->load = is_sequential(state->seqs, ai->indices, ai->n);
        }
        if (!ind_trystore(state->vars, es->indices, es->n, v, &state->vars)) {
            ctx_failure(*pctx, "Store: bad variable");
            return;
        }
    }
    (*pctx)->pc++;
}

void op_Store(const void *env, struct state *state, struct context **pctx){
    ext_Store(env, state, pctx, NULL);
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

        if (!ind_trystore((*pctx)->vars, indices, size, v, &(*pctx)->vars)) {
            ctx_failure(*pctx, "StoreVar: bad address");
            return;
        }
        (*pctx)->pc++;
    }
    else {
        var_match(*pctx, es->args, v);
        if ((*pctx)->failure == 0) {
            (*pctx)->pc++;
        }
    }
}

void op_Trap(const void *env, struct state *state, struct context **pctx){
    extern int code_len;

    (*pctx)->trap_pc = ctx_pop(pctx);
    if (((*pctx)->trap_pc & VALUE_MASK) != VALUE_PC) {
        ctx_failure(*pctx, "trap: not a method");
        return;
    }
    int pc = (*pctx)->trap_pc >> VALUE_BITS;
    assert(pc < code_len);
    assert(strcmp(code[pc].oi->name, "Frame") == 0);
    (*pctx)->trap_arg = ctx_pop(pctx);
    (*pctx)->pc++;
}

void *init_Address(struct dict *map){ return NULL; }
void *init_Apply(struct dict *map){ return NULL; }
void *init_Assert(struct dict *map){ return NULL; }
void *init_Assert2(struct dict *map){ return NULL; }
void *init_AtomicDec(struct dict *map){ return NULL; }
void *init_AtomicInc(struct dict *map){ return NULL; }
void *init_Choose(struct dict *map){ return NULL; }
void *init_Continue(struct dict *map){ return NULL; }
void *init_Del(struct dict *map){ return NULL; }
void *init_Dup(struct dict *map){ return NULL; }
void *init_Go(struct dict *map){ return NULL; }
void *init_Pop(struct dict *map){ return NULL; }
void *init_ReadonlyDec(struct dict *map){ return NULL; }
void *init_ReadonlyInc(struct dict *map){ return NULL; }
void *init_Return(struct dict *map){ return NULL; }
void *init_Sequential(struct dict *map){ return NULL; }
void *init_SetIntLevel(struct dict *map){ return NULL; }
void *init_Spawn(struct dict *map){ return NULL; }
void *init_Trap(struct dict *map){ return NULL; }

void *init_Cut(struct dict *map){
    struct env_Cut *env = new_alloc(struct env_Cut);
    struct json_value *set = dict_lookup(map, "set", 3);
    assert(set->type == JV_ATOM);
    env->set = value_put_atom(set->u.atom.base, set->u.atom.len);
    struct json_value *var = dict_lookup(map, "var", 3);
    assert(var->type == JV_ATOM);
    env->var = value_put_atom(var->u.atom.base, var->u.atom.len);
    return env;
}

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

void *init_IncVar(struct dict *map){
    struct env_IncVar *env = new_alloc(struct env_IncVar);
    struct json_value *name = dict_lookup(map, "value", 5);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(name->u.atom.base, name->u.atom.len);
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

void *init_Stop(struct dict *map){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Stop *env = new_alloc(struct env_Stop);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(uint64_t));
    for (int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(index->u.map);
    }
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

uint64_t nametag(struct context *ctx){
    uint64_t nt = dict_store(VALUE_DICT,
            (0 << VALUE_BITS) | VALUE_INT, ctx->entry);
    return dict_store(nt,
            (1 << VALUE_BITS) | VALUE_INT, ctx->arg);
}

uint64_t f_atLabel(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 1);
    if (ctx->atomic == 0) {
        return ctx_failure(ctx, "atLabel: can only be called in atomic mode");
    }
    uint64_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_PC) {
        return ctx_failure(ctx, "atLabel: not a method");
    }
    e >>= VALUE_BITS;

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
        if (ctx->pc == e) {
            bag = bag_add(bag, nametag(ctx));
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
    e1 >>= VALUE_BITS;
    if (e1 == 0) {
        return ctx_failure(ctx, "divide by zero");
    }
    int64_t result = (e2 >> VALUE_BITS) / e1;
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
	if (e1 == VALUE_SET) {
		return VALUE_SET;
	}
    if ((e1 & VALUE_MASK) == VALUE_SET) {
        // get all the sets
		assert(n > 0);
        struct val_info *vi = malloc(n * sizeof(*vi));
        int min_size = vi[0].size;              // minimum set size
        uint64_t max_val = vi[0].vals[0];       // maximum value over the minima of all sets
        for (int i = 1; i < n; i++) {
            if ((args[i] & VALUE_MASK) != VALUE_SET) {
                return ctx_failure(ctx, "'&' applied to mix of sets and other types");
            }
            if (args[i] == VALUE_SET) {
                min_size = 0;
            }
            else {
                vi[i].vals = value_get(args[i], &vi[i].size); 
                vi[i].index = 0;
				if (vi[i].size < min_size) {
					min_size = vi[i].size;
				}
				if (value_cmp(vi[i].vals[0], max_val) > 0) {
					max_val = vi[i].vals[0];
				}
            }
        }

        // If any are empty lists, we're done.
        if (min_size == 0) {
            return VALUE_SET;
        }

        // Allocate sufficient memory.
        uint64_t *vals = malloc((size_t) min_size), *v = vals;

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

	if (e1 == VALUE_DICT) {
		return VALUE_DICT;
	}
    if ((e1 & VALUE_MASK) != VALUE_DICT) {
        return ctx_failure(ctx, "'&' can only be applied to ints and dicts");
    }
    // get all the dictionaries
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_DICT) {
            return ctx_failure(ctx, "'&' applied to mix of dictionaries and other types");
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

    // If all are empty dictionaries, we're done.
    if (total == 0) {
        return VALUE_DICT;
    }

    // Concatenate the dictionaries
    uint64_t *vals = malloc(total), *v;
    total = 0;
    for (int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // sort lexicographically, leaving duplicate keys
    int cnt = total / (2 * sizeof(uint64_t));
    qsort(vals, cnt, 2 * sizeof(uint64_t), q_kv_cmp);

    // now only leave the min value for duplicate keys
    int in = 0, out = 0;
    for (;;) {
        // if there are fewer than n copies of the key, then it's out
        if (in + n > cnt) {
            break;
        }
        int i;
        for (i = in + 1; i < in + n; i++) {
            if (vals[2*i] != vals[2*in]) {
                break;
            }
        }
        if (i == in + n) {
            // copy over the first value
            vals[2*out] = vals[2*in];
            vals[2*out+1] = vals[2*in+1];
            out++;
        }
        in = i;
    }

    uint64_t result = value_put_dict(vals, 2 * out * sizeof(uint64_t));
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
    panic("op_isEmpty: not a set or dict");
    return 0;
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
		return VALUE_INT;
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
        uint64_t max = v[1];
        for (int i = 0; i < size; i++) {
            if (value_cmp(v[2*i+1], max) > 0) {
                max = v[2*i+1];
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
        uint64_t min = v[1];
        for (int i = 0; i < size; i++) {
            if (value_cmp(v[2*i+1], min) < 0) {
                min = v[2*i+1];
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
        if (e == VALUE_MAX) {
            return ((uint64_t) VALUE_MIN << VALUE_BITS) | VALUE_INT;
        }
        if (e == VALUE_MIN) {
            return (VALUE_MAX << VALUE_BITS) | VALUE_INT;
        }
        if (-e <= VALUE_MIN || -e >= VALUE_MAX) {
            return ctx_failure(ctx, "unary minus overflow (model too large)");
        }
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
            int64_t result = e2 - e1;
            if (result <= VALUE_MIN || result >= VALUE_MAX) {
                return ctx_failure(ctx, "minus overflow (model too large)");
            }
            return (result << VALUE_BITS) | VALUE_INT;
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
    int64_t mod = (e1 >> VALUE_BITS);
    int64_t result = (e2 >> VALUE_BITS) % mod;
    if (result < 0) {
        result += mod;
    }
    return (result << VALUE_BITS) | VALUE_INT;
}

uint64_t f_get_context(struct state *state, struct context *ctx, uint64_t *args, int n){
    return value_put_context(ctx);
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
    int64_t e1 = args[0];
    if ((e1 & VALUE_MASK) == VALUE_INT) {
        e1 >>= VALUE_BITS;
        for (int i = 1; i < n; i++) {
            int64_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return ctx_failure(ctx,
                    "+: applied to mix of integers and other values");
            }
            e2 >>= VALUE_BITS;
            int64_t sum = e1 + e2;
            if (sum <= VALUE_MIN || sum >= VALUE_MAX) {
                return ctx_failure(ctx,
                    "+: integer overflow (model too large)");
            }
            e1 = sum;
        }
        return (e1 << VALUE_BITS) | VALUE_INT;
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
    if (exp == 0) {
        return (1 << VALUE_BITS) | VALUE_INT;
    }
    if (exp < 0) {
        return ctx_failure(ctx, "**: negative exponent");
    }

    int64_t result = 1, orig = base;
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
    if (result < orig) {
        // TODO.  Improve overflow detection
        return ctx_failure(ctx, "**: overflow (model too large)");
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

uint64_t f_dict_add(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 3);
    int64_t value = args[0], key = args[1], dict = args[2];
    assert((dict & VALUE_MASK) == VALUE_DICT);
    int size;
    uint64_t *vals = value_get(dict, &size), *v;

    int i = 0, cmp = 1;
    for (v = vals; i < size; i += 2 * sizeof(uint64_t), v += 2) {
        cmp = value_cmp(key, *v);
        if (cmp <= 0) {
            break;
        }
    }

    // See if we found the key.  In that case, we take the bigger value.
    if (cmp == 0) {
        cmp = value_cmp(value, v[1]);
        if (cmp <= 0) {
            return dict;
        }
        uint64_t *nvals = malloc(size);
        memcpy(nvals, vals, size);
        * (uint64_t *) ((char *) nvals + (i + sizeof(uint64_t))) = value;

        uint64_t result = value_put_dict(nvals, size);
        free(nvals);
        return result;
    }
    else {
        uint64_t *nvals = malloc(size + 2*sizeof(uint64_t));
        memcpy(nvals, vals, i);
        * (uint64_t *) ((char *) nvals + i) = key;
        * (uint64_t *) ((char *) nvals + (i + sizeof(uint64_t))) = value;
        memcpy((char *) nvals + i + 2*sizeof(uint64_t), v, size - i);

        uint64_t result = value_put_dict(nvals, size + 2*sizeof(uint64_t));
        free(nvals);
        return result;
    }
}

uint64_t f_set_add(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int64_t elt = args[0], set = args[1];
    assert((set & VALUE_MASK) == VALUE_SET);
    int size;
    uint64_t *vals = value_get(set, &size), *v;

    int i = 0;
    for (v = vals; i < size; i += sizeof(uint64_t), v++) {
        int cmp = value_cmp(elt, *v);
        if (cmp == 0) {
            return set;
        }
        if (cmp < 0) {
            break;
        }
    }

    uint64_t *nvals = malloc(size + sizeof(uint64_t));
    memcpy(nvals, vals, i);
    * (uint64_t *) ((char *) nvals + i) = elt;
    memcpy((char *) nvals + i + sizeof(uint64_t), v, size - i);

    uint64_t result = value_put_set(nvals, size + sizeof(uint64_t));
    free(nvals);
    return result;
}

uint64_t f_bag_add(struct state *state, struct context *ctx, uint64_t *args, int n){
    assert(n == 2);
    int64_t elt = args[0], dict = args[1];
    assert((dict & VALUE_MASK) == VALUE_DICT);
    int size;
    uint64_t *vals = value_get(dict, &size), *v;

    int i = 0, cmp = 1;
    for (v = vals; i < size; i += 2 * sizeof(uint64_t), v++) {
        cmp = value_cmp(elt, *v);
        if (cmp <= 0) {
            break;
        }
    }

    if (cmp == 0) {
        assert((v[1] & VALUE_MASK) == VALUE_INT);
        int cnt = (v[1] >> VALUE_BITS) + 1;
        uint64_t *nvals = malloc(size);
        memcpy(nvals, vals, size);
        * (uint64_t *) ((char *) nvals + (i + sizeof(uint64_t))) =
                                        (cnt << VALUE_BITS) | VALUE_INT;

        uint64_t result = value_put_dict(nvals, size);
        free(nvals);
        return result;
    }
    else {
        uint64_t *nvals = malloc(size + 2*sizeof(uint64_t));
        memcpy(nvals, vals, i);
        * (uint64_t *) ((char *) nvals + i) = elt;
        * (uint64_t *) ((char *) nvals + (i + sizeof(uint64_t))) =
                                        (1 << VALUE_BITS) | VALUE_INT;
        memcpy((char *) nvals + i + 2*sizeof(uint64_t), v, size - i);

        uint64_t result = value_put_dict(nvals, size + 2*sizeof(uint64_t));
        free(nvals);
        return result;
    }
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
    if (e1 < 0) {
        return ctx_failure(ctx, "<<: negative shift count");
    }
    e2 >>= VALUE_BITS;
    int64_t result = e2 << e1;
    if (((result << VALUE_BITS) >> VALUE_BITS) != result) {
        return ctx_failure(ctx, "<<: overflow (model too large)");
    }
    if (result <= VALUE_MIN || result >= VALUE_MAX) {
        return ctx_failure(ctx, "<<: overflow (model too large)");
    }
    return (result << VALUE_BITS) | VALUE_INT;
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
    if (e1 < 0) {
        return ctx_failure(ctx, ">>: negative shift count");
    }
    e1 >>= VALUE_BITS;
    e2 >>= VALUE_BITS;
    return ((e2 >> e1) << VALUE_BITS) | VALUE_INT;
}

uint64_t f_times(struct state *state, struct context *ctx, uint64_t *args, int n){
    int64_t result = 1;
    int list = -1;
    bool haszero = false;
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
            e >>= VALUE_BITS;
            if (e == 0) {
                result = 0;
            }
            else {
                int64_t product = result * e;
                if (product / result != e) {
                    return ctx_failure(ctx, "*: overflow (model too large)");
                }
                result = product;
            }
        }
    }
    if (list < 0) {
        if (result != (result << VALUE_BITS) >> VALUE_BITS) {
            return ctx_failure(ctx, "*: overflow (model too large)");
        }
        return (result << VALUE_BITS) | VALUE_INT;
    }
    if (result == 0) {
        return VALUE_DICT;
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

    if ((e1 & VALUE_MASK) == VALUE_SET) {
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

    if ((e1 & VALUE_MASK) != VALUE_DICT) {
        return ctx_failure(ctx, "'|' can only be applied to ints and dicts");
    }
    // get all the dictionaries
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_DICT) {
            return ctx_failure(ctx, "'|' applied to mix of dictionaries and other types");
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

    // If all are empty dictionaries, we're done.
    if (total == 0) {
        return VALUE_DICT;
    }

    // Concatenate the dictionaries
    uint64_t *vals = malloc(total), *v;
    total = 0;
    for (int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // sort lexicographically, leaving duplicate keys
    int cnt = total / (2 * sizeof(uint64_t));
    qsort(vals, cnt, 2 * sizeof(uint64_t), q_kv_cmp);

    // now only leave the max value for duplicate keys
    n = 0;
    for (int i = 1; i < cnt; i++) {
        if (vals[2*i] != vals[2*n]) {
            n++;
        }
        vals[2*n] = vals[2*i];
        vals[2*n+1] = vals[2*i+1];
    }
    n++;

    uint64_t result = value_put_dict(vals, 2 * n * sizeof(uint64_t));
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
	{ "Continue", init_Continue, op_Continue },
	{ "Cut", init_Cut, op_Cut },
	{ "Del", init_Del, op_Del },
	{ "DelVar", init_DelVar, op_DelVar },
	{ "Dup", init_Dup, op_Dup },
	{ "Frame", init_Frame, op_Frame },
	{ "Go", init_Go, op_Go },
	{ "IncVar", init_IncVar, op_IncVar },
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
	{ "Sequential", init_Sequential, op_Sequential },
	{ "SetIntLevel", init_SetIntLevel, op_SetIntLevel },
	{ "Spawn", init_Spawn, op_Spawn },
	{ "Split", init_Split, op_Split },
	{ "Stop", init_Stop, op_Stop },
	{ "Store", init_Store, op_Store },
	{ "StoreVar", init_StoreVar, op_StoreVar },
	{ "Trap", init_Trap, op_Trap },
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
    { "BagAdd", f_bag_add },
    { "DictAdd", f_dict_add },
    { "get_context", f_get_context },
    { "in", f_in },
    { "IsEmpty", f_isEmpty },
    { "keys", f_keys },
    { "len", f_len },
    { "max", f_max },
    { "min", f_min },
	{ "mod", f_mod },
    { "not", f_not },
    { "SetAdd", f_set_add },
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
