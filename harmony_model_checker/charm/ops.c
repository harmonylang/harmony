#include "head.h"

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#include "ops.h"
#include "strbuf.h"
#include "dfa.h"
#include "hashdict.h"
#include "spawn.h"

#define MAX_ARITY   16

struct val_info {
    unsigned int size, index;
    hvalue_t *vals;
};

struct f_info {
    char *name;
    hvalue_t (*f)(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine);
};

struct var_tree {
    enum { VT_NAME, VT_TUPLE } type;
    union {
        hvalue_t name;
        struct {
            unsigned int n;
            struct var_tree **elements;
        } tuple;
    } u;
};

// These are initialized in ops_init and are immutable.
static struct dict *ops_map, *f_map;
static hvalue_t underscore, this_atom;
static hvalue_t type_bool, type_int, type_str, type_pc, type_list;
static hvalue_t type_dict, type_set, type_address, type_context;

static inline void ctx_push(struct context *ctx, hvalue_t v){
    // TODO.  Check for stack overflow
    ctx->stack[ctx->sp++] = v;
}

static inline hvalue_t ctx_pop(struct context *ctx){
    assert(ctx->sp > 0);
    return ctx->stack[--ctx->sp];
}

static bool is_sequential(hvalue_t seqvars, hvalue_t *indices, unsigned int n){
    assert(VALUE_TYPE(seqvars) == VALUE_SET);
    unsigned int size;
    hvalue_t *seqs = value_get(seqvars, &size);
    size /= sizeof(hvalue_t);

    n *= sizeof(hvalue_t);
    for (unsigned int i = 0; i < size; i++) {
        assert(VALUE_TYPE(seqs[i]) == VALUE_ADDRESS);
        unsigned int sn;
        hvalue_t *inds = value_get(seqs[i], &sn);
        if (n >= sn && sn >= 0 && memcmp(indices, inds, sn) == 0) {
            return true;
        }
    }
    return false;
}

hvalue_t var_match_rec(struct context *ctx, struct var_tree *vt, struct engine *engine,
                            hvalue_t arg, hvalue_t vars){
    switch (vt->type) {
    case VT_NAME:
        if (vt->u.name == underscore) {
            return vars;
        }
        return value_dict_store(engine, vars, vt->u.name, arg);
    case VT_TUPLE:
        if (VALUE_TYPE(arg) != VALUE_LIST) {
            if (vt->u.tuple.n == 0) {
                return value_ctx_failure(ctx, engine, "match: expected ()");
            }
            else {
                char *v = value_string(arg);
                return value_ctx_failure(ctx, engine, "match: expected a tuple instead of %s", v);
            }
        }
        if (arg == VALUE_LIST) {
            if (vt->u.tuple.n != 0) {
                return value_ctx_failure(ctx, engine, "match: expected a %d-tuple",
                                                vt->u.tuple.n);
            }
            return vars;
        }
        if (vt->u.tuple.n == 0) {
            return value_ctx_failure(ctx, engine, "match: expected an empty tuple");
        }
        unsigned int size;
        hvalue_t *vals = value_get(arg, &size);
        size /= sizeof(hvalue_t);
        if (vt->u.tuple.n != size) {
            return value_ctx_failure(ctx, engine, "match: tuple size mismatch");
        }
        for (unsigned int i = 0; i < size; i++) {
            vars = var_match_rec(ctx, vt->u.tuple.elements[i], engine, vals[i], vars);
        }
        return vars;
    default:
        panic("var_tree_rec: bad vartree type");
        return 0;
    }
}

void var_match(struct context *ctx, struct var_tree *vt, struct engine *engine, hvalue_t arg){
    hvalue_t vars = var_match_rec(ctx, vt, engine, arg, ctx->vars);
    if (ctx->failure == 0) {
        ctx->vars = vars;
    }
}

static void skip_blanks(char *s, int len, int *index){
    while (*index < len && s[*index] == ' ') {
        (*index)++;
    }
}

struct var_tree *var_parse(struct engine *engine, char *s, int len, int *index){
    assert(*index < len);
    struct var_tree *vt = new_alloc(struct var_tree);

    skip_blanks(s, len, index);
    if (s[*index] == '(' || s[*index] == '[') {
        char closer = s[*index] == '(' ? ')' : ']';
        vt->type = VT_TUPLE;
        (*index)++;
        skip_blanks(s, len, index);
        assert(*index < len);
        if (s[*index] == closer) {
            (*index)++;
        }
        else {
            while (true) {
                struct var_tree *elt = var_parse(engine, s, len, index);
                vt->u.tuple.elements = realloc(vt->u.tuple.elements,
                        (vt->u.tuple.n + 1) * sizeof(elt));
                vt->u.tuple.elements[vt->u.tuple.n++] = elt;
                skip_blanks(s, len, index);
                assert(*index < len);
                if (s[*index] == closer) {
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
        assert(isalpha(s[i]) || s[i] == '_' || s[i] == '$');
        i++;
        while (i < len && (isalpha(s[i]) || s[i] == '_' || isdigit(s[i]))) {
            i++;
        }
        vt->u.name = value_put_atom(engine, &s[*index], i - *index);
        *index = i;
    }
    return vt;
}

void interrupt_invoke(struct step *step){
    assert(!step->ctx->interruptlevel);
	assert(VALUE_TYPE(step->ctx->trap_pc) == VALUE_PC);
    ctx_push(step->ctx, VALUE_TO_PC(step->ctx->pc));
    ctx_push(step->ctx, VALUE_TO_INT(CALLTYPE_INTERRUPT));
    ctx_push(step->ctx, step->ctx->trap_arg);
    step->ctx->pc = VALUE_FROM_PC(step->ctx->trap_pc);
    step->ctx->trap_pc = 0;
    step->ctx->interruptlevel = true;
}

bool ind_tryload(struct engine *engine, hvalue_t dict, hvalue_t *indices, int n, hvalue_t *result){
    hvalue_t d = dict;
    for (int i = 0; i < n; i++) {
        if (!value_tryload(engine, d, indices[i], &d)) {
            return false;
        }
    }
    *result = d;
    return true;
}

static bool ind_trystore(hvalue_t root, hvalue_t *indices, int n, hvalue_t value, struct engine *engine, hvalue_t *result){
    assert(VALUE_TYPE(root) == VALUE_DICT || VALUE_TYPE(root) == VALUE_LIST);
    assert(n > 0);

    if (n == 1) {
        return value_trystore(engine, root, indices[0], value, true, result);
    }
    unsigned int size;
    hvalue_t *vals = value_get(root, &size);
    size /= sizeof(hvalue_t);

    if (VALUE_TYPE(root) == VALUE_DICT) {
        assert(size % 2 == 0);

        for (unsigned i = 0; i < size; i += 2) {
            if (vals[i] == indices[0]) {
                hvalue_t d = vals[i+1];
                if (VALUE_TYPE(d) != VALUE_DICT && VALUE_TYPE(d) != VALUE_LIST) {
                    return false;
                }
                hvalue_t nd;
                if (!ind_trystore(d, indices + 1, n - 1, value, engine, &nd)) {
                    return false;
                }
                if (d == nd) {
                    *result = root;
                    return true;
                }
                int n = size * sizeof(hvalue_t);
                hvalue_t *copy = malloc(n);
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                hvalue_t v = value_put_dict(engine, copy, n);
                free(copy);
                *result = v;
                return true;
            }
            /* value_cmp is an expensive function.  Breaking here
             * is probably more expensive than just going on.
                if (value_cmp(vals[i], indices[0]) > 0) {
                    assert(false);
                }
             */
        }
        return false;
    }
    else {
        assert(VALUE_TYPE(root) == VALUE_LIST);
        if (VALUE_TYPE(indices[0]) != VALUE_INT) {
            return false;
        }
        unsigned int index = (unsigned int) VALUE_FROM_INT(indices[0]);
        if (index >= size) {
            return false;
        }
        hvalue_t d = vals[index];
        if (VALUE_TYPE(d) != VALUE_DICT && VALUE_TYPE(d) != VALUE_LIST) {
            return false;
        }
        hvalue_t nd;
        if (!ind_trystore(d, indices + 1, n - 1, value, engine, &nd)) {
            return false;
        }
        if (d == nd) {
            *result = root;
            return true;
        }
        int nsize = size * sizeof(hvalue_t);
        hvalue_t *copy = malloc(nsize);
        memcpy(copy, vals, nsize);
        copy[index] = nd;
        hvalue_t v = value_put_list(engine, copy, nsize);
        free(copy);
        *result = v;
        return true;
    }
}

bool ind_remove(hvalue_t root, hvalue_t *indices, int n, struct engine *engine,
                                        hvalue_t *result) {
    assert(VALUE_TYPE(root) == VALUE_DICT || VALUE_TYPE(root) == VALUE_LIST);
    assert(n > 0);

    if (n == 1) {
        *result = value_remove(engine, root, indices[0]);
        return true;
    }

    unsigned int size;
    hvalue_t *vals = value_get(root, &size);
    size /= sizeof(hvalue_t);

    if (VALUE_TYPE(root) == VALUE_DICT) {
        assert(size % 2 == 0);

        for (unsigned i = 0; i < size; i += 2) {
            if (vals[i] == indices[0]) {
                hvalue_t d = vals[i+1];
                if (VALUE_TYPE(d) != VALUE_DICT && VALUE_TYPE(d) != VALUE_LIST) {
                    return false;
                }
                hvalue_t nd;
                if (!ind_remove(d, indices + 1, n - 1, engine, &nd)) {
                    return false;
                }
                if (d == nd) {
                    *result = root;
                    return true;
                }
                int n = size * sizeof(hvalue_t);
                hvalue_t *copy = malloc(n);
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                hvalue_t v = value_put_dict(engine, copy, n);
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
    else {
        assert(VALUE_TYPE(root) == VALUE_LIST);
        assert(VALUE_TYPE(root) == VALUE_LIST);
        if (VALUE_TYPE(indices[0]) != VALUE_INT) {
            return false;
        }
        int index = VALUE_FROM_INT(indices[0]);
        if (index < 0 || index >= n) {
            return false;
        }
        hvalue_t d = vals[index];
        if (VALUE_TYPE(d) != VALUE_DICT && VALUE_TYPE(d) != VALUE_LIST) {
            return false;
        }
        hvalue_t nd;
        if (!ind_remove(d, indices + 1, n - 1, engine, &nd)) {
            return false;
        }
        if (d == nd) {
            *result = root;
            return true;
        }
        int n = size * sizeof(hvalue_t);
        hvalue_t *copy = malloc(n);
        memcpy(copy, vals, n);
        copy[index] = nd;
        hvalue_t v = value_put_list(engine, copy, n);
        free(copy);
        *result = v;
        return true;
    }
    return false;
}

void op_Address(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t index = ctx_pop(step->ctx);
    hvalue_t av = ctx_pop(step->ctx);
    if (VALUE_TYPE(av) != VALUE_ADDRESS) {
        char *p = value_string(av);
        value_ctx_failure(step->ctx, &step->engine, "%s: not an address", p);
        free(p);
        return;
    }
    if (av == VALUE_ADDRESS) {
        value_ctx_failure(step->ctx, &step->engine, "None unexpected");
        return;
    }

    unsigned int size;
    hvalue_t *indices = value_copy(av, &size);
    indices = realloc(indices, size + sizeof(index));
    indices[size / sizeof(hvalue_t)] = index;
    ctx_push(step->ctx, value_put_address(&step->engine, indices, size + sizeof(index)));
    free(indices);
    step->ctx->pc++;
}

void op_Apply(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t e = ctx_pop(step->ctx);
    hvalue_t method = ctx_pop(step->ctx);

    hvalue_t type = VALUE_TYPE(method);
    switch (type) {
    case VALUE_DICT:
        {
            hvalue_t v;
            if (!value_tryload(&step->engine, method, e, &v)) {
                char *m = value_string(method);
                char *x = value_string(e);
                value_ctx_failure(step->ctx, &step->engine, "Bad index %s: not in %s", x, m);
                free(m);
                free(x);
                return;
            }
            ctx_push(step->ctx, v);
            step->ctx->pc++;
        }
        return;
    case VALUE_LIST:
        {
            if (VALUE_TYPE(e) != VALUE_INT) {
                value_ctx_failure(step->ctx, &step->engine, "Bad index type for list");
                return;
            }
            e = VALUE_FROM_INT(e);
            unsigned int size;
            hvalue_t *vals = value_get(method, &size);
            if (e >= (hvalue_t) size) {
                value_ctx_failure(step->ctx, &step->engine, "Index out of range");
                return;
            }
            ctx_push(step->ctx, vals[e]);
            step->ctx->pc++;
        }
        return;
    case VALUE_ATOM:
        {
            if (VALUE_TYPE(e) != VALUE_INT) {
                value_ctx_failure(step->ctx, &step->engine, "Bad index type for string");
                return;
            }
            e = VALUE_FROM_INT(e);
            unsigned int size;
            char *chars = value_get(method, &size);
            if (e >= (hvalue_t) size) {
                value_ctx_failure(step->ctx, &step->engine, "Index out of range");
                return;
            }
            hvalue_t v = value_put_atom(&step->engine, &chars[e], 1);
            ctx_push(step->ctx, v);
            step->ctx->pc++;
        }
        return;
    case VALUE_PC:
        ctx_push(step->ctx, VALUE_TO_PC(step->ctx->pc + 1));
        ctx_push(step->ctx, VALUE_TO_INT(CALLTYPE_NORMAL));
        ctx_push(step->ctx, e);
        assert(VALUE_FROM_PC(method) != step->ctx->pc);
        step->ctx->pc = VALUE_FROM_PC(method);
        return;
    default:
        {
            char *x = value_string(method);
            value_ctx_failure(step->ctx, &step->engine, "Can only apply to methods or dictionaries, not to: %s", x);
            free(x);
        }
    }
}

void op_Assert(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t v = ctx_pop(step->ctx);
    if (VALUE_TYPE(v) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, &step->engine, "assert can only be applied to bool engine");
    }
    if (v == VALUE_FALSE) {
        value_ctx_failure(step->ctx, &step->engine, "Harmony assertion failed");
    }
    else {
        step->ctx->pc++;
    }
}

void op_Assert2(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t e = ctx_pop(step->ctx);
    hvalue_t v = ctx_pop(step->ctx);
    if (VALUE_TYPE(v) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, &step->engine, "assert2 can only be applied to bool engine");
    }
    if (v == VALUE_FALSE) {
        char *p = value_string(e);
        value_ctx_failure(step->ctx, &step->engine, "Harmony assertion failed: %s", p);
        free(p);
    }
    else {
        step->ctx->pc++;
    }
}

void op_Print(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t symbol = ctx_pop(step->ctx);
    if (global->run_direct) {
        char *s = value_string(symbol);
        printf("%s\n", s);
        free(s);
    }
    step->log = realloc(step->log, (step->nlog + 1) * sizeof(symbol));
    step->log[step->nlog++] = symbol;
    if (global->dfa != NULL) {
        int nstate = dfa_step(global->dfa, state->dfa_state, symbol);
        if (nstate < 0) {
            char *p = value_string(symbol);
            value_ctx_failure(step->ctx, &step->engine, "Behavior failure on %s", p);
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
    struct context *ctx = step->ctx;

    ctx->atomic++;
    ctx->pc++;
}

void op_Choose(const void *env, struct state *state, struct step *step, struct global_t *global){
    if (global->run_direct) {
        hvalue_t choices = ctx_pop(step->ctx);
        unsigned int size;
        hvalue_t *vals = value_get(choices, &size);
        size /= sizeof(hvalue_t);
        printf("Choose one from the following options:\n");
        for (unsigned int i = 0; i < size; i++) {
            char *s = value_string(vals[i]);
            printf("   %u: %s\n", i + 1, s);
            free(s);
        }
        for (;;) {
            printf("--> "); fflush(stdout);
            unsigned int selection;
            scanf("%u", &selection);
            selection -= 1;
            if (selection < size) {
                step->ctx->pc++;
                ctx_push(step->ctx, vals[selection]);
                return;
            }
            printf("Bad selection. Try again\n");
        }
    }
    else {
        panic("op_Choose: should not be called");
    }
}

void op_Continue(const void *env, struct state *state, struct step *step, struct global_t *global){
    step->ctx->pc++;
}

// This operation expects on the top of the stack the set to iterate over
// and an integer index.  If the index is valid (not the size of the
// collection), then it assigns the given element to key and value and
// pushes True.  Otherwise it pops the two engine from the stack and
// pushes False.
void op_Cut(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Cut *ec = env;
    struct context *ctx = step->ctx;

    // Get the index
    hvalue_t index = ctx_pop(step->ctx);
    assert(VALUE_TYPE(index) == VALUE_INT);
    unsigned int idx = (unsigned int) VALUE_FROM_INT(index);

    // Peek at the collection
    assert(ctx->sp > 0);
    hvalue_t v = ctx->stack[ctx->sp - 1];        // the collection

    if (VALUE_TYPE(v) == VALUE_SET || VALUE_TYPE(v) == VALUE_LIST) {
        // Get the collection
        unsigned int size;
        hvalue_t *vals = value_get(v, &size);
        size /= sizeof(hvalue_t);
        if (idx >= size) {
            ctx->stack[ctx->sp - 1] = VALUE_FALSE;
        }
        else {
            var_match(step->ctx, ec->value, &step->engine, vals[idx]);
            if (ec->key != NULL) {
                var_match(step->ctx, ec->key, &step->engine, index);
            }
            ctx_push(step->ctx, VALUE_TO_INT(idx + 1));
            ctx_push(step->ctx, VALUE_TRUE);
        }
        step->ctx->pc++;
        return;
    }
    if (VALUE_TYPE(v) == VALUE_DICT) {
        unsigned int size;
        hvalue_t *vals = value_get(v, &size);
        size /= 2 * sizeof(hvalue_t);
        if (idx >= size) {
            ctx->stack[ctx->sp - 1] = VALUE_FALSE;
        }
        else {
            if (ec->key == NULL) {
                var_match(step->ctx, ec->value, &step->engine, vals[2*idx]);
            }
            else {
                var_match(step->ctx, ec->key, &step->engine, vals[2*idx]);
                var_match(step->ctx, ec->value, &step->engine, vals[2*idx + 1]);
            }
            ctx_push(step->ctx, VALUE_TO_INT(idx + 1));
            ctx_push(step->ctx, VALUE_TRUE);
        }
        step->ctx->pc++;
        return;
    }
    if (VALUE_TYPE(v) == VALUE_ATOM) {
        unsigned int size;
        char *chars = value_get(v, &size);
        if (idx >= size) {
            ctx->stack[ctx->sp - 1] = VALUE_FALSE;
        }
        else {
            hvalue_t e = value_put_atom(&step->engine, &chars[idx], 1);
            var_match(step->ctx, ec->value, &step->engine, e);
            if (ec->key != NULL) {
                var_match(step->ctx, ec->key, &step->engine, index);
            }
            ctx_push(step->ctx, VALUE_TO_INT(idx + 1));
            ctx_push(step->ctx, VALUE_TRUE);
        }
        step->ctx->pc++;
        return;
    }
    value_ctx_failure(step->ctx, &step->engine, "op_Cut: not an iterable type");
}

void op_Del(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Del *ed = env;

    assert(VALUE_TYPE(state->vars) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, &step->engine, "Can't update state in assert or invariant");
        return;
    }

    if (ed == 0) {
        hvalue_t av = ctx_pop(step->ctx);
        if (VALUE_TYPE(av) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &step->engine, "Del %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS) {
            value_ctx_failure(step->ctx, &step->engine, "Del: address is None");
            return;
        }

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        if (step->ai != NULL) {
            step->ai->indices = indices;
            step->ai->n = size;
            step->ai->load = false;
        }
        hvalue_t nd;
        if (!ind_remove(state->vars, indices, size, &step->engine, &nd)) {
            value_ctx_failure(step->ctx, &step->engine, "Del: no such variable");
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
        if (!ind_remove(state->vars, ed->indices, ed->n, &step->engine, &nd)) {
            value_ctx_failure(step->ctx, &step->engine, "Del: bad variable");
        }
        else {
            state->vars = nd;
            step->ctx->pc++;
        }
    }
}

void op_DelVar(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_DelVar *ed = env;

    assert(VALUE_TYPE(step->ctx->vars) == VALUE_DICT);
    if (ed == NULL) {
        hvalue_t av = ctx_pop(step->ctx);
        assert(VALUE_TYPE(av) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);

        bool result;
        if (indices[0] == this_atom) {
            if (VALUE_TYPE(step->ctx->this) != VALUE_DICT) {
                value_ctx_failure(step->ctx, &step->engine, "DelVar: 'this' is not a dictionary");
                return;
            }
		    result = ind_remove(step->ctx->this, &indices[1], size - 1, &step->engine, &step->ctx->this);
        }
        else {
		    result = ind_remove(step->ctx->vars, indices, size, &step->engine, &step->ctx->vars);
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &step->engine, "DelVar: bad address: %s", x);
            free(x);
			return;
		}
    }
	else {
        if (ed->name == this_atom) {
            value_ctx_failure(step->ctx, &step->engine, "DelVar: can't del 'this'");
            return;
        }
        else {
            step->ctx->vars = value_dict_remove(&step->engine, step->ctx->vars, ed->name);
        }
	}
	step->ctx->pc++;
}

void op_Dup(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t v = ctx_pop(step->ctx);
    ctx_push(step->ctx, v);
    ctx_push(step->ctx, v);
    step->ctx->pc++;
}

void op_Frame(const void *env, struct state *state, struct step *step, struct global_t *global){
    static hvalue_t result = 0;

    if (result == 0) {
        result = value_put_atom(&step->engine, "result", 6);
    }

    const struct env_Frame *ef = env;

    // peek at argument
    hvalue_t arg = ctx_pop(step->ctx);
    ctx_push(step->ctx, arg);

    hvalue_t oldvars = step->ctx->vars;

    // Set result to None
    step->ctx->vars = value_dict_store(&step->engine, VALUE_DICT, result, VALUE_ADDRESS);

    // try to match against parameters
    var_match(step->ctx, ef->args, &step->engine, arg);
    if (step->ctx->failure != 0) {
        return;
    }
 
    ctx_push(step->ctx, oldvars);
    ctx_push(step->ctx, VALUE_TO_INT(step->ctx->fp));

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
    hvalue_t ctx = ctx_pop(step->ctx);
    if (VALUE_TYPE(ctx) != VALUE_CONTEXT) {
        value_ctx_failure(step->ctx, &step->engine, "Go: not a context");
        return;
    }

    // Remove from stopbag if it's there
    hvalue_t count;
    if (value_tryload(&step->engine, state->stopbag, ctx, &count)) {
        assert(VALUE_TYPE(count) == VALUE_INT);
        assert(count != VALUE_INT);
        count -= 1 << VALUE_BITS;
        if (count != VALUE_INT) {
            state->stopbag = value_dict_store(&step->engine, state->stopbag, ctx, count);
        }
        else {
            state->stopbag = value_dict_remove(&step->engine, state->stopbag, ctx);
        }
    }

    hvalue_t result = ctx_pop(step->ctx);
    unsigned int size;
    struct context *copy = value_copy(ctx, &size);
    copy = realloc(copy, size + sizeof(hvalue_t));
    ctx_push(copy, result);
    copy->stopped = false;
    hvalue_t v = value_put_context(&step->engine, copy);
    free(copy);
    state->ctxbag = value_bag_add(&step->engine, state->ctxbag, v, 1);
    step->ctx->pc++;
}

void op_Invariant(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Invariant *ei = env;

    assert(VALUE_TYPE(state->invariants) == VALUE_SET);
    unsigned int size;
    hvalue_t *vals;
    if (state->invariants == VALUE_SET) {
        size = 0;
        vals = NULL;
    }
    else {
        vals = value_get(state->invariants, &size);
    }
    vals = realloc(vals, size + sizeof(hvalue_t));
    * (hvalue_t *) ((char *) vals + size) = VALUE_TO_PC(step->ctx->pc);
    state->invariants = value_put_set(&step->engine, vals, size + sizeof(hvalue_t));
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

    hvalue_t v = ctx_pop(step->ctx);
    if ((ej->cond == VALUE_FALSE || ej->cond == VALUE_TRUE) &&
                            !(v == VALUE_FALSE || v == VALUE_TRUE)) {
        value_ctx_failure(step->ctx, &step->engine, "JumpCond: not an boolean");
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

    assert(VALUE_TYPE(state->vars) == VALUE_DICT);

    hvalue_t v;
    if (el == 0) {
        hvalue_t av = ctx_pop(step->ctx);
        if (VALUE_TYPE(av) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &step->engine, "Load %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS) {
            value_ctx_failure(step->ctx, &step->engine, "Load: can't load from None");
            return;
        }

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        if (step->ai != NULL) {
            step->ai->indices = indices;
            step->ai->n = size;
            step->ai->load = true;
        }

        if (!ind_tryload(&step->engine, state->vars, indices, size, &v)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &step->engine, "Load: unknown address %s", x);
            free(x);
            return;
        }
        ctx_push(step->ctx, v);
    }
    else {
        if (step->ai != NULL) {
            step->ai->indices = el->indices;
            step->ai->n = el->n;
            step->ai->load = true;
        }
        if (!ind_tryload(&step->engine, state->vars, el->indices, el->n, &v)) {
            char *x = indices_string(el->indices, el->n);
            value_ctx_failure(step->ctx, &step->engine, "Load: unknown variable %s", x);
            free(x);
            return;
        }
        ctx_push(step->ctx, v);
    }
    step->ctx->pc++;
}

void op_LoadVar(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_LoadVar *el = env;
    assert(VALUE_TYPE(step->ctx->vars) == VALUE_DICT);

    hvalue_t v;
    if (el == NULL) {
        hvalue_t av = ctx_pop(step->ctx);
        assert(VALUE_TYPE(av) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);

        bool result;
        if (indices[0] == this_atom) {
            if (VALUE_TYPE(step->ctx->this) != VALUE_DICT) {
                value_ctx_failure(step->ctx, &step->engine, "LoadVar: 'this' is not a dictionary");
                return;
            }
            result = ind_tryload(&step->engine, step->ctx->this, &indices[1], size - 1, &v);
        }
        else {
            result = ind_tryload(&step->engine, step->ctx->vars, indices, size, &v);
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &step->engine, "LoadVar: bad address: %s", x);
            free(x);
            return;
        }
        ctx_push(step->ctx, v);
    }
    else {
        if (el->name == this_atom) {
            ctx_push(step->ctx, step->ctx->this);
        }
        else if (value_tryload(&step->engine, step->ctx->vars, el->name, &v)) {
            ctx_push(step->ctx, v);
        }
        else {
            char *p = value_string(el->name);
            value_ctx_failure(step->ctx, &step->engine, "LoadVar: unknown variable %s", p);
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

    for (unsigned int i = 0; i < en->arity; i++) {
        args[i] = ctx_pop(step->ctx);
    }
    hvalue_t result = (*en->fi->f)(state, step->ctx, args, en->arity, &step->engine);
    if (step->ctx->failure == 0) {
        ctx_push(step->ctx, result);
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

    ctx_push(step->ctx, ep->value);
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
    hvalue_t result = value_dict_load(step->ctx->vars, value_put_atom(&step->engine, "result", 6));
    hvalue_t fp = ctx_pop(step->ctx);
    if (VALUE_TYPE(fp) != VALUE_INT) {
        printf("XXX %d %d %s\n", step->ctx->pc, step->ctx->sp, value_string(fp));
        value_ctx_failure(step->ctx, &step->engine, "XXX");
        return;
        // exit(1);
    }
    assert(VALUE_TYPE(fp) == VALUE_INT);
    step->ctx->fp = VALUE_FROM_INT(fp);
    hvalue_t oldvars = ctx_pop(step->ctx);
    assert(VALUE_TYPE(oldvars) == VALUE_DICT);
    step->ctx->vars = oldvars;
    (void) ctx_pop(step->ctx);   // argument saved for stack trace
    if (step->ctx->sp == 0) {     // __init__
        step->ctx->terminated = true;
        return;
    }
    hvalue_t calltype = ctx_pop(step->ctx);
    assert(VALUE_TYPE(calltype) == VALUE_INT);
    switch (VALUE_FROM_INT(calltype)) {
    case CALLTYPE_PROCESS:
        step->ctx->terminated = true;
        break;
    case CALLTYPE_NORMAL:
        {
            hvalue_t pc = ctx_pop(step->ctx);
            assert(VALUE_TYPE(pc) == VALUE_PC);
            pc = VALUE_FROM_PC(pc);
            assert(pc != (hvalue_t) step->ctx->pc);
            ctx_push(step->ctx, result);
            step->ctx->pc = pc;
        }
        break;
    case CALLTYPE_INTERRUPT:
        step->ctx->interruptlevel = false;
        hvalue_t pc = ctx_pop(step->ctx);
        assert(VALUE_TYPE(pc) == VALUE_PC);
        pc = VALUE_FROM_PC(pc);
        assert(pc != (hvalue_t) step->ctx->pc);
        step->ctx->pc = pc;
        break;
    default:
        panic("op_Return: bad call type");
    }
}

void op_Sequential(const void *env, struct state *state, struct step *step, struct global_t *global){
    hvalue_t addr = ctx_pop(step->ctx);
    if (VALUE_TYPE(addr) != VALUE_ADDRESS) {
        char *p = value_string(addr);
        value_ctx_failure(step->ctx, &step->engine, "Sequential %s: not an address", p);
        free(p);
        return;
    }

    /* Insert in state's set of sequential variables.
     */
    unsigned int size;
    hvalue_t *seqs = value_copy(state->seqs, &size);
    size /= sizeof(hvalue_t);
    unsigned int i;
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
    state->seqs = value_put_set(&step->engine, seqs, (size + 1) * sizeof(hvalue_t));
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
	hvalue_t newlevel =  ctx_pop(step->ctx);
    if (VALUE_TYPE(newlevel) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, &step->engine, "setintlevel can only be set to a boolean");
        return;
    }
    step->ctx->interruptlevel = VALUE_FROM_BOOL(newlevel);
	ctx_push(step->ctx, VALUE_TO_BOOL(oldlevel));
    step->ctx->pc++;
}

void op_Spawn(
    const void *env,
    struct state *state,
    struct step *step,
    struct global_t *global
) {
    const struct env_Spawn *se = env;

    hvalue_t thisval = ctx_pop(step->ctx);
    hvalue_t arg = ctx_pop(step->ctx);

    hvalue_t pc = ctx_pop(step->ctx);
    if (VALUE_TYPE(pc) != VALUE_PC) {
        value_ctx_failure(step->ctx, &step->engine, "spawn: not a method");
        return;
    }
    pc = VALUE_FROM_PC(pc);

    assert(pc < (hvalue_t) global->code.len);
    assert(strcmp(global->code.instrs[pc].oi->name, "Frame") == 0);

    struct context *ctx = calloc(1, sizeof(struct context) +
                        2 * sizeof(hvalue_t));

    const struct env_Frame *ef = global->code.instrs[pc].env;
    ctx->name = ef->name;
    ctx->arg = arg;
    ctx->this = thisval;
    ctx->entry = VALUE_TO_PC(pc);
    ctx->pc = pc;
    ctx->vars = VALUE_DICT;
    ctx->interruptlevel = false;
    ctx->eternal = se->eternal;
    ctx_push(ctx, VALUE_TO_INT(CALLTYPE_PROCESS));
    ctx_push(ctx, arg);
    if (global->run_direct) {
        spawn_thread(global, state, ctx);
    }
    else {
        hvalue_t v = value_put_context(&step->engine, ctx);
        free(ctx);
        state->ctxbag = value_bag_add(&step->engine, state->ctxbag, v, 1);
    }
    step->ctx->pc++;
}

void op_Split(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Split *es = env;

    hvalue_t v = ctx_pop(step->ctx);
    hvalue_t type = VALUE_TYPE(v);
    if (type != VALUE_SET && type != VALUE_LIST) {
        value_ctx_failure(step->ctx, &step->engine, "Can only split tuples or sets");
        return;
    }
    if (v == VALUE_SET || v == VALUE_LIST) {
        if (es->count != 0) {
            value_ctx_failure(step->ctx, &step->engine, "Split: empty set or tuple");
        }
        else {
            step->ctx->pc++;
        }
        return;
    }

    unsigned int size;
    hvalue_t *vals = value_get(v, &size);
    size /= sizeof(hvalue_t);
    if (size != es->count) {
        value_ctx_failure(step->ctx, &step->engine, "Split: wrong size");
        return;
    }
    for (unsigned int i = 0; i < size; i++) {
        ctx_push(step->ctx, vals[i]);
    }
    step->ctx->pc++;
}

void op_Save(const void *env, struct state *state, struct step *step, struct global_t *global){
    assert(VALUE_TYPE(state->vars) == VALUE_DICT);
    hvalue_t e = ctx_pop(step->ctx);

    // Save the context
    step->ctx->stopped = true;
    step->ctx->pc++;
    hvalue_t v = value_put_context(&step->engine, step->ctx);

    // Restore the stopped mode to false
    step->ctx->stopped = false;

    // Push a tuple returning e and the context
    hvalue_t d[2];
    d[0] = e;
    d[1] = v;
    hvalue_t result = value_put_list(&step->engine, d, sizeof(d));
    ctx_push(step->ctx, result);
}

void op_Stop(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Stop *es = env;

    assert(VALUE_TYPE(state->vars) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, &step->engine, "Stop: in read-only mode");
        return;
    }

    if (es == 0) {
        hvalue_t av = ctx_pop(step->ctx);
        if (av == VALUE_ADDRESS || av == VALUE_LIST) {
            step->ctx->pc++;
            step->ctx->terminated = true;
            return;
        }

        if (VALUE_TYPE(av) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &step->engine, "Stop %s: not an address", p);
            free(p);
            return;
        }
        step->ctx->pc++;

        step->ctx->stopped = true;
        hvalue_t v = value_put_context(&step->engine, step->ctx);
        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        if (!ind_trystore(state->vars, indices, size, v, &step->engine, &state->vars)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &step->engine, "Stop: bad address: %s", x);
            free(x);
        }
    }
    else {
        step->ctx->stopped = true;
        step->ctx->pc++;
        hvalue_t v = value_put_context(&step->engine, step->ctx);
        if (!ind_trystore(state->vars, es->indices, es->n, v, &step->engine, &state->vars)) {
            value_ctx_failure(step->ctx, &step->engine, "Store: bad variable");
        }
    }
}

void op_Store(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_Store *es = env;

    assert(VALUE_TYPE(state->vars) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, &step->engine, "Can't update state in assert or invariant (including acquiring locks)");
        return;
    }

    hvalue_t v = ctx_pop(step->ctx);

    if (es == 0) {
        hvalue_t av = ctx_pop(step->ctx);
        if (VALUE_TYPE(av) != VALUE_ADDRESS) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, &step->engine, "Store %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS) {
            value_ctx_failure(step->ctx, &step->engine, "Store: address is None");
            return;
        }

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        if (step->ai != NULL) {
            step->ai->indices = indices;
            step->ai->n = size;
            step->ai->load = is_sequential(state->seqs, step->ai->indices, step->ai->n);
        }

        if (size == 1 && step->ctx->name != global->init_name) {
            hvalue_t newvars;
            if (!value_dict_trystore(&step->engine, state->vars, indices[0], v, step->ctx->name == global->init_name, &newvars)){
                char *x = indices_string(indices, size);
                value_ctx_failure(step->ctx, &step->engine, "Store: declare a local variable %s (or set during initialization)", x);
                free(x);
                return;
            }
            state->vars = newvars;
        }
        else if (!ind_trystore(state->vars, indices, size, v, &step->engine, &state->vars)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &step->engine, "Store: bad address: %s", x);
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
        if (es->n == 1 && step->ctx->name != global->init_name) {
            hvalue_t newvars;
            if (!value_dict_trystore(&step->engine, state->vars, es->indices[0], v, step->ctx->name == global->init_name, &newvars)){
                char *x = indices_string(es->indices, es->n);
                value_ctx_failure(step->ctx, &step->engine, "Store: declare a local variable %s (or set during initialization)", x);
                free(x);
                return;
            }
            state->vars = newvars;
        }
        else if (!ind_trystore(state->vars, es->indices, es->n, v, &step->engine, &state->vars)) {
            char *x = indices_string(es->indices, es->n);
            value_ctx_failure(step->ctx, &step->engine, "Store: bad variable %s", x);
            free(x);
            return;
        }
    }
    step->ctx->pc++;
}

void op_StoreVar(const void *env, struct state *state, struct step *step, struct global_t *global){
    const struct env_StoreVar *es = env;
    hvalue_t v = ctx_pop(step->ctx);

    assert(VALUE_TYPE(step->ctx->vars) == VALUE_DICT);
    if (es == NULL) {
        hvalue_t av = ctx_pop(step->ctx);
        assert(VALUE_TYPE(av) == VALUE_ADDRESS);
        assert(av != VALUE_ADDRESS);

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);

        bool result;
        if (indices[0] == this_atom) {
            if (VALUE_TYPE(step->ctx->this) != VALUE_DICT) {
                value_ctx_failure(step->ctx, &step->engine, "StoreVar: 'this' is not a dictionary");
                return;
            }
            result = ind_trystore(step->ctx->this, &indices[1], size - 1, v, &step->engine, &step->ctx->this);
        }

        else {
            result = ind_trystore(step->ctx->vars, indices, size, v, &step->engine, &step->ctx->vars);
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, &step->engine, "StoreVar: bad address: %s", x);
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
            var_match(step->ctx, es->args, &step->engine, v);
            if (step->ctx->failure == 0) {
                step->ctx->pc++;
            }
        }
    }
}

void op_Trap(const void *env, struct state *state, struct step *step, struct global_t *global){
    step->ctx->trap_pc = ctx_pop(step->ctx);
    if (VALUE_TYPE(step->ctx->trap_pc) != VALUE_PC) {
        value_ctx_failure(step->ctx, &step->engine, "trap: not a method");
        return;
    }
    assert(VALUE_FROM_PC(step->ctx->trap_pc) < (hvalue_t) global->code.len);
    assert(strcmp(global->code.instrs[VALUE_FROM_PC(step->ctx->trap_pc)].oi->name, "Frame") == 0);
    step->ctx->trap_arg = ctx_pop(step->ctx);
    step->ctx->pc++;
}

void *init_Address(struct dict *map, struct engine *engine){ return NULL; }
void *init_Apply(struct dict *map, struct engine *engine){ return NULL; }
void *init_Assert(struct dict *map, struct engine *engine){ return NULL; }
void *init_Assert2(struct dict *map, struct engine *engine){ return NULL; }
void *init_AtomicDec(struct dict *map, struct engine *engine){ return NULL; }
void *init_Choose(struct dict *map, struct engine *engine){ return NULL; }
void *init_Continue(struct dict *map, struct engine *engine){ return NULL; }
void *init_Dup(struct dict *map, struct engine *engine){ return NULL; }
void *init_Go(struct dict *map, struct engine *engine){ return NULL; }
void *init_Print(struct dict *map, struct engine *engine){ return NULL; }
void *init_Pop(struct dict *map, struct engine *engine){ return NULL; }
void *init_ReadonlyDec(struct dict *map, struct engine *engine){ return NULL; }
void *init_ReadonlyInc(struct dict *map, struct engine *engine){ return NULL; }
void *init_Return(struct dict *map, struct engine *engine){ return NULL; }
void *init_Save(struct dict *map, struct engine *engine){ return NULL; }
void *init_Sequential(struct dict *map, struct engine *engine){ return NULL; }
void *init_SetIntLevel(struct dict *map, struct engine *engine){ return NULL; }
void *init_Trap(struct dict *map, struct engine *engine){ return NULL; }

void *init_Cut(struct dict *map, struct engine *engine){
    struct env_Cut *env = new_alloc(struct env_Cut);
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    int index = 0;
    env->value = var_parse(engine, value->u.atom.base, value->u.atom.len, &index);

    struct json_value *key = dict_lookup(map, "key", 3);
    if (key != NULL) {
        assert(key->type == JV_ATOM);
        index = 0;
        env->key = var_parse(engine, key->u.atom.base, key->u.atom.len, &index);
    }

    return env;
}

void *init_AtomicInc(struct dict *map, struct engine *engine){
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

void *init_Del(struct dict *map, struct engine *engine){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Del *env = new_alloc(struct env_Del);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (unsigned int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(engine, index->u.map);
    }
    return env;
}

void *init_DelVar(struct dict *map, struct engine *engine){
    struct json_value *name = dict_lookup(map, "value", 5);
	if (name == NULL) {
		return NULL;
	}
	else {
		struct env_DelVar *env = new_alloc(struct env_DelVar);
		assert(name->type == JV_ATOM);
		env->name = value_put_atom(engine, name->u.atom.base, name->u.atom.len);
		return env;
	}
}

void *init_Frame(struct dict *map, struct engine *engine){
    struct env_Frame *env = new_alloc(struct env_Frame);

    struct json_value *name = dict_lookup(map, "name", 4);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(engine, name->u.atom.base, name->u.atom.len);

    struct json_value *args = dict_lookup(map, "args", 4);
    assert(args->type == JV_ATOM);
    int index = 0;
    env->args = var_parse(engine, args->u.atom.base, args->u.atom.len, &index);

    return env;
}

void *init_Load(struct dict *map, struct engine *engine){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Load *env = new_alloc(struct env_Load);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (unsigned int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(engine, index->u.map);
    }
    return env;
}

void *init_LoadVar(struct dict *map, struct engine *engine){
    struct json_value *value = dict_lookup(map, "value", 5);
    if (value == NULL) {
        return NULL;
    }
    else {
        struct env_LoadVar *env = new_alloc(struct env_LoadVar);
        assert(value->type == JV_ATOM);
        env->name = value_put_atom(engine, value->u.atom.base, value->u.atom.len);
        return env;
    }
}

void *init_Move(struct dict *map, struct engine *engine){
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

void *init_Nary(struct dict *map, struct engine *engine){
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

void *init_Invariant(struct dict *map, struct engine *engine){
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

void *init_Jump(struct dict *map, struct engine *engine){
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

void *init_JumpCond(struct dict *map, struct engine *engine){
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
    env->cond = value_from_json(engine, cond->u.map);

    return env;
}

void *init_Push(struct dict *map, struct engine *engine) {
    struct json_value *jv = dict_lookup(map, "value", 5);
    assert(jv->type == JV_MAP);
    struct env_Push *env = new_alloc(struct env_Push);
    env->value = value_from_json(engine, jv->u.map);
    return env;
}

void *init_Spawn(struct dict *map, struct engine *engine){
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

void *init_Split(struct dict *map, struct engine *engine){
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

void *init_Stop(struct dict *map, struct engine *engine){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Stop *env = new_alloc(struct env_Stop);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (unsigned int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(engine, index->u.map);
    }
    return env;
}

void *init_Store(struct dict *map, struct engine *engine){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Store *env = new_alloc(struct env_Store);
    env->n = jv->u.list.nvals;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    for (unsigned int i = 0; i < env->n; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i] = value_from_json(engine, index->u.map);
    }
    return env;
}

void *init_StoreVar(struct dict *map, struct engine *engine){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    else {
        assert(jv->type == JV_ATOM);
        struct env_StoreVar *env = new_alloc(struct env_StoreVar);
        int index = 0;
        env->args = var_parse(engine, jv->u.atom.base, jv->u.atom.len, &index);
        return env;
    }
}

hvalue_t f_abs(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "abs() can only be applied to integers");
    }
    e = VALUE_FROM_INT(e);
    return e >= 0 ? args[0] : VALUE_TO_INT(-e);
}

hvalue_t f_all(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_LIST) {
		return VALUE_TRUE;
    }
    if (VALUE_TYPE(e) == VALUE_SET || VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        for (unsigned int i = 0; i < size; i++) {
            if (VALUE_TYPE(v[i]) != VALUE_BOOL) {
                return value_ctx_failure(ctx, engine, "all() can only be applied to booleans");
            }
            if (v[i] == VALUE_FALSE) {
                return VALUE_FALSE;
            }
        }
		return VALUE_TRUE;
    }
    return value_ctx_failure(ctx, engine, "all() can only be applied to sets or lists");
}

hvalue_t f_any(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_LIST) {
		return VALUE_FALSE;
    }
    if (VALUE_TYPE(e) == VALUE_SET || VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        for (unsigned int i = 0; i < size; i++) {
            if (VALUE_TYPE(v[i]) != VALUE_BOOL) {
                return value_ctx_failure(ctx, engine, "any() can only be applied to booleans");
            }
            if (v[i] != VALUE_FALSE) {
                return VALUE_TRUE;
            }
        }
		return VALUE_FALSE;
    }
    return value_ctx_failure(ctx, engine, "any() can only be applied to sets or dictionaries");
}

hvalue_t nametag(struct context *ctx, struct engine *engine){
    hvalue_t nt = value_dict_store(engine, VALUE_DICT,
            VALUE_TO_INT(0), ctx->entry);
    return value_dict_store(engine, nt, VALUE_TO_INT(1), ctx->arg);
}

hvalue_t f_atLabel(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    if (ctx->atomic == 0) {
        return value_ctx_failure(ctx, engine, "atLabel: can only be called in atomic mode");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_PC) {
        return value_ctx_failure(ctx, engine, "atLabel: not a label");
    }
    e = VALUE_FROM_PC(e);

    unsigned int size;
    hvalue_t *vals = value_get(state->ctxbag, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    assert(size % 2 == 0);
    hvalue_t bag = VALUE_DICT;
    for (unsigned int i = 0; i < size; i += 2) {
        assert(VALUE_TYPE(vals[i]) == VALUE_CONTEXT);
        assert(VALUE_TYPE(vals[i+1]) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        if ((hvalue_t) ctx->pc == e) {
            bag = value_bag_add(engine, bag, nametag(ctx, engine),
                (int) VALUE_FROM_INT(vals[i+1]));
        }
    }
    return bag;
}

hvalue_t f_countLabel(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    if (ctx->atomic == 0) {
        return value_ctx_failure(ctx, engine, "countLabel: can only be called in atomic mode");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_PC) {
        return value_ctx_failure(ctx, engine, "countLabel: not a label");
    }
    e = VALUE_FROM_PC(e);

    unsigned int size;
    hvalue_t *vals = value_get(state->ctxbag, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    assert(size % 2 == 0);
    hvalue_t result = 0;
    for (unsigned int i = 0; i < size; i += 2) {
        assert(VALUE_TYPE(vals[i]) == VALUE_CONTEXT);
        assert(VALUE_TYPE(vals[i+1]) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        if ((hvalue_t) ctx->pc == e) {
            result += VALUE_FROM_INT(vals[i+1]);
        }
    }
    return VALUE_TO_INT(result);
}

hvalue_t f_div(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    int64_t e1 = args[0], e2 = args[1];
    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "right argument to / not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "left argument to / not an integer");
    }
    e1 = VALUE_FROM_INT(e1);
    if (e1 == 0) {
        return value_ctx_failure(ctx, engine, "divide by zero");
    }
    int64_t result = VALUE_FROM_INT(e2) / e1;
    return VALUE_TO_INT(result);
}

hvalue_t f_eq(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    return VALUE_TO_BOOL(args[0] == args[1]);
}

hvalue_t f_ge(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return VALUE_TO_BOOL(cmp >= 0);
}

hvalue_t f_gt(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return VALUE_TO_BOOL(cmp > 0);
}

hvalue_t f_ne(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    return VALUE_TO_BOOL(args[0] != args[1]);
}

hvalue_t f_in(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    hvalue_t s = args[0], e = args[1];
	if (s == VALUE_SET || s == VALUE_DICT || s == VALUE_LIST) {
		return VALUE_FALSE;
	}
    if (VALUE_TYPE(s) == VALUE_ATOM) {
        if (VALUE_TYPE(e) != VALUE_ATOM) {
            return value_ctx_failure(ctx, engine, "'in <string>' can only be applied to another string");
        }
        if (s == VALUE_ATOM) {
            return VALUE_TO_BOOL(e == VALUE_ATOM);
        }
        unsigned int size1, size2;
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
    if (VALUE_TYPE(s) == VALUE_SET || VALUE_TYPE(s) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *v = value_get(s, &size);
        size /= sizeof(hvalue_t);
        for (unsigned int i = 0; i < size; i++) {
            if (v[i] == e) {
                return VALUE_TRUE;
            }
        }
        return VALUE_FALSE;
    }
    if (VALUE_TYPE(s) == VALUE_DICT) {
        unsigned int size;
        hvalue_t *v = value_get(s, &size);
        size /= 2 * sizeof(hvalue_t);
        for (unsigned int i = 0; i < size; i++) {
            if (v[2*i] == e) {
                return VALUE_TRUE;
            }
        }
        return VALUE_FALSE;
    }
    return value_ctx_failure(ctx, engine, "'in' can only be applied to sets or dictionaries");
}

hvalue_t f_intersection(
    struct state *state,
    struct context *ctx,
    hvalue_t *args,
    int n,
    struct engine *engine
) {
    hvalue_t e1 = args[0];

    if (VALUE_TYPE(e1) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(ctx, engine, "'&' applied to mix of ints and other types");
            }
            e1 &= e2;
        }
        return e1;
    }
	if (e1 == VALUE_SET) {
		return VALUE_SET;
	}
    if (VALUE_TYPE(e1) == VALUE_SET) {
        // get all the sets
		assert(n > 0);
        struct val_info *vi = malloc(n * sizeof(*vi));
		vi[0].vals = value_get(args[0], &vi[0].size); 
		vi[0].index = 0;
        unsigned int min_size = vi[0].size;     // minimum set size
        hvalue_t max_val = vi[0].vals[0];       // maximum value over the minima of all sets
        for (int i = 1; i < n; i++) {
            if (VALUE_TYPE(args[i]) != VALUE_SET) {
                return value_ctx_failure(ctx, engine, "'&' applied to mix of sets and other types");
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
        for (unsigned int i = 0; i < min_size; i++) {
            hvalue_t old_max = max_val;
            for (int j = 0; j < n; j++) {
                unsigned int k, size = vi[j].size / sizeof(hvalue_t);
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

        hvalue_t result = value_put_set(engine, vals, (char *) v - (char *) vals);
        free(vi);
        free(vals);
        return result;
    }

	if (e1 == VALUE_DICT) {
		return VALUE_DICT;
	}
    if (VALUE_TYPE(e1) != VALUE_DICT) {
        return value_ctx_failure(ctx, engine, "'&' can only be applied to ints and dicts");
    }
    // get all the dictionaries
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if (VALUE_TYPE(args[i]) != VALUE_DICT) {
            return value_ctx_failure(ctx, engine, "'&' applied to mix of dictionaries and other types");
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

    hvalue_t result = value_put_dict(engine, vals, 2 * out * sizeof(hvalue_t));
    free(vi);
    free(vals);
    return result;
}

hvalue_t f_invert(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    int64_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "~ can only be applied to ints");
    }
    e = VALUE_FROM_INT(e);
    return VALUE_TO_INT(~e);
}

// TODO: obsolete
hvalue_t f_isEmpty(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) == VALUE_DICT) {
        return VALUE_TO_BOOL(e == VALUE_DICT);
    }
    if (VALUE_TYPE(e) == VALUE_SET) {
        return VALUE_TO_BOOL(e == VALUE_SET);
    }
    if (VALUE_TYPE(e) == VALUE_ATOM) {
        return VALUE_TO_BOOL(e == VALUE_ATOM);
    }
    if (VALUE_TYPE(e) == VALUE_LIST) {
        return VALUE_TO_BOOL(e == VALUE_LIST);
    }
    return value_ctx_failure(ctx, engine, "loops can only iterate over dictionaries, lists, and sets");
}

hvalue_t f_keys(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t v = args[0];
    if (VALUE_TYPE(v) != VALUE_DICT) {
        return value_ctx_failure(ctx, engine, "keys() can only be applied to dictionaries");
    }
    if (v == VALUE_DICT) {
        return VALUE_SET;
    }

    unsigned int size;
    hvalue_t *vals = value_get(v, &size);
    hvalue_t *keys = malloc(size / 2);
    size /= 2 * sizeof(hvalue_t);
    for (unsigned int i = 0; i < size; i++) {
        keys[i] = vals[2*i];
    }
    hvalue_t result = value_put_set(engine, keys, size * sizeof(hvalue_t));
    free(keys);
    return result;
}

hvalue_t f_str(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
    char *s = value_string(e);
    hvalue_t v = value_put_atom(engine, s, strlen(s));
    free(s);
    return v;
}

hvalue_t f_len(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_DICT || e == VALUE_LIST || e == VALUE_ATOM) {
		return VALUE_INT;
	}
    if (VALUE_TYPE(e) == VALUE_SET) {
        unsigned int size;
        (void) value_get(e, &size);
        size /= sizeof(hvalue_t);
        return VALUE_TO_INT(size);
    }
    if (VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int size;
        (void) value_get(e, &size);
        size /= sizeof(hvalue_t);
        return VALUE_TO_INT(size);
    }
    if (VALUE_TYPE(e) == VALUE_DICT) {
        unsigned int size;
        (void) value_get(e, &size);
        size /= 2 * sizeof(hvalue_t);
        return VALUE_TO_INT(size);
    }
    if (VALUE_TYPE(e) == VALUE_ATOM) {
        unsigned int size;
        (void) value_get(e, &size);
        return VALUE_TO_INT(size);
    }
    return value_ctx_failure(ctx, engine, "len() can only be applied to sets, dictionaries, lists, or strings");
}

hvalue_t f_type(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
    switch (VALUE_TYPE(e)) {
    case VALUE_BOOL:
        return type_bool;
    case VALUE_INT:
        return type_int;
    case VALUE_ATOM:
        return type_str;
    case VALUE_PC:
        return type_pc;
    case VALUE_LIST:
        return type_list;
    case VALUE_DICT:
        return type_dict;
    case VALUE_SET:
        return type_set;
    case VALUE_ADDRESS:
        return type_address;
    case VALUE_CONTEXT:
        return type_context;
    default:
        assert(false);
    }
    return value_ctx_failure(ctx, engine, "unknown type???");
}

hvalue_t f_le(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return VALUE_TO_BOOL(cmp <= 0);
}

hvalue_t f_lt(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int cmp = value_cmp(args[1], args[0]);
    return VALUE_TO_BOOL(cmp < 0);
}

hvalue_t f_max(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET) {
        return value_ctx_failure(ctx, engine, "can't apply max() to empty set");
    }
    if (e == VALUE_LIST) {
        return value_ctx_failure(ctx, engine, "can't apply max() to empty list");
    }
    if (VALUE_TYPE(e) == VALUE_SET) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        return v[size - 1];
    }
    if (VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        hvalue_t max = v[0];
        for (unsigned int i = 1; i < size; i++) {
            if (value_cmp(v[i], max) > 0) {
                max = v[i];
            }
        }
		return max;
    }
    return value_ctx_failure(ctx, engine, "max() can only be applied to sets or lists");
}

hvalue_t f_min(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
	if (e == VALUE_SET) {
        return value_ctx_failure(ctx, engine, "can't apply min() to empty set");
    }
    if (e == VALUE_LIST) {
        return value_ctx_failure(ctx, engine, "can't apply min() to empty list");
    }
    if (VALUE_TYPE(e) == VALUE_SET) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        return v[0];
    }
    if (VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        hvalue_t min = v[0];
        for (unsigned int i = 1; i < size; i++) {
            if (value_cmp(v[i], min) < 0) {
                min = v[i];
            }
        }
		return min;
    }
    return value_ctx_failure(ctx, engine, "min() can only be applied to sets or lists");
}

hvalue_t f_minus(
    struct state *state,
    struct context *ctx,
    hvalue_t *args,
    int n,
    struct engine *engine
) {
    assert(n == 1 || n == 2);
    if (n == 1) {
        int64_t e = args[0];
        if (VALUE_TYPE(e) != VALUE_INT) {
            return value_ctx_failure(ctx, engine, "unary minus can only be applied to ints");
        }
        e = VALUE_FROM_INT(e);
        if (e == VALUE_MAX) {
            return VALUE_TO_INT(VALUE_MIN);
        }
        if (e == VALUE_MIN) {
            return VALUE_TO_INT(VALUE_MAX);
        }
        if (-e <= VALUE_MIN || -e >= VALUE_MAX) {
            return value_ctx_failure(ctx, engine, "unary minus overflow (model too large)");
        }
        return VALUE_TO_INT(-e);
    }
    else {
        if (VALUE_TYPE(args[0]) == VALUE_INT) {
            int64_t e1 = args[0], e2 = args[1];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(ctx, engine, "minus applied to int and non-int");
            }
            e1 = VALUE_FROM_INT(e1);
            e2 = VALUE_FROM_INT(e2);
            int64_t result = e2 - e1;
            if (result <= VALUE_MIN || result >= VALUE_MAX) {
                return value_ctx_failure(ctx, engine, "minus overflow (model too large)");
            }
            return VALUE_TO_INT(result);
        }

        hvalue_t e1 = args[0], e2 = args[1];
        if (VALUE_TYPE(e1) != VALUE_SET || VALUE_TYPE(e2) != VALUE_SET) {
            return value_ctx_failure(ctx, engine, "minus can only be applied to ints or sets");
        }
        unsigned int size1, size2;
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
        hvalue_t result = value_put_set(engine, vals, (char *) q - (char *) vals);
        free(vals);
        return result;
    }
}

hvalue_t f_mod(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    int64_t e1 = args[0], e2 = args[1];
    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "right argument to mod not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "left argument to mod not an integer");
    }
    int64_t mod = VALUE_FROM_INT(e1);
    int64_t result = VALUE_FROM_INT(e2) % mod;
    if (result < 0) {
        result += mod;
    }
    return VALUE_TO_INT(result);
}

hvalue_t f_not(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 1);
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_BOOL) {
        return value_ctx_failure(ctx, engine, "not can only be applied to booleans");
    }
    return e ^ (1 << VALUE_BITS);
}

hvalue_t f_plus(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    int64_t e1 = args[0];
    if (VALUE_TYPE(e1) == VALUE_INT) {
        e1 = VALUE_FROM_INT(e1);
        for (int i = 1; i < n; i++) {
            int64_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(ctx, engine,
                    "+: applied to mix of integers and other engine");
            }
            e2 = VALUE_FROM_INT(e2);
            int64_t sum = e1 + e2;
            if (sum <= VALUE_MIN || sum >= VALUE_MAX) {
                return value_ctx_failure(ctx, engine,
                    "+: integer overflow (model too large)");
            }
            e1 = sum;
        }
        return VALUE_TO_INT(e1);
    }

    if (VALUE_TYPE(e1) == VALUE_ATOM) {
        struct strbuf sb;
        strbuf_init(&sb);
        for (int i = n; --i >= 0;) {
            if (VALUE_TYPE(args[i]) != VALUE_ATOM) {
                return value_ctx_failure(ctx, engine,
                    "+: applied to mix of strings and other engine");
            }
            unsigned int size;
            char *chars = value_get(args[i], &size);
            strbuf_append(&sb, chars, size);
        }
        char *result = strbuf_convert(&sb);
        hvalue_t v = value_put_atom(engine, result, strbuf_getlen(&sb));
        return v;
    }

    if (VALUE_TYPE(e1) == VALUE_LIST) {
        // get all the lists
        struct val_info *vi = malloc(n * sizeof(*vi));
        int total = 0;
        for (int i = 0; i < n; i++) {
            if (VALUE_TYPE(args[i]) != VALUE_LIST) {
                value_ctx_failure(ctx, engine, "+: applied to mix of value types");
                free(vi);
                return 0;
            }
            if (args[i] == VALUE_LIST) {
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
            return VALUE_LIST;
        }

        // Concatenate the lists
        hvalue_t *vals = malloc(total);
        total = 0;
        for (int i = n; --i >= 0;) {
            memcpy((char *) vals + total, vi[i].vals, vi[i].size);
            total += vi[i].size;
        }

        hvalue_t result = value_put_list(engine, vals, total);

        free(vi);
        free(vals);
        return result;
    }

    value_ctx_failure(ctx, engine, "+: can only apply to ints, strings, or lists");
    return 0;
}

hvalue_t f_power(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "right argument to ** not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "left argument to ** not an integer");
    }
    int64_t base = VALUE_FROM_INT(e2);
    int64_t exp = VALUE_FROM_INT(e1);
    if (exp == 0) {
        return VALUE_TO_INT(1);
    }
    if (exp < 0) {
        return value_ctx_failure(ctx, engine, "**: negative exponent");
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
        return value_ctx_failure(ctx, engine, "**: overflow (model too large)");
    }

    return VALUE_TO_INT(result);
}

hvalue_t f_range(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "right argument to .. not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "left argument to .. not an integer");
    }
    int64_t start = VALUE_FROM_INT(e2);
    int64_t finish = VALUE_FROM_INT(e1);
	if (finish < start) {
		return VALUE_SET;
	}
    int cnt = (finish - start) + 1;
	assert(cnt > 0);
	assert(cnt < 1000);		// seems unlikely...
    hvalue_t *v = malloc(cnt * sizeof(hvalue_t));
    for (int i = 0; i < cnt; i++) {
        v[i] = VALUE_TO_INT(start + i);
    }
    hvalue_t result = value_put_set(engine, v, cnt * sizeof(hvalue_t));
    free(v);
    return result;
}

hvalue_t f_list_add(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    hvalue_t list = args[1];
    assert(VALUE_TYPE(list) == VALUE_LIST);
    unsigned int size;
    hvalue_t *vals = value_get(list, &size);
    hvalue_t *nvals = malloc(size + sizeof(hvalue_t));
    memcpy(nvals, vals, size);
    memcpy((char *) nvals + size, &args[0], sizeof(hvalue_t));
    hvalue_t result = value_put_list(engine, nvals, size + sizeof(hvalue_t));
    free(nvals);
    return result;
}

hvalue_t f_dict_add(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 3);
    int64_t value = args[0], key = args[1], dict = args[2];
    assert(VALUE_TYPE(dict) == VALUE_DICT);
    unsigned int size;
    hvalue_t *vals = value_get(dict, &size), *v;

    unsigned int i = 0;
    int cmp = 1;
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

        hvalue_t result = value_put_dict(engine, nvals, size);
        free(nvals);
        return result;
    }
    else {
        hvalue_t *nvals = malloc(size + 2*sizeof(hvalue_t));
        memcpy(nvals, vals, i);
        * (hvalue_t *) ((char *) nvals + i) = key;
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) = value;
        memcpy((char *) nvals + i + 2*sizeof(hvalue_t), v, size - i);

        hvalue_t result = value_put_dict(engine, nvals, size + 2*sizeof(hvalue_t));
        free(nvals);
        return result;
    }
}

hvalue_t f_set_add(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int64_t elt = args[0], set = args[1];
    assert(VALUE_TYPE(set) == VALUE_SET);
    unsigned int size;
    hvalue_t *vals = value_get(set, &size), *v;

    unsigned int i = 0;
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

    hvalue_t result = value_put_set(engine, nvals, size + sizeof(hvalue_t));
    free(nvals);
    return result;
}

// TODO: is this used??
hvalue_t f_value_bag_add(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int64_t elt = args[0], dict = args[1];
    assert(VALUE_TYPE(dict) == VALUE_DICT);
    unsigned int size;
    hvalue_t *vals = value_get(dict, &size), *v;

    unsigned int i = 0;
    int cmp = 1;
    for (v = vals; i < size; i += 2 * sizeof(hvalue_t), v++) {
        cmp = value_cmp(elt, *v);
        if (cmp <= 0) {
            break;
        }
    }

    if (cmp == 0) {
        assert(VALUE_TYPE(v[1]) == VALUE_INT);
        int cnt = VALUE_FROM_INT(v[1]) + 1;
        hvalue_t *nvals = malloc(size);
        memcpy(nvals, vals, size);
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) =
                                        VALUE_TO_INT(cnt);

        hvalue_t result = value_put_dict(engine, nvals, size);
        free(nvals);
        return result;
    }
    else {
        hvalue_t *nvals = malloc(size + 2*sizeof(hvalue_t));
        memcpy(nvals, vals, i);
        * (hvalue_t *) ((char *) nvals + i) = elt;
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) =
                                        VALUE_TO_INT(1);
        memcpy((char *) nvals + i + 2*sizeof(hvalue_t), v, size - i);

        hvalue_t result = value_put_dict(engine, nvals, size + 2*sizeof(hvalue_t));
        free(nvals);
        return result;
    }
}

hvalue_t f_shiftleft(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "right argument to << not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "left argument to << not an integer");
    }
    e1 = VALUE_FROM_INT(e1);
    if (e1 < 0) {
        return value_ctx_failure(ctx, engine, "<<: negative shift count");
    }
    e2 = VALUE_FROM_INT(e2);
    int64_t result = e2 << e1;
    if (((result << VALUE_BITS) >> VALUE_BITS) != result) {
        return value_ctx_failure(ctx, engine, "<<: overflow (model too large)");
    }
    if (result <= VALUE_MIN || result >= VALUE_MAX) {
        return value_ctx_failure(ctx, engine, "<<: overflow (model too large)");
    }
    return VALUE_TO_INT(result);
}

hvalue_t f_shiftright(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];

    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "right argument to >> not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(ctx, engine, "left argument to >> not an integer");
    }
    if (e1 < 0) {
        return value_ctx_failure(ctx, engine, ">>: negative shift count");
    }
    e1 = VALUE_FROM_INT(e1);
    e2 = VALUE_FROM_INT(e2);
    return VALUE_TO_INT(e2 >> e1);
}

hvalue_t f_times(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    int64_t result = 1;
    int list = -1;
    for (int i = 0; i < n; i++) {
        int64_t e = args[i];
        if (VALUE_TYPE(e) == VALUE_ATOM || VALUE_TYPE(e) == VALUE_LIST) {
            if (list >= 0) {
                return value_ctx_failure(ctx, engine, "* can only have at most one list or string");
            }
            list = i;
        }
        else {
            if (VALUE_TYPE(e) != VALUE_INT) {
                return value_ctx_failure(ctx, engine,
                    "* can only be applied to integers and at most one list or string");
            }
            e = VALUE_FROM_INT(e);
            if (e == 0) {
                result = 0;
            }
            else {
                int64_t product = result * e;
                if (product / result != e) {
                    return value_ctx_failure(ctx, engine, "*: overflow (model too large)");
                }
                result = product;
            }
        }
    }
    if (result != (result << VALUE_BITS) >> VALUE_BITS) {
        return value_ctx_failure(ctx, engine, "*: overflow (model too large)");
    }
    if (list < 0) {
        return VALUE_TO_INT(result);
    }
    if (result == 0) {
        // empty list or empty string
        return VALUE_TYPE(args[list]);
    }
    if (VALUE_TYPE(args[list]) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *vals = value_get(args[list], &size);
        if (size == 0) {
            return VALUE_DICT;
        }
        unsigned int n = size / sizeof(hvalue_t);
        hvalue_t *r = malloc(result * size);
        for (unsigned int i = 0; i < result; i++) {
            memcpy(&r[i * n], vals, size);
        }
        hvalue_t v = value_put_list(engine, r, result * size);
        free(r);
        return v;
    }
    assert(VALUE_TYPE(args[list]) == VALUE_ATOM);
	unsigned int size;
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
	hvalue_t v = value_put_atom(engine, s, result * size);
	free(s);
	return v;
}

hvalue_t f_union(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    hvalue_t e1 = args[0];

    if (VALUE_TYPE(e1) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(ctx, engine, "'|' applied to mix of ints and other types");
            }
            e1 |= e2;
        }
        return e1;
    }

    if (VALUE_TYPE(e1) == VALUE_SET) {
        // get all the sets
        struct val_info *vi = malloc(n * sizeof(*vi));
        int total = 0;
        for (int i = 0; i < n; i++) {
            if (VALUE_TYPE(args[i]) != VALUE_SET) {
                return value_ctx_failure(ctx, engine, "'|' applied to mix of sets and other types");
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
        hvalue_t result = value_put_set(engine, vals, n * sizeof(hvalue_t));
        free(vi);
        free(vals);
        return result;
    }

    if (VALUE_TYPE(e1) != VALUE_DICT) {
        return value_ctx_failure(ctx, engine, "'|' can only be applied to ints, sets, and dicts");
    }
    // get all the dictionaries
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if (VALUE_TYPE(args[i]) != VALUE_DICT) {
            return value_ctx_failure(ctx, engine, "'|' applied to mix of dictionaries and other types");
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

    hvalue_t result = value_put_dict(engine, vals, 2 * n * sizeof(hvalue_t));
    free(vi);
    free(vals);
    return result;
}

hvalue_t f_xor(struct state *state, struct context *ctx, hvalue_t *args, int n, struct engine *engine){
    hvalue_t e1 = args[0];

    if (VALUE_TYPE(e1) == VALUE_INT) {
        for (int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(ctx, engine, "'^' applied to mix of ints and other types");
            }
            e1 ^= e2;
        }
        return e1 | VALUE_INT;
    }

    // get all the sets
    struct val_info *vi = malloc(n * sizeof(*vi));
    int total = 0;
    for (int i = 0; i < n; i++) {
        if (VALUE_TYPE(args[i]) != VALUE_SET) {
            return value_ctx_failure(ctx, engine, "'^' applied to mix of value types");
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

    // sort the engine, but retain duplicates
    int cnt = total / sizeof(hvalue_t);
    qsort(vals, cnt, sizeof(hvalue_t), q_value_cmp);

    // Now remove the engine that have an even number
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

    hvalue_t result = value_put_set(engine, vals, k * sizeof(hvalue_t));
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
	{ "Save", init_Save, op_Save },
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
    { "in", f_in },
    { "IsEmpty", f_isEmpty },
    { "ListAdd", f_list_add },
    { "keys", f_keys },
    { "len", f_len },
    { "max", f_max },
    { "min", f_min },
	{ "mod", f_mod },
    { "not", f_not },
    { "str", f_str },
    { "SetAdd", f_set_add },
    { "type", f_type },
    { NULL, NULL }
};

struct op_info *ops_get(char *opname, int size){
    return dict_lookup(ops_map, opname, size);
}

void ops_init(struct engine *engine) {
    ops_map = dict_new(0, 0, NULL, NULL);
    f_map = dict_new(0, 0, NULL, NULL);
	underscore = value_put_atom(engine, "_", 1);
	this_atom = value_put_atom(engine, "this", 4);
    type_bool = value_put_atom(engine, "bool", 4);
    type_int = value_put_atom(engine, "int", 3);
    type_str = value_put_atom(engine, "str", 3);
    type_pc = value_put_atom(engine, "pc", 2);
    type_list = value_put_atom(engine, "list", 4);
    type_dict = value_put_atom(engine, "dict", 4);
    type_set = value_put_atom(engine, "set", 3);
    type_address = value_put_atom(engine, "address", 7);
    type_context = value_put_atom(engine, "context", 7);

    for (struct op_info *oi = op_table; oi->name != NULL; oi++) {
        void **p = dict_insert(ops_map, NULL, oi->name, strlen(oi->name));
        *p = oi;
    }
    for (struct f_info *fi = f_table; fi->name != NULL; fi++) {
        void **p = dict_insert(f_map, NULL, fi->name, strlen(fi->name));
        *p = fi;
    }
}
