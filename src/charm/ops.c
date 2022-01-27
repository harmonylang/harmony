#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#ifndef HARMONY_COMBINE
#include "ops.h"
#endif

#define MAX_ARITY   16

struct val_info {
    int size, index;
    hvalue_t *vals;
};

struct f_info {
    char *name;
    hvalue_t (*f)(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values);
};

struct var_tree {
    enum { VT_NAME, VT_TUPLE } type;
    union {
        hvalue_t name;
        struct {
            int n;
            struct var_tree **elements;
        } tuple;
    } u;
};

// These are initialized in ops_init and are immutable.
static struct dict *ops_map, *f_map;
static hvalue_t underscore, this_atom;

bool is_sequential(hvalue_t seqvars, hvalue_t *indices, int n){
    assert((seqvars & VALUE_MASK) == VALUE_SET);
    int size;
    hvalue_t *seqs = value_get(seqvars, &size);
    size /= sizeof(hvalue_t);

    n *= sizeof(hvalue_t);
    for (int i = 0; i < size; i++) {
        assert((seqs[i] & VALUE_MASK) == VALUE_ADDRESS);
        int sn;
        hvalue_t *inds = value_get(seqs[i], &sn);
        if (n >= sn && sn >= 0 && memcmp(indices, inds, sn) == 0) {
            return true;
        }
    }
    return false;
}

hvalue_t var_match_rec(struct context *ctx, struct var_tree *vt, struct values_t *values,
                            hvalue_t arg, hvalue_t vars){
    switch (vt->type) {
    case VT_NAME:
        if (vt->u.name == underscore) {
            return vars;
        }
        return value_dict_store(values, vars, vt->u.name, arg);
    case VT_TUPLE:
        if ((arg & VALUE_MASK) != VALUE_DICT) {
            if (vt->u.tuple.n == 0) {
                return value_ctx_failure(ctx, values, "match: expected ()");
            }
            else {
                return value_ctx_failure(ctx, values, "match: expected a tuple");
            }
        }
        if (arg == VALUE_DICT) {
            if (vt->u.tuple.n != 0) {
                return value_ctx_failure(ctx, values, "match: expected a %d-tuple",
                                                vt->u.tuple.n);
            }
            return vars;
        }
        if (vt->u.tuple.n == 0) {
            return value_ctx_failure(ctx, values, "match: expected an empty tuple");
        }
        int size;
        hvalue_t *vals = value_get(arg, &size);
        size /= 2 * sizeof(hvalue_t);
        if (vt->u.tuple.n != size) {
            return value_ctx_failure(ctx, values, "match: tuple size mismatch");
        }
        for (int i = 0; i < size; i++) {
            if (vals[2*i] != (((hvalue_t) i << VALUE_BITS) | VALUE_INT)) {
                return value_ctx_failure(ctx, values, "match: not a tuple");
            }
            vars = var_match_rec(ctx, vt->u.tuple.elements[i], values, vals[2*i+1], vars);
        }
        return vars;
    default:
        panic("var_tree_rec: bad vartree type");
        return 0;
    }
}

void var_match(struct context *ctx, struct var_tree *vt, struct values_t *values, hvalue_t arg){
    hvalue_t vars = var_match_rec(ctx, vt, values, arg, ctx->vars);
    if (ctx->failure == 0) {
        ctx->vars = vars;
    }
}

static void skip_blanks(char *s, int len, int *index){
    while (*index < len && s[*index] == ' ') {
        (*index)++;
    }
}

struct var_tree *var_parse(struct values_t *values, char *s, int len, int *index){
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
                struct var_tree *elt = var_parse(values, s, len, index);
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
        vt->u.name = value_put_atom(values, &s[*index], i - *index);
        *index = i;
    }
    return vt;
}

void interrupt_invoke(struct step *step){
    assert(!step->ctx->interruptlevel);
	assert((step->ctx->trap_pc & VALUE_MASK) == VALUE_PC);
    value_ctx_push(&step->ctx, (step->ctx->pc << VALUE_BITS) | VALUE_PC);
    value_ctx_push(&step->ctx, (CALLTYPE_INTERRUPT << VALUE_BITS) | VALUE_INT);
    value_ctx_push(&step->ctx, step->ctx->trap_arg);
    step->ctx->pc = step->ctx->trap_pc >> VALUE_BITS;
    step->ctx->trap_pc = 0;
    step->ctx->interruptlevel = true;
}

bool ind_tryload(struct values_t *values, hvalue_t dict, hvalue_t *indices, int n, hvalue_t *result){
    hvalue_t d = dict;
    for (int i = 0; i < n; i++) {
        if (!value_dict_tryload(values, d, indices[i], &d)) {
            return false;
        }
    }
    *result = d;
    return true;
}

bool ind_trystore(hvalue_t dict, hvalue_t *indices, int n, hvalue_t value, struct values_t *values, hvalue_t *result){
    assert((dict & VALUE_MASK) == VALUE_DICT);
    assert(n > 0);

    if (n == 1) {
        *result = value_dict_store(values, dict, indices[0], value);
        return true;
    }
    else {
        hvalue_t *vals;
        int size;
        if (dict == VALUE_DICT) {
            vals = NULL;
            size = 0;
        }
        else {
            vals = value_get(dict & ~VALUE_MASK, &size);
            size /= sizeof(hvalue_t);
            assert(size % 2 == 0);
        }

        int i;
        for (i = 0; i < size; i += 2) {
            if (vals[i] == indices[0]) {
                hvalue_t d = vals[i+1];
                if ((d & VALUE_MASK) != VALUE_DICT) {
                    return false;
                }
                hvalue_t nd;
                if (!ind_trystore(d, indices + 1, n - 1, value, values, &nd)) {
                    return false;
                }
                if (d == nd) {
                    *result = dict;
                    return true;
                }
                int n = size * sizeof(hvalue_t);
                hvalue_t *copy = malloc(n);
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                hvalue_t v = value_put_dict(values, copy, n);
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

bool ind_remove(hvalue_t dict, hvalue_t *indices, int n, struct values_t *values,
                                        hvalue_t *result) {
    assert((dict & VALUE_MASK) == VALUE_DICT);
    assert(n > 0);

    if (n == 1) {
        *result = value_dict_remove(values, dict, indices[0]);
        return true;
    }
    else {
        hvalue_t *vals;
        int size;
        if (dict == VALUE_DICT) {
            vals = NULL;
            size = 0;
        }
        else {
            vals = value_get(dict & ~VALUE_MASK, &size);
            size /= sizeof(hvalue_t);
            assert(size % 2 == 0);
        }

        int i;
        for (i = 0; i < size; i += 2) {
            if (vals[i] == indices[0]) {
                hvalue_t d = vals[i+1];
                if ((d & VALUE_MASK) != VALUE_DICT) {
                    return false;
                }
                hvalue_t nd;
                if (!ind_remove(d, indices + 1, n - 1, values, &nd)) {
                    return false;
                }
                if (d == nd) {
                    *result = dict;
                    return true;
                }
                int n = size * sizeof(hvalue_t);
                hvalue_t *copy = malloc(n);
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                hvalue_t v = value_put_dict(values, copy, n);
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
        return false;
    }
}

void op_Address(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t index = value_ctx_pop(&step->ctx);
    hvalue_t av = value_ctx_pop(&step->ctx);
    if ((av & VALUE_MASK) != VALUE_ADDRESS) {
        char *p = value_string(av);
        value_ctx_failure(step->ctx, &global->values, "%s: not an address", p);
        free(p);
        return;
    }
    if (av == VALUE_ADDRESS) {
        value_ctx_failure(step->ctx, &global->values, "None unexpected");
        return;
    }

    int size;
    hvalue_t *indices = value_copy(av, &size);
    indices = realloc(indices, size + sizeof(index));
    indices[size / sizeof(hvalue_t)] = index;
    value_ctx_push(&step->ctx, value_put_address(&global->values, indices, size + sizeof(index)));
    free(indices);
    step->ctx->pc++;
}

void op_Apply(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t e = value_ctx_pop(&step->ctx);
    hvalue_t method = value_ctx_pop(&step->ctx);

    hvalue_t type = method & VALUE_MASK;
    switch (type) {
    case VALUE_DICT:
        {
            hvalue_t v;
            if (!value_dict_tryload(&global->values, method, e, &v)) {
                char *m = value_string(method);
                char *x = value_string(e);
                value_ctx_failure(step->ctx, &global->values, "Bad index %s: not in %s", x, m);
                free(m);
                free(x);
                return;
            }
            value_ctx_push(&step->ctx, v);
            step->ctx->pc++;
        }
        return;
    case VALUE_ATOM:
        {
            if ((e & VALUE_MASK) != VALUE_INT) {
                value_ctx_failure(step->ctx, &global->values, "Bad index type for string");
                return;
            }
            e >>= VALUE_BITS;
            int size;
            char *chars = value_get(method, &size);
            if ((int) e >= size) {
                value_ctx_failure(step->ctx, &global->values, "Index out of range");
                return;
            }
            hvalue_t v = value_put_atom(&global->values, &chars[e], 1);
            value_ctx_push(&step->ctx, v);
            step->ctx->pc++;
        }
        return;
    case VALUE_PC:
        value_ctx_push(&step->ctx, ((step->ctx->pc + 1) << VALUE_BITS) | VALUE_PC);
        value_ctx_push(&step->ctx, (CALLTYPE_NORMAL << VALUE_BITS) | VALUE_INT);
        value_ctx_push(&step->ctx, e);
        assert((method >> VALUE_BITS) != step->ctx->pc);
        step->ctx->pc = method >> VALUE_BITS;
        return;
    default:
        {
            char *x = value_string(method);
            value_ctx_failure(step->ctx, &global->values, "Can only apply to methods or dictionaries, not to: %s", x);
            free(x);
        }
    }
}

void op_Assert(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t v = value_ctx_pop(&step->ctx);
    if ((v & VALUE_MASK) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, &global->values, "assert can only be applied to bool values");
    }
    if (v == VALUE_FALSE) {
        value_ctx_failure(step->ctx, &global->values, "Harmony assertion failed");
    }
    else {
        step->ctx->pc++;
    }
}

void op_Assert2(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t e = value_ctx_pop(&step->ctx);
    hvalue_t v = value_ctx_pop(&step->ctx);
    if ((v & VALUE_MASK) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, &global->values, "assert2 can only be applied to bool values");
    }
    if (v == VALUE_FALSE) {
        char *p = value_string(e);
        value_ctx_failure(step->ctx, &global->values, "Harmony assertion failed: %s", p);
        free(p);
    }
    else {
        step->ctx->pc++;
    }
}

void op_Print(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t symbol = value_ctx_pop(&step->ctx);
    step->log = realloc(step->log, (step->nlog + 1) * sizeof(symbol));
    step->log[step->nlog++] = symbol;
    if (global->dfa != NULL) {
        int nstate = dfa_step(global->dfa, state->dfa_state, symbol);
        if (nstate < 0) {
            char *p = value_string(symbol);
            value_ctx_failure(step->ctx, &global->values, "Behavior failure on %s", p);
            free(p);
            return;
        }
        state->dfa_state = nstate;

    }
    step->ctx->pc++;
}

void op_AtomicDec(const void *env, struct state *state, struct step *step, struct global_t *global){
    struct context *ctx = step->ctx;

    assert(ctx->atomic > 0);
    if (--ctx->atomic == 0) {
        ctx->atomicFlag = false;
    }
    ctx->pc++;
}

void op_AtomicInc(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_AtomicInc *ea = env;
    struct context *ctx = step->ctx;

    ctx->atomic++;
    if (!ea->lazy) {
        ctx->atomicFlag = true;
    }
    ctx->pc++;
}

void op_Choose(const void *env, struct state *state, struct step *step, struct global_t *global){
    panic("op_Choose: should not be called");
}

void op_Continue(const void *env, struct state *state, struct step *step, struct global_t *global){
    step->ctx->pc++;
}

void op_Cut(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Cut *ec = env;
    struct context *ctx = step->ctx;

    hvalue_t v = value_dict_load(ctx->vars, ec->set);
    if ((v & VALUE_MASK) == VALUE_SET) {
        if (ec->key != NULL) {
            value_ctx_failure(ctx, &global->values, "Can't cut set in key/value pairs");
            return;
        }
        assert(v != VALUE_SET);
        void *p = (void *) (v & ~VALUE_MASK);

        int size;
        hvalue_t *vals = dict_retrieve(p, &size);
        assert(size > 0);

        ctx->vars = value_dict_store(&global->values, ctx->vars, ec->set, value_put_set(&global->values, &vals[1], size - sizeof(hvalue_t)));
        var_match(step->ctx, ec->value, &global->values, vals[0]);
        step->ctx->pc++;
        return;
    }
    if ((v & VALUE_MASK) == VALUE_DICT) {
        assert(v != VALUE_DICT);
        void *p = (void *) (v & ~VALUE_MASK);

        int size;
        hvalue_t *vals = dict_retrieve(p, &size);
        assert(size > 0);

        ctx->vars = value_dict_store(&global->values, ctx->vars, ec->set, value_put_dict(&global->values, &vals[2], size - 2 * sizeof(hvalue_t)));
        var_match(step->ctx, ec->value, &global->values, vals[1]);
        if (ec->key != NULL) {
            var_match(step->ctx, ec->key, &global->values, vals[0]);
        }
        step->ctx->pc++;
        return;
    }
    if ((v & VALUE_MASK) == VALUE_ATOM) {
        if (ec->key != NULL) {
            value_ctx_failure(ctx, &global->values, "Can't cut string in key/value pairs");
            return;
        }
        assert(v != VALUE_ATOM);
        int size;
        char *chars = value_get(v, &size);
        assert(size > 0);

        ctx->vars = value_dict_store(&global->values, ctx->vars, ec->set, value_put_atom(&global->values, &chars[1], size - 1));
        hvalue_t e = value_put_atom(&global->values, chars, 1);
        var_match(step->ctx, ec->value, &global->values, e);
        step->ctx->pc++;
        return;
    }
    value_ctx_failure(step->ctx, &global->values, "op_Cut: not a set, dict, or string");
}

void op_Del(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Del *ed = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, &global->values, "Can't update state in assert or invariant");
        return;
    }

    if (ed == 0) {
        hvalue_t av = value_ctx_pop(&step->ctx);
        if ((av & VALUE_MASK) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &global->values, "Del %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS) {
            value_ctx_failure(step->ctx, &global->values, "Del: address is None");
            return;
        }

        int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        if (step->ai != NULL) {
            step->ai->indices = indices;
            step->ai->n = size;
            step->ai->load = false;
        }
        hvalue_t nd;
        if (!ind_remove(state->vars, indices, size, &global->values, &nd)) {
            value_ctx_failure(step->ctx, &global->values, "Del: no such variable");
        }
        else {
            state->vars = nd;
            step->ctx->pc++;
        }
    }
    else {
        if (step->ai != NULL) {
            step->ai->indices = ed->indices;
            step->ai->n = ed->n;
            step->ai->load = false;
        }
        hvalue_t nd;
        if (!ind_remove(state->vars, ed->indices, ed->n, &global->values, &nd)) {
            value_ctx_failure(step->ctx, &global->values, "Del: bad variable");
        }
        else {
            state->vars = nd;
            step->ctx->pc++;
        }
    }
}

void op_DelVar(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_DelVar *ed = env;

    assert((step->ctx->vars & VALUE_MASK) == VALUE_DICT);
    if (ed == NULL) {
        hvalue_t av = value_ctx_pop(&step->ctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);

        bool result;
        if (indices[0] == this_atom) {
            if ((step->ctx->this & VALUE_MASK) != VALUE_DICT) {
                value_ctx_failure(step->ctx, &global->values, "DelVar: 'this' is not a dictionary");
                return;
            }
		    result = ind_remove(step->ctx->this, &indices[1], size - 1, &global->values, &step->ctx->this);
        }
        else {
		    result = ind_remove(step->ctx->vars, indices, size, &global->values, &step->ctx->vars);
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &global->values, "DelVar: bad address: %s", x);
            free(x);
			return;
		}
    }
	else {
        if (ed->name == this_atom) {
            value_ctx_failure(step->ctx, &global->values, "DelVar: can't del 'this'");
            return;
        }
        else {
            step->ctx->vars = value_dict_remove(&global->values, step->ctx->vars, ed->name);
        }
	}
	step->ctx->pc++;
}

void op_Dup(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t v = value_ctx_pop(&step->ctx);
    value_ctx_push(&step->ctx, v);
    value_ctx_push(&step->ctx, v);
    step->ctx->pc++;
}

void op_Frame(const void *env, struct state *state, struct step *step, struct global_t *global){
    static hvalue_t result = 0;

    if (result == 0) {
        result = value_put_atom(&global->values, "result", 6);
    }

    const struct env_Frame *ef = env;

    // peek at argument
    hvalue_t arg = value_ctx_pop(&step->ctx);
    value_ctx_push(&step->ctx, arg);

    hvalue_t oldvars = step->ctx->vars;

    // Set result to None
    step->ctx->vars = value_dict_store(&global->values, VALUE_DICT, result, VALUE_ADDRESS);

    // try to match against parameters
    var_match(step->ctx, ef->args, &global->values, arg);
    if (step->ctx->failure != 0) {
        return;
    }
 
    value_ctx_push(&step->ctx, oldvars);
    value_ctx_push(&step->ctx, (step->ctx->fp << VALUE_BITS) | VALUE_INT);

    struct context *ctx = step->ctx;
    ctx->fp = ctx->sp;
    ctx->pc += 1;
}

void op_Go(
    const void *env,
    struct state *state,
    struct step *step,
    struct global_t *global
){
    hvalue_t ctx = value_ctx_pop(&step->ctx);
    if ((ctx & VALUE_MASK) != VALUE_CONTEXT) {
        value_ctx_failure(step->ctx, &global->values, "Go: not a context");
        return;
    }

    // Remove from stopbag if it's there
    hvalue_t count;
    if (value_dict_tryload(&global->values, state->stopbag, ctx, &count)) {
        assert((count & VALUE_MASK) == VALUE_INT);
        assert(count != VALUE_INT);
        count -= 1 << VALUE_BITS;
        if (count != VALUE_INT) {
            state->stopbag = value_dict_store(&global->values, state->stopbag, ctx, count);
        }
        else {
            state->stopbag = value_dict_remove(&global->values, state->stopbag, ctx);
        }
    }

    hvalue_t result = value_ctx_pop(&step->ctx);
    struct context *copy = value_copy(ctx, NULL);
    value_ctx_push(&copy, result);
    copy->stopped = false;
    hvalue_t v = value_put_context(&global->values, copy);
    free(copy);
    state->ctxbag = value_bag_add(&global->values, state->ctxbag, v, 1);
    step->ctx->pc++;
}

void op_IncVar(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_IncVar *ei = env;
    struct context *ctx = step->ctx;

    assert((ctx->vars & VALUE_MASK) == VALUE_DICT);

    hvalue_t v = value_dict_load(ctx->vars, ei->name);
    assert((v & VALUE_MASK) == VALUE_INT);
    v += 1 << VALUE_BITS;
    ctx->vars = value_dict_store(&global->values, ctx->vars, ei->name, v);
    step->ctx->pc++;
}

void op_Invariant(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Invariant *ei = env;

    assert((state->invariants & VALUE_MASK) == VALUE_SET);
    int size;
    hvalue_t *vals;
    if (state->invariants == VALUE_SET) {
        size = 0;
        vals = NULL;
    }
    else {
        vals = value_get(state->invariants, &size);
    }
    vals = realloc(vals, size + sizeof(hvalue_t));
    * (hvalue_t *) ((char *) vals + size) = (step->ctx->pc << VALUE_BITS) | VALUE_PC;
    state->invariants = value_put_set(&global->values, vals, size + sizeof(hvalue_t));
    step->ctx->pc = ei->end + 1;
}

int invariant_cnt(const void *env){
    const struct env_Invariant *ei = env;

    return ei->end;
}

void op_Jump(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Jump *ej = env;
    step->ctx->pc = ej->pc;
}

void op_JumpCond(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_JumpCond *ej = env;

    hvalue_t v = value_ctx_pop(&step->ctx);
    if ((ej->cond == VALUE_FALSE || ej->cond == VALUE_TRUE) &&
                            !(v == VALUE_FALSE || v == VALUE_TRUE)) {
        value_ctx_failure(step->ctx, &global->values, "JumpCond: not an boolean");
    }
    else if (v == ej->cond) {
        assert(step->ctx->pc != ej->pc);
        step->ctx->pc = ej->pc;
    }
    else {
        step->ctx->pc++;
    }
}

void op_Load(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Load *el = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    hvalue_t v;
    if (el == 0) {
        hvalue_t av = value_ctx_pop(&step->ctx);
        if ((av & VALUE_MASK) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &global->values, "Load %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS) {
            value_ctx_failure(step->ctx, &global->values, "Load: can't load from None");
            return;
        }

        int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        if (step->ai != NULL) {
            step->ai->indices = indices;
            step->ai->n = size;
            step->ai->load = true;
        }

        if (!ind_tryload(&global->values, state->vars, indices, size, &v)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &global->values, "Load: unknown address %s", x);
            free(x);
            return;
        }
        value_ctx_push(&step->ctx, v);
    }
    else {
        if (step->ai != NULL) {
            step->ai->indices = el->indices;
            step->ai->n = el->n;
            step->ai->load = true;
        }
        if (!ind_tryload(&global->values, state->vars, el->indices, el->n, &v)) {
            char *x = indices_string(el->indices, el->n);
            value_ctx_failure(step->ctx, &global->values, "Load: unknown variable %s", x+1);
            free(x);
            return;
        }
        value_ctx_push(&step->ctx, v);
    }
    step->ctx->pc++;
}

void op_LoadVar(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_LoadVar *el = env;
    assert((step->ctx->vars & VALUE_MASK) == VALUE_DICT);

    hvalue_t v;
    if (el == NULL) {
        hvalue_t av = value_ctx_pop(&step->ctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);

        bool result;
        if (indices[0] == this_atom) {
            if ((step->ctx->this & VALUE_MASK) != VALUE_DICT) {
                value_ctx_failure(step->ctx, &global->values, "LoadVar: 'this' is not a dictionary");
                return;
            }
            result = ind_tryload(&global->values, step->ctx->this, &indices[1], size - 1, &v);
        }
        else {
            result = ind_tryload(&global->values, step->ctx->vars, indices, size, &v);
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &global->values, "LoadVar: bad address: %s", x);
            free(x);
            return;
        }
        value_ctx_push(&step->ctx, v);
    }
    else {
        if (el->name == this_atom) {
            value_ctx_push(&step->ctx, step->ctx->this);
        }
        else if (value_dict_tryload(&global->values, step->ctx->vars, el->name, &v)) {
            value_ctx_push(&step->ctx, v);
        }
        else {
            char *p = value_string(el->name);
            value_ctx_failure(step->ctx, &global->values, "LoadVar: unknown variable %s", p + 1);
            free(p);
            return;
        }
    }
    step->ctx->pc++;
}

void op_Move(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Move *em = env;
    struct context *ctx = step->ctx;
    int offset = ctx->sp - em->offset;

    hvalue_t v = ctx->stack[offset];
    memmove(&ctx->stack[offset], &ctx->stack[offset + 1],
                (em->offset - 1) * sizeof(hvalue_t));
    ctx->stack[ctx->sp - 1] = v;
    ctx->pc++;
}

void op_Nary(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Nary *en = env;
    hvalue_t args[MAX_ARITY];

    for (int i = 0; i < en->arity; i++) {
        args[i] = value_ctx_pop(&step->ctx);
    }
    hvalue_t result = (*en->fi->f)(state, step->ctx, args, en->arity, &global->values);
    if (step->ctx->failure == 0) {
        value_ctx_push(&step->ctx, result);
        step->ctx->pc++;
    }
}

void op_Pop(const void *env, struct state *state, struct step *step, struct global_t *global){
    assert(step->ctx->sp > 0);
    step->ctx->sp--;
    step->ctx->pc++;
}

void op_Push(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Push *ep = env;

    value_ctx_push(&step->ctx, ep->value);
    step->ctx->pc++;
}

void op_ReadonlyDec(const void *env, struct state *state, struct step *step, struct global_t *global){
    struct context *ctx = step->ctx;

    assert(ctx->readonly > 0);
    ctx->readonly--;
    ctx->pc++;
}

void op_ReadonlyInc(const void *env, struct state *state, struct step *step, struct global_t *global){
    struct context *ctx = step->ctx;

    ctx->readonly++;
    ctx->pc++;
}

// On the stack are:
//  - frame pointer
//  - saved variables
//  - saved argument for stack trace
//  - process, normal, or interrupt
//  - return address if normal or interrupt
void op_Return(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t result = value_dict_load(step->ctx->vars, value_put_atom(&global->values, "result", 6));
    hvalue_t fp = value_ctx_pop(&step->ctx);
    if ((fp & VALUE_MASK) != VALUE_INT) {
        printf("XXX %d %d %s\n", step->ctx->pc, step->ctx->sp, value_string(fp));
        value_ctx_failure(step->ctx, &global->values, "XXX");
        return;
        // exit(1);
    }
    assert((fp & VALUE_MASK) == VALUE_INT);
    step->ctx->fp = fp >> VALUE_BITS;
    hvalue_t oldvars = value_ctx_pop(&step->ctx);
    assert((oldvars & VALUE_MASK) == VALUE_DICT);
    step->ctx->vars = oldvars;
    (void) value_ctx_pop(&step->ctx);   // argument saved for stack trace
    if (step->ctx->sp == 0) {     // __init__
        step->ctx->terminated = true;
        return;
    }
    hvalue_t calltype = value_ctx_pop(&step->ctx);
    assert((calltype & VALUE_MASK) == VALUE_INT);
    switch (calltype >> VALUE_BITS) {
    case CALLTYPE_PROCESS:
        step->ctx->terminated = true;
        break;
    case CALLTYPE_NORMAL:
        {
            hvalue_t pc = value_ctx_pop(&step->ctx);
            assert((pc & VALUE_MASK) == VALUE_PC);
            pc >>= VALUE_BITS;
            assert(pc != step->ctx->pc);
            value_ctx_push(&step->ctx, result);
            step->ctx->pc = pc;
        }
        break;
    case CALLTYPE_INTERRUPT:
        step->ctx->interruptlevel = false;
        hvalue_t pc = value_ctx_pop(&step->ctx);
        assert((pc & VALUE_MASK) == VALUE_PC);
        pc >>= VALUE_BITS;
        assert(pc != step->ctx->pc);
        step->ctx->pc = pc;
        break;
    default:
        panic("op_Return: bad call type");
    }
}

void op_Sequential(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t addr = value_ctx_pop(&step->ctx);
    if ((addr & VALUE_MASK) != VALUE_ADDRESS) {
        char *p = value_string(addr);
        value_ctx_failure(step->ctx, &global->values, "Sequential %s: not an address", p);
        free(p);
        return;
    }

    /* Insert in state's set of sequential variables.
     */
    int size;
    hvalue_t *seqs = value_copy(state->seqs, &size);
    size /= sizeof(hvalue_t);
    int i;
    for (i = 0; i < size; i++) {
        int k = value_cmp(seqs[i], addr);
        if (k == 0) {
            free(seqs);
            step->ctx->pc++;
            return;
        }
        if (k > 0) {
            break;
        }
    }
    seqs = realloc(seqs, (size + 1) * sizeof(hvalue_t));
    memmove(&seqs[i + 1], &seqs[i], (size - i) * sizeof(hvalue_t));
    seqs[i] = addr;
    state->seqs = value_put_set(&global->values, seqs, (size + 1) * sizeof(hvalue_t));
    free(seqs);
    step->ctx->pc++;
}

// sort two key/value pairs
static int q_kv_cmp(const void *e1, const void *e2){
    const hvalue_t *kv1 = (const hvalue_t *) e1;
    const hvalue_t *kv2 = (const hvalue_t *) e2;

    int k = value_cmp(kv1[0], kv2[0]);
    if (k != 0) {
        return k;
    }
    return value_cmp(kv1[1], kv2[1]);
}

static int q_value_cmp(const void *v1, const void *v2){
    return value_cmp(* (const hvalue_t *) v1, * (const hvalue_t *) v2);
}

// Sort the resulting set and remove duplicates
static int sort(hvalue_t *vals, int n){
    qsort(vals, n, sizeof(hvalue_t), q_value_cmp);

    hvalue_t *p = vals, *q = vals + 1;
    for (int i = 1; i < n; i++, q++) {
        if (*q != *p) {
            *++p = *q;
        }
    }
    p++;
    return p - vals;
}

void op_SetIntLevel(const void *env, struct state *state, struct step *step, struct global_t *global){
	bool oldlevel = step->ctx->interruptlevel;
	hvalue_t newlevel =  value_ctx_pop(&step->ctx);
    if ((newlevel & VALUE_MASK) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, &global->values, "setintlevel can only be set to a boolean");
        return;
    }
    step->ctx->interruptlevel = newlevel >> VALUE_BITS;
	value_ctx_push(&step->ctx, (oldlevel << VALUE_BITS) | VALUE_BOOL);
    step->ctx->pc++;
}

void op_Spawn(
    const void *env,
    struct state *state,
    struct step *step,
    struct global_t *global
) {
    const struct env_Spawn *se = env;

    hvalue_t thisval = value_ctx_pop(&step->ctx);
    hvalue_t arg = value_ctx_pop(&step->ctx);

    hvalue_t pc = value_ctx_pop(&step->ctx);
    if ((pc & VALUE_MASK) != VALUE_PC) {
        value_ctx_failure(step->ctx, &global->values, "spawn: not a method");
        return;
    }
    pc >>= VALUE_BITS;

    assert(pc < global->code.len);
    assert(strcmp(global->code.instrs[pc].oi->name, "Frame") == 0);

    struct context *ctx = new_alloc(struct context);

    const struct env_Frame *ef = global->code.instrs[pc].env;
    ctx->name = ef->name;
    ctx->arg = arg;
    ctx->this = thisval;
    ctx->entry = (pc << VALUE_BITS) | VALUE_PC;
    ctx->pc = pc;
    ctx->vars = VALUE_DICT;
    ctx->interruptlevel = VALUE_FALSE;
    ctx->eternal = se->eternal;
    value_ctx_push(&ctx, (CALLTYPE_PROCESS << VALUE_BITS) | VALUE_INT);
    value_ctx_push(&ctx, arg);
    hvalue_t v = value_put_context(&global->values, ctx);
    state->ctxbag = value_bag_add(&global->values, state->ctxbag, v, 1);
    step->ctx->pc++;
}

void op_Split(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Split *es = env;

    hvalue_t v = value_ctx_pop(&step->ctx);
    hvalue_t type = v & VALUE_MASK;
    if (type != VALUE_DICT && type != VALUE_SET) {
        value_ctx_failure(step->ctx, &global->values, "Can only split tuples or sets");
        return;
    }
    if (v == VALUE_DICT || v == VALUE_SET) {
        if (es->count != 0) {
            value_ctx_failure(step->ctx, &global->values, "Split: empty set or tuple");
        }
        else {
            step->ctx->pc++;
        }
        return;
    }

    int size;
    hvalue_t *vals = value_get(v, &size);

    if (type == VALUE_DICT) {
        size /= 2 * sizeof(hvalue_t);
        if (size != es->count) {
            value_ctx_failure(step->ctx, &global->values, "Split: list of wrong size");
            return;
        }
        for (int i = 0; i < size; i++) {
            value_ctx_push(&step->ctx, vals[2*i + 1]);
        }
        step->ctx->pc++;
        return;
    }
    if (type == VALUE_SET) {
        size /= sizeof(hvalue_t);
        if (size != es->count) {
            value_ctx_failure(step->ctx, &global->values, "Split: set of wrong size");
            return;
        }
        for (int i = 0; i < size; i++) {
            value_ctx_push(&step->ctx, vals[i]);
        }
        step->ctx->pc++;
        return;
    }
    panic("op_Split: not a set or dict");
}

void op_Stop(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Stop *es = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, &global->values, "Stop: in read-only mode");
        return;
    }

    if (es == 0) {
        hvalue_t av = value_ctx_pop(&step->ctx);
        if ((av & VALUE_MASK) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &global->values, "Stop %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS) {
            value_ctx_failure(step->ctx, &global->values, "Stop: address is None");
            return;
        }

        int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);

        step->ctx->stopped = true;
        step->ctx->pc++;
        hvalue_t v = value_put_context(&global->values, step->ctx);

        if (!ind_trystore(state->vars, indices, size, v, &global->values, &state->vars)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &global->values, "Stop: bad address: %s", x);
            free(x);
            return;
        }
    }
    else {
        step->ctx->stopped = true;
        step->ctx->pc++;
        hvalue_t v = value_put_context(&global->values, step->ctx);

        if (!ind_trystore(state->vars, es->indices, es->n, v, &global->values, &state->vars)) {
            value_ctx_failure(step->ctx, &global->values, "Store: bad variable");
            return;
        }
    }
}

void op_Store(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Store *es = env;

    assert((state->vars & VALUE_MASK) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, &global->values, "Can't update state in assert or invariant (including acquiring locks)");
        return;
    }

    hvalue_t v = value_ctx_pop(&step->ctx);

    if (es == 0) {
        hvalue_t av = value_ctx_pop(&step->ctx);
        if ((av & VALUE_MASK) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &global->values, "Store %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS) {
            value_ctx_failure(step->ctx, &global->values, "Store: address is None");
            return;
        }

        int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        if (step->ai != NULL) {
            step->ai->indices = indices;
            step->ai->n = size;
            step->ai->load = is_sequential(state->seqs, step->ai->indices, step->ai->n);
        }

        if (!ind_trystore(state->vars, indices, size, v, &global->values, &state->vars)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &global->values, "Store: bad address: %s", x);
            free(x);
            return;
        }
    }
    else {
        if (step->ai != NULL) {
            step->ai->indices = es->indices;
            step->ai->n = es->n;
            step->ai->load = is_sequential(state->seqs, step->ai->indices, step->ai->n);
        }
        if (!ind_trystore(state->vars, es->indices, es->n, v, &global->values, &state->vars)) {
            value_ctx_failure(step->ctx, &global->values, "Store: bad variable");
            return;
        }
    }
    step->ctx->pc++;
}

void op_StoreVar(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_StoreVar *es = env;
    hvalue_t v = value_ctx_pop(&step->ctx);

    assert((step->ctx->vars & VALUE_MASK) == VALUE_DICT);
    if (es == NULL) {
        hvalue_t av = value_ctx_pop(&step->ctx);
        assert((av & VALUE_MASK) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);

        bool result;
        if (indices[0] == this_atom) {
            if ((step->ctx->this & VALUE_MASK) != VALUE_DICT) {
                value_ctx_failure(step->ctx, &global->values, "StoreVar: 'this' is not a dictionary");
                return;
            }
            result = ind_trystore(step->ctx->this, &indices[1], size - 1, v, &global->values, &step->ctx->this);
        }

        else {
            result = ind_trystore(step->ctx->vars, indices, size, v, &global->values, &step->ctx->vars);
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &global->values, "StoreVar: bad address: %s", x);
            free(x);
            return;
        }
        step->ctx->pc++;
    }
    else {
        if (es->args->type == VT_NAME && es->args->u.name == this_atom) {
            step->ctx->this = v;
            step->ctx->pc++;
        }
        else {
            var_match(step->ctx, es->args, &global->values, v);
            if (step->ctx->failure == 0) {
                step->ctx->pc++;
            }
        }
    }
}

void op_Trap(const void *env, struct state *state, struct step *step, struct global_t *global){
    step->ctx->trap_pc = value_ctx_pop(&step->ctx);
    if ((step->ctx->trap_pc & VALUE_MASK) != VALUE_PC) {
        value_ctx_failure(step->ctx, &global->values, "trap: not a method");
        return;
    }
    assert((step->ctx->trap_pc >> VALUE_BITS) < global->code.len);
    assert(strcmp(global->code.instrs[step->ctx->trap_pc >> VALUE_BITS].oi->name, "Frame") == 0);
    step->ctx->trap_arg = value_ctx_pop(&step->ctx);
    step->ctx->pc++;
}

void *init_Address(struct dict *map, struct values_t *values){ return NULL; }
void *init_Apply(struct dict *map, struct values_t *values){ return NULL; }
void *init_Assert(struct dict *map, struct values_t *values){ return NULL; }
void *init_Assert2(struct dict *map, struct values_t *values){ return NULL; }
void *init_AtomicDec(struct dict *map, struct values_t *values){ return NULL; }
void *init_Choose(struct dict *map, struct values_t *values){ return NULL; }
void *init_Continue(struct dict *map, struct values_t *values){ return NULL; }
void *init_Dup(struct dict *map, struct values_t *values){ return NULL; }
void *init_Go(struct dict *map, struct values_t *values){ return NULL; }
void *init_Print(struct dict *map, struct values_t *values){ return NULL; }
void *init_Pop(struct dict *map, struct values_t *values){ return NULL; }
void *init_ReadonlyDec(struct dict *map, struct values_t *values){ return NULL; }
void *init_ReadonlyInc(struct dict *map, struct values_t *values){ return NULL; }
void *init_Return(struct dict *map, struct values_t *values){ return NULL; }
void *init_Sequential(struct dict *map, struct values_t *values){ return NULL; }
void *init_SetIntLevel(struct dict *map, struct values_t *values){ return NULL; }
void *init_Trap(struct dict *map, struct values_t *values){ return NULL; }

void *init_Cut(struct dict *map, struct values_t *values){
    struct env_Cut *env = new_alloc(struct env_Cut);
    struct json_value *set = dict_lookup(map, "set", 3);
    assert(set->type == JV_ATOM);
    env->set = value_put_atom(values, set->u.atom.base, set->u.atom.len);

    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    int index = 0;
    env->value = var_parse(values, value->u.atom.base, value->u.atom.len, &index);

    struct json_value *key = dict_lookup(map, "key", 3);
    if (key != NULL) {
        assert(key->type == JV_ATOM);
        index = 0;
        env->key = var_parse(values, key->u.atom.base, key->u.atom.len, &index);
    }

    return env;
}

void *init_AtomicInc(struct dict *map, struct values_t *values){
    struct env_AtomicInc *env = new_alloc(struct env_AtomicInc);
    struct json_value *lazy = dict_lookup(map, "lazy", 4);
    if (lazy == NULL) {
        env->lazy = false;
    }
    else {
		assert(lazy->type == JV_ATOM);
        if (lazy->u.atom.len == 0) {
            env->lazy = false;
        }
        else {
            char *p = lazy->u.atom.base;
            env->lazy = *p == 't' || *p == 'T';
        }
    }
    return env;
}

void *init_Del(struct dict *map, struct values_t *values){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Del *env = new_alloc(struct env_Del);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(values, index->u.map);
    }
    return env;
}

void *init_DelVar(struct dict *map, struct values_t *values){
    struct json_value *name = dict_lookup(map, "value", 5);
	if (name == NULL) {
		return NULL;
	}
	else {
		struct env_DelVar *env = new_alloc(struct env_DelVar);
		assert(name->type == JV_ATOM);
		env->name = value_put_atom(values, name->u.atom.base, name->u.atom.len);
		return env;
	}
}

void *init_Frame(struct dict *map, struct values_t *values){
    struct env_Frame *env = new_alloc(struct env_Frame);

    struct json_value *name = dict_lookup(map, "name", 4);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(values, name->u.atom.base, name->u.atom.len);

    struct json_value *args = dict_lookup(map, "args", 4);
    assert(args->type == JV_ATOM);
    int index = 0;
    env->args = var_parse(values, args->u.atom.base, args->u.atom.len, &index);

    return env;
}

void *init_IncVar(struct dict *map, struct values_t *values){
    struct env_IncVar *env = new_alloc(struct env_IncVar);
    struct json_value *name = dict_lookup(map, "value", 5);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(values, name->u.atom.base, name->u.atom.len);
    return env;
}

void *init_Load(struct dict *map, struct values_t *values){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Load *env = new_alloc(struct env_Load);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(values, index->u.map);
    }
    return env;
}

void *init_LoadVar(struct dict *map, struct values_t *values){
    struct json_value *value = dict_lookup(map, "value", 5);
    if (value == NULL) {
        return NULL;
    }
    else {
        struct env_LoadVar *env = new_alloc(struct env_LoadVar);
        assert(value->type == JV_ATOM);
        env->name = value_put_atom(values, value->u.atom.base, value->u.atom.len);
        return env;
    }
}

void *init_Move(struct dict *map, struct values_t *values){
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

void *init_Nary(struct dict *map, struct values_t *values){
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

void *init_Invariant(struct dict *map, struct values_t *values){
    struct env_Invariant *env = new_alloc(struct env_Invariant);

    struct json_value *end = dict_lookup(map, "end", 3);
    assert(end->type == JV_ATOM);
    char *copy = malloc(end->u.atom.len + 1);
    memcpy(copy, end->u.atom.base, end->u.atom.len);
    copy[end->u.atom.len] = 0;
    env->end = atoi(copy);
    free(copy);
    return env;
}

void *init_Jump(struct dict *map, struct values_t *values){
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

void *init_JumpCond(struct dict *map, struct values_t *values){
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
    env->cond = value_from_json(values, cond->u.map);

    return env;
}

void *init_Push(struct dict *map, struct values_t *values) {
    struct json_value *jv = dict_lookup(map, "value", 5);
    assert(jv->type == JV_MAP);
    struct env_Push *env = new_alloc(struct env_Push);
    env->value = value_from_json(values, jv->u.map);
    return env;
}

void *init_Spawn(struct dict *map, struct values_t *values){
    struct env_Spawn *env = new_alloc(struct env_Spawn);
    struct json_value *eternal = dict_lookup(map, "eternal", 7);
    if (eternal == NULL) {
        env->eternal = false;
    }
    else {
		assert(eternal->type == JV_ATOM);
        if (eternal->u.atom.len == 0) {
            env->eternal = false;
        }
        else {
            char *p = eternal->u.atom.base;
            env->eternal = *p == 't' || *p == 'T';
        }
    }
    return env;
}

void *init_Split(struct dict *map, struct values_t *values){
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

void *init_Stop(struct dict *map, struct values_t *values){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Stop *env = new_alloc(struct env_Stop);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(values, index->u.map);
    }
    return env;
}

void *init_Store(struct dict *map, struct values_t *values){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Store *env = new_alloc(struct env_Store);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(values, index->u.map);
    }
    return env;
}

void *init_StoreVar(struct dict *map, struct values_t *values){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    else {
        assert(jv->type == JV_ATOM);
        struct env_StoreVar *env = new_alloc(struct env_StoreVar);
        int index = 0;
        env->args = var_parse(values, jv->u.atom.base, jv->u.atom.len, &index);
        return env;
    }
}

hvalue_t f_abs(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "abs() can only be applied to integers");
    }
    e >>= VALUE_BITS;
    return e >= 0 ? args[0] : (((-e) << VALUE_BITS) | VALUE_INT);
}

hvalue_t f_all(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_DICT) {
		return VALUE_TRUE;
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        for (int i = 0; i < size; i++) {
            if ((v[i] & VALUE_MASK) != VALUE_BOOL) {
                return value_ctx_failure(ctx, values, "set.all() can only be applied to booleans");
            }
            if (v[i] == VALUE_FALSE) {
                return VALUE_FALSE;
            }
        }
		return VALUE_TRUE;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= 2 * sizeof(hvalue_t);
        for (int i = 0; i < size; i++) {
            if ((v[2*i+1] & VALUE_MASK) != VALUE_BOOL) {
                return value_ctx_failure(ctx, values, "dict.all() can only be applied to booleans");
            }
            if (v[2*i+1] == VALUE_FALSE) {
                return VALUE_FALSE;
            }
        }
		return VALUE_TRUE;
    }
    return value_ctx_failure(ctx, values, "all() can only be applied to sets or dictionaries");
}

hvalue_t f_any(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_DICT) {
		return VALUE_FALSE;
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        for (int i = 0; i < size; i++) {
            if ((v[i] & VALUE_MASK) != VALUE_BOOL) {
                return value_ctx_failure(ctx, values, "set.any() can only be applied to booleans");
            }
            if (v[i] != VALUE_FALSE) {
                return VALUE_TRUE;
            }
        }
		return VALUE_FALSE;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= 2 * sizeof(hvalue_t);
        for (int i = 0; i < size; i++) {
            if ((v[2*i+1] & VALUE_MASK) != VALUE_BOOL) {
                return value_ctx_failure(ctx, values, "dict.any() can only be applied to booleans");
            }
            if (v[2*i+1] != VALUE_FALSE) {
                return VALUE_TRUE;
            }
        }
		return VALUE_FALSE;
    }
    return value_ctx_failure(ctx, values, "any() can only be applied to sets or dictionaries");
}

hvalue_t nametag(struct context *ctx, struct values_t *values){
    hvalue_t nt = value_dict_store(values, VALUE_DICT,
            (0 << VALUE_BITS) | VALUE_INT, ctx->entry);
    return value_dict_store(values, nt,
            (1 << VALUE_BITS) | VALUE_INT, ctx->arg);
}

hvalue_t f_atLabel(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    if (ctx->atomic == 0) {
        return value_ctx_failure(ctx, values, "atLabel: can only be called in atomic mode");
    }
    hvalue_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_PC) {
        return value_ctx_failure(ctx, values, "atLabel: not a label");
    }
    e >>= VALUE_BITS;

    int size;
    hvalue_t *vals = value_get(state->ctxbag, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    assert(size % 2 == 0);
    hvalue_t bag = VALUE_DICT;
    for (int i = 0; i < size; i += 2) {
        assert((vals[i] & VALUE_MASK) == VALUE_CONTEXT);
        assert((vals[i+1] & VALUE_MASK) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        if ((hvalue_t) ctx->pc == e) {
            bag = value_bag_add(values, bag, nametag(ctx, values),
                (int) (vals[i+1] >> VALUE_BITS));
        }
    }
    return bag;
}

hvalue_t f_countLabel(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    if (ctx->atomic == 0) {
        return value_ctx_failure(ctx, values, "countLabel: can only be called in atomic mode");
    }
    hvalue_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_PC) {
        return value_ctx_failure(ctx, values, "countLabel: not a label");
    }
    e >>= VALUE_BITS;

    int size;
    hvalue_t *vals = value_get(state->ctxbag, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    assert(size % 2 == 0);
    hvalue_t result = 0;
    for (int i = 0; i < size; i += 2) {
        assert((vals[i] & VALUE_MASK) == VALUE_CONTEXT);
        assert((vals[i+1] & VALUE_MASK) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        if ((hvalue_t) ctx->pc == e) {
            result += vals[i+1] >> VALUE_BITS;;
        }
    }
    return (result << VALUE_BITS) | VALUE_INT;
}

hvalue_t f_div(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    int64_t e1 = args[0], e2 = args[1];
    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "right argument to / not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "left argument to / not an integer");
    }
    e1 >>= VALUE_BITS;
    if (e1 == 0) {
        return value_ctx_failure(ctx, values, "divide by zero");
    }
    int64_t result = (e2 >> VALUE_BITS) / e1;
    return (result << VALUE_BITS) | VALUE_INT;
}

hvalue_t f_eq(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    return ((args[0] == args[1]) << VALUE_BITS) | VALUE_BOOL;
}

hvalue_t f_ge(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp >= 0) << VALUE_BITS) | VALUE_BOOL;
}

hvalue_t f_gt(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp > 0) << VALUE_BITS) | VALUE_BOOL;
}

hvalue_t f_ne(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    return ((args[0] != args[1]) << VALUE_BITS) | VALUE_BOOL;
}

hvalue_t f_in(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    hvalue_t s = args[0], e = args[1];
	if (s == VALUE_SET || s == VALUE_DICT) {
		return VALUE_FALSE;
	}
    if ((s & VALUE_MASK) == VALUE_ATOM) {
        if ((e & VALUE_MASK) != VALUE_ATOM) {
            return value_ctx_failure(ctx, values, "'in <string>' can only be applied to another string");
        }
        if (s == VALUE_ATOM) {
            return ((e == VALUE_ATOM) << VALUE_BITS) | VALUE_BOOL;
        }
        int size1, size2;
        char *v1 = value_get(e, &size1);
        char *v2 = value_get(s, &size2);
        if (size1 > size2) {
            return VALUE_FALSE;
        }
        // stupid way of checking if v1 is a substring of v2
        int n = size2 - size1;
        for (int i = 0; i <= n; i++) {
            if (memcmp(v1, v2 + i, size1) == 0) {
                return VALUE_TRUE;
            }
        }
        return VALUE_FALSE;
    }
    if ((s & VALUE_MASK) == VALUE_SET) {
        int size;
        hvalue_t *v = value_get(s, &size);
        size /= sizeof(hvalue_t);
        for (int i = 0; i < size; i++) {
            if (v[i] == e) {
                return VALUE_TRUE;
            }
        }
        return VALUE_FALSE;
    }
    if ((s & VALUE_MASK) == VALUE_DICT) {
        int size;
        hvalue_t *v = value_get(s, &size);
        size /= 2 * sizeof(hvalue_t);
        for (int i = 0; i < size; i++) {
            if (v[2*i+1] == e) {
                return VALUE_TRUE;
            }
        }
        return VALUE_FALSE;
    }
    return value_ctx_failure(ctx, values, "'in' can only be applied to sets or dictionaries");
}

hvalue_t f_intersection(
    struct state *state,
    struct context *ctx,
    hvalue_t *args,
    int n,
    struct values_t *values
) {
    hvalue_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return value_ctx_failure(ctx, values, "'&' applied to mix of ints and other types");
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
		vi[0].vals = value_get(args[0], &vi[0].size); 
		vi[0].index = 0;
        int min_size = vi[0].size;              // minimum set size
        hvalue_t max_val = vi[0].vals[0];       // maximum value over the minima of all sets
        for (int i = 1; i < n; i++) {
            if ((args[i] & VALUE_MASK) != VALUE_SET) {
                return value_ctx_failure(ctx, values, "'&' applied to mix of sets and other types");
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
        hvalue_t *vals = malloc((size_t) min_size), *v = vals;

        bool done = false;
        for (int i = 0; i < min_size; i++) {
            hvalue_t old_max = max_val;
            for (int j = 0; j < n; j++) {
                int k, size = vi[j].size / sizeof(hvalue_t);
                while ((k = vi[j].index) < size) {
                    hvalue_t v = vi[j].vals[k];
                    int cmp = value_cmp(v, max_val);
                    if (cmp > 0) {
                        max_val = v;
                    }
                    if (cmp >= 0) {
                        break;
                    }
                    vi[j].index++;
                }
                if (vi[j].index == size) {
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
                    assert(vi[j].index < vi[j].size / sizeof(hvalue_t));
                    vi[j].index++;
                    int k, size = vi[j].size / sizeof(hvalue_t);
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

        hvalue_t result = value_put_set(values, vals, (char *) v - (char *) vals);
        free(vi);
        free(vals);
        return result;
    }

	if (e1 == VALUE_DICT) {
		return VALUE_DICT;
	}
    if ((e1 & VALUE_MASK) != VALUE_DICT) {
        return value_ctx_failure(ctx, values, "'&' can only be applied to ints and dicts");
    }
    // get all the dictionaries
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_DICT) {
            return value_ctx_failure(ctx, values, "'&' applied to mix of dictionaries and other types");
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
    hvalue_t *vals = malloc(total);
    total = 0;
    for (int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // sort lexicographically, leaving duplicate keys
    int cnt = total / (2 * sizeof(hvalue_t));
    qsort(vals, cnt, 2 * sizeof(hvalue_t), q_kv_cmp);

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

    hvalue_t result = value_put_dict(values, vals, 2 * out * sizeof(hvalue_t));
    free(vi);
    free(vals);
    return result;
}

hvalue_t f_invert(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    int64_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "~ can only be applied to ints");
    }
    e >>= VALUE_BITS;
    return ((~e) << VALUE_BITS) | VALUE_INT;
}

hvalue_t f_isEmpty(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
    if ((e & VALUE_MASK) == VALUE_DICT) {
        return ((e == VALUE_DICT) << VALUE_BITS) | VALUE_BOOL;
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        return ((e == VALUE_SET) << VALUE_BITS) | VALUE_BOOL;
    }
    if ((e & VALUE_MASK) == VALUE_ATOM) {
        return ((e == VALUE_ATOM) << VALUE_BITS) | VALUE_BOOL;
    }
    return value_ctx_failure(ctx, values, "loops can only iterate over dictionaries and sets");
}

hvalue_t f_keys(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t v = args[0];
    if ((v & VALUE_MASK) != VALUE_DICT) {
        return value_ctx_failure(ctx, values, "keys() can only be applied to dictionaries");
    }
    if (v == VALUE_DICT) {
        return VALUE_SET;
    }

    int size;
    hvalue_t *vals = value_get(v, &size);
    hvalue_t *keys = malloc(size / 2);
    size /= 2 * sizeof(hvalue_t);
    for (int i = 0; i < size; i++) {
        keys[i] = vals[2*i];
    }
    hvalue_t result = value_put_set(values, keys, size * sizeof(hvalue_t));
    free(keys);
    return result;
}

hvalue_t f_str(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
    char *s = value_string(e);
    hvalue_t v = value_put_atom(values, s, strlen(s));
    free(s);
    return v;
}

hvalue_t f_len(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_DICT) {
		return VALUE_INT;
	}
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        (void) value_get(e, &size);
        size /= sizeof(hvalue_t);
        return (size << VALUE_BITS) | VALUE_INT;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        (void) value_get(e, &size);
        size /= 2 * sizeof(hvalue_t);
        return (size << VALUE_BITS) | VALUE_INT;
    }
    if ((e & VALUE_MASK) == VALUE_ATOM) {
        int size;
        (void) value_get(e, &size);
        return (size << VALUE_BITS) | VALUE_INT;
    }
    return value_ctx_failure(ctx, values, "len() can only be applied to sets, dictionaries, or strings");
}

hvalue_t f_le(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp <= 0) << VALUE_BITS) | VALUE_BOOL;
}

hvalue_t f_lt(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return ((cmp < 0) << VALUE_BITS) | VALUE_BOOL;
}

hvalue_t f_max(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET) {
        return value_ctx_failure(ctx, values, "can't apply max() to empty set");
    }
    if (e == VALUE_DICT) {
        return value_ctx_failure(ctx, values, "can't apply max() to empty list");
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        hvalue_t max = v[0];
        for (int i = 1; i < size; i++) {
            if (value_cmp(v[i], max) > 0) {
                max = v[i];
            }
        }
		return max;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= 2 * sizeof(hvalue_t);
        hvalue_t max = v[1];
        for (int i = 0; i < size; i++) {
            if (value_cmp(v[2*i+1], max) > 0) {
                max = v[2*i+1];
            }
        }
		return max;
    }
    return value_ctx_failure(ctx, values, "max() can only be applied to sets or lists");
}

hvalue_t f_min(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET) {
        return value_ctx_failure(ctx, values, "can't apply min() to empty set");
    }
    if (e == VALUE_DICT) {
        return value_ctx_failure(ctx, values, "can't apply min() to empty list");
    }
    if ((e & VALUE_MASK) == VALUE_SET) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        hvalue_t min = v[0];
        for (int i = 1; i < size; i++) {
            if (value_cmp(v[i], min) < 0) {
                min = v[i];
            }
        }
		return min;
    }
    if ((e & VALUE_MASK) == VALUE_DICT) {
        int size;
        hvalue_t *v = value_get(e, &size);
        size /= 2 * sizeof(hvalue_t);
        hvalue_t min = v[1];
        for (int i = 0; i < size; i++) {
            if (value_cmp(v[2*i+1], min) < 0) {
                min = v[2*i+1];
            }
        }
		return min;
    }
    return value_ctx_failure(ctx, values, "min() can only be applied to sets or lists");
}

hvalue_t f_minus(
    struct state *state,
    struct context *ctx,
    hvalue_t *args,
    int n,
    struct values_t *values
) {
    assert(n == 1 || n == 2);
    if (n == 1) {
        int64_t e = args[0];
        if ((e & VALUE_MASK) != VALUE_INT) {
            return value_ctx_failure(ctx, values, "unary minus can only be applied to ints");
        }
        e >>= VALUE_BITS;
        if (e == VALUE_MAX) {
            return ((hvalue_t) VALUE_MIN << VALUE_BITS) | VALUE_INT;
        }
        if (e == VALUE_MIN) {
            return (VALUE_MAX << VALUE_BITS) | VALUE_INT;
        }
        if (-e <= VALUE_MIN || -e >= VALUE_MAX) {
            return value_ctx_failure(ctx, values, "unary minus overflow (model too large)");
        }
        return ((-e) << VALUE_BITS) | VALUE_INT;
    }
    else {
        if ((args[0] & VALUE_MASK) == VALUE_INT) {
            int64_t e1 = args[0], e2 = args[1];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return value_ctx_failure(ctx, values, "minus applied to int and non-int");
            }
            e1 >>= VALUE_BITS;
            e2 >>= VALUE_BITS;
            int64_t result = e2 - e1;
            if (result <= VALUE_MIN || result >= VALUE_MAX) {
                return value_ctx_failure(ctx, values, "minus overflow (model too large)");
            }
            return (result << VALUE_BITS) | VALUE_INT;
        }

        hvalue_t e1 = args[0], e2 = args[1];
        if ((e1 & VALUE_MASK) != VALUE_SET || (e2 & VALUE_MASK) != VALUE_SET) {
            return value_ctx_failure(ctx, values, "minus can only be applied to ints or sets");
        }
        int size1, size2;
        hvalue_t *vals1, *vals2;
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
        hvalue_t *vals = malloc(size2);
        size1 /= sizeof(hvalue_t);
        size2 /= sizeof(hvalue_t);

        hvalue_t *p1 = vals1, *p2 = vals2, *q = vals;
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
        hvalue_t result = value_put_set(values, vals, (char *) q - (char *) vals);
        free(vals);
        return result;
    }
}

hvalue_t f_mod(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    int64_t e1 = args[0], e2 = args[1];
    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "right argument to mod not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "left argument to mod not an integer");
    }
    int64_t mod = (e1 >> VALUE_BITS);
    int64_t result = (e2 >> VALUE_BITS) % mod;
    if (result < 0) {
        result += mod;
    }
    return (result << VALUE_BITS) | VALUE_INT;
}

hvalue_t f_get_context(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    return value_put_context(values, ctx);
}

hvalue_t f_not(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 1);
    hvalue_t e = args[0];
    if ((e & VALUE_MASK) != VALUE_BOOL) {
        return value_ctx_failure(ctx, values, "not can only be applied to booleans");
    }
    return e ^ (1 << VALUE_BITS);
}

hvalue_t f_plus(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    int64_t e1 = args[0];
    if ((e1 & VALUE_MASK) == VALUE_INT) {
        e1 >>= VALUE_BITS;
        for (int i = 1; i < n; i++) {
            int64_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return value_ctx_failure(ctx, values,
                    "+: applied to mix of integers and other values");
            }
            e2 >>= VALUE_BITS;
            int64_t sum = e1 + e2;
            if (sum <= VALUE_MIN || sum >= VALUE_MAX) {
                return value_ctx_failure(ctx, values,
                    "+: integer overflow (model too large)");
            }
            e1 = sum;
        }
        return (e1 << VALUE_BITS) | VALUE_INT;
    }

    if ((e1 & VALUE_MASK) == VALUE_ATOM) {
        struct strbuf sb;
        strbuf_init(&sb);
        for (int i = n; --i >= 0;) {
            if ((args[i] & VALUE_MASK) != VALUE_ATOM) {
                return value_ctx_failure(ctx, values,
                    "+: applied to mix of strings and other values");
            }
            int size;
            char *chars = value_get(args[i], &size);
            strbuf_append(&sb, chars, size);
        }
        char *result = strbuf_convert(&sb);
        hvalue_t v = value_put_atom(values, result, strbuf_getlen(&sb));
        return v;
    }

    // get all the lists
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_DICT) {
            value_ctx_failure(ctx, values, "+: applied to mix of value types");
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
    hvalue_t *vals = malloc(total);
    total = 0;
    for (int i = n; --i >= 0;) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // Update the indices
    n = total / (2 * sizeof(hvalue_t));
    for (int i = 0; i < n; i++) {
        vals[2*i] = (i << VALUE_BITS) | VALUE_INT;
    }
    hvalue_t result = value_put_dict(values, vals, total);

    free(vi);
    free(vals);
    return result;
}

hvalue_t f_power(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "right argument to ** not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "left argument to ** not an integer");
    }
    int64_t base = e2 >> VALUE_BITS;
    int64_t exp = e1 >> VALUE_BITS;
    if (exp == 0) {
        return (1 << VALUE_BITS) | VALUE_INT;
    }
    if (exp < 0) {
        return value_ctx_failure(ctx, values, "**: negative exponent");
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
        return value_ctx_failure(ctx, values, "**: overflow (model too large)");
    }

    return (result << VALUE_BITS) | VALUE_INT;
}

hvalue_t f_range(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "right argument to .. not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "left argument to .. not an integer");
    }
    int64_t start = e2 >> VALUE_BITS;
    int64_t finish = e1 >> VALUE_BITS;
	if (finish < start) {
		return VALUE_SET;
	}
    int cnt = (finish - start) + 1;
	assert(cnt > 0);
	assert(cnt < 1000);		// seems unlikely...
    hvalue_t *v = malloc(cnt * sizeof(hvalue_t));
    for (int i = 0; i < cnt; i++) {
        v[i] = ((start + i) << VALUE_BITS) | VALUE_INT;
    }
    hvalue_t result = value_put_set(values, v, cnt * sizeof(hvalue_t));
    free(v);
    return result;
}

hvalue_t f_dict_add(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 3);
    int64_t value = args[0], key = args[1], dict = args[2];
    assert((dict & VALUE_MASK) == VALUE_DICT);
    int size;
    hvalue_t *vals = value_get(dict, &size), *v;

    int i = 0, cmp = 1;
    for (v = vals; i < size; i += 2 * sizeof(hvalue_t), v += 2) {
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
        hvalue_t *nvals = malloc(size);
        memcpy(nvals, vals, size);
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) = value;

        hvalue_t result = value_put_dict(values, nvals, size);
        free(nvals);
        return result;
    }
    else {
        hvalue_t *nvals = malloc(size + 2*sizeof(hvalue_t));
        memcpy(nvals, vals, i);
        * (hvalue_t *) ((char *) nvals + i) = key;
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) = value;
        memcpy((char *) nvals + i + 2*sizeof(hvalue_t), v, size - i);

        hvalue_t result = value_put_dict(values, nvals, size + 2*sizeof(hvalue_t));
        free(nvals);
        return result;
    }
}

hvalue_t f_set_add(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int64_t elt = args[0], set = args[1];
    assert((set & VALUE_MASK) == VALUE_SET);
    int size;
    hvalue_t *vals = value_get(set, &size), *v;

    int i = 0;
    for (v = vals; i < size; i += sizeof(hvalue_t), v++) {
        int cmp = value_cmp(elt, *v);
        if (cmp == 0) {
            return set;
        }
        if (cmp < 0) {
            break;
        }
    }

    hvalue_t *nvals = malloc(size + sizeof(hvalue_t));
    memcpy(nvals, vals, i);
    * (hvalue_t *) ((char *) nvals + i) = elt;
    memcpy((char *) nvals + i + sizeof(hvalue_t), v, size - i);

    hvalue_t result = value_put_set(values, nvals, size + sizeof(hvalue_t));
    free(nvals);
    return result;
}

hvalue_t f_value_bag_add(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int64_t elt = args[0], dict = args[1];
    assert((dict & VALUE_MASK) == VALUE_DICT);
    int size;
    hvalue_t *vals = value_get(dict, &size), *v;

    int i = 0, cmp = 1;
    for (v = vals; i < size; i += 2 * sizeof(hvalue_t), v++) {
        cmp = value_cmp(elt, *v);
        if (cmp <= 0) {
            break;
        }
    }

    if (cmp == 0) {
        assert((v[1] & VALUE_MASK) == VALUE_INT);
        int cnt = (v[1] >> VALUE_BITS) + 1;
        hvalue_t *nvals = malloc(size);
        memcpy(nvals, vals, size);
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) =
                                        (cnt << VALUE_BITS) | VALUE_INT;

        hvalue_t result = value_put_dict(values, nvals, size);
        free(nvals);
        return result;
    }
    else {
        hvalue_t *nvals = malloc(size + 2*sizeof(hvalue_t));
        memcpy(nvals, vals, i);
        * (hvalue_t *) ((char *) nvals + i) = elt;
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) =
                                        (1 << VALUE_BITS) | VALUE_INT;
        memcpy((char *) nvals + i + 2*sizeof(hvalue_t), v, size - i);

        hvalue_t result = value_put_dict(values, nvals, size + 2*sizeof(hvalue_t));
        free(nvals);
        return result;
    }
}

hvalue_t f_shiftleft(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "right argument to << not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "left argument to << not an integer");
    }
    e1 >>= VALUE_BITS;
    if (e1 < 0) {
        return value_ctx_failure(ctx, values, "<<: negative shift count");
    }
    e2 >>= VALUE_BITS;
    int64_t result = e2 << e1;
    if (((result << VALUE_BITS) >> VALUE_BITS) != result) {
        return value_ctx_failure(ctx, values, "<<: overflow (model too large)");
    }
    if (result <= VALUE_MIN || result >= VALUE_MAX) {
        return value_ctx_failure(ctx, values, "<<: overflow (model too large)");
    }
    return (result << VALUE_BITS) | VALUE_INT;
}

hvalue_t f_shiftright(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if ((e1 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "right argument to >> not an integer");
    }
    if ((e2 & VALUE_MASK) != VALUE_INT) {
        return value_ctx_failure(ctx, values, "left argument to >> not an integer");
    }
    if (e1 < 0) {
        return value_ctx_failure(ctx, values, ">>: negative shift count");
    }
    e1 >>= VALUE_BITS;
    e2 >>= VALUE_BITS;
    return ((e2 >> e1) << VALUE_BITS) | VALUE_INT;
}

hvalue_t f_times(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    int64_t result = 1;
    int list = -1;
    for (int i = 0; i < n; i++) {
        int64_t e = args[i];
        if ((e & VALUE_MASK) == VALUE_DICT || (e & VALUE_MASK) == VALUE_ATOM) {
            if (list >= 0) {
                return value_ctx_failure(ctx, values, "* can only have at most one list or string");
            }
            list = i;
        }
        else {
            if ((e & VALUE_MASK) != VALUE_INT) {
                return value_ctx_failure(ctx, values,
                    "* can only be applied to integers and at most one list or string");
            }
            e >>= VALUE_BITS;
            if (e == 0) {
                result = 0;
            }
            else {
                int64_t product = result * e;
                if (product / result != e) {
                    return value_ctx_failure(ctx, values, "*: overflow (model too large)");
                }
                result = product;
            }
        }
    }
    if (result != (result << VALUE_BITS) >> VALUE_BITS) {
        return value_ctx_failure(ctx, values, "*: overflow (model too large)");
    }
    if (list < 0) {
        return (result << VALUE_BITS) | VALUE_INT;
    }
    if (result == 0) {
        return args[list] & VALUE_MASK;
    }
    if ((args[list] & VALUE_MASK) == VALUE_DICT) {
        int size;
        hvalue_t *vals = value_get(args[list], &size);
        if (size == 0) {
            return VALUE_DICT;
        }
        hvalue_t *r = malloc(result * size);
        unsigned int cnt = size / (2 * sizeof(hvalue_t));
        int index = 0;
        for (int i = 0; i < result; i++) {
            for (unsigned int j = 0; j < cnt; j++) {
                r[2*index] = (index << VALUE_BITS) | VALUE_INT;
                r[2*index+1] = vals[2*j+1];
                index++;
            }
        }
        hvalue_t v = value_put_dict(values, r, result * size);
        free(r);
        return v;
    }
    assert((args[list] & VALUE_MASK) == VALUE_ATOM);
	int size;
	char *chars = value_get(args[list], &size);
	if (size == 0) {
		return VALUE_ATOM;
	}
	struct strbuf sb;
	strbuf_init(&sb);
	for (int i = 0; i < result; i++) {
		strbuf_append(&sb, chars, size);
	}
	char *s = strbuf_getstr(&sb);
	hvalue_t v = value_put_atom(values, s, result * size);
	free(s);
	return v;
}

hvalue_t f_union(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    hvalue_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return value_ctx_failure(ctx, values, "'|' applied to mix of ints and other types");
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
                return value_ctx_failure(ctx, values, "'|' applied to mix of sets and other types");
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
        hvalue_t *vals = malloc(total);
        total = 0;
        for (int i = 0; i < n; i++) {
            memcpy((char *) vals + total, vi[i].vals, vi[i].size);
            total += vi[i].size;
        }

        n = sort(vals, total / sizeof(hvalue_t));
        hvalue_t result = value_put_set(values, vals, n * sizeof(hvalue_t));
        free(vi);
        free(vals);
        return result;
    }

    if ((e1 & VALUE_MASK) != VALUE_DICT) {
        return value_ctx_failure(ctx, values, "'|' can only be applied to ints and dicts");
    }
    // get all the dictionaries
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if ((args[i] & VALUE_MASK) != VALUE_DICT) {
            return value_ctx_failure(ctx, values, "'|' applied to mix of dictionaries and other types");
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
    hvalue_t *vals = malloc(total);
    total = 0;
    for (int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // sort lexicographically, leaving duplicate keys
    int cnt = total / (2 * sizeof(hvalue_t));
    qsort(vals, cnt, 2 * sizeof(hvalue_t), q_kv_cmp);

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

    hvalue_t result = value_put_dict(values, vals, 2 * n * sizeof(hvalue_t));
    free(vi);
    free(vals);
    return result;
}

hvalue_t f_xor(struct state *state, struct context *ctx, hvalue_t *args, int n, struct values_t *values){
    hvalue_t e1 = args[0];

    if ((e1 & VALUE_MASK) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if ((e2 & VALUE_MASK) != VALUE_INT) {
                return value_ctx_failure(ctx, values, "'^' applied to mix of ints and other types");
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
            return value_ctx_failure(ctx, values, "'^' applied to mix of value types");
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
    hvalue_t *vals = malloc(total);
    total = 0;
    for (int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // sort the values, but retain duplicates
    int cnt = total / sizeof(hvalue_t);
    qsort(vals, cnt, sizeof(hvalue_t), q_value_cmp);

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

    hvalue_t result = value_put_set(values, vals, k * sizeof(hvalue_t));
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
	{ "Print", init_Print, op_Print },
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
    { "BagAdd", f_value_bag_add },
    { "countLabel", f_countLabel },
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
    { "str", f_str },
    { "SetAdd", f_set_add },
    { NULL, NULL }
};

struct op_info *ops_get(char *opname, int size){
    return dict_lookup(ops_map, opname, size);
}

void ops_init(struct global_t *global) {
    ops_map = dict_new(0);
    f_map = dict_new(0);
	underscore = value_put_atom(&global->values, "_", 1);
	this_atom = value_put_atom(&global->values, "this", 4);

    for (struct op_info *oi = op_table; oi->name != NULL; oi++) {
        void **p = dict_insert(ops_map, oi->name, strlen(oi->name));
        *p = oi;
    }
    for (struct f_info *fi = f_table; fi->name != NULL; fi++) {
        void **p = dict_insert(f_map, fi->name, strlen(fi->name));
        *p = fi;
    }
}
