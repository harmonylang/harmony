// This module implements all the functionality for Harmony VM operations.
// In particular, for each instruction X, there are functions init_X(),
// op_X(), and next_X() in this module.  Moreover, for the Nary instruction,
// which takes a function name as argument, there is a function f_Y() for
// each operation Y.
//
// The prototype for init_X is as follows:
//      void *init_X(struct dict *map, struct allocator *allocator);
//
//  It is invoked for each such HVM instruction in the code during
//  initialization of this module for any preprocessing that can happen
//  before model checking starts.  'map' contains the arguments to
//  the instruction.  It returns a 'environment' that is passed to
//  the corresponding op_X() function each time it is executed.
//
// The prototype for op_X is as follows:
//      void op_X(const void *env, struct state *state,
//                   struct step *step);
//  This function is invoked everytime the model checker executes
//  instruction X.  It is passed the 'env' from init_X(), the state
//  of the model, the state of the executing thread (step), and a
//  pointer to the global variables that the model checker maintains.
//
// The prototype for next_X is as follows:
//      void next_X(const void *env, struct context *ctx, FILE *fp);
//  This optional function is invoked only during replay.  The thread
//  with the given ctx is about to execute instruction X.  The function
//  writes to file handle fp a JSON description of that operation.  This
//  is very useful when trying to understand a counter-example.
//
// The prototype for f_Y is as follows:
//      hvalue_t f_Y(struct state *state, struct step *step,
//                           hvalue_t *args, unsigned int n);
//  This function is invoked with a Nary operation is executed with
//  operation Y. 'args' is an array containing the arguments that
//  were on the stack, and n is the numbers of arguments.

#ifndef _WIN32
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#include <unistd.h>
#endif
#endif

#include "head.h"

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#include "value.h"
#include "ops.h"
#include "strbuf.h"
#include "dfa.h"
#include "hashdict.h"
#include "spawn.h"

#ifdef BIRDS
#define main xmain
#include "birds.h"
#undef main
#endif

// Maximum number of arguments of the Nary (N-Ary) HVM operation
#define MAX_ARITY   16

// It is often useful to unpack an aggregate value such as a list, set,
// or dict.
struct val_info {
    unsigned int index;         // index of some particular value in array
    unsigned int size;          // # values
    hvalue_t *vals;             // points to array of values
};

// Each Harmony N-ary function has a name and a C function that implements it
struct f_info {
    char *name;
    hvalue_t (*f)(struct state *state, struct step *step, hvalue_t *args, unsigned int n);
};

// Bounded variables occur in various Harmony expressions, e.g.:
//      let x, (y, z) = 1, (2, 3):
//      for i, j in ...:
//      def f(x, y):
// In each case, the bounded variable form a tree where the leaves are
// variable names and the internal nodes are tuples.
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
static hvalue_t alloc_pool_atom, alloc_next_atom;
static hvalue_t type_bool, type_int, type_str, type_pc, type_list;
static hvalue_t type_dict, type_set, type_address, type_context;

bool has_countLabel;            // TODO.  Hack for backward compatibility

// Helper function for vt_string()
static void vt_string_recurse(struct strbuf *sb, const struct var_tree *vt){
    switch (vt->type) {
    case VT_NAME:
        {
            unsigned int size;
            char *name = value_get(vt->u.name, &size);
            strbuf_printf(sb, "%.*s", size, name);
        }
        break;
    case VT_TUPLE:
        strbuf_printf(sb, "(");
        for (unsigned int i = 0; i < vt->u.tuple.n; i++) {
            if (i != 0) {
                strbuf_printf(sb, ", ");
            }
            vt_string_recurse(sb, vt->u.tuple.elements[i]);
        }
        strbuf_printf(sb, ")");
        break;
    default:
        panic("vt_string_recurse");
    }
}

// Return a string representation of a bound variable, which may be
// a nested tuple of variable names.
static char *vt_string(struct var_tree *vt){
    struct strbuf sb;

    strbuf_init(&sb);
    vt_string_recurse(&sb, vt);
    return strbuf_convert(&sb);
}

// Push a value onto the context stack of the current thread
static inline void ctx_push(struct context *ctx, hvalue_t v){
    assert(v != 0);
    ctx_stack(ctx)[ctx->sp++] = v;
}

// Pop a value from the context stack of the current thread
static inline hvalue_t ctx_pop(struct context *ctx){
    assert(ctx->sp > 0);
    assert(ctx_stack(ctx)[ctx->sp - 1] != 0);
    return ctx_stack(ctx)[--ctx->sp];
}

// Peep at the top of the stack
static inline hvalue_t ctx_peep(struct context *ctx){
    assert(ctx->sp > 0);
    return ctx_stack(ctx)[ctx->sp - 1];
}

// See if the given shared variable (identified by indices) is sequential, in
// which case Load and Store operations on it are considered atomic (race-free).
// indices is a path in the shared variable tree of length n.
static inline bool is_sequential(hvalue_t *indices, unsigned int n){
    assert(n > 1);
    assert(indices[0] == VALUE_PC_SHARED);
    for (unsigned int i = 0; i < global.nseqs; i++) {
        if (indices[1] == global.seqs[i]) {
            return true;
        }
    }
    return false;
}

// Helper function for var_match().
hvalue_t var_match_rec(struct context *ctx, struct var_tree *vt, struct allocator *allocator,
                            hvalue_t arg, hvalue_t vars){
    switch (vt->type) {
    case VT_NAME:
        if (vt->u.name == underscore) {
            return vars;
        }
        return value_dict_store(allocator, vars, vt->u.name, arg);
    case VT_TUPLE:
        if (VALUE_TYPE(arg) != VALUE_LIST) {
            if (vt->u.tuple.n == 0) {
                return value_ctx_failure(ctx, allocator, "match: expected ()");
            }
            else {
                char *v = value_string(arg);
                return value_ctx_failure(ctx, allocator, "match: expected a tuple instead of %s", v);
            }
        }
        if (arg == VALUE_LIST) {
            if (vt->u.tuple.n != 0) {
                return value_ctx_failure(ctx, allocator, "match: expected a %d-tuple",
                                                vt->u.tuple.n);
            }
            return vars;
        }
        if (vt->u.tuple.n == 0) {
            return value_ctx_failure(ctx, allocator, "match: expected an empty tuple");
        }
        unsigned int size;
        hvalue_t *vals = value_get(arg, &size);
        size /= sizeof(hvalue_t);
        if (vt->u.tuple.n != size) {
            return value_ctx_failure(ctx, allocator, "match: tuple size mismatch");
        }
        for (unsigned int i = 0; i < size; i++) {
            vars = var_match_rec(ctx, vt->u.tuple.elements[i], allocator, vals[i], vars);
        }
        return vars;
    default:
        panic("var_match_rec: bad vartree type");
        return 0;
    }
}

// vt represents a bound variable (or nested tuple of bound variables) and
// arg is a Harmony value.  This function matches the value with the bound
// variable and assigns values accordingly to the local variables of the
// current method (which are in ctx->vars).
void var_match(struct context *ctx, struct var_tree *vt, struct allocator *allocator, hvalue_t arg){
    hvalue_t vars = var_match_rec(ctx, vt, allocator, arg, ctx->vars);
    if (!ctx->failed) {
        ctx->vars = vars;
    }
}

// Helper function for var_parse() to skip over spaces
static void skip_blanks(char *s, int len, int *index){
    while (*index < len && s[*index] == ' ') {
        (*index)++;
    }
}

// Bound variables (e.g., "(a, (b, c))") are represented as strings in
// the HVM code.  This code parses those strings to create a var_tree.
struct var_tree *var_parse(struct allocator *allocator, char *s, int len, int *index){
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
                struct var_tree *elt = var_parse(allocator, s, len, index);
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
        vt->u.name = value_put_atom(allocator, &s[*index], i - *index);
        *index = i;
    }
    return vt;
}

// Check for potential stack overflow
static inline bool check_stack(struct context *ctx, unsigned int needed) {
    return ctx->sp < MAX_CONTEXT_STACK - ctx_extent - needed;
}

// This code invokes the interrupt handler of a thread.
void interrupt_invoke(struct step *step){
    assert(step->ctx->extended);
    assert(!step->ctx->interruptlevel);
    if (!check_stack(step->ctx, 2)) {
        value_ctx_failure(step->ctx, step->allocator, "interrupt: out of stack");
        return;
    }
    ctx_push(step->ctx,
        VALUE_TO_INT((step->ctx->pc << CALLTYPE_BITS) | CALLTYPE_INTERRUPT));
    if (step->keep_callstack) {
        struct callstack *cs = new_alloc(struct callstack);
        cs->parent = step->callstack;
        cs->pc = (unsigned int) VALUE_FROM_PC(ctx_trap_pc(step->ctx));
        cs->arg = ctx_trap_arg(step->ctx);
        cs->sp = step->ctx->sp;
        cs->vars = step->ctx->vars;
        cs->return_address = ((step->ctx->pc + 1) << CALLTYPE_BITS) | CALLTYPE_INTERRUPT;
        step->callstack = cs;
        strbuf_printf(&step->explain, "operation aborted; interrupt invoked");
    }
    ctx_push(step->ctx, ctx_trap_arg(step->ctx));
    step->ctx->pc = (uint16_t) VALUE_FROM_PC(ctx_trap_pc(step->ctx));
    ctx_trap_pc(step->ctx) = 0;
    step->ctx->interruptlevel = true;
}

// This function tries to load as much as possible of a given address
// from the given dictionary dict.  The dictionary represents a tree
// of values, which internal nodes consisting of either more dictionaries
// or lists or strings (atoms).  The address is a list of 'indices" of length n.
// The index into indices and the last value are returned.
static unsigned int ind_tryload(struct allocator *allocator, hvalue_t dict, hvalue_t *indices, unsigned int n, hvalue_t *result){
    hvalue_t d = dict;
    for (unsigned int i = 0; i < n; i++) {
        if (!value_tryload(allocator, d, indices[i], &d)) {
            *result = d;
            return i;
        }
    }
    *result = d;
    return n;
}

// Try to store a value in the given variable identified by root (a dictionary
// or a list) and a list of indices of length n.  The updated 'root' is
// returned in *result.  The function returns whether this succeeded.
static bool ind_trystore(hvalue_t root, hvalue_t *indices, int n, hvalue_t value, struct allocator *allocator, bool *is_append, hvalue_t *result){
    assert(VALUE_TYPE(root) == VALUE_DICT || VALUE_TYPE(root) == VALUE_LIST);
    assert(n > 0);

    if (n == 1) {
        return value_trystore(allocator, root, indices[0], value, true, is_append, result);
    }
    unsigned int size;
    hvalue_t *vals = value_get(root, &size);
    size /= sizeof(hvalue_t);

    if (VALUE_TYPE(root) == VALUE_DICT) {
        assert(size % 2 == 0);

        for (unsigned i = 0; i < size; i += 2) {
            if (vals[i] == indices[0]) {
                hvalue_t d = vals[i+1];
                if (VALUE_TYPE(d) != VALUE_DICT && VALUE_TYPE(d) != VALUE_LIST && VALUE_TYPE(d) != VALUE_ATOM) {
                    return false;
                }
                hvalue_t nd;
                if (!ind_trystore(d, indices + 1, n - 1, value, allocator, is_append, &nd)) {
                    return false;
                }
                if (d == nd) {
                    *result = root;
                    return true;
                }
                int n = size * sizeof(hvalue_t);
#ifdef HEAP_ALLOC
                hvalue_t *copy = malloc(n * sizeof(hvalue_t));
#else
                hvalue_t copy[n];
#endif
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                hvalue_t v = value_put_dict(allocator, copy, n);
#ifdef HEAP_ALLOC
                free(copy);
#endif
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
        if (!ind_trystore(d, indices + 1, n - 1, value, allocator, is_append, &nd)) {
            return false;
        }
        if (d == nd) {
            *result = root;
            return true;
        }
        int nsize = size * sizeof(hvalue_t);
#ifdef HEAP_ALLOC
        hvalue_t *copy = malloc(nsize * sizeof(hvalue_t));
#else
        hvalue_t copy[nsize];
#endif
        memcpy(copy, vals, nsize);
        copy[index] = nd;
        hvalue_t v = value_put_list(allocator, copy, nsize);
#ifdef HEAP_ALLOC
        free(copy);
#endif
        *result = v;
        return true;
    }
}

// Remove a variable from 'root' identified by the given indices of length n.
// The updated 'root' is returned in *result.  The function returns whether
// the operation was successful.
static bool ind_remove(struct context *ctx, hvalue_t root, hvalue_t *indices, int n,
                        struct allocator *allocator, bool *is_list, hvalue_t *result) {
    // TODO.  Is this assertion warranted?
    assert(VALUE_TYPE(root) == VALUE_DICT || VALUE_TYPE(root) == VALUE_LIST || VALUE_TYPE(root) == VALUE_ATOM);
    assert(n > 0);

    if (n == 1) {
        *is_list = false;
        *result = value_remove(ctx, allocator, root, indices[0]);
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
                if (VALUE_TYPE(d) != VALUE_DICT && VALUE_TYPE(d) != VALUE_LIST && VALUE_TYPE(d) != VALUE_ATOM) {
                    return false;
                }
                hvalue_t nd;
                if (!ind_remove(ctx, d, indices + 1, n - 1, allocator, is_list, &nd)) {
                    return false;
                }
                if (d == nd) {
                    *result = root;
                    return true;
                }
                int n = size * sizeof(hvalue_t);
#ifdef HEAP_ALLOC
                hvalue_t *copy = malloc(n * sizeof(hvalue_t));
#else
                hvalue_t copy[n];
#endif
                memcpy(copy, vals, n);
                copy[i + 1] = nd;
                hvalue_t v = value_put_dict(allocator, copy, n);
#ifdef HEAP_ALLOC
                free(copy);
#endif
                *is_list = false;
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
        // TODO.  Is this assertion warranted?  Should it return an error?
        assert (VALUE_TYPE(root) == VALUE_LIST);
        if (VALUE_TYPE(indices[0]) != VALUE_INT) {
            return false;
        }
        int index = (int) VALUE_FROM_INT(indices[0]);
        if (index < 0 || index >= (int) size) {
            return false;
        }
        hvalue_t d = vals[index];
        if (VALUE_TYPE(d) != VALUE_DICT && VALUE_TYPE(d) != VALUE_LIST && VALUE_TYPE(d) != VALUE_ATOM) {
            return false;
        }
        hvalue_t nd;
        if (!ind_remove(ctx, d, indices + 1, n - 1, allocator, is_list, &nd)) {
            return false;
        }
        if (d == nd) {
            *result = root;
            return true;
        }
        int n = size * sizeof(hvalue_t);
#ifdef HEAP_ALLOC
        hvalue_t *copy = malloc(n * sizeof(hvalue_t));
#else
        hvalue_t copy[n];
#endif
        memcpy(copy, vals, n);
        copy[index] = nd;
        hvalue_t v = value_put_list(allocator, copy, n);
#ifdef HEAP_ALLOC
        free(copy);
#endif
        *is_list = true;
        *result = v;
        return true;
    }
    return false;
}

// For better, easier-to-understand output, Charm maintains, during replay of
// a counter-example, a callstack for each thread that is not actually part
// of its state.  This function pushes the method and its argument as well
// as the return address and the local variables of the old method onto the
// callstack.
static void update_callstack(struct step *step, hvalue_t method, hvalue_t arg) {
    unsigned int pc = (unsigned int) VALUE_FROM_PC(method);

    // This may not hold because Builtin commands
    // assert(strcmp(global.code.instrs[pc].oi->name, "Frame") == 0);

    struct callstack *cs = new_alloc(struct callstack);
    cs->parent = step->callstack;
    cs->pc = pc;
    cs->arg = arg;
    cs->sp = step->ctx->sp;
    cs->vars = step->ctx->vars;
    cs->return_address = ((step->ctx->pc + 1) << CALLTYPE_BITS) | CALLTYPE_NORMAL;
    step->callstack = cs;

    const struct env_Frame *ef = global.code.instrs[pc].env;
    strbuf_printf(&step->explain, "pop an argument (#+) and call method (%u: #+)", pc);
    step->explain_args[step->explain_nargs++] = arg;
    step->explain_args[step->explain_nargs++] = ef->name;
}

void op_Apply(const void *env, struct state *state, struct step *step){
    const struct env_Apply *ea = env;

    hvalue_t arg = ctx_pop(step->ctx);
    ctx_push(step->ctx, VALUE_LIST);
    ctx_push(step->ctx, VALUE_TO_INT((step->ctx->pc << CALLTYPE_BITS) | CALLTYPE_NORMAL));

    // See if we need to keep track of the call stack
    if (step->keep_callstack) {
        update_callstack(step, ea->method, arg);
    }

    // Push the argument
    ctx_push(step->ctx, arg);

    // Continue at the given function
    step->ctx->pc = (uint16_t) VALUE_FROM_PC(ea->method);
}

void op_Assert(const void *env, struct state *state, struct step *step){
    hvalue_t v = ctx_pop(step->ctx);

    if (VALUE_TYPE(v) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, step->allocator, "assert can only be applied to booleans");
    }
    if (v == VALUE_FALSE) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "pop a value (False) and raise exception");
        }
        value_ctx_failure(step->ctx, step->allocator, "Harmony assertion failed");
    }
    else {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "pop a value (True); do not raise exception");
        }
        step->ctx->pc++;
    }
}

void op_Assert2(const void *env, struct state *state, struct step *step){
    hvalue_t e = ctx_pop(step->ctx);
    hvalue_t v = ctx_pop(step->ctx);
    if (VALUE_TYPE(v) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, step->allocator, "assert2 can only be applied to booleans");
    }
    if (v == VALUE_FALSE) {
        char *p = value_string(e);
        value_ctx_failure(step->ctx, step->allocator, "Harmony assertion failed: %s", p);
        free(p);
    }
    else {
        step->ctx->pc++;
    }
}

void next_Print(const void *env, struct context *ctx, FILE *fp){
    hvalue_t symbol = ctx_peep(ctx);
    char *s = value_json(symbol);
    fprintf(fp, "{ \"type\": \"Print\", \"value\": %s }", s);
    free(s);
}

static void do_print(hvalue_t symbol){
    if (VALUE_TYPE(symbol) == VALUE_ATOM) {
        unsigned int size;
        char *s = value_get(symbol, &size);
        printf("%.*s", size, s);
    }
    else {
        char *s = value_string(symbol);
        printf("%s", s);
        free(s);
    }
}

void op_Print(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "Can't print in read-only mode");
        return;
    }
    hvalue_t symbol = ctx_pop(step->ctx);
    if (global.run_direct) {
        if (global.dfa != NULL) {
            int t = dfa_step(global.dfa, state->dfa_state, symbol);
            if (t < 0) {
                panic("bad behavior");
            }
            state->dfa_state = dfa_dest(global.dfa, t);
        }
        else {
            if (VALUE_TYPE(symbol) == VALUE_LIST) {
                unsigned int size;
                hvalue_t *vals = value_get(symbol, &size);
                size /= sizeof(hvalue_t);
                for (unsigned int i = 0; i < size; i++) {
                    if (i != 0) {
                        printf(" ");
                    }
                    do_print(vals[i]);
                }
            }
            else {
                do_print(symbol);
            }
            printf("\n");
        }
    }
    else {
        // TODO.  Can get rid of this test and MAX_PRINT.
        if (step->nlog == MAX_PRINT) {
            value_ctx_failure(step->ctx, step->allocator, "Print: too many prints");
            return;
        }
        assert(step->nlog == 0);
        step->log[step->nlog++] = symbol;
    }
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "pop value (#+) and add to print log");
        step->explain_args[step->explain_nargs++] = symbol;

        // TODO.  This is currently duplicated in onestep/twostep
        if (global.dfa != NULL) {
            int t = dfa_step(global.dfa, state->dfa_state, symbol);
            if (t < 0) {
                char *p = value_string(symbol);
                value_ctx_failure(step->ctx, step->allocator, "Behavior failure on %s", p);
                free(p);
                return;
            }
            state->dfa_state = dfa_dest(global.dfa, t);
        }
    }
    step->ctx->pc++;
}

void op_AtomicDec(const void *env, struct state *state, struct step *step){
    struct context *ctx = step->ctx;

    if (step->keep_callstack) {
        if (ctx->atomic == 1) {
            strbuf_printf(&step->explain, "decrement atomic counter from 1 to 0: no longer atomic");
        }
        else {
            strbuf_printf(&step->explain, "decrement atomic counter from %d to %d: remains atomic", ctx->atomic, ctx->atomic - 1);
        }
    }

    assert(ctx->atomic > 0);
    ctx->atomic--;
    ctx->pc++;
}

void op_AtomicInc(const void *env, struct state *state, struct step *step){
    struct context *ctx = step->ctx;

    if (step->keep_callstack) {
        if (ctx->atomic == 0) {
            strbuf_printf(&step->explain, "increment atomic counter from 0 to 1: becomes atomic");
        }
        else {
            strbuf_printf(&step->explain, "increment atomic counter from %d to %d: remains atomic", ctx->atomic, ctx->atomic + 1);
        }
    }

    ctx->atomic++;
    if (ctx->atomic == 0) {
        value_ctx_failure(step->ctx, step->allocator, "AtomicInc overflow");
    }
    else {
        ctx->pc++;
    }
}

void next_Choose(const void *env, struct context *ctx, FILE *fp){
    hvalue_t choices = ctx_peep(ctx);
    assert(VALUE_TYPE(choices) == VALUE_SET);
    assert(choices != VALUE_SET);
    char *val = value_json(choices);
    fprintf(fp, "{ \"type\": \"Choose\", \"value\": %s }", val);
    free(val);
}

void op_Choose(const void *env, struct state *state, struct step *step){
    if (global.run_direct) {
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
        printf("   <newline>: random choice\n");
        for (;;) {
            printf("--> "); fflush(stdout);
            char line[128];
            if (fgets(line, sizeof(line), stdin) == NULL || feof(stdin)) {
                printf("EOF\n");
                exit(1);
            }
            if (line[0] == '\n') {
                unsigned int selection = rand() % size;
                ctx_push(step->ctx, vals[selection]);
                step->ctx->pc++;
                return;
            }
            else {
                unsigned int selection;
                if (sscanf(line, "%u", &selection) == 1) {
                    selection -= 1;
                    if (selection < size) {
                        ctx_push(step->ctx, vals[selection]);
                        step->ctx->pc++;
                        return;
                    }
                }
            }
            fflush(stdin);
            printf("Bad selection. Try again\n");
        }
    }
    else {
        panic("op_Choose: should not be called");
    }
}

void op_Continue(const void *env, struct state *state, struct step *step){
    step->ctx->pc++;
}

// This is helper fumction to execute the return of a method call. Usually
// this would be when a Return instruction is executed, but Charm also
// supports built-in methods that need to return the same way.  We also
// need to special case the return of an interrupt handler or the top-level
// method of a thread (i.e., when the thread terminates).
// The top of the stack contains an integer that has the call type
// and the return value OR-ed together.
static void do_return(struct state *state, struct step *step, hvalue_t result){
    // If there is nothing on the stack, this is the last return and the
    // thread has terminated
    if (step->ctx->sp == 0) {
        ctx_push(step->ctx, result);
        step->ctx->terminated = true;
        return;
    }

    // See if it's a normal call or an interrupt
    hvalue_t callval = ctx_pop(step->ctx);
    assert(VALUE_TYPE(callval) == VALUE_INT);
    unsigned int call = (unsigned int) VALUE_FROM_INT(callval);
    switch (call & CALLTYPE_MASK) {
    case CALLTYPE_NORMAL:
        // In case of a normal call, the list of arguments of a Load
        // instruction are on the stack and the pc still points to
        // the Load instruction
        {
            unsigned int pc = call >> CALLTYPE_BITS;
            assert(pc != step->ctx->pc);

            // Get the remaining arguments
            hvalue_t args = ctx_pop(step->ctx);
            assert(VALUE_TYPE(args) == VALUE_LIST);

            // If it's the empty list, we're done and can move
            // on the instruction beyond the Load instruction
            if (args == VALUE_LIST) {
                ctx_push(step->ctx, result);
                step->ctx->pc = pc + 1;
            }

            // Otherwise re-execute the Load instruction with a new address
            // That is, we turn the remaining arguments back into an address
            // (a 'thunk', actually) and execute the Load instruction once more.
            else {
                unsigned int size;
                hvalue_t *list = value_get(args, &size);
                unsigned int asize = size + sizeof(hvalue_t);
                
#ifdef HEAP_ALLOC
                hvalue_t *addr = malloc(asize);
#else
                hvalue_t addr[asize];
#endif
                addr[0] = result;
                memcpy(&addr[1], list, size);
                ctx_push(step->ctx, value_put_address(step->allocator, addr, asize));
#ifdef HEAP_ALLOC
                free(addr);
#endif
                step->ctx->pc = pc;
            }
        }
        break;
    // In case of the return of an interrupt handler, we simply restore
    // the state from just before the interrupt
    case CALLTYPE_INTERRUPT:
        step->ctx->interruptlevel = false;
        unsigned int pc = call >> CALLTYPE_BITS;
        assert(pc != step->ctx->pc);
        step->ctx->pc = pc;
        break;
    default:
        fprintf(stderr, "CT: %x %x\n", call, call & CALLTYPE_MASK);
        panic("Return: bad call type");
    }

    // During the generation of the counter-example, pop the top of the
    // callstack.
    if (step->keep_callstack) {
        struct callstack *cs = step->callstack;
        step->callstack = cs->parent;
    }
}

// To find data races, we track for each step which variables are read and
// written.  This also turns out to be useful for optimizing counterexamples.
static void ai_add(struct step *step, hvalue_t *indices, unsigned int n, bool load){
#ifdef notdef // TODO
    // Assertions and invariants do not conflict with normal ops.
    if (step->ctx->readonly) {
        return;
    }
#endif

    struct allocator *al = step->allocator;
    if (al != NULL) {
        // Find the end of the list
        struct access_info **pai, *ai;
        for (pai = &step->ai; (ai = *pai) != NULL; pai = &ai->next)
            ;

        // Add a new entry
        ai = (*al->alloc)(al->ctx, sizeof(*ai), true, false);
        ai->indices = indices;
        ai->n = n;
        ai->atomic = (step->ctx->atomic > 0) || is_sequential(indices, n);
        ai->load = load;
        ai->next = NULL;
        *pai = ai;
    }
}

// Built-in alloc.malloc method
// TODO.  DISABLED.  Two problems: ai_add and atomic mode
void op_Alloc_Malloc(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    hvalue_t next = value_dict_load(step->vars, alloc_next_atom);

    // Assign arg to alloc$pool[alloc$next]
    hvalue_t addr[3];
    addr[0] = VALUE_PC_SHARED;
    addr[1] = alloc_pool_atom;
    addr[2] = next;
    // TODO.  THIS CANNOT WORK AS addr IS NOT COPIED
    ai_add(step, addr, 3, false);
    if (!ind_trystore(step->vars, addr + 1, 2, arg, step->allocator, NULL, &step->vars)) {
        panic("op_Alloc_Malloc: store value failed");
    }

    // Increment next
    hvalue_t addr2[2];
    addr2[0] = VALUE_PC_SHARED;
    addr2[1] = alloc_next_atom;
    // TODO.  THIS CANNOT WORK AS addr IS NOT COPIED
    ai_add(step, addr2, 2, false);
    next = VALUE_TO_INT(VALUE_FROM_INT(next) + 1);
    step->vars = value_dict_store(step->allocator, step->vars, alloc_next_atom, next);

    // Return the address
    hvalue_t result = value_put_address(step->allocator, addr, sizeof(addr));
    do_return(state, step, result);
}

// Built-in list.tail method
void op_List_Tail(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    if (VALUE_TYPE(arg) != VALUE_LIST) {
        value_ctx_failure(step->ctx, step->allocator, "list.tail: not a list");
        return;
    }
    unsigned int size;
    hvalue_t *list = value_get(arg, &size);
    if (size == 0) {
        value_ctx_failure(step->ctx, step->allocator, "list.tail: empty list");
        return;
    }
    hvalue_t result = value_put_list(step->allocator, &list[1], size - sizeof(hvalue_t));
    do_return(state, step, result);
}

static unsigned int direct_count;
static mutex_t direct_mutex;
struct direct_done {
    struct direct_done *next;
    hvalue_t ctx, result;
};
static struct direct_done *direct_done;

// Increment the number of outstanding activities.
static void direct_outstanding(){
    mutex_acquire(&direct_mutex);
    direct_count++;
    mutex_release(&direct_mutex);
}

// Add ctx/result to the done list
static void direct_completed(hvalue_t ctx, hvalue_t result){
    assert(result != 0);
    mutex_acquire(&direct_mutex);
    direct_count--;
    struct direct_done *dd = calloc(1, sizeof(*dd));
    dd->ctx = ctx;
    dd->result = result;
    dd->next = direct_done;
    direct_done = dd;
    mutex_release(&direct_mutex);
}

// See if any external activities completed.
void direct_check(struct state *state, struct step *step){
    mutex_acquire(&direct_mutex);

    struct direct_done *dd;
    while ((dd = direct_done) != NULL) {
        assert(dd->result != 0);
        direct_done = dd->next;

        // Copy the context and reserve an extra hvalue_t
        unsigned int size;
        struct context *orig = value_get(dd->ctx, &size);
#ifdef HEAP_ALLOC
        char *buffer = malloc(size + sizeof(hvalue_t));
#else
        char buffer[size + sizeof(hvalue_t)];
#endif
        memcpy(buffer, orig, size);
        struct context *copy = (struct context *) buffer;
        ctx_push(copy, dd->result);
        copy->stopped = false;
        hvalue_t context = value_put_context(step->allocator, copy);
#ifdef HEAP_ALLOC
        free(buffer);
#endif

        // Remove old context from stopbag if it's there
        // TODO.  Can potentially be optimized when it's a matter of just moving it to
        //        the context bag
        // TODO.  Duplicated from else part below.  Make subroutine
        hvalue_t *ctxlist = state_ctxlist(state);
        for (unsigned int i = state->bagsize; i < state->total; i++) {
            hvalue_t ctxi = ctxlist[i] & ~STATE_MULTIPLICITY;
            if (ctxi == dd->ctx) {
                if ((ctxlist[i] & STATE_MULTIPLICITY) > ((hvalue_t) 1 << STATE_M_SHIFT)) {
                    ctxlist[i] -= ((hvalue_t) 1 << STATE_M_SHIFT);
                }
                else {
                    assert(state->total > state->bagsize);
                    state->total--;
                    memmove(&ctxlist[i], &ctxlist[i+1], (state->total - i) * sizeof(hvalue_t));
                }
                break;
            }
        }

        // Add new context to the context bag
        if (context_add(state, context) < 0) {
            panic("direct_check: too many threads");
        }
        free(dd);
    }
    mutex_release(&direct_mutex);
}

struct iqueue {
    mutex_t lock;
    hvalue_t *vals;
    unsigned int nvals;
};

struct bogus_op {
    enum {
        IQ_NEW, IQ_ENQUEUE, IQ_DEQUEUE,
#ifdef BIRDS
        OLB_NEW, OLB_WB_ACQUIRE, OLB_WB_RELEASE,
                 OLB_EB_ACQUIRE, OLB_EB_RELEASE
#endif
    } type;
    struct allocator *allocator;
    hvalue_t context;
    struct {
#ifdef BIRDS
        struct {
            struct device *olb;
        } olb;
#endif
        struct {
            struct iqueue *iq;  // only for enqueue and dequeue;
            hvalue_t arg;       // only for enqueue
        } iq;
    } args;
};

#ifdef BIRDS
static void olb_print(struct strbuf *sb, void *ref){
    strbuf_printf(sb, "OLB<%p>", ref);
}

static int olb_compare(void *ref1, void *ref2){
    if (ref1 < ref2) return -1;
    if (ref1 > ref2) return 1;
    return 0;
}
#endif

static void iq_print(struct strbuf *sb, void *ref){
    strbuf_printf(sb, "IQueue<%p>", ref);
}

static int iq_compare(void *ref1, void *ref2){
    if (ref1 < ref2) return -1;
    if (ref1 > ref2) return 1;
    return 0;
}

#ifdef BIRDS
struct external_descriptor olb_descr = {
    .type_name = "OLB",
    .print = olb_print,
    .compare = olb_compare
};
#endif

struct external_descriptor iq_descr = {
    .type_name = "IQueue",
    .print = iq_print,
    .compare = iq_compare
};

static void bogus_run(void *arg){
    struct bogus_op *bop = arg;

    hvalue_t result = 0;
    switch (bop->type) {
#ifdef BIRDS
    case OLB_NEW:
        {
            struct device *olb = malloc(sizeof(*olb));
            dev_init(olb);
            result = value_put_external(bop->allocator, &olb_descr, olb);
        }
        break;
    case OLB_WB_ACQUIRE:
        {
            struct device *olb = bop->args.olb.olb;
            dev_enter(olb, 0);
            result = VALUE_ADDRESS_SHARED;  // None
        }
        break;
    case OLB_WB_RELEASE:
        {
            struct device *olb = bop->args.olb.olb;
            dev_exit(olb, 0);
            result = VALUE_ADDRESS_SHARED;  // None
        }
        break;
    case OLB_EB_ACQUIRE:
        {
            struct device *olb = bop->args.olb.olb;
            dev_enter(olb, 1);
            result = VALUE_ADDRESS_SHARED;  // None
        }
        break;
    case OLB_EB_RELEASE:
        {
            struct device *olb = bop->args.olb.olb;
            dev_exit(olb, 1);
            result = VALUE_ADDRESS_SHARED;  // None
        }
        break;
#endif
    case IQ_NEW:
        {
            struct iqueue *iq = calloc(1, sizeof(*iq));
            mutex_init(&iq->lock);
            result = value_put_external(bop->allocator, &iq_descr, iq);
        }
        break;
    case IQ_ENQUEUE:
        {
            struct iqueue *iq = bop->args.iq.iq;
            mutex_acquire(&iq->lock);
            iq->vals = realloc(iq->vals,
                            (iq->nvals + 1) * sizeof(hvalue_t));
            iq->vals[iq->nvals++] = bop->args.iq.arg;
            mutex_release(&iq->lock);
            result = VALUE_ADDRESS_SHARED;  // None
        }
        break;
    case IQ_DEQUEUE:
        {
            struct iqueue *iq = bop->args.iq.iq;
            mutex_acquire(&iq->lock);
            if (iq->nvals == 0) {
                result = VALUE_ADDRESS_SHARED;  // None
            }
            else {
                result = iq->vals[0];
                assert(result != 0);
                iq->nvals--;
                memmove(iq->vals, &iq->vals[1],
                                iq->nvals * sizeof(hvalue_t));
            }
            mutex_release(&iq->lock);
        }
        break;
    default:
        panic("bogus_run: unknown type");
    }

    direct_completed(bop->context, result);
    free(bop);
}

static hvalue_t direct_getarg(struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);

    // See if it's a normal call.
    hvalue_t callval = ctx_pop(step->ctx);
    assert(VALUE_TYPE(callval) == VALUE_INT);
    unsigned int call = (unsigned int) VALUE_FROM_INT(callval);
    assert((call & CALLTYPE_MASK) == CALLTYPE_NORMAL);
    unsigned int pc = call >> CALLTYPE_BITS;
    assert(pc != step->ctx->pc);

    // Get the remaining arguments
#ifndef NDEBUG
    hvalue_t args =
#endif
    ctx_pop(step->ctx);
    assert(args == VALUE_LIST);

    // Go on to the next instruction after resuming
    step->ctx->pc = pc + 1;
    step->ctx->stopped = true;

    return arg;
}

#ifdef BIRDS
// Built-in bogus.olb_new method
void op_Bogus_olb_new(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_new: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);
    if (arg != VALUE_LIST) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_new: must have no argument");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = OLB_NEW;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}

// Built-in bogus.olb_wb_acquire method
void op_Bogus_olb_wb_acquire(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_wb_acquire: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);
    struct val_external *ve = value_get_external(arg);
    if (ve->descr != &olb_descr) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_wb_acquire: arg must be an olb");
        return;
    }
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_wb_acquire: in read-only mode");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = OLB_WB_ACQUIRE;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);
    bop->args.olb.olb = ve->ref;

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}

// Built-in bogus.olb_wb_release method
void op_Bogus_olb_wb_release(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_wb_acquire: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);
    struct val_external *ve = value_get_external(arg);
    if (ve->descr != &olb_descr) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_wb_release: arg must be an olb");
        return;
    }
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_wb_release: in read-only mode");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = OLB_WB_RELEASE;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);
    bop->args.olb.olb = ve->ref;

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}

// Built-in bogus.olb_eb_acquire method
void op_Bogus_olb_eb_acquire(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_eb_acquire: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);
    struct val_external *ve = value_get_external(arg);
    if (ve->descr != &olb_descr) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_eb_acquire: arg must be an olb");
        return;
    }
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_eb_acquire: in read-only mode");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = OLB_EB_ACQUIRE;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);
    bop->args.olb.olb = ve->ref;

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}

// Built-in bogus.olb_eb_release method
void op_Bogus_olb_eb_release(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_eb_acquire: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);
    struct val_external *ve = value_get_external(arg);
    if (ve->descr != &olb_descr) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_eb_release: arg must be an olb");
        return;
    }
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.olb_eb_release: in read-only mode");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = OLB_EB_RELEASE;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);
    bop->args.olb.olb = ve->ref;

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}
#endif // BIRDS

// Built-in bogus.iq_new method
void op_Bogus_iq_new(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_new: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);
    if (arg != VALUE_LIST) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_new: must have no argument");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = IQ_NEW;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}

// Built-in bogus.iq_enqueue method
void op_Bogus_iq_enqueue(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_new: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);

    // TODO.  Check that arg is a list

    unsigned int size;
    hvalue_t *args = value_get(arg, &size);
    if (size != 2 * sizeof(hvalue_t)) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_enqueue: must have two arguments");
        return;
    }
    if (VALUE_TYPE(args[0]) != VALUE_EXTERNAL) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_enqueue: first arg must be external");
        return;
    }
    struct val_external *ve = value_get_external(args[0]);
    if (ve->descr != &iq_descr) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_enqueue: first arg must be an iqueue");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = IQ_ENQUEUE;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);
    bop->args.iq.iq = ve->ref;
    bop->args.iq.arg = args[1];

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}

// Built-in bogus.iq_dequeue method
void op_Bogus_iq_dequeue(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_new: in read-only mode");
        return;
    }
    hvalue_t arg = direct_getarg(step);
    struct val_external *ve = value_get_external(arg);
    if (ve->descr != &iq_descr) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_dequeue: arg must be an iqueue");
        return;
    }
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "bogus.iq_dequeue: in read-only mode");
        return;
    }

    struct bogus_op *bop = calloc(1, sizeof(*bop));
    bop->type = IQ_DEQUEUE;
    bop->allocator = step->allocator;
    bop->context = value_put_context(step->allocator, step->ctx);
    bop->args.iq.iq = ve->ref;

    // Note that an external activity is outstanding
    direct_outstanding();

    // Start a native thread to execute the operation.
    thread_create(bogus_run, bop);
}

// Built-in bag.add method
void op_Bag_Add(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    if (VALUE_TYPE(arg) != VALUE_LIST) {
        value_ctx_failure(step->ctx, step->allocator, "bag.add: not a tuple");
        return;
    }
    unsigned int size;
    hvalue_t *args = value_get(arg, &size);
    if (size != 2 * sizeof(hvalue_t)) {
        value_ctx_failure(step->ctx, step->allocator, "bag.add: requires two arguments");
        return;
    }
    if (VALUE_TYPE(args[0]) != VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.add: first argument must be a bag");
        return;
    }
    hvalue_t result = value_bag_add(step->allocator, args[0], args[1], 1);
    do_return(state, step, result);
}

// Built-in bag.remove method
void op_Bag_Remove(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    if (VALUE_TYPE(arg) != VALUE_LIST) {
        value_ctx_failure(step->ctx, step->allocator, "bag.remove: not a tuple");
        return;
    }
    unsigned int size;
    hvalue_t *args = value_get(arg, &size);
    if (size != 2 * sizeof(hvalue_t)) {
        value_ctx_failure(step->ctx, step->allocator, "bag.remove: requires two arguments");
        return;
    }
    if (VALUE_TYPE(args[0]) != VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.remove: first argument must be a bag");
        return;
    }
    hvalue_t result = value_bag_remove(step->allocator, args[0], args[1]);
    if (result == 0) {
        // element was not in the bag
        do_return(state, step, args[0]);
    }
    else {
        do_return(state, step, result);
    }
}

// Built-in bag.multiplicity method
void op_Bag_Multiplicity(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    if (VALUE_TYPE(arg) != VALUE_LIST) {
        value_ctx_failure(step->ctx, step->allocator, "bag.multiplicity: not a tuple");
        return;
    }
    unsigned int size;
    hvalue_t *args = value_get(arg, &size);
    if (size != 2 * sizeof(hvalue_t)) {
        value_ctx_failure(step->ctx, step->allocator, "bag.multiplicity: requires two arguments");
        return;
    }
    if (VALUE_TYPE(args[0]) != VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.multiplicity: first argument must be a bag");
        return;
    }
    hvalue_t result;
    if (value_tryload(step->allocator, args[0], args[1], &result)) {
        if (VALUE_TYPE(result) != VALUE_INT) {
            value_ctx_failure(step->ctx, step->allocator, "bag.multiplicity: not a good bag");
        }
        do_return(state, step, result);
    }
    else {
        do_return(state, step, VALUE_TO_INT(0));
    }
}

// Built-in bag.size method
void op_Bag_Size(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    if (VALUE_TYPE(arg) != VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.size: not a dict");
        return;
    }
    unsigned int size;
    hvalue_t *list = value_get(arg, &size);
    size /= sizeof(hvalue_t);
    unsigned int total = 0;
    for (unsigned int i = 1; i < size; i += 2) {
        if (VALUE_TYPE(list[i]) != VALUE_INT) {
            value_ctx_failure(step->ctx, step->allocator, "bag.size: not a bag");
            return;
        }
        total += (unsigned int) VALUE_FROM_INT(list[i]);
    }
    do_return(state, step, VALUE_TO_INT(total));
}

// Built-in bag.bmax method
void op_Bag_Bmax(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    if (arg == VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.bmax: empty bag");
        return;
    }
    if (VALUE_TYPE(arg) != VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.bmax: not a dict");
        return;
    }
    unsigned int size;
    hvalue_t *list = value_get(arg, &size);
    size /= sizeof(hvalue_t);
    assert(size >= 2);
    hvalue_t result = list[0];
    for (unsigned int i = 2; i < size; i += 2) {
        int cmp = value_cmp(result, list[i]);
        if (cmp > 0) {
            result = list[i];
        }
    }
    do_return(state, step, result);
}

// Built-in bag.bmin method
void op_Bag_Bmin(const void *env, struct state *state, struct step *step){
    hvalue_t arg = ctx_pop(step->ctx);
    if (arg == VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.bmax: empty bag");
        return;
    }
    if (VALUE_TYPE(arg) != VALUE_DICT) {
        value_ctx_failure(step->ctx, step->allocator, "bag.bmax: not a dict");
        return;
    }
    unsigned int size;
    hvalue_t *list = value_get(arg, &size);
    size /= sizeof(hvalue_t);
    assert(size >= 2);
    hvalue_t result = list[0];
    for (unsigned int i = 2; i < size; i += 2) {
        int cmp = value_cmp(result, list[i]);
        if (cmp < 0) {
            result = list[i];
        }
    }
    do_return(state, step, result);
}

// This operation expects on the top of the stack an enumerable value
// and an integer index.  If the index is valid (not the size of the
// collection), then it assigns the given element to key and value and
// pushes True.  Otherwise it pops the two allocator from the stack and
// pushes False.
void op_Cut(const void *env, struct state *state, struct step *step){
    const struct env_Cut *ec = env;
    struct context *ctx = step->ctx;

    // Get the index
    hvalue_t index = ctx_pop(step->ctx);
    assert(VALUE_TYPE(index) == VALUE_INT);
    unsigned int idx = (unsigned int) VALUE_FROM_INT(index);

    // Peek at the collection
    assert(ctx->sp > 0);
    hvalue_t v = ctx_stack(ctx)[ctx->sp - 1];        // the collection

    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "pop index (#+) and value (#+); ");
        step->explain_args[step->explain_nargs++] = index;
        step->explain_args[step->explain_nargs++] = v;
    }

    if (VALUE_TYPE(v) == VALUE_SET || VALUE_TYPE(v) == VALUE_LIST) {
        // Get the collection
        unsigned int size;
        hvalue_t *vals = value_get(v, &size);
        size /= sizeof(hvalue_t);
        if (idx >= size) {
            if (step->keep_callstack) {
                strbuf_printf(&step->explain, "out of range -> push False");
            }
            ctx_stack(ctx)[ctx->sp - 1] = VALUE_FALSE;
        }
        else {
            if (step->keep_callstack) {
                char *var = vt_string(ec->value);
                strbuf_printf(&step->explain, "assign value (#+) to %s; ", var);
                step->explain_args[step->explain_nargs++] = vals[idx];
                free(var);
            }
            var_match(step->ctx, ec->value, step->allocator, vals[idx]);
            if (ec->key != NULL) {
                if (step->keep_callstack) {
                    char *key = vt_string(ec->key);
                    strbuf_printf(&step->explain, "assign index (%u) to %s; ", idx, key);
                    free(key);
                }
                var_match(step->ctx, ec->key, step->allocator, index);
            }
            if (step->keep_callstack) {
                strbuf_printf(&step->explain, "push new index (%u) and True", idx + 1);
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
            if (step->keep_callstack) {
                strbuf_printf(&step->explain, "out of range -> push False");
            }
            ctx_stack(ctx)[ctx->sp - 1] = VALUE_FALSE;
        }
        else {
            if (ec->key == NULL) {
                if (step->keep_callstack) {
                    char *var = vt_string(ec->value);
                    strbuf_printf(&step->explain, "assign value (#+) to %s; ", var);
                    step->explain_args[step->explain_nargs++] = vals[2*idx];
                    free(var);
                }
                var_match(step->ctx, ec->value, step->allocator, vals[2*idx]);
            }
            else {
                if (step->keep_callstack) {
                    char *var = vt_string(ec->key);
                    strbuf_printf(&step->explain, "assign key (#+) to %s; ", var);
                    step->explain_args[step->explain_nargs++] = vals[2*idx];
                    free(var);
                }
                var_match(step->ctx, ec->key, step->allocator, vals[2*idx]);
                if (step->keep_callstack) {
                    char *var = vt_string(ec->value);
                    strbuf_printf(&step->explain, "assign value (#+) to %s; ", var);
                    step->explain_args[step->explain_nargs++] = vals[2*idx + 1];
                    free(var);
                }
                var_match(step->ctx, ec->value, step->allocator, vals[2*idx + 1]);
            }
            if (step->keep_callstack) {
                strbuf_printf(&step->explain, "push new index (%u) and True", idx + 1);
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
            if (step->keep_callstack) {
                strbuf_printf(&step->explain, "out of range -> push False");
            }
            ctx_stack(ctx)[ctx->sp - 1] = VALUE_FALSE;
        }
        else {
            hvalue_t e = value_put_atom(step->allocator, &chars[idx], 1);
            if (step->keep_callstack) {
                char *var = vt_string(ec->value);
                strbuf_printf(&step->explain, "assign character (#+) to %s; ", var);
                step->explain_args[step->explain_nargs++] = e;
                free(var);
            }
            var_match(step->ctx, ec->value, step->allocator, e);
            if (ec->key != NULL) {
                if (step->keep_callstack) {
                    char *key = vt_string(ec->key);
                    strbuf_printf(&step->explain, "assign index (%u) to %s; ", idx, key);
                    free(key);
                }
                var_match(step->ctx, ec->key, step->allocator, index);
            }
            if (step->keep_callstack) {
                strbuf_printf(&step->explain, "push new index (%u) and True", idx + 1);
            }
            ctx_push(step->ctx, VALUE_TO_INT(idx + 1));
            ctx_push(step->ctx, VALUE_TRUE);
        }
        step->ctx->pc++;
        return;
    }
    value_ctx_failure(step->ctx, step->allocator, "op_Cut: not an iterable type");
}

void op_Del(const void *env, struct state *state, struct step *step){
    const struct env_Del *ed = env;

    assert(VALUE_TYPE(step->vars) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "Can't update state in assert or invariant");
        return;
    }

    if (ed == 0) {
        hvalue_t av = ctx_pop(step->ctx);
        if (VALUE_TYPE(av) != VALUE_ADDRESS_SHARED) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, step->allocator, "Del %s: not an address", p);
            free(p);
            return;
        }
        if (av == VALUE_ADDRESS_SHARED) {
            value_ctx_failure(step->ctx, step->allocator, "Del: address is None");
            return;
        }

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        if (indices[0] != VALUE_PC_SHARED) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, step->allocator, "Del %s: not the address of a shared variable", p);
            free(p);
            return;
        }
        size /= sizeof(hvalue_t);

        hvalue_t nd;
        bool is_list;
        if (!ind_remove(step->ctx, step->vars, indices + 1, size - 1, step->allocator, &is_list, &nd)) {
            value_ctx_failure(step->ctx, step->allocator, "Del: no such variable");
        }
        else {
            // If del is applied to a list, it updates the list.  But if
            // applied to a dictionary, it only updates that entry.
            assert(size > 0);
            ai_add(step, indices, is_list ? size - 1 : size, false);

            step->vars = nd;
            step->ctx->pc++;
        }
    }
    else {
        // Currently this can only mean deleting a variable
        assert(ed->n == 1);

        hvalue_t nd;
        bool is_list;
        if (!ind_remove(step->ctx, step->vars, ed->indices + 1, ed->n - 1, step->allocator, &is_list, &nd)) {
            value_ctx_failure(step->ctx, step->allocator, "Del: bad variable");
        }
        else {
            assert(!is_list);
            ai_add(step, ed->indices, ed->n, false);
            step->vars = nd;
            step->ctx->pc++;
        }
    }
}

void op_DelVar(const void *env, struct state *state, struct step *step){
    const struct env_DelVar *ed = env;

    assert(VALUE_TYPE(step->ctx->vars) == VALUE_DICT);
    if (ed == NULL) {
        hvalue_t av = ctx_pop(step->ctx);
        assert(VALUE_TYPE(av) == VALUE_ADDRESS_PRIVATE);
        assert(av != VALUE_ADDRESS_PRIVATE);

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        if (indices[0] != VALUE_PC_LOCAL) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, step->allocator, "DelVar %s: not the address of a method variable", p);
            free(p);
            return;
        }
        size /= sizeof(hvalue_t);

        bool result;
        if (indices[1] == this_atom) {
            if (!step->ctx->extended) {
                value_ctx_failure(step->ctx, step->allocator, "DelVar: context does not have 'this'");
                return;
            }
            if (VALUE_TYPE(ctx_this(step->ctx)) != VALUE_DICT) {
                value_ctx_failure(step->ctx, step->allocator, "DelVar: 'this' is not a dictionary");
                return;
            }
            bool is_list;
		    result = ind_remove(step->ctx, ctx_this(step->ctx), &indices[2], size - 2, step->allocator, &is_list, &ctx_this(step->ctx));
        }
        else {
            bool is_list;
		    result = ind_remove(step->ctx, step->ctx->vars, indices + 1, size - 1, step->allocator, &is_list, &step->ctx->vars);
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, step->allocator, "DelVar: bad address: %s", x);
            free(x);
			return;
		}
    }
	else {
        if (ed->name == this_atom) {
            value_ctx_failure(step->ctx, step->allocator, "DelVar: can't del 'this'");
            return;
        }
        else {
            step->ctx->vars = value_dict_remove(step->allocator, step->ctx->vars, ed->name);
        }
	}
	step->ctx->pc++;
}

void op_Dup(const void *env, struct state *state, struct step *step){
    hvalue_t v = ctx_pop(step->ctx);
    ctx_push(step->ctx, v);
    ctx_push(step->ctx, v);
    step->ctx->pc++;
}

void next_Frame(const void *env, struct context *ctx, FILE *fp){
    const struct env_Frame *ef = env;

    hvalue_t arg = ctx_peep(ctx);
    char *name = value_string(ef->name);
    char *args = vt_string(ef->args);
    char *val = value_json(arg);
    fprintf(fp, "{ \"type\": \"Frame\", \"name\": %s, \"args\": \"%s\", \"value\": %s }",
                name, args, val);
    free(name);
    free(args);
    free(val);
}

void op_Frame(const void *env, struct state *state, struct step *step){
    const struct env_Frame *ef = env;
    hvalue_t oldvars = step->ctx->vars;

    if (!check_stack(step->ctx, 1)) {
        value_ctx_failure(step->ctx, step->allocator, "Frame: out of stack (recursion too deep?)");
        return;
    }

    step->ctx->vars = VALUE_DICT;

    hvalue_t arg = ctx_pop(step->ctx);
    if (step->keep_callstack) {
        char *args = vt_string(ef->args);
        if (strcmp(args, "()") == 0 && arg == VALUE_LIST) {
            strbuf_printf(&step->explain, "pop argument () and run method #+");
            step->explain_args[step->explain_nargs++] = ef->name;
        }
        else {
            strbuf_printf(&step->explain, "pop argument (#+), assign to %s, and run method #+", args);
            step->explain_args[step->explain_nargs++] = arg;
            step->explain_args[step->explain_nargs++] = ef->name;
        }
        free(args);
    }

    // match argument against parameters
    var_match(step->ctx, ef->args, step->allocator, arg);
    if (step->ctx->failed) {
        printf("Frame match failed\n");
        return;
    }

    ctx_push(step->ctx, oldvars);   // Save old variables
    step->ctx->pc += 1;
}

void op_Go(
    const void *env,
    struct state *state,
    struct step *step
){
    hvalue_t ctx = ctx_pop(step->ctx);
    if (VALUE_TYPE(ctx) != VALUE_CONTEXT) {
        value_ctx_failure(step->ctx, step->allocator, "Go: not a context");
        return;
    }
    hvalue_t result = ctx_pop(step->ctx);

    // Copy the context and reserve an extra hvalue_t
    unsigned int size;
    struct context *orig = value_get(ctx, &size);
#ifdef HEAP_ALLOC
    char *buffer = malloc(size + sizeof(hvalue_t));
#else
    char buffer[size + sizeof(hvalue_t)];
#endif
    memcpy(buffer, orig, size);
    struct context *copy = (struct context *) buffer;
    ctx_push(copy, result);
    copy->stopped = false;
    hvalue_t context = value_put_context(step->allocator, copy);
#ifdef HEAP_ALLOC
    free(buffer);
#endif
    step->ctx->pc++;

    if (global.run_direct) {
        // Remove old context from stopbag if it's there
        // TODO.  Can potentially be optimized when it's a matter of just moving it to
        //        the context bag
        // TODO.  Duplicated from else part below.  Make subroutine
        hvalue_t *ctxlist = state_ctxlist(state);
        for (unsigned int i = state->bagsize; i < state->total; i++) {
            hvalue_t ctxi = ctxlist[i] & ~STATE_MULTIPLICITY;
            if (ctxi == ctx) {
                if ((ctxlist[i] & STATE_MULTIPLICITY) > ((hvalue_t) 1 << STATE_M_SHIFT)) {
                    ctxlist[i] -= ((hvalue_t) 1 << STATE_M_SHIFT);
                }
                else {
                    assert(state->total > state->bagsize);
                    state->total--;
                    memmove(&ctxlist[i], &ctxlist[i+1], (state->total - i) * sizeof(hvalue_t));
                }
                break;
            }
        }
        if (context_add(state, context) < 0) {
            value_ctx_failure(step->ctx, step->allocator, "go: too many threads");
        }
    }
    else if (step->keep_callstack) {
        // Remove old context from stopbag if it's there
        // TODO.  Can potentially be optimized when it's a matter of just moving it to
        //        the context bag
        hvalue_t *ctxlist = state_ctxlist(state);
        for (unsigned int i = state->bagsize; i < state->total; i++) {
            hvalue_t ctxi = ctxlist[i] & ~STATE_MULTIPLICITY;
            if (ctxi == ctx) {
                if ((ctxlist[i] & STATE_MULTIPLICITY) > ((hvalue_t) 1 << STATE_M_SHIFT)) {
                    ctxlist[i] -= ((hvalue_t) 1 << STATE_M_SHIFT);
                }
                else {
                    assert(state->total > state->bagsize);
                    state->total--;
                    memmove(&ctxlist[i], &ctxlist[i+1], (state->total - i) * sizeof(hvalue_t));
                }
                break;
            }
        }

        // Add new context to context bag
        if (context_add(state, context) < 0) {
            panic("op_Go: context_add");
        }

        // Find the process
        unsigned int pid;
        for (pid = 0; pid < global.nprocesses; pid++) {
            if (global.processes[pid] == ctx) {
                global.processes[pid] = context;
                break;
            }
        }
        if (pid >= global.nprocesses) {
            panic("op_Go: can't find process");
        }
    }
    else {
        if (step->nunstopped == MAX_SPAWN) {
            value_ctx_failure(step->ctx, step->allocator, "Maximum #threads unstopped exceeded");
        }
        step->unstopped[step->nunstopped++] = ctx;
        if (step->nspawned == MAX_SPAWN) {
            value_ctx_failure(step->ctx, step->allocator, "Maximum #threads resumed exceeded");
        }
        step->spawned[step->nspawned++] = context;
    }
}

void op_Finally(const void *env, struct state *state, struct step *step){
#ifdef OBSOLETE
    const struct env_Finally *ef = env;

    // Create a context for the predicate
    char context[sizeof(struct context) +
                        (ctx_extent + 2) * sizeof(hvalue_t)];
    struct context *ctx = (struct context *) context;
    memset(ctx, 0, sizeof(*ctx));
    ctx->pc = ef->pc;
    ctx->vars = VALUE_DICT;
    ctx->readonly = 1;
    ctx->atomic = 1;
    ctx_push(ctx, VALUE_LIST);
    hvalue_t finctx = value_put_context(step->allocator, ctx);

    mutex_acquire(&global.inv_lock);
    global.finals = realloc(global.finals, (global.nfinals + 1) * sizeof(*global.finals));
    global.finals[global.nfinals++] = finctx;
    mutex_release(&global.inv_lock);
#endif

    step->ctx->pc += 1;
}

void op_Invariant(const void *env, struct state *state, struct step *step){
#ifdef OBSOLETE
    const struct env_Invariant *ei = env;

    // Create a context for the invariant
    char context[sizeof(struct context) +
                        (ctx_extent + 2) * sizeof(hvalue_t)];
    struct context *ctx = (struct context *) context;
    memset(ctx, 0, sizeof(*ctx));
    ctx->pc = ei->pc;
    ctx->vars = VALUE_DICT;
    ctx->readonly = 1;
    ctx->atomic = 1;
    ctx_push(ctx, VALUE_LIST);	// HACK
    hvalue_t invctx = value_put_context(step->allocator, ctx);

    mutex_acquire(&global.inv_lock);
    global.invs = realloc(global.invs, (global.ninvs + 1) * sizeof(*global.invs));
    struct invariant *inv = &global.invs[global.ninvs++];
    inv->context = invctx;
    inv->pc = ei->pc;
    inv->pre = ei->pre;
    if (ei->pre) {
        global.inv_pre = true;
    }
    mutex_release(&global.inv_lock);
#endif

    step->ctx->pc += 1;
}

void op_Jump(const void *env, struct state *state, struct step *step){
    const struct env_Jump *ej = env;
    step->ctx->pc = ej->pc;
}

void op_JumpCond(const void *env, struct state *state, struct step *step){
    const struct env_JumpCond *ej = env;

    hvalue_t v = ctx_pop(step->ctx);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "pop value (#+), compare to #+, and jump to %u if the same", ej->pc);
        step->explain_args[step->explain_nargs++] = v;
        step->explain_args[step->explain_nargs++] = ej->cond;
    }
    if ((ej->cond == VALUE_FALSE || ej->cond == VALUE_TRUE) &&
                            !(v == VALUE_FALSE || v == VALUE_TRUE)) {
        value_ctx_failure(step->ctx, step->allocator, "JumpCond: not an boolean");
    }
    else if (v == ej->cond) {
        assert(step->ctx->pc != ej->pc);
        step->ctx->pc = ej->pc;
    }
    else {
        step->ctx->pc++;
    }
}

void next_Load(const void *env, struct context *ctx, FILE *fp){
    const struct env_Load *el = env;
    char *x;

    if (el == 0) {
        assert(ctx->sp > 0);
        hvalue_t av = ctx_peep(ctx);
        assert(VALUE_TYPE(av) == VALUE_ADDRESS_SHARED || VALUE_TYPE(av) == VALUE_ADDRESS_PRIVATE);
        assert(av != VALUE_ADDRESS_SHARED && av != VALUE_ADDRESS_PRIVATE);

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        x = indices_string(indices, size);
    }
    else {
        x = indices_string(el->indices, el->n);
    }
    assert(x[0] == '?');
    size_t n = strlen(x);
    char *json = json_escape(x+1, n-1);
    fprintf(fp, "{ \"type\": \"Load\", \"var\": \"%s\" }", json);
    free(json);
    free(x);
}

// This is a helper function to call a method.  Harmony supports method
// calls in two ways.  The simple and more efficient way is to execute an
// Apply instruction.  However, another way is to execute a Load instruction
// using an address (thunk) that has a PcValue for the function.  Here,
// 'av' is the original address that was loaded, method is the PcValue,
// 'args' are the remaining arguments in the address, and size the number
// of remaining arguments.  This function first pushes the list of arguments
// (except the first) and then pushes an integer onto the stack that contains
// the program counter of the Load instruction OR-ed together with
// CALLTYPE_NORMAL.  It pushes the first argument as an argument to the
// method and then sets the program counter to the first instruction of
// the method (which should be a Frame instruction, by the way).
void do_Call(struct step *step,
            hvalue_t av, hvalue_t method, hvalue_t *args, unsigned int size){
    assert(VALUE_TYPE(method) == VALUE_PC);
    if (VALUE_FROM_PC(method) <= 0) {
        char *p = value_string(av);
        value_ctx_failure(step->ctx, step->allocator, "Load %s: bad pc %d", p, (int) VALUE_FROM_PC(method));
        free(p);
        return;
    }

    // Push the remaining arguments of the address.
    hvalue_t remainder = value_put_list(step->allocator,
            &args[1], (size - 1) * sizeof(hvalue_t));
    ctx_push(step->ctx, remainder);

    // Push the return address
    ctx_push(step->ctx, VALUE_TO_INT((step->ctx->pc << CALLTYPE_BITS) | CALLTYPE_NORMAL));

    // See if we need to keep track of the call stack
    if (step->keep_callstack) {
        update_callstack(step, method, args[0]);
    }

    // Push the argument
    ctx_push(step->ctx, args[0]);

    // Continue at the given function
    step->ctx->pc = (uint16_t) VALUE_FROM_PC(method);
}

// Helper function to load as much as possible using the address (or really,
// 'thunk').  If it ends in a PC value, call the method.  When the method
// returns, the Load instruction will be re-executed with the remaining part
// of the thunk.  Here, 'av' is the original address, 'root' is the Harmony
// value that we're indexing into, 'indices' is the list of arguments or
// index values, and 'size' is the number of arguments.
void do_Load(struct state *state, struct step *step,
            hvalue_t av, hvalue_t root, hvalue_t *indices, unsigned int size){
    // See how much we can load from the shared memory
    hvalue_t v;
    unsigned int k = ind_tryload(step->allocator, root, indices, size, &v);

    if (k != size) {
        // Implement concatenation of strings and lists.  In Python, you're
        // allowed to write x = "a" "b", which assigns "ab" to x.  This is
        // only allowed for string constants.  In order to support the
        // same functionality in Harmony, we detect if the program is trying
        // to index into a string using another string instead of an integer.
        // In that case, we concatenate.  This is no longer restricted to
        // just string constants.
        if (VALUE_TYPE(v) == VALUE_ATOM) {
            // All the remaining values must be strings as well
#ifdef HEAP_ALLOC
            struct val_info *vi = malloc((size - k + 1) * sizeof(struct val_info));
#else
            struct val_info vi[size - k + 1];
#endif
            struct val_info *vip = vi;
            vip->vals = value_get(v, &vip->size);
            unsigned total = vip->size;
            vip++;
            for (unsigned int i = k; i < size; i++, vip++) {
                if (VALUE_TYPE(indices[k]) != VALUE_ATOM) {
                    char *p = value_string(av);
                    value_ctx_failure(step->ctx, step->allocator, "Load %s: bad string index", p);
                    free(p);
#ifdef HEAP_ALLOC
                    free(vi);
#endif
                    return;
                }
                vip->vals = value_get(indices[i], &vip->size);
                total += vip->size;
            }
#ifdef HEAP_ALLOC
            char *chars = malloc(total);
#else
            char chars[total];
#endif
            char *p = chars;
            for (struct val_info *vip2 = vi; vip2 < vip; vip2++) {
                memcpy(p, vip2->vals, vip2->size);
                p += vip2->size;
            }
            hvalue_t result = value_put_atom(step->allocator, chars, total);
#ifdef HEAP_ALLOC
            free(vi);
            free(chars);
#endif
            ctx_push(step->ctx, result);
            step->ctx->pc++;
            return;
        }

        // Given that we implement string concatenation, it makes sense
        // to also implement list concatenation the same way...
        if (VALUE_TYPE(v) == VALUE_LIST) {
            // All the remaining values must be lists as well
#ifdef HEAP_ALLOC
            struct val_info *vi = malloc((size - k + 1) * sizeof(struct val_info));
#else
            struct val_info vi[size - k + 1];
#endif
            struct val_info *vip = vi;
            vip->vals = value_get(v, &vip->size);
            unsigned total = vip->size;
            vip++;
            for (unsigned int i = k; i < size; i++, vip++) {
                if (VALUE_TYPE(indices[k]) != VALUE_LIST) {
                    char *p = value_string(av);
                    value_ctx_failure(step->ctx, step->allocator, "Load %s: bad list index", p);
                    free(p);
#ifdef HEAP_ALLOC
                    free(vi);
#endif
                    return;
                }
                vip->vals = value_get(indices[i], &vip->size);
                total += vip->size;
            }
#ifdef HEAP_ALLOC
            char *items = malloc(total);
#else
            char items[total];
#endif
            char *p = items;
            for (struct val_info *vip2 = vi; vip2 < vip; vip2++) {
                memcpy(p, vip2->vals, vip2->size);
                p += vip2->size;
            }
            hvalue_t result = value_put_list(step->allocator, items, total);
#ifdef HEAP_ALLOC
            free(vi);
            free(items);
#endif
            ctx_push(step->ctx, result);
            step->ctx->pc++;
            return;
        }

        // If we could not load all, the remainder should be a method call.
        if (VALUE_TYPE(v) != VALUE_PC) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, step->allocator, "Load %s: can't load", p);
            free(p);
            return;
        }
        do_Call(step, av, v, &indices[k], size - k);
        return;
    }

    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "pop address (#+) and push value (#+)");
        step->explain_args[step->explain_nargs++] = av;
        step->explain_args[step->explain_nargs++] = v;
    }

    // We were able to process the entire address
    ctx_push(step->ctx, v);
    step->ctx->pc++;
}

// There are two versions of Load.  Load can take a shared variable name as
// argument, in which case the value of the shared variable should be pushed
// onto the stack.  It exists to improve readability of the HVM code of
// simple Harmony programs.  However, if there is no argument, there is
// an Address on top of the stack.  An address is a "thunk", consisting
// of a function and a list of arguments.  If the function is f() and the
// list is [a, b, c], then Load should push the value of "f a b c".  That
// is, it should evaluate "f a" first, then apply the result to b, and
// the result of that to c.  Given the recursive nature of Load, it is more
// or less evaluated that way.  Load pushes [b c] onto the stack and then
// evaluates "f a".  The result of that, say g, is combined with [b c] to
// push a new thunk, and the Load instruction is executed again.  This
// continues until the list of arguments is empty, after which execution
// continues after the Load instruction (with the result still on the stack).
//
// However, there are a few special cases, depending on the function in
// the thunk:
//  - it could be "VALUE_PC_SHARED" (a PcValue of -1), in which case
//    the arguments are really an index into shared memory.
//  - it could be a list, dictionary, or string, in which case the arguments
//    index into it.
//  - it could be a PcValue, in which case the method should be invoked
//    with the first argument, and the result should be applied to the
//    remaining arguments.
//
// As a very important optimization, when indexing into a tree of lists and/or
// indices, op_Load tries to evaluate as much as possible (using do_Load)
// until it hits a PcValue (if ever).  If we didn't do this, a Load of
// some "deep" variable would result in many steps.  Now, in the best case,
// it's just a single step.
void op_Load(const void *env, struct state *state, struct step *step){
    const struct env_Load *el = env;

    assert(VALUE_TYPE(step->vars) == VALUE_DICT);

    // See if the address is on the stack
    if (el == 0) {
        // Pop the address and do a sanity check
        hvalue_t av = ctx_pop(step->ctx);
        if (VALUE_TYPE(av) != VALUE_ADDRESS_SHARED && VALUE_TYPE(av) != VALUE_ADDRESS_PRIVATE) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, step->allocator, "Load %s: not an address", p);
            free(p);
            return;
        }
        assert(av != VALUE_ADDRESS_PRIVATE);
        if (av == VALUE_ADDRESS_SHARED) {
            value_ctx_failure(step->ctx, step->allocator, "Load: can't load from None");
            return;
        }

        // Get the function and arguments
        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        assert(size > 1);

        // See if it's reading a shared variable
        if (indices[0] == VALUE_PC_SHARED) {
            assert(VALUE_TYPE(av) == VALUE_ADDRESS_SHARED);
            assert(step->keep_callstack || step->allocator != NULL);

            // Keep track for race detection
            // TODO.  Should it check the entire address?  Maybe part
            //        of it is not memory.
            ai_add(step, indices, size, true);

            do_Load(state, step, av, step->vars, indices + 1, size - 1);
        }
        else {
            assert(VALUE_TYPE(av) == VALUE_ADDRESS_PRIVATE);
            if (indices[0] == VALUE_PC_LOCAL) {
                do_Load(state, step, av, step->ctx->vars, indices + 1, size - 1);
            }
            else if (VALUE_TYPE(indices[0]) != VALUE_PC) {
                do_Load(state, step, av, indices[0], indices + 1, size - 1);
            }
            else {
                do_Call(step, av, indices[0], indices + 1, size - 1);
            }
        }
    }
    else {
        if (!check_stack(step->ctx, 1)) {
            value_ctx_failure(step->ctx, step->allocator, "Load: out of stack");
            return;
        }

        ai_add(step, el->indices, el->n, true);
        hvalue_t v;
        unsigned int k = ind_tryload(step->allocator, step->vars, el->indices + 1, el->n - 1, &v);
        if (k != el->n - 1) {
            char *x = indices_string(el->indices, el->n);
            value_ctx_failure(step->ctx, step->allocator, "Load: unknown variable %s", x);
            free(x);
            return;
        }

        if (step->keep_callstack) {
            char *x = indices_string(el->indices, el->n);
            strbuf_printf(&step->explain, "push value (#+) of variable %s", x + 1);
            step->explain_args[step->explain_nargs++] = v;
            free(x);
        }

        ctx_push(step->ctx, v);
        step->ctx->pc++;
    }
}

void op_LoadVar(const void *env, struct state *state, struct step *step){
    const struct env_LoadVar *el = env;
    assert(VALUE_TYPE(step->ctx->vars) == VALUE_DICT);

    hvalue_t v;
    if (el->name == this_atom) {
        if (!step->ctx->extended) {
            value_ctx_failure(step->ctx, step->allocator, "LoadVar: context does not have 'this'");
            return;
        }
        if (VALUE_TYPE(ctx_this(step->ctx)) != VALUE_DICT) {
            value_ctx_failure(step->ctx, step->allocator, "LoadVar: 'this' is not a dictionary");
            return;
        }
        ctx_push(step->ctx, ctx_this(step->ctx));
    }
    else if (value_tryload(step->allocator, step->ctx->vars, el->name, &v)) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "push value (#+) of variable #+");
            step->explain_args[step->explain_nargs++] = v;
            step->explain_args[step->explain_nargs++] = el->name;
        }
        ctx_push(step->ctx, v);
    }
    else {
        char *p = value_string(el->name);
        value_ctx_failure(step->ctx, step->allocator, "LoadVar: unknown variable %s", p);
        free(p);
        return;
    }
    step->ctx->pc++;
}

void op_Move(const void *env, struct state *state, struct step *step){
    const struct env_Move *em = env;
    struct context *ctx = step->ctx;
    int offset = ctx->sp - em->offset;
    hvalue_t *stack = ctx_stack(ctx);

    hvalue_t v = stack[offset];
    memmove(&stack[offset], &stack[offset + 1],
                (em->offset - 1) * sizeof(hvalue_t));
    stack[ctx->sp - 1] = v;
    ctx->pc++;
}

void op_Nary(const void *env, struct state *state, struct step *step){
    const struct env_Nary *en = env;
    hvalue_t args[MAX_ARITY];

    if (step->keep_callstack) {
        if (en->arity > 0) {
            if (en->arity == 1) {
                strbuf_printf(&step->explain, "pop a value (");
            }
            else {
                strbuf_printf(&step->explain, "pop %d values (", en->arity);
            }
        }
    }
    for (unsigned int i = 0; i < en->arity; i++) {
        args[i] = ctx_pop(step->ctx);
        if (step->keep_callstack) {
            if (i > 0) {
                strbuf_printf(&step->explain, ", ");
            }
            strbuf_printf(&step->explain, "#+");
            assert(step->explain_nargs <= MAX_ARGS);        // TODO
            step->explain_args[step->explain_nargs++] = args[i];
        }
    }
    if (step->keep_callstack) {
        if (en->arity > 0) {
            strbuf_printf(&step->explain, "); ");
        }
    }
    hvalue_t result = (*en->fi->f)(state, step, args, en->arity);
    if (!step->ctx->failed) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "push result (#+)");
            assert(step->explain_nargs <= MAX_ARGS);        // TODO
            step->explain_args[step->explain_nargs++] = result;
        }
        ctx_push(step->ctx, result);
        step->ctx->pc++;
    }
    else if (step->keep_callstack) {
        strbuf_printf(&step->explain, "operation failed");
    }
}

void op_Pop(const void *env, struct state *state, struct step *step){
    assert(step->ctx->sp > 0);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "pop and discard value (%+)");
        step->explain_args[step->explain_nargs++] = ctx_peep(step->ctx);
    }
    step->ctx->sp--;
    step->ctx->pc++;
}

void op_Push(const void *env, struct state *state, struct step *step){
    const struct env_Push *ep = env;

    if (step->keep_callstack && VALUE_TYPE(ep->value) == VALUE_PC) {
        unsigned int pc = (unsigned int) VALUE_FROM_PC(ep->value);
        if (strcmp(global.code.instrs[pc].oi->name, "Frame") == 0) {
            const struct env_Frame *ef = global.code.instrs[pc].env;
            strbuf_printf(&step->explain, "push program counter constant %u (%+)", pc);
            step->explain_args[step->explain_nargs++] = ef->name;
        }
    }
    if (!check_stack(step->ctx, 1)) {
        value_ctx_failure(step->ctx, step->allocator, "Push: out of stack");
        return;
    }
    ctx_push(step->ctx, ep->value);
    step->ctx->pc++;
}

void op_ReadonlyDec(const void *env, struct state *state, struct step *step){
    struct context *ctx = step->ctx;

    if (step->keep_callstack) {
        if (ctx->readonly == 1) {
            strbuf_printf(&step->explain, "decrement readonly counter from 1 to 0: no longer readonly");
        }
        else {
            strbuf_printf(&step->explain, "decrement readonly counter from %d to %d: remains readonly", ctx->readonly, ctx->readonly - 1);
        }
    }
    assert(ctx->readonly > 0);
    ctx->readonly--;
    ctx->pc++;
}

void op_ReadonlyInc(const void *env, struct state *state, struct step *step){
    struct context *ctx = step->ctx;

    if (step->keep_callstack) {
        if (ctx->readonly == 0) {
            strbuf_printf(&step->explain, "increment readonly counter from 0 to 1: becomes readonly");
        }
        else {
            strbuf_printf(&step->explain, "increment readonly counter from %d to %d: remains readonly", ctx->readonly, ctx->readonly + 1);
        }
    }

    ctx->readonly++;
    if (ctx->readonly == 0) {
        value_ctx_failure(step->ctx, step->allocator, "ReadonlyInc overflow");
    }
    else {
        ctx->pc++;
    }
}

// There are two versions of Return.  If Return has no arguments, then
// the result of the method is on the stack.  If it does have an argument,
// the result of the method is stored in the named local variable.  This
// function gets the result, restores the old variables (of the calling
// method), and then calls do_return() to do the remaining work.
void op_Return(const void *env, struct state *state, struct step *step){
    const struct env_Return *er = env;

    hvalue_t result;
    if (er->result == 0) {
        result = ctx_pop(step->ctx);
    }
    else {
        result = value_dict_load(step->ctx->vars, er->result);
        if (result == 0) {
            result = er->deflt;
        }
        if (result == 0) {
            value_ctx_failure(step->ctx, step->allocator, "OpReturn: no return value");
            return;
        }
    }

    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "pop caller's method variables and pc and push result (%+), or terminate if no caller");
        step->explain_args[step->explain_nargs++] = result;
    }

    // Restore old variables
    hvalue_t oldvars = ctx_pop(step->ctx);
    assert(VALUE_TYPE(oldvars) == VALUE_DICT);
    step->ctx->vars = oldvars;

    do_return(state, step, result);
}

void op_Builtin(const void *env, struct state *state, struct step *step){
    const struct env_Builtin *eb = env;
    hvalue_t pc = ctx_pop(step->ctx);
    if (VALUE_TYPE(pc) != VALUE_PC) {
        char *p = value_string(pc);
        value_ctx_failure(step->ctx, step->allocator, "Builtin %s: not a PC value", p);
        free(p);
        return;
    }
    if (VALUE_FROM_PC(pc) >= global.code.len) {
        value_ctx_failure(step->ctx, step->allocator, "Builtin %u: not a valid pc", (unsigned) VALUE_FROM_PC(pc));
        return;
    }
    struct op_info *oi = global.code.instrs[VALUE_FROM_PC(pc)].oi;
//    if (strcmp(oi->name, "Frame") != 0) {
//        value_ctx_failure(step->ctx, step->allocator, "Builtin %u: not a Frame instruction", (unsigned) VALUE_FROM_PC(pc));
//        return;
//    }

    unsigned int len;
    char *p = value_get(eb->method, &len);

    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "pop pc (%+) and bind to built-in method %.*s", len, p);
        step->explain_args[step->explain_nargs++] = pc;
    }

    oi = dict_lookup(ops_map, p, len);
    if (oi == NULL) {
        value_ctx_failure(step->ctx, step->allocator, "Builtin: no method %.*s", len, p);
        return;
    }

    global.code.instrs[VALUE_FROM_PC(pc)].oi = oi;
    step->ctx->pc++;
}

void op_Sequential(const void *env, struct state *state, struct step *step){
#ifdef OBSOLETE
    const struct env_Sequential *es = env;
    printf("SEQ %s\n", value_string(es->name));

    hvalue_t addr = ctx_pop(step->ctx);
    if (VALUE_TYPE(addr) != VALUE_ADDRESS_SHARED) {
        char *p = value_string(addr);
        value_ctx_failure(step->ctx, step->allocator, "Sequential %s: not an address", p);
        free(p);
        return;
    }

    /* Insert in set of sequential variables.
     *
     * TODO.  Could lead to race between workers.  Use a lock.
     *        Fortunately unlikely as sequential is mostly used in initialization.
     */
    unsigned int size;
    hvalue_t *seqs = value_copy_extend(global.seqs, sizeof(hvalue_t), &size);
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
    memmove(&seqs[i + 1], &seqs[i], (size - i) * sizeof(hvalue_t));
    seqs[i] = addr;
    global.seqs = value_put_set(step->allocator, seqs, (size + 1) * sizeof(hvalue_t));
    free(seqs);
#endif
    step->ctx->pc++;
}

// Compare two key/value pairs lexicographically, first by key, then by value.
static int q_kv_cmp(const void *e1, const void *e2){
    const hvalue_t *kv1 = (const hvalue_t *) e1;
    const hvalue_t *kv2 = (const hvalue_t *) e2;

    int k = value_cmp(kv1[0], kv2[0]);
    if (k != 0) {
        return k;
    }
    return value_cmp(kv1[1], kv2[1]);
}

// Compare two Harmony values
static int q_value_cmp(const void *v1, const void *v2){
    return value_cmp(* (const hvalue_t *) v1, * (const hvalue_t *) v2);
}

// Sort the set of values (in place) and remove duplicates.  Return the #values.
static unsigned int sort(hvalue_t *vals, unsigned int n){
    qsort(vals, n, sizeof(hvalue_t), q_value_cmp);

    hvalue_t *p = vals, *q = vals + 1;
    for (unsigned int i = 1; i < n; i++, q++) {
        if (*q != *p) {
            *++p = *q;
        }
    }
    p++;
    return (unsigned int) (p - vals);
}

void op_SetIntLevel(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "Can't set interrupt level in read-only mode");
        return;
    }
	bool oldlevel = step->ctx->interruptlevel;
	hvalue_t newlevel =  ctx_pop(step->ctx);
    if (VALUE_TYPE(newlevel) != VALUE_BOOL) {
        value_ctx_failure(step->ctx, step->allocator, "setintlevel can only be set to a boolean");
        return;
    }
    step->ctx->interruptlevel = VALUE_FROM_BOOL(newlevel);
	ctx_push(step->ctx, VALUE_TO_BOOL(oldlevel));
    step->ctx->pc++;
}

void op_Spawn(
    const void *env,
    struct state *state,
    struct step *step
) {
    const struct env_Spawn *se = env;

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "Can't spawn in read-only mode");
        return;
    }
    if (step->nspawned == MAX_SPAWN) {
        value_ctx_failure(step->ctx, step->allocator, "Maximum #threads spawned exceeded");
        return;
    }

    hvalue_t thisval = ctx_pop(step->ctx);
    hvalue_t closure = ctx_pop(step->ctx);
    if (VALUE_TYPE(closure) != VALUE_ADDRESS_PRIVATE) {
        char *p = value_string(closure);
        value_ctx_failure(step->ctx, step->allocator, "Spawn %s: not an address", p);
        free(p);
        return;
    }

    unsigned int size;
    hvalue_t *indices = value_get(closure, &size);
    if (size != 2 * sizeof(hvalue_t)) {
        char *p = value_string(closure);
        value_ctx_failure(step->ctx, step->allocator, "Spawn %s: expected method and arg", p);
        free(p);
        return;
    }
    if (VALUE_TYPE(indices[0]) != VALUE_PC) {
        char *p = value_string(closure);
        value_ctx_failure(step->ctx, step->allocator, "Spawn %s: not a method", p);
        free(p);
        return;
    }
    hvalue_t pc = indices[0], arg = indices[1];

    if (step->keep_callstack && VALUE_TYPE(pc) == VALUE_PC) {
        unsigned int ip = (unsigned int) VALUE_FROM_PC(pc);
        if (strcmp(global.code.instrs[ip].oi->name, "Frame") == 0) {
            const struct env_Frame *ef = global.code.instrs[ip].env;
            strbuf_printf(&step->explain, "pop local state (#+), arg (#+), and pc (%d: #+), and spawn thread", ip);
            step->explain_args[step->explain_nargs++] = thisval;
            step->explain_args[step->explain_nargs++] = arg;
            step->explain_args[step->explain_nargs++] = ef->name;
        }
    }

    pc = VALUE_FROM_PC(pc);

    assert(pc < (hvalue_t) global.code.len);
    assert(strcmp(global.code.instrs[pc].oi->name, "Frame") == 0);

    char context[sizeof(struct context) +
                        (ctx_extent + 2) * sizeof(hvalue_t)];
    struct context *ctx = (struct context *) context;
    memset(ctx, 0, sizeof(*ctx));

    if (thisval != VALUE_DICT) {
        value_ctx_extend(ctx);
        ctx_this(ctx) = thisval;
    }
    ctx->pc = (uint16_t) pc;
    ctx->vars = VALUE_DICT;
    ctx->interruptlevel = false;
    ctx->eternal = se->eternal;
    ctx_push(ctx, arg);
    hvalue_t cc = value_put_context(step->allocator, ctx);
    if (global.run_direct) {
        if (context_add(state, cc) < 0) {
            value_ctx_failure(step->ctx, step->allocator, "spawn: too many threads");
        }
        else {
            step->ctx->pc++;
        }
        return;
    }
    else if (step->keep_callstack) {
        if (context_add(state, cc) < 0) {
            value_ctx_failure(step->ctx, step->allocator, "spawn: too many threads");
            return;
        }
        // Called in second phase, so sequential
        global.processes = realloc(global.processes, (global.nprocesses + 1) * sizeof(hvalue_t));
        global.callstacks = realloc(global.callstacks, (global.nprocesses + 1) * sizeof(struct callstack *));
        global.processes[global.nprocesses] = cc;
        // printf("Add T%u %p\n", global.nprocesses, (void *) cc);
        struct callstack *cs = new_alloc(struct callstack);
        cs->pc = (unsigned int) pc;
        cs->arg = arg;
        cs->vars = VALUE_DICT;
        // TODO.  What's the purpose of the next line exactly
        cs->return_address = (step->ctx->pc << CALLTYPE_BITS) | CALLTYPE_PROCESS;
        global.callstacks[global.nprocesses] = cs;
        global.nprocesses++;
    }
    else {
        step->spawned[step->nspawned++] = cc;
    }

    step->ctx->pc++;
}

void op_Split(const void *env, struct state *state, struct step *step){
    const struct env_Split *es = env;

    hvalue_t v = ctx_pop(step->ctx);
    hvalue_t type = VALUE_TYPE(v);
    if (type != VALUE_SET && type != VALUE_LIST) {
        value_ctx_failure(step->ctx, step->allocator, "Can only split tuples or sets");
        return;
    }
    if (v == VALUE_SET || v == VALUE_LIST) {
        if (es->count != 0) {
            value_ctx_failure(step->ctx, step->allocator, "Split: empty set or tuple");
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
        value_ctx_failure(step->ctx, step->allocator, "Split: wrong size");
        return;
    }
    for (unsigned int i = 0; i < size; i++) {
        ctx_push(step->ctx, vals[i]);
    }
    step->ctx->pc++;
}

void op_Save(const void *env, struct state *state, struct step *step){
    assert(VALUE_TYPE(step->vars) == VALUE_DICT);
    hvalue_t e = ctx_pop(step->ctx);

    // Save the context
    step->ctx->stopped = true;
    step->ctx->pc++;
    hvalue_t v = value_put_context(step->allocator, step->ctx);

    // Restore the stopped mode to false
    step->ctx->stopped = false;

    // Push a tuple returning e and the context
    hvalue_t d[2];
    d[0] = e;
    d[1] = v;
    hvalue_t result = value_put_list(step->allocator, d, sizeof(d));
    ctx_push(step->ctx, result);
}

void op_Stop(const void *env, struct state *state, struct step *step){
    const struct env_Stop *es = env;

    assert(VALUE_TYPE(step->vars) == VALUE_DICT);

    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "Stop: in read-only mode");
        return;
    }

    if (es == 0) {
        hvalue_t av = ctx_pop(step->ctx);
        if (av == VALUE_ADDRESS_SHARED || av == VALUE_LIST) {
            step->ctx->pc++;
            step->ctx->terminated = true;
            return;
        }

        if (VALUE_TYPE(av) != VALUE_ADDRESS_SHARED) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, step->allocator, "Stop %s: not an address", p);
            free(p);
            return;
        }
        step->ctx->pc++;

        step->ctx->stopped = true;
        hvalue_t v = value_put_context(step->allocator, step->ctx);
        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        size /= sizeof(hvalue_t);
        // TODO: check if indices[0] == VALUE_PC_SHARED?
        bool is_append;
        if (!ind_trystore(step->vars, indices + 1, size - 1, v, step->allocator, &is_append, &step->vars)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, step->allocator, "Stop: bad address: %s", x);
            free(x);
        }
        else {
            ai_add(step, indices, is_append ? size - 1 : size, false);
        }
    }
    else {
        // TODO.  Can it even get here???
        step->ctx->stopped = true;
        step->ctx->pc++;
        hvalue_t v = value_put_context(step->allocator, step->ctx);
        // TODO: check if indices[0] == VALUE_PC_SHARED?
        bool is_append;
        if (!ind_trystore(step->vars, es->indices + 1, es->n - 1, v, step->allocator, &is_append, &step->vars)) {
            value_ctx_failure(step->ctx, step->allocator, "Stop: bad variable");
        }
        else {
            ai_add(step, es->indices, is_append ? es->n - 1 : es->n, false);
        }
    }
}

void next_Store(const void *env, struct context *ctx, FILE *fp){
    const struct env_Store *es = env;

    assert(ctx->sp > 0);
    hvalue_t v = ctx_stack(ctx)[ctx->sp - 1];

    if (es == 0) {
        assert(ctx->sp > 1);
        hvalue_t av = ctx_stack(ctx)[ctx->sp - 2];
        assert(VALUE_TYPE(av) == VALUE_ADDRESS_SHARED);
        assert(av != VALUE_ADDRESS_SHARED);

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        assert(indices[0] == VALUE_PC_SHARED);
        size /= sizeof(hvalue_t);
        char *x = indices_string(indices, size);
        assert(x[0] == '?');
        size_t n = strlen(x);
        char *json = json_escape(x+1, n-1);
        char *val = value_json(v);
        fprintf(fp, "{ \"type\": \"Store\", \"var\": \"%s\", \"value\": %s }", json, val);
        free(x);
        free(json);
        free(val);
    }
    else {
        char *x = indices_string(es->indices, es->n);
        assert(x[0] == '?');
        size_t n = strlen(x);
        char *json = json_escape(x+1, n-1);
        char *val = value_json(v);
        fprintf(fp, "{ \"type\": \"Store\", \"var\": \"%s\", \"value\": %s }", json, val);
        free(json);
        free(x);
        free(val);
    }
}

// Store value v at address av.  av is a thunk, so it may not point to
// a shared variable.  If it does, we store v in the shared variable.
// If av is the address of a constant, then we only allow that if the
// value is the same as the constant.  That is, Harmony allows 3 = 3, but
// not 3 = 4.  This is mostly useful in expressions such as (3, x) = (y, 4),
// where x is assigned 4 but fails if y is not 3.
static bool store_match(struct state *state, struct step *step,
                    hvalue_t av, hvalue_t v){
    if (VALUE_TYPE(av) != VALUE_ADDRESS_SHARED &&
                            VALUE_TYPE(av) != VALUE_ADDRESS_PRIVATE) {
        char *p = value_string(av);
        value_ctx_failure(step->ctx, step->allocator, "Store %s: not an address", p);
        free(p);
        return false;
    }
    if (av == VALUE_ADDRESS_SHARED) {
        value_ctx_failure(step->ctx, step->allocator, "Store: address is None");
        return false;
    }

    unsigned int size;
    hvalue_t *indices = value_get(av, &size);
    size /= sizeof(hvalue_t);

    // You can store a constant only at its own address.
    if (VALUE_TYPE(indices[0]) == VALUE_BOOL ||
            VALUE_TYPE(indices[0]) == VALUE_INT ||
            VALUE_TYPE(indices[0]) == VALUE_ATOM ||
            VALUE_TYPE(indices[0]) == VALUE_LIST ||
            VALUE_TYPE(indices[0]) == VALUE_DICT ||
            VALUE_TYPE(indices[0]) == VALUE_SET ||
            VALUE_TYPE(indices[0]) == VALUE_ADDRESS_SHARED) {
        if (indices[0] != v || size != 1) {
            char *addr = value_string(av);
            char *val = value_string(v);
            value_ctx_failure(step->ctx, step->allocator, "Store: bad address %s: value is %s", addr, val);
            free(addr);
            free(val);
            return false;
        }
        return true;
    }

    if (indices[0] != VALUE_PC_SHARED) {
        char *p = value_string(av);
        value_ctx_failure(step->ctx, step->allocator, "Store %s: not the address of a shared variable", p);
        free(p);
        return false;
    }
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "Can't update state in assert or invariant (including acquiring locks)");
        return false;
    }
    if (step->keep_callstack) {
        char *x = indices_string(indices, size);
        strbuf_printf(&step->explain, "pop value (#+) and address (#+) and store", x);
        step->explain_args[step->explain_nargs++] = v;
        step->explain_args[step->explain_nargs++] = av;
        free(x);
    }

    if (size == 2 && !step->ctx->initial) {
        hvalue_t newvars;
        if (!value_dict_trystore(step->allocator, step->vars, indices[1], v, false, &newvars)){
            // Complain if some shared variable is first set after
            // initialization
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, step->allocator, "Store: declare a local variable %s (or set during initialization)", x);
            free(x);
            return false;
        }
        else {
            ai_add(step, indices, size, false);
        }
        step->vars = newvars;
    }
    else {
        bool is_append;
        if (!ind_trystore(step->vars, indices + 1, size - 1, v, step->allocator, &is_append, &step->vars)) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, step->allocator, "Store: bad address: %s", x);
            free(x);
            return false;
        }
        ai_add(step, indices, is_append ? size - 1 : size, false);
    }
    return true;
}

void op_Store(const void *env, struct state *state, struct step *step){
    const struct env_Store *es = env;

    assert(VALUE_TYPE(step->vars) == VALUE_DICT);

    hvalue_t v = ctx_pop(step->ctx);

    if (es == 0) {
        hvalue_t av = ctx_pop(step->ctx);
        if (!store_match(state, step, av, v)) {
            return;
        }
    }
    else {
        if (step->ctx->readonly > 0) {
            value_ctx_failure(step->ctx, step->allocator, "Can't update state in assert or invariant (including acquiring locks)");
            return;
        }
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "pop value (#+) and store into variable #@");
            step->explain_args[step->explain_nargs++] = v;
            step->explain_args[step->explain_nargs++] = es->address;
        }
        if (es->n == 2 && !step->ctx->initial) {
            hvalue_t newvars;
            if (!value_dict_trystore(step->allocator, step->vars, es->indices[1], v, false, &newvars)){
                char *x = indices_string(es->indices, es->n);
                value_ctx_failure(step->ctx, step->allocator, "Store: declare a local variable %s (or set during initialization)", x);
                free(x);
                return;
            }
            ai_add(step, es->indices, es->n, false);
            step->vars = newvars;
        }
        else {
            bool is_append;
            if (!ind_trystore(step->vars, es->indices + 1, es->n - 1, v, step->allocator, &is_append, &step->vars)) {
                char *x = indices_string(es->indices, es->n);
                value_ctx_failure(step->ctx, step->allocator, "Store: bad variable %s", x);
                free(x);
                return;
            }
            ai_add(step, es->indices, is_append ? es->n - 1 : es->n, false);
        }
    }
    step->ctx->pc++;
}

void op_StoreVar(const void *env, struct state *state, struct step *step){
    const struct env_StoreVar *es = env;
    hvalue_t v = ctx_pop(step->ctx);

    assert(VALUE_TYPE(step->ctx->vars) == VALUE_DICT);
    if (es == NULL) {
        hvalue_t av = ctx_pop(step->ctx);
        if (VALUE_TYPE(av) != VALUE_ADDRESS_PRIVATE) {
            printf("STOREVAR ===> %u %s\n", step->ctx->pc, value_string(av));
        }
        assert(VALUE_TYPE(av) == VALUE_ADDRESS_PRIVATE);
        assert(av != VALUE_ADDRESS_PRIVATE);

        unsigned int size;
        hvalue_t *indices = value_get(av, &size);
        if (indices[0] != VALUE_PC_LOCAL) {
            char *p = value_string(av);
            value_ctx_failure(step->ctx, step->allocator, "StoreVar %s: not the address of a method variable", p);
            free(p);
            return;
        }
        size /= sizeof(hvalue_t);

        if (step->keep_callstack) {
            char *x = indices_string(indices, size);
            strbuf_printf(&step->explain, "pop value (#+) and address (%s) and store locally", x);
            step->explain_args[step->explain_nargs++] = v;
            free(x);
        }

        bool result;
        if (indices[1] == this_atom) {      // TODOADDR
            assert(size > 2);
            if (!step->ctx->extended) {
                value_ctx_extend(step->ctx);
            }
            if (VALUE_TYPE(ctx_this(step->ctx)) != VALUE_DICT) {
                value_ctx_failure(step->ctx, step->allocator, "StoreVar: 'this' is not a dictionary");
                return;
            }
            bool is_append;
            result = ind_trystore(ctx_this(step->ctx), &indices[2], size - 2, v, step->allocator, &is_append, &ctx_this(step->ctx));
        }

        else {
            if (indices[1] == underscore) {
                result = step->ctx->vars;
            }
            else {
                bool is_append;
                result = ind_trystore(step->ctx->vars, indices + 1, size - 1, v, step->allocator, &is_append, &step->ctx->vars);
            }
        }
        if (!result) {
            char *x = indices_string(indices, size);
            value_ctx_failure(step->ctx, step->allocator, "StoreVar: bad address: %s", x);
            free(x);
            return;
        }
        step->ctx->pc++;
    }
    else {
        if (step->keep_callstack) {
            char *x = vt_string(es->args);
            strbuf_printf(&step->explain, "pop value (#+) and store locally in variable \"%s\"", x);
            step->explain_args[step->explain_nargs++] = v;
            free(x);
        }
        if (es->args->type == VT_NAME && es->args->u.name == this_atom) {
            if (!step->ctx->extended) {
                value_ctx_extend(step->ctx);
            }
            if (VALUE_TYPE(ctx_this(step->ctx)) != VALUE_DICT) {
                value_ctx_failure(step->ctx, step->allocator, "StoreVar: 'this' is not a dictionary");
                return;
            }
            ctx_this(step->ctx) = v;
            step->ctx->pc++;
        }
        else {
            var_match(step->ctx, es->args, step->allocator, v);
            if (!step->ctx->failed) {
                step->ctx->pc++;
            }
        }
    }
}

void op_Trap(const void *env, struct state *state, struct step *step){
    if (step->ctx->readonly > 0) {
        value_ctx_failure(step->ctx, step->allocator, "Can't trap in read-only mode");
        return;
    }

    hvalue_t closure = ctx_pop(step->ctx);
    if (VALUE_TYPE(closure) != VALUE_ADDRESS_PRIVATE) {
        char *p = value_string(closure);
        value_ctx_failure(step->ctx, step->allocator, "Trap %s: not an address", p);
        free(p);
        return;
    }

    unsigned int size;
    hvalue_t *indices = value_get(closure, &size);
    if (size != 2 * sizeof(hvalue_t)) {
        char *p = value_string(closure);
        value_ctx_failure(step->ctx, step->allocator, "Trap %s: expected method and arg", p);
        free(p);
        return;
    }
    if (VALUE_TYPE(indices[0]) != VALUE_PC) {
        char *p = value_string(closure);
        value_ctx_failure(step->ctx, step->allocator, "Trap %s: not a method", p);
        free(p);
        return;
    }
    hvalue_t trap_pc = indices[0], arg = indices[1];

    // TODO. ctx_trap_pc/ctx_trap_arg can be replaced with ctx_closure
    value_ctx_extend(step->ctx);
    ctx_trap_pc(step->ctx) = trap_pc;
    assert(VALUE_FROM_PC(trap_pc) < global.code.len);
    assert(strcmp(global.code.instrs[VALUE_FROM_PC(trap_pc)].oi->name, "Frame") == 0);
    ctx_trap_arg(step->ctx) = arg;
    step->ctx->pc++;
}

void *init_Assert(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Assert2(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_AtomicDec(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Choose(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Continue(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Dup(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Go(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Print(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Pop(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_ReadonlyDec(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_ReadonlyInc(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Save(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_SetIntLevel(struct dict *map, struct allocator *allocator){ return NULL; }
void *init_Trap(struct dict *map, struct allocator *allocator){ return NULL; }

void *init_Apply(struct dict *map, struct allocator *allocator) {
    struct json_value *jv = dict_lookup(map, "value", 5);
    assert(jv->type == JV_MAP);
    struct env_Apply *env = new_alloc(struct env_Apply);
    env->method = value_from_json(allocator, jv->u.map);
    assert(VALUE_TYPE(env->method) == VALUE_PC);
    return env;
}

void *init_Builtin(struct dict *map, struct allocator *allocator){
    struct env_Builtin *env = new_alloc(struct env_Builtin);
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    env->method = value_put_atom(allocator, value->u.atom.base, value->u.atom.len);
    return env;
}

void *init_Cut(struct dict *map, struct allocator *allocator){
    struct env_Cut *env = new_alloc(struct env_Cut);
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    int index = 0;
    env->value = var_parse(allocator, value->u.atom.base, value->u.atom.len, &index);

    struct json_value *key = dict_lookup(map, "key", 3);
    if (key != NULL) {
        assert(key->type == JV_ATOM);
        index = 0;
        env->key = var_parse(allocator, key->u.atom.base, key->u.atom.len, &index);
    }

    return env;
}

void *init_AtomicInc(struct dict *map, struct allocator *allocator){
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

void *init_Del(struct dict *map, struct allocator *allocator){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Del *env = new_alloc(struct env_Del);
    env->n = jv->u.list.nvals + 1;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    env->indices[0] = VALUE_PC_SHARED;
    for (unsigned int i = 0; i < jv->u.list.nvals; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i + 1] = value_from_json(allocator, index->u.map);
    }
    return env;
}

void *init_DelVar(struct dict *map, struct allocator *allocator){
    struct json_value *name = dict_lookup(map, "value", 5);
	if (name == NULL) {
		return NULL;
	}
	else {
		struct env_DelVar *env = new_alloc(struct env_DelVar);
		assert(name->type == JV_ATOM);
		env->name = value_put_atom(allocator, name->u.atom.base, name->u.atom.len);
		return env;
	}
}

void *init_Frame(struct dict *map, struct allocator *allocator){
    struct env_Frame *env = new_alloc(struct env_Frame);

    struct json_value *name = dict_lookup(map, "name", 4);
    assert(name->type == JV_ATOM);
    env->name = value_put_atom(allocator, name->u.atom.base, name->u.atom.len);

    struct json_value *args = dict_lookup(map, "args", 4);
    assert(args->type == JV_ATOM);
    int index = 0;
    env->args = var_parse(allocator, args->u.atom.base, args->u.atom.len, &index);

    return env;
}

void *init_Load(struct dict *map, struct allocator *allocator){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Load *env = new_alloc(struct env_Load);
    env->n = jv->u.list.nvals + 1;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    env->indices[0] = VALUE_PC_SHARED;
    for (unsigned int i = 0; i < jv->u.list.nvals; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i + 1] = value_from_json(allocator, index->u.map);
    }
    return env;
}

void *init_LoadVar(struct dict *map, struct allocator *allocator){
    struct json_value *value = dict_lookup(map, "value", 5);
    struct env_LoadVar *env = new_alloc(struct env_LoadVar);
    assert(value->type == JV_ATOM);
    env->name = value_put_atom(allocator, value->u.atom.base, value->u.atom.len);
    return env;
}

void *init_Move(struct dict *map, struct allocator *allocator){
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

void *init_Nary(struct dict *map, struct allocator *allocator){
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

    // TODO.  Hack for backward compatibility
    if (strcmp(fi->name, "countLabel") == 0) {
        has_countLabel = true;
    }

    return env;
}

void *init_Finally(struct dict *map, struct allocator *allocator){
    struct env_Finally *env = new_alloc(struct env_Finally);

    struct json_value *pc = dict_lookup(map, "pc", 2);
    assert(pc->type == JV_ATOM);
    char *copy = malloc(pc->u.atom.len + 1);
    memcpy(copy, pc->u.atom.base, pc->u.atom.len);
    copy[pc->u.atom.len] = 0;
    env->pc = atoi(copy);
    free(copy);

    return env;
}

void *init_Invariant(struct dict *map, struct allocator *allocator){
    struct env_Invariant *env = new_alloc(struct env_Invariant);

    struct json_value *pc = dict_lookup(map, "pc", 2);
    assert(pc->type == JV_ATOM);
    char *copy = malloc(pc->u.atom.len + 1);
    memcpy(copy, pc->u.atom.base, pc->u.atom.len);
    copy[pc->u.atom.len] = 0;
    env->pc = atoi(copy);
    free(copy);

    struct json_value *pre = dict_lookup(map, "pre", 3);
    assert(pre->type == JV_ATOM);
    assert(pre->u.atom.len > 0);
    env->pre = pre->u.atom.base[0] != 'F';

    return env;
}

void *init_Jump(struct dict *map, struct allocator *allocator){
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

void *init_JumpCond(struct dict *map, struct allocator *allocator){
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
    env->cond = value_from_json(allocator, cond->u.map);

    return env;
}

void *init_Push(struct dict *map, struct allocator *allocator) {
    struct json_value *jv = dict_lookup(map, "value", 5);
    assert(jv->type == JV_MAP);
    struct env_Push *env = new_alloc(struct env_Push);
    env->value = value_from_json(allocator, jv->u.map);
    return env;
}

void *init_Return(struct dict *map, struct allocator *allocator) {
    struct env_Return *env = new_alloc(struct env_Return);
    struct json_value *result = dict_lookup(map, "result", 6);
    if (result != NULL) {
        assert(result->type == JV_ATOM);
        env->result = value_put_atom(allocator, result->u.atom.base, result->u.atom.len);
    }
    struct json_value *deflt = dict_lookup(map, "default", 7);
    if (deflt != NULL) {
        assert(deflt->type == JV_MAP);
        env->deflt = value_from_json(allocator, deflt->u.map);
    }
    return env;
}

void *init_Sequential(struct dict *map, struct allocator *allocator){
    struct json_value *name = dict_lookup(map, "var", 3);
    assert(name->type == JV_ATOM);
    struct env_Sequential *env = new_alloc(struct env_Sequential);
    env->name = value_put_atom(allocator, name->u.atom.base, name->u.atom.len);
    return env;
}

void *init_Spawn(struct dict *map, struct allocator *allocator){
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

void *init_Split(struct dict *map, struct allocator *allocator){
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

void *init_Stop(struct dict *map, struct allocator *allocator){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Stop *env = new_alloc(struct env_Stop);
    env->n = jv->u.list.nvals + 1;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    env->indices[0] = VALUE_PC_SHARED;
    for (unsigned int i = 0; i < jv->u.list.nvals + 1; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i + 1] = value_from_json(allocator, index->u.map);
    }
    return env;
}

void *init_Store(struct dict *map, struct allocator *allocator){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    assert(jv->type == JV_LIST);
    struct env_Store *env = new_alloc(struct env_Store);
    env->n = jv->u.list.nvals + 1;
    env->indices = malloc(env->n * sizeof(hvalue_t));
    env->indices[0] = VALUE_PC_SHARED;
    for (unsigned int i = 0; i < jv->u.list.nvals; i++) {
        struct json_value *index = jv->u.list.vals[i];
        assert(index->type == JV_MAP);
        env->indices[i + 1] = value_from_json(allocator, index->u.map);
    }
    env->address = value_put_address(allocator, env->indices, env->n * sizeof(hvalue_t));
    return env;
}

void *init_StoreVar(struct dict *map, struct allocator *allocator){
    struct json_value *jv = dict_lookup(map, "value", 5);
    if (jv == NULL) {
        return NULL;
    }
    else {
        assert(jv->type == JV_ATOM);
        struct env_StoreVar *env = new_alloc(struct env_StoreVar);
        int index = 0;
        env->args = var_parse(allocator, jv->u.atom.base, jv->u.atom.len, &index);
        return env;
    }
}

hvalue_t f_abs(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "compute the absolute value; ");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "abs() can only be applied to integers");
    }
    int64_t r = VALUE_FROM_INT(e);
    return r >= 0 ? e : VALUE_TO_INT(-r);
}

hvalue_t f_all(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if all values are True; ");
    }
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
                return value_ctx_failure(step->ctx, step->allocator, "all() can only be applied to booleans");
            }
            if (v[i] == VALUE_FALSE) {
                return VALUE_FALSE;
            }
        }
		return VALUE_TRUE;
    }
    return value_ctx_failure(step->ctx, step->allocator, "all() can only be applied to sets or lists");
}

hvalue_t f_any(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if any value is True; ");
    }
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
                return value_ctx_failure(step->ctx, step->allocator, "any() can only be applied to booleans");
            }
            if (v[i] != VALUE_FALSE) {
                return VALUE_TRUE;
            }
        }
		return VALUE_FALSE;
    }
    return value_ctx_failure(step->ctx, step->allocator, "any() can only be applied to sets or dictionaries");
}

hvalue_t f_add_arg(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);

    if (VALUE_TYPE(args[1]) != VALUE_ADDRESS_SHARED && VALUE_TYPE(args[1]) != VALUE_ADDRESS_PRIVATE) {
        return value_ctx_failure(step->ctx, step->allocator, "AddArg: not an address");
    }

    unsigned int size;
    hvalue_t *list = value_get(args[1], &size);
    assert(size > 0);

#ifdef notdef
    if (size == sizeof(hvalue_t) && VALUE_TYPE(list[0]) == VALUE_LIST) {
        if (VALUE_TYPE(args[0]) != VALUE_INT) {
            return value_ctx_failure(step->ctx, step->allocator, "AddArg: not an integer");
        }
        unsigned int n;
        hvalue_t *tuple = value_get(list[0], &n);
        n /= sizeof(hvalue_t);
        unsigned int index = VALUE_FROM_INT(args[0]);
        if (index >= n) {
            return value_ctx_failure(step->ctx, step->allocator, "AddArg: index out of range");
        }
        return value_put_address(step->allocator, &tuple[index], sizeof(hvalue_t));
    }
#endif

#ifdef HEAP_ALLOC
    char *nl = malloc(size + sizeof(hvalue_t));
    memcpy(nl, list, size);
    * (hvalue_t *) &nl[size] = args[0];
    hvalue_t result = value_put_address(step->allocator, nl, size + sizeof(hvalue_t));
    free(nl);
    return result;
#else
    char nl[size + sizeof(hvalue_t)];
    memcpy(nl, list, size);
    * (hvalue_t *) &nl[size] = args[0];
    return value_put_address(step->allocator, nl, size + sizeof(hvalue_t));
#endif
}

hvalue_t f_closure(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    if (n == 1) {
        return value_put_address(step->allocator, &args[0], sizeof(hvalue_t));
    }
    assert(n == 2);
    hvalue_t list[2];
    list[0] = args[1];
    list[1] = args[0];
    return value_put_address(step->allocator, list, sizeof(list));
}

// C is not good at integer divide with negative values.  This code
// tries to fix that...
static int64_t int_div(int64_t x, int64_t y) {
    int64_t q = x / y;
    int64_t r = x % y;
    if (r != 0 && (r < 0) != (y < 0)) {
        q--;
    }
    return q;
}

// C is not good at integer divide with negative values.  This code
// tries to fix that...
static int64_t int_mod(int64_t x, int64_t y) {
    int64_t r = x % y;
    if (r != 0 && (r < 0) != (y < 0)) {
        r += y;
    }
    return r;
}

hvalue_t f_div(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    int64_t e1 = args[0], e2 = args[1];
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "integer divide; ");
    }
    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "right argument to / not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "left argument to / not an integer");
    }
    e1 = VALUE_FROM_INT(e1);
    if (e1 == 0) {
        return value_ctx_failure(step->ctx, step->allocator, "divide by zero");
    }
    int64_t result = int_div(VALUE_FROM_INT(e2), e1);
    return VALUE_TO_INT(result);
}

hvalue_t f_eq(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if both values are the same; ");
    }
    return VALUE_TO_BOOL(args[0] == args[1]);
}

hvalue_t f_ge(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if second value is less than the first; ");
    }
    if (VALUE_TYPE(args[0]) != VALUE_TYPE(args[1])) {
        value_ctx_failure(step->ctx, step->allocator, "can only compare values of same type");
        return 0;
    }
    if (VALUE_TYPE(args[0]) == VALUE_SET) {
        if (args[0] == args[1]) {
            return VALUE_TRUE;
        }
        return VALUE_TO_BOOL(value_subset(args[0], args[1]));
    }
    else {
        int cmp = value_order(step->ctx, step->allocator, args[1], args[0]);
        return VALUE_TO_BOOL(cmp >= 0);
    }
}

hvalue_t f_get_ident(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "get thread identifier; ");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "get_ident() can only be applied to ()");
    }
    if (step->ctx->initial) {
        return VALUE_TO_INT(0);
    }
    if (step->ctx->id == 0) {
        return value_ctx_failure(step->ctx, step->allocator, "get_ident() not implemented currently");
    }
    return VALUE_TO_INT(step->ctx->id);
}

hvalue_t f_gt(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if second value is less than the first; ");
    }
    if (VALUE_TYPE(args[0]) != VALUE_TYPE(args[1])) {
        value_ctx_failure(step->ctx, step->allocator, "can only compare values of same type");
        return 0;
    }
    if (VALUE_TYPE(args[0]) == VALUE_SET) {
        if (args[0] == args[1]) {
            return VALUE_FALSE;
        }
        return VALUE_TO_BOOL(value_subset(args[0], args[1]));
    }
    else {
        int cmp = value_order(step->ctx, step->allocator, args[1], args[0]);
        return VALUE_TO_BOOL(cmp > 0);
    }
}

hvalue_t f_ne(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if the values are unequal; ");
    }
    return VALUE_TO_BOOL(args[0] != args[1]);
}

hvalue_t f_in(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    hvalue_t s = args[0], e = args[1];
	if (!step->keep_callstack &&
            (s == VALUE_SET || s == VALUE_DICT || s == VALUE_LIST)) {
		return VALUE_FALSE;
	}
    if (VALUE_TYPE(s) == VALUE_ATOM) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "check if the second value is a substring of the first; ");
        }
        if (VALUE_TYPE(e) != VALUE_ATOM) {
            return value_ctx_failure(step->ctx, step->allocator, "'in <string>' can only be applied to another string");
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
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "check if the second value is a member of the first; ");
        }
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
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "check if the second value is a key in the first; ");
        }
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
    return value_ctx_failure(step->ctx, step->allocator, "'in' can only be applied to sets or dictionaries");
}

hvalue_t f_intersection(
    struct state *state,
    struct step *step,
    hvalue_t *args,
    unsigned int n
) {
    assert(n > 1);
    hvalue_t e1 = args[0];

    if (VALUE_TYPE(e1) == VALUE_INT) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "bitwise and; ");
        }
        for (unsigned int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(step->ctx, step->allocator, "'&' applied to mix of ints and other types");
            }
            e1 &= e2;
        }
        return e1;
    }
	// if (!step->keep_callstack && e1 == VALUE_SET) {
    // 		return VALUE_SET;
	// }
    if (VALUE_TYPE(e1) == VALUE_SET) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "intersect the sets; ");
        }
        // get all the sets
#ifdef HEAP_ALLOC
        struct val_info *vi = malloc(n * sizeof(struct val_info));
#else
        struct val_info vi[n];
#endif
		vi[0].vals = value_get(args[0], &vi[0].size); 
		vi[0].index = 0;
        unsigned int min_size = vi[0].size;     // minimum set size
        for (unsigned int i = 1; i < n; i++) {
            if (VALUE_TYPE(args[i]) != VALUE_SET) {
                return value_ctx_failure(step->ctx, step->allocator, "'&' applied to mix of sets and other types");
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
            }
        }

        // If any is an empty list, we're done.
        if (min_size == 0) {
#ifdef HEAP_ALLOC
            free(vi);
#endif
            return VALUE_SET;
        }

        // Allocate sufficient memory.
#ifdef HEAP_ALLOC
        hvalue_t *vals = malloc(min_size);
#else
        hvalue_t vals[min_size / sizeof(hvalue_t)];
#endif
        hvalue_t *v = vals;

        hvalue_t cur = vi[0].vals[0];
        unsigned int ring = 1;
        for (unsigned int i = 1;; i = (i + 1) % n) {
            ring++;

            if (vi[i].index == vi[i].size / sizeof(hvalue_t)) {
                break;
            }

            // Find a match with the current value
            int cmp = value_cmp(vi[i].vals[vi[i].index], cur);
            while (cmp < 0) {
                if (++vi[i].index == vi[i].size / sizeof(hvalue_t)) {
                    break;
                }
                cmp = value_cmp(vi[i].vals[vi[i].index], cur);
            }
            if (vi[i].index == vi[i].size / sizeof(hvalue_t)) {
                break;
            }

            // If the value is bigger, start a new ring
            if (cmp > 0) {
                cur = vi[i].vals[vi[i].index++];
                ring = 1;
            }

            // Same value
            else {
                vi[i].index++;

                // If we have gone all the way around, it's a match
                if (ring == n) {
                    *v++ = cur;
                    if (vi[i].index == vi[i].size / sizeof(hvalue_t)) {
                        break;
                    }
                    cur = vi[i].vals[vi[i].index++];
                    ring = 1;
                }

                // Keep going to see if we have a match
                else {
                    ring++;
                }
            }
        }

        hvalue_t result = value_put_set(step->allocator, vals, (unsigned int) ((char *) v - (char *) vals));
#ifdef HEAP_ALLOC
        free(vals);
        free(vi);
#endif
        return result;
    }

	// if (!step->keep_callstack && e1 == VALUE_DICT) {
	// 	return VALUE_DICT;
	// }
    if (VALUE_TYPE(e1) != VALUE_DICT) {
        return value_ctx_failure(step->ctx, step->allocator, "'&' can only be applied to ints and dicts");
    }
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "dictionary intersection; ");
    }
    // get all the dictionaries
#ifdef HEAP_ALLOC
    struct val_info *vi = malloc(n * sizeof(struct val_info));
#else
    struct val_info vi[n];
#endif
    unsigned int total = 0;
    for (unsigned int i = 0; i < n; i++) {
        if (VALUE_TYPE(args[i]) != VALUE_DICT) {
#ifdef HEAP_ALLOC
            free(vi);
#endif
            return value_ctx_failure(step->ctx, step->allocator, "'&' applied to mix of dictionaries and other types");
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
#ifdef HEAP_ALLOC
        free(vi);
#endif
        return VALUE_DICT;
    }

    // Concatenate the dictionaries
#ifdef HEAP_ALLOC
    hvalue_t *vals = malloc(total);
#else
    hvalue_t vals[total / sizeof(hvalue_t)];
#endif
    total = 0;
    for (unsigned int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // sort lexicographically, leaving duplicate keys
    unsigned int cnt = total / (2 * sizeof(hvalue_t));
    qsort(vals, cnt, 2 * sizeof(hvalue_t), q_kv_cmp);

    // now only leave the min value for duplicate keys
    unsigned int in = 0, out = 0;
    for (;;) {
        // if there are fewer than n copies of the key, then it's out
        if (in + n > cnt) {
            break;
        }
        unsigned int i;
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

    hvalue_t result = value_put_dict(step->allocator, vals, 2 * out * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(vals);
    free(vi);
#endif
    return result;
}

hvalue_t f_invert(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "one's complement (flip the bits); ");
    }
    int64_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "~ can only be applied to ints");
    }
    e = VALUE_FROM_INT(e);
    return VALUE_TO_INT(~e);
}

hvalue_t f_keys(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "extract the keys; ");
    }
    hvalue_t v = args[0];
    if (VALUE_TYPE(v) == VALUE_DICT) {
        if (v == VALUE_DICT) {
            return VALUE_SET;
        }

        unsigned int size;
        hvalue_t *vals = value_get(v, &size);
#ifdef HEAP_ALLOC
        hvalue_t *keys = malloc(size / 2);
#else
        hvalue_t keys[size / 2 / sizeof(hvalue_t)];
#endif
        size /= 2 * sizeof(hvalue_t);
        for (unsigned int i = 0; i < size; i++) {
            keys[i] = vals[2*i];
        }
        hvalue_t result = value_put_set(step->allocator, keys, size * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
        free(keys);
#endif
        return result;
    }
    if (VALUE_TYPE(v) == VALUE_LIST || VALUE_TYPE(v) == VALUE_ATOM) {
        if (v == VALUE_DICT || v == VALUE_ATOM) {
            return VALUE_SET;
        }

        unsigned int size;
        (void) value_get(v, &size);
        if (VALUE_TYPE(v) == VALUE_LIST) {
            size /= sizeof(hvalue_t);
        }
#ifdef HEAP_ALLOC
        hvalue_t *keys = malloc(size);
#else
        hvalue_t keys[size];
#endif
        for (unsigned int i = 0; i < size; i++) {
            keys[i] = VALUE_TO_INT(i);
        }
        hvalue_t result = value_put_set(step->allocator, keys, size * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
        free(keys);
#endif
        return result;
    }

    return value_ctx_failure(step->ctx, step->allocator, "keys() can only be applied to dictionaries");
}

hvalue_t f_int(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "parse a int; ");
    }
    hvalue_t e = args[0];
    unsigned int base = 10;
    if (VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int asize;
        hvalue_t *av = value_get(e, &asize);
        if (asize != 2 * sizeof(hvalue_t)) {
            return value_ctx_failure(step->ctx, step->allocator, "int() must have 1 or 2 arguments");
        }
        if (VALUE_TYPE(av[1]) != VALUE_INT) {
            return value_ctx_failure(step->ctx, step->allocator, "int(): second argument must be an integer");
        }
        base = (unsigned int) VALUE_FROM_INT(av[1]);
        if (base < 2 || base > 36) {
            return value_ctx_failure(step->ctx, step->allocator, "int(): unsupported base");
        }
        e = av[0];
    }

    if (VALUE_TYPE(e) != VALUE_ATOM) {
        return value_ctx_failure(step->ctx, step->allocator, "int() can only be applied to strings");
    }
    unsigned int size;
    char *v = value_get(e, &size);
    unsigned int i = 0;

    // Skip blank space
    while (i < size && (v[i] == ' ' || v[i] == '\t' || v[i] == '\n' || v[i] == '\r')) {
        i++;
    }

    // Figure out the base
    if (size - i > 2 && v[i] == '0') {
        switch (v[i+1]) {
        case 'x': case 'X': base = 16; break;
        case 'b': case 'B': base =  2; break;
        case 'o': case 'O': base =  8; break;
        default:
            return value_ctx_failure(step->ctx, step->allocator, "int(): unknown base");
        }
        i += 2;
    }

    if (i == size) {
        return value_ctx_failure(step->ctx, step->allocator, "int() cannot be applied to empty strings");
    }

    unsigned int result = 0;
    while (i < size) {
        unsigned int next;
        if ('0' <= v[i] && v[i] <= '9') {
            next = v[i] - '0';
        }
        else if ('a' <= v[i] && v[i] <= 'z') {
            next = v[i] - 'a' + 10;
        }
        else if ('A' <= v[i] && v[i] <= 'Z') {
            next = v[i] - 'A' + 10;
        }
        else {
            // Trailing blanks are ok.
            while (i < size && (v[i] == ' ' || v[i] == '\t' || v[i] == '\n' || v[i] == '\r')) {
                i++;
            }
            if (i == size) {
                return VALUE_TO_INT(result);
            }
            return value_ctx_failure(step->ctx, step->allocator, "int(): not an integer");
        }
        if (next >= base) {
            return value_ctx_failure(step->ctx, step->allocator, "int(): digit exceeds base");
        }
        result *= base;
        result += next;
        i++;
    }
    return VALUE_TO_INT(result);
}

hvalue_t f_set(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "create a set; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_LIST || e == VALUE_ATOM || e == VALUE_DICT) {
        return VALUE_SET;
    }
    if (VALUE_TYPE(e) == VALUE_SET) {
        return e;
    }
    if (VALUE_TYPE(e) != VALUE_LIST && VALUE_TYPE(e) != VALUE_ATOM && VALUE_TYPE(e) != VALUE_DICT) {
        return value_ctx_failure(step->ctx, step->allocator, "set() can only be applied to lists or strings");
    }
    if (VALUE_TYPE(e) == VALUE_DICT) {
        return f_keys(state, step, args, n);
    }
    if (VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        if (size == sizeof(hvalue_t)) {
            // TODO.  Can make this more efficient
            return value_put_set(step->allocator, v, size);
        }
        unsigned int cnt = size / sizeof(hvalue_t);
#ifdef HEAP_ALLOC
        hvalue_t *w = malloc(size);
#else
        hvalue_t w[cnt];
#endif
        memcpy(w, v, size);
        cnt = sort(w, cnt);
        hvalue_t result = value_put_set(step->allocator, w, cnt * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
        free(w);
#endif
        return result;
    }
    else {
        assert(VALUE_TYPE(e) == VALUE_ATOM);
        unsigned int size;
        char *v = value_get(e, &size);
#ifdef HEAP_ALLOC
        hvalue_t *w = malloc(size * sizeof(hvalue_t));
#else
        hvalue_t w[size];
#endif
        for (unsigned i = 0; i < size; i++) {
            w[i] = value_put_atom(step->allocator, &v[i], 1);
        }
        size = sort(w, size);
        hvalue_t result = value_put_set(step->allocator, w, size * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
        free(w);
#endif
        return result;
    }
}

hvalue_t f_zip(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "zip; ");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "zip() requires a list/tuple argument");
    }
    if (e == VALUE_LIST) {
        return VALUE_LIST;
    }
    unsigned int size;
    hvalue_t *v = value_get(e, &size);
    unsigned int cnt = size / sizeof(hvalue_t);

    // Get all the lists or sets
#ifdef HEAP_ALLOC
    struct val_info *vi = malloc(cnt * sizeof(struct val_info));
#else
    struct val_info vi[cnt];
#endif
    unsigned int min = (unsigned int ) -1;
    for (unsigned int i = 0; i < cnt; i++) {
        if (VALUE_TYPE(v[i]) != VALUE_LIST && VALUE_TYPE(v[i]) != VALUE_SET) {
#ifdef HEAP_ALLOC
            free(vi);
#endif
            return value_ctx_failure(step->ctx, step->allocator, "zip() can only operate on lists and sets");
        }
        vi[i].vals = value_get(v[i], &vi[i].size);
        vi[i].size /= sizeof(hvalue_t);
        if (vi[i].size < min) {
            min = vi[i].size;
        }
    }

#ifdef HEAP_ALLOC
    hvalue_t *vec = malloc(cnt * sizeof(*vec));
    hvalue_t *w = malloc(min * sizeof(*w));
#else
    hvalue_t vec[cnt];
    hvalue_t w[min];
#endif
    for (unsigned i = 0; i < min; i++) {
        for (unsigned j = 0; j < cnt; j++) {
            vec[j] = vi[j].vals[i];
        }
        w[i] = value_put_list(step->allocator, vec, cnt * sizeof(*vec));
    }
    hvalue_t result = value_put_list(step->allocator, w, min * sizeof(*w));

#ifdef HEAP_ALLOC
    free(vi);
    free(w);
    free(vec);
#endif

    return result;
}

hvalue_t f_dict(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "create a dictionary; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_LIST) {
        return VALUE_DICT;
    }
    if (VALUE_TYPE(e) != VALUE_SET && VALUE_TYPE(e) != VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "dict() can only be applied to sets or lists");
    }
    unsigned int size;
    hvalue_t *v = value_get(e, &size);
    unsigned int cnt = size / sizeof(hvalue_t);

#ifdef HEAP_ALLOC
    hvalue_t *dict = malloc(size * 2);
#else
    hvalue_t dict[cnt * 2];
#endif
    unsigned int total = 0;

    for (unsigned int i = 0; i < cnt; i++) {
        if (VALUE_TYPE(v[i]) != VALUE_LIST) {
            return value_ctx_failure(step->ctx, step->allocator, "dict() can only be applied to sets or lists");
        }
        unsigned int psize;
        hvalue_t *pair = value_get(v[i], &psize);
        if (psize != 2 * sizeof(hvalue_t)) {
            return value_ctx_failure(step->ctx, step->allocator, "dict() can only be applied to sets or lists of pairs");
        }

        // Look for the key
        int cmp = 1;
        unsigned int j = 0;
        for (; j < total; j += 2) {
            cmp = value_cmp(pair[0], dict[j]);
            if (cmp <= 0) {
                break;
            }
        }

        if (cmp != 0) {
            memmove(&dict[j+2], &dict[j], total - j);
            dict[j] = pair[0];
            total += 2;
        }
        dict[j+1] = pair[1];
    }

    hvalue_t result = value_put_dict(step->allocator, dict, total * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(dict);
#endif
    return result;
}

hvalue_t f_list(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "create a list; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_LIST || e == VALUE_ATOM || e == VALUE_DICT) {
        return VALUE_LIST;
    }
    if (VALUE_TYPE(e) == VALUE_LIST) {
        return e;
    }
    if (VALUE_TYPE(e) != VALUE_SET && VALUE_TYPE(e) != VALUE_ATOM && VALUE_TYPE(e) != VALUE_DICT) {
        return value_ctx_failure(step->ctx, step->allocator, "list() can only be applied to sets or strings");
    }

    if (VALUE_TYPE(e) == VALUE_SET) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        return value_put_list(step->allocator, v, size);
    }
    if (VALUE_TYPE(e) == VALUE_DICT) {
        unsigned int size;
        hvalue_t *vals = value_get(e, &size);
#ifdef HEAP_ALLOC
        hvalue_t *keys = malloc(size / 2);
#else
        hvalue_t keys[size / 2 / sizeof(hvalue_t)];
#endif
        size /= 2 * sizeof(hvalue_t);
        for (unsigned int i = 0; i < size; i++) {
            keys[i] = vals[2*i];
        }
        hvalue_t result = value_put_list(step->allocator, keys, size * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
        free(keys);
#endif
        return result;
    }

    assert(VALUE_TYPE(e) == VALUE_ATOM);
    unsigned int size;
    char *v = value_get(e, &size);
#ifdef HEAP_ALLOC
    hvalue_t *w = malloc(size * sizeof(hvalue_t));
#else
    hvalue_t w[size];
#endif
    for (unsigned i = 0; i < size; i++) {
        w[i] = value_put_atom(step->allocator, &v[i], 1);
    }
    hvalue_t result = value_put_list(step->allocator, w, size * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(w);
#endif
    return result;
}

hvalue_t f_reversed(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "reverse elements in list; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_LIST) {
        return VALUE_LIST;
    }
    if (VALUE_TYPE(e) != VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "reversed() can only be applied to lists");
    }
    unsigned int size;
    hvalue_t *v = value_get(e, &size);
    if (size == sizeof(hvalue_t)) {
        return e;
    }
    unsigned int cnt = size / sizeof(hvalue_t);
#ifdef HEAP_ALLOC
    hvalue_t *w = malloc(size);
#else
    hvalue_t w[cnt];
#endif
    for (unsigned int i = 0; i < cnt; i++) {
        w[i] = v[cnt - i - 1];
    }
    hvalue_t result = value_put_list(step->allocator, w, size);
#ifdef HEAP_ALLOC
    free(w);
#endif
    return result;
}

hvalue_t f_sorted(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "sort; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_LIST) {
        return VALUE_LIST;
    }
    if (VALUE_TYPE(e) == VALUE_SET) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        // TODO.  Can make this more efficient
        return value_put_list(step->allocator, v, size);
    }
    if (VALUE_TYPE(e) != VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "sorted() can only be applied to sets or lists");
    }
    unsigned int size;
    hvalue_t *v = value_get(e, &size);
    if (size == sizeof(hvalue_t)) {
        return e;
    }
    unsigned int cnt = size / sizeof(hvalue_t);
#ifdef HEAP_ALLOC
    hvalue_t *w = malloc(size);
#else
    hvalue_t w[cnt];
#endif
    memcpy(w, v, size);
    qsort(w, cnt, sizeof(hvalue_t), q_value_cmp);
    hvalue_t result = value_put_list(step->allocator, w, cnt * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(w);
#endif
    return result;
}

hvalue_t f_hex(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "convert into a hexadecimal string; ");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "hex() can only be applied to integers");
    }
    long int r = VALUE_FROM_INT(e);
    char buf[100], *p = buf;
    if (r < 0) {
        *p++ = '-';
        r = -r;
    }
    sprintf(buf, "0x%lx", r);
    return value_put_atom(step->allocator, buf, strlen(buf));
}

hvalue_t f_oct(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "convert into an octal string; ");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "oct() can only be applied to integers");
    }
    long int r = VALUE_FROM_INT(e);
    char buf[100], *p = buf;
    if (r < 0) {
        *p++ = '-';
        r = -r;
    }
    sprintf(buf, "0o%lo", r);
    return value_put_atom(step->allocator, buf, strlen(buf));
}

hvalue_t f_bin(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "convert into a binary string; ");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "bin() can only be applied to integers");
    }
    char buf[100], *p = &buf[sizeof(buf) - 1];
    *p = 0;
    long int r = VALUE_FROM_INT(e);
    unsigned int u = r < 0 ? -r : r;
    if (u == 0) {
        *--p = '0';
    }
    else {
        do {
            *--p = "01"[u & 1];
            u >>= 1;
        } while (u != 0);
    }
    *--p = 'b';
    *--p = '0';
    if (r < 0) {
        *--p = '-';
    }

    hvalue_t v = value_put_atom(step->allocator, p, strlen(p));
    return v;
}

hvalue_t f_str(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "convert into a string; ");
    }
    hvalue_t e = args[0];
    char *s = value_string(e);
    hvalue_t v = value_put_atom(step->allocator, s, strlen(s));
    free(s);
    return v;
}

hvalue_t f_len(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    hvalue_t e = args[0];
	if (step->keep_callstack &&
            (e == VALUE_SET || e == VALUE_DICT || e == VALUE_LIST || e == VALUE_ATOM)) {
		return VALUE_INT;
	}
    if (VALUE_TYPE(e) == VALUE_SET) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "compute cardinality; ");
        }
        unsigned int size;
        (void) value_get(e, &size);
        size /= sizeof(hvalue_t);
        return VALUE_TO_INT(size);
    }
    if (VALUE_TYPE(e) == VALUE_LIST) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "compute the length of the list; ");
        }
        unsigned int size;
        (void) value_get(e, &size);
        size /= sizeof(hvalue_t);
        return VALUE_TO_INT(size);
    }
    if (VALUE_TYPE(e) == VALUE_DICT) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "compute the number of entries; ");
        }
        unsigned int size;
        (void) value_get(e, &size);
        size /= 2 * sizeof(hvalue_t);
        return VALUE_TO_INT(size);
    }
    if (VALUE_TYPE(e) == VALUE_ATOM) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "compute the length of the string; ");
        }
        unsigned int size;
        (void) value_get(e, &size);
        return VALUE_TO_INT(size);
    }
    return value_ctx_failure(step->ctx, step->allocator, "len() can only be applied to sets, dictionaries, lists, or strings");
}

hvalue_t f_type(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "determine the type; ");
    }
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
    case VALUE_ADDRESS_SHARED:
    case VALUE_ADDRESS_PRIVATE:
        return type_address;
    case VALUE_CONTEXT:
        return type_context;
    default:
        assert(false);
    }
    return value_ctx_failure(step->ctx, step->allocator, "unknown type???");
}

hvalue_t f_le(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if second value is less than the first; ");
    }
    if (VALUE_TYPE(args[0]) != VALUE_TYPE(args[1])) {
        value_ctx_failure(step->ctx, step->allocator, "can only compare values of same type");
        return 0;
    }
    if (VALUE_TYPE(args[0]) == VALUE_SET) {
        if (args[0] == args[1]) {
            return VALUE_TRUE;
        }
        return VALUE_TO_BOOL(value_subset(args[1], args[0]));
    }
    else {
        int cmp = value_order(step->ctx, step->allocator, args[1], args[0]);
        return VALUE_TO_BOOL(cmp <= 0);
    }
}

hvalue_t f_lt(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "check if second value is less than the first; ");
    }
    if (VALUE_TYPE(args[0]) != VALUE_TYPE(args[1])) {
        value_ctx_failure(step->ctx, step->allocator, "can only compare values of same type");
        return 0;
    }
    if (VALUE_TYPE(args[0]) == VALUE_SET) {
        if (args[0] == args[1]) {
            return VALUE_FALSE;
        }
        return VALUE_TO_BOOL(value_subset(args[1], args[0]));
    }
    else {
        int cmp = value_order(step->ctx, step->allocator, args[1], args[0]);
        return VALUE_TO_BOOL(cmp < 0);
    }
}

hvalue_t f_max(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "compute the maximum of the values; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_SET) {
        return value_ctx_failure(step->ctx, step->allocator, "can't apply max() to empty set");
    }
    if (e == VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "can't apply max() to empty list");
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
    return value_ctx_failure(step->ctx, step->allocator, "max() can only be applied to sets or lists");
}

hvalue_t f_min(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "compute the minimum of the values; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_SET) {
        return value_ctx_failure(step->ctx, step->allocator, "can't apply min() to empty set");
    }
    if (e == VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "can't apply min() to empty list");
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
    return value_ctx_failure(step->ctx, step->allocator, "min() can only be applied to sets or lists");
}

hvalue_t f_minus(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1 || n == 2);
    if (n == 1) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "unary minus; ");
        }
        if (VALUE_TYPE(args[0]) != VALUE_INT) {
            return value_ctx_failure(step->ctx, step->allocator, "unary minus can only be applied to ints");
        }
        int64_t e = VALUE_FROM_INT(args[0]);
        if (e == VALUE_MAX) {
            return VALUE_TO_INT(VALUE_MIN);
        }
        if (e == VALUE_MIN) {
            return VALUE_TO_INT(VALUE_MAX);
        }
        if (-e <= VALUE_MIN || -e >= VALUE_MAX) {
            return value_ctx_failure(step->ctx, step->allocator, "unary minus overflow (model too large)");
        }
        return VALUE_TO_INT(-e);
    }
    else {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "the second integer minus the first; ");
        }
        if (VALUE_TYPE(args[0]) == VALUE_INT) {
            int64_t e1 = args[0], e2 = args[1];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(step->ctx, step->allocator, "minus applied to int and non-int");
            }
            e1 = VALUE_FROM_INT(e1);
            e2 = VALUE_FROM_INT(e2);
            int64_t result = e2 - e1;
            if (result <= VALUE_MIN || result >= VALUE_MAX) {
                return value_ctx_failure(step->ctx, step->allocator, "minus overflow (model too large)");
            }
            return VALUE_TO_INT(result);
        }

        hvalue_t e1 = args[0], e2 = args[1];
        if (VALUE_TYPE(e1) != VALUE_SET || VALUE_TYPE(e2) != VALUE_SET) {
            return value_ctx_failure(step->ctx, step->allocator, "minus can only be applied to ints or sets");
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
#ifdef HEAP_ALLOC
        hvalue_t *vals = malloc(size2);
#else
        hvalue_t vals[size2 / sizeof(hvalue_t)];
#endif
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
        hvalue_t result = value_put_set(step->allocator, vals, (char *) q - (char *) vals);
#ifdef HEAP_ALLOC
        free(vals);
#endif
        return result;
    }
}

hvalue_t f_mod(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    int64_t e1 = args[0], e2 = args[1];
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "second value modulo the first; ");
    }
    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "right argument to mod not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "left argument to mod not an integer");
    }
    int64_t mod = VALUE_FROM_INT(e1);
    int64_t result = int_mod(VALUE_FROM_INT(e2), mod);
    return VALUE_TO_INT(result);
}

hvalue_t f_not(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "logical not; ");
    }
    hvalue_t e = args[0];
    if (VALUE_TYPE(e) != VALUE_BOOL) {
        return value_ctx_failure(step->ctx, step->allocator, "not can only be applied to booleans");
    }
    return e ^ (1 << VALUE_BITS);
}

hvalue_t f_plus(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    int64_t e1 = args[0];
    if (VALUE_TYPE(e1) == VALUE_INT) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "add the integers; ");
        }
        e1 = VALUE_FROM_INT(e1);
        for (unsigned int i = 1; i < n; i++) {
            int64_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(step->ctx, step->allocator,
                    "+: applied to mix of integers and other types");
            }
            e2 = VALUE_FROM_INT(e2);
            int64_t sum = e1 + e2;
            if (sum <= VALUE_MIN || sum >= VALUE_MAX) {
                return value_ctx_failure(step->ctx, step->allocator,
                    "+: integer overflow (model too large)");
            }
            e1 = sum;
        }
        return VALUE_TO_INT(e1);
    }

    if (VALUE_TYPE(e1) == VALUE_ATOM) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "concatenate the strings; ");
        }
        struct strbuf sb;
        strbuf_init(&sb);
        for (int i = n; --i >= 0;) {
            if (VALUE_TYPE(args[i]) != VALUE_ATOM) {
                return value_ctx_failure(step->ctx, step->allocator,
                    "+: applied to mix of strings and other types");
            }
            unsigned int size;
            char *chars = value_get(args[i], &size);
            strbuf_append(&sb, chars, size);
        }
        char *result = strbuf_convert(&sb);
        hvalue_t v = value_put_atom(step->allocator, result, strbuf_getlen(&sb));
        return v;
    }

    if (VALUE_TYPE(e1) == VALUE_LIST) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "concatenate the lists; ");
        }
        // get all the lists
#ifdef HEAP_ALLOC
        struct val_info *vi = malloc(n * sizeof(struct val_info));
#else
        struct val_info vi[n];
#endif
        int total = 0;
        for (unsigned int i = 0; i < n; i++) {
            if (VALUE_TYPE(args[i]) != VALUE_LIST) {
#ifdef HEAP_ALLOC
                free(vi);
#endif
                value_ctx_failure(step->ctx, step->allocator, "+: applied to mix of value types");
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
#ifdef HEAP_ALLOC
            free(vi);
#endif
            return VALUE_LIST;
        }

        // Concatenate the lists
#ifdef HEAP_ALLOC
        hvalue_t *vals = malloc(total);
#else
        hvalue_t vals[total / sizeof(hvalue_t)];
#endif
        total = 0;
        for (int i = n; --i >= 0;) {
            memcpy((char *) vals + total, vi[i].vals, vi[i].size);
            total += vi[i].size;
        }

        hvalue_t result = value_put_list(step->allocator, vals, total);
#ifdef HEAP_ALLOC
        free(vals);
        free(vi);
#endif
        return result;
    }

    value_ctx_failure(step->ctx, step->allocator, "+: can only apply to ints, strings, or lists");
    return 0;
}

hvalue_t f_power(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "exponentiation; ");
    }
    int64_t e1 = args[0], e2 = args[1];

    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "right argument to ** not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "left argument to ** not an integer");
    }
    int64_t base = VALUE_FROM_INT(e2);
    int64_t exp = VALUE_FROM_INT(e1);
    if (exp == 0) {
        return VALUE_TO_INT(1);
    }
    if (exp < 0) {
        return value_ctx_failure(step->ctx, step->allocator, "**: negative exponent");
    }

    bool neg = base < 0;
    if (neg) {
        base = -base;
        if ((exp % 2) == 0) {
            neg = false;
        }
    }
    uint64_t result = 1, orig = base;
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
        return value_ctx_failure(step->ctx, step->allocator, "**: overflow (model too large)");
    }

    return neg ? VALUE_TO_INT(-result) : VALUE_TO_INT(result);
}

hvalue_t f_range(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "range of integers; ");
    }
    int64_t e1 = args[0], e2 = args[1];
    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "right argument to .. not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "left argument to .. not an integer");
    }
    int64_t start = VALUE_FROM_INT(e2);
    int64_t finish = VALUE_FROM_INT(e1);
	if (finish < start) {
		return VALUE_SET;
	}
    int cnt = (finish - start) + 1;
	assert(cnt > 0);
	assert(cnt < 1000);		// seems unlikely...
#ifdef HEAP_ALLOC
    hvalue_t *v = malloc(cnt * sizeof(hvalue_t));
#else
    hvalue_t v[cnt];
#endif
    for (int i = 0; i < cnt; i++) {
        v[i] = VALUE_TO_INT(start + i);
    }
    hvalue_t result = value_put_set(step->allocator, v, cnt * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(v);
#endif
    return result;
}

hvalue_t f_list_add(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "insert first value into the second; ");
    }
    hvalue_t list = args[1];
    if (VALUE_TYPE(list) != VALUE_LIST) {
        return value_ctx_failure(step->ctx, step->allocator, "can only add to list");
    }
    unsigned int size;
    char *vals = value_get(list, &size);
#ifdef HEAP_ALLOC
    char *nvals = malloc(size + sizeof(hvalue_t));
#else
    char nvals[size + sizeof(hvalue_t)];
#endif
    memcpy(nvals, vals, size);
    * (hvalue_t *) (nvals + size) = args[0];
    hvalue_t result = value_put_list(step->allocator, nvals, size + sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(nvals);
#endif
    return result;
}

hvalue_t f_dict_add(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 3);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "add key/value pair to dictionary; ");
    }
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
#ifdef HEAP_ALLOC
        hvalue_t *nvals = malloc(size);
#else
        hvalue_t nvals[size / sizeof(hvalue_t)];
#endif
        memcpy(nvals, vals, size);
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) = value;

        hvalue_t result = value_put_dict(step->allocator, nvals, size);
#ifdef HEAP_ALLOC
        free(nvals);
#endif
        return result;
    }
    else {
#ifdef HEAP_ALLOC
        hvalue_t *nvals = malloc(size + 2 * sizeof(hvalue_t));
#else
        hvalue_t nvals[size / sizeof(hvalue_t) + 2];
#endif
        memcpy(nvals, vals, i);
        * (hvalue_t *) ((char *) nvals + i) = key;
        * (hvalue_t *) ((char *) nvals + (i + sizeof(hvalue_t))) = value;
        memcpy((char *) nvals + i + 2*sizeof(hvalue_t), v, size - i);

        hvalue_t result = value_put_dict(step->allocator, nvals, size + 2*sizeof(hvalue_t));
#ifdef HEAP_ALLOC
        free(nvals);
#endif
        return result;
    }
}

hvalue_t f_set_add(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "insert first value into the second; ");
    }
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

#ifdef HEAP_ALLOC
    hvalue_t *nvals = malloc(size + sizeof(hvalue_t));
#else
    hvalue_t nvals[size / sizeof(hvalue_t) + 1];
#endif
    memcpy(nvals, vals, i);
    * (hvalue_t *) ((char *) nvals + i) = elt;
    memcpy((char *) nvals + i + sizeof(hvalue_t), v, size - i);

    hvalue_t result = value_put_set(step->allocator, nvals, size + sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(nvals);
#endif
    return result;
}

hvalue_t f_shiftleft(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "shift second value left by the number of bits given by the first value; ");
    }
    int64_t e1 = args[0], e2 = args[1];

    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "right argument to << not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "left argument to << not an integer");
    }
    e1 = VALUE_FROM_INT(e1);
    if (e1 < 0) {
        return value_ctx_failure(step->ctx, step->allocator, "<<: negative shift count");
    }
    e2 = VALUE_FROM_INT(e2);
    int64_t result = e2 << e1;
    if (((result << VALUE_BITS) >> VALUE_BITS) != result) {
        return value_ctx_failure(step->ctx, step->allocator, "<<: overflow (model too large)");
    }
    if (result <= VALUE_MIN || result >= VALUE_MAX) {
        return value_ctx_failure(step->ctx, step->allocator, "<<: overflow (model too large)");
    }
    return VALUE_TO_INT(result);
}

hvalue_t f_shiftright(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 2);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "shift second value right by the number of bits given by the first value; ");
    }
    int64_t e1 = args[0], e2 = args[1];

    if (VALUE_TYPE(e1) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "right argument to >> not an integer");
    }
    if (VALUE_TYPE(e2) != VALUE_INT) {
        return value_ctx_failure(step->ctx, step->allocator, "left argument to >> not an integer");
    }
    if (e1 < 0) {
        return value_ctx_failure(step->ctx, step->allocator, ">>: negative shift count");
    }
    e1 = VALUE_FROM_INT(e1);
    e2 = VALUE_FROM_INT(e2);
    return VALUE_TO_INT(e2 >> e1);
}

hvalue_t f_sum(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    assert(n == 1);
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "compute sum; ");
    }
    hvalue_t e = args[0];
	if (e == VALUE_SET || e == VALUE_LIST) {
		return VALUE_TO_INT(0);
    }
    if (VALUE_TYPE(e) == VALUE_SET || VALUE_TYPE(e) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *v = value_get(e, &size);
        size /= sizeof(hvalue_t);
        unsigned int sum = 0;
        for (unsigned int i = 0; i < size; i++) {
            if (VALUE_TYPE(v[i]) != VALUE_INT) {
                return value_ctx_failure(step->ctx, step->allocator, "sum() can only add integers");
            }
            sum += VALUE_FROM_INT(v[i]);
        }
		return VALUE_TO_INT(sum);
    }
    return value_ctx_failure(step->ctx, step->allocator, "sum() can only be applied to sets or lists");
}

hvalue_t f_times(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    int64_t result = 1;
    int list = -1;
    for (unsigned int i = 0; i < n; i++) {
        int64_t e = args[i];
        if (VALUE_TYPE(e) == VALUE_ATOM || VALUE_TYPE(e) == VALUE_LIST) {
            if (step->keep_callstack) {
                strbuf_printf(&step->explain, "create multiple copies of list; ");
            }
            if (list >= 0) {
                return value_ctx_failure(step->ctx, step->allocator, "* can only have at most one list or string");
            }
            list = i;
        }
        else {
            if (VALUE_TYPE(e) != VALUE_INT) {
                return value_ctx_failure(step->ctx, step->allocator,
                    "* can only be applied to integers and at most one list or string");
            }
            e = VALUE_FROM_INT(e);
            if (e == 0) {
                result = 0;
            }
            else if (result != 0 && e != 1) {
                int64_t product = result * e;
                if (product / result != e) {
                    return value_ctx_failure(step->ctx, step->allocator, "*: overflow (model too large)");
                }
                result = product;
            }
        }
    }
    if (result != (result << VALUE_BITS) >> VALUE_BITS) {
        return value_ctx_failure(step->ctx, step->allocator, "*: overflow (model too large)");
    }
    if (list < 0) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "multiply; ");
        }
        return VALUE_TO_INT(result);
    }
    if (result == 0) {
        // empty list or empty string
        return VALUE_TYPE(args[list]);
    }
    if (result < 0) {
        return value_ctx_failure(step->ctx, step->allocator, "*: negative multiplier");
    }
    if (VALUE_TYPE(args[list]) == VALUE_LIST) {
        unsigned int size;
        hvalue_t *vals = value_get(args[list], &size);
        if (size == 0) {
            return VALUE_DICT;
        }
        unsigned int n = size / sizeof(hvalue_t);
#ifdef HEAP_ALLOC
        hvalue_t *r = malloc(result * size);
#else
        hvalue_t r[result * size / sizeof(hvalue_t)];
#endif
        for (unsigned int i = 0; i < result; i++) {
            memcpy(&r[i * n], vals, size);
        }
        hvalue_t v = value_put_list(step->allocator, r, result * size);
#ifdef HEAP_ALLOC
        free(r);
#endif
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
	hvalue_t v = value_put_atom(step->allocator, s, result * size);
	free(s);
	return v;
}

hvalue_t f_union(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    hvalue_t e1 = args[0];

    if (VALUE_TYPE(e1) == VALUE_INT) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "bitwise or; ");
        }
        for (unsigned int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(step->ctx, step->allocator, "'|' applied to mix of ints and other types");
            }
            e1 |= e2;
        }
        return e1;
    }

    if (VALUE_TYPE(e1) == VALUE_SET) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "union; ");
        }
        // get all the sets
#ifdef HEAP_ALLOC
        struct val_info *vi = malloc(n * sizeof(struct val_info));;
#else
        struct val_info vi[n];
#endif
        int total = 0;
        for (unsigned int i = 0; i < n; i++) {
            if (VALUE_TYPE(args[i]) != VALUE_SET) {
#ifdef HEAP_ALLOC
                free(vi);
#endif
                return value_ctx_failure(step->ctx, step->allocator, "'|' applied to mix of sets and other types");
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
#ifdef HEAP_ALLOC
            free(vi);
#endif
            return VALUE_SET;
        }

        // Concatenate the sets
#ifdef HEAP_ALLOC
        hvalue_t *vals = malloc(total);
#else
        hvalue_t vals[total / sizeof(hvalue_t)];
#endif
        total = 0;
        for (unsigned int i = 0; i < n; i++) {
            memcpy((char *) vals + total, vi[i].vals, vi[i].size);
            total += vi[i].size;
        }

        n = sort(vals, total / sizeof(hvalue_t));
        hvalue_t result = value_put_set(step->allocator, vals, n * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
        free(vals);
        free(vi);
#endif
        return result;
    }

    if (VALUE_TYPE(e1) != VALUE_DICT) {
        return value_ctx_failure(step->ctx, step->allocator, "'|' can only be applied to ints, sets, and dicts");
    }
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "dictionary union; ");
    }
    // get all the dictionaries
#ifdef HEAP_ALLOC
    struct val_info *vi = malloc(n * sizeof(struct val_info));
#else
    struct val_info vi[n];
#endif
    int total = 0;
    for (unsigned int i = 0; i < n; i++) {
        if (VALUE_TYPE(args[i]) != VALUE_DICT) {
#ifdef HEAP_ALLOC
            free(vi);
#endif
            return value_ctx_failure(step->ctx, step->allocator, "'|' applied to mix of dictionaries and other types");
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
#ifdef HEAP_ALLOC
        free(vi);
#endif
        return VALUE_DICT;
    }

    // Concatenate the dictionaries
#ifdef HEAP_ALLOC
    hvalue_t *vals = malloc(total);
#else
    hvalue_t vals[total / sizeof(hvalue_t)];
#endif
    total = 0;
    for (unsigned int i = 0; i < n; i++) {
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

    hvalue_t result = value_put_dict(step->allocator, vals, 2 * n * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(vals);
    free(vi);
#endif
    return result;
}

hvalue_t f_xor(struct state *state, struct step *step, hvalue_t *args, unsigned int n){
    hvalue_t e1 = args[0];

    if (VALUE_TYPE(e1) == VALUE_INT) {
        if (step->keep_callstack) {
            strbuf_printf(&step->explain, "bitwise exclusive or; ");
        }
        for (unsigned int i = 1; i < n; i++) {
            hvalue_t e2 = args[i];
            if (VALUE_TYPE(e2) != VALUE_INT) {
                return value_ctx_failure(step->ctx, step->allocator, "'^' applied to mix of ints and other types");
            }
            e1 ^= e2;
        }
        return e1 | VALUE_INT;
    }

    // get all the sets
    if (step->keep_callstack) {
        strbuf_printf(&step->explain, "excluded values: compute the values that are in an odd number of sets; ");
    }
#ifdef HEAP_ALLOC
    struct val_info *vi = malloc(n * sizeof(struct val_info));
#else
    struct val_info vi[n];
#endif
    int total = 0;
    for (unsigned int i = 0; i < n; i++) {
        if (VALUE_TYPE(args[i]) != VALUE_SET) {
#ifdef HEAP_ALLOC
            free(vi);
#endif
            return value_ctx_failure(step->ctx, step->allocator, "'^' applied to mix of value types");
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
#ifdef HEAP_ALLOC
        free(vi);
#endif
        return VALUE_SET;
    }

    // Concatenate the sets
#ifdef HEAP_ALLOC
    hvalue_t *vals = malloc(total);
#else
    hvalue_t vals[total / sizeof(hvalue_t)];
#endif
    total = 0;
    for (unsigned int i = 0; i < n; i++) {
        memcpy((char *) vals + total, vi[i].vals, vi[i].size);
        total += vi[i].size;
    }

    // sort the values, retaining duplicates
    int cnt = total / sizeof(hvalue_t);
    qsort(vals, cnt, sizeof(hvalue_t), q_value_cmp);

    // Now remove the step->allocator that have an even number
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

    hvalue_t result = value_put_set(step->allocator, vals, k * sizeof(hvalue_t));
#ifdef HEAP_ALLOC
    free(vals);
    free(vi);
#endif
    return result;
}

struct op_info op_table[] = {
	{ "Apply", init_Apply, op_Apply, NULL },
	{ "Assert", init_Assert, op_Assert, NULL },
	{ "Assert2", init_Assert2, op_Assert2, NULL },
	{ "AtomicDec", init_AtomicDec, op_AtomicDec, NULL },
	{ "AtomicInc", init_AtomicInc, op_AtomicInc, NULL },
	{ "Builtin", init_Builtin, op_Builtin, NULL },
	{ "Choose", init_Choose, op_Choose, next_Choose },
	{ "Continue", init_Continue, op_Continue, NULL },
	{ "Cut", init_Cut, op_Cut, NULL },
	{ "Del", init_Del, op_Del, NULL },
	{ "DelVar", init_DelVar, op_DelVar, NULL },
	{ "Dup", init_Dup, op_Dup, NULL },
	{ "Finally", init_Finally, op_Finally, NULL },
	{ "Frame", init_Frame, op_Frame, next_Frame },
	{ "Go", init_Go, op_Go, NULL },
	{ "Invariant", init_Invariant, op_Invariant, NULL },
	{ "Jump", init_Jump, op_Jump, NULL },
	{ "JumpCond", init_JumpCond, op_JumpCond, NULL },
	{ "Load", init_Load, op_Load, next_Load },
	{ "LoadVar", init_LoadVar, op_LoadVar, NULL },
	{ "Move", init_Move, op_Move, NULL },
	{ "Nary", init_Nary, op_Nary, NULL },
	{ "Pop", init_Pop, op_Pop, NULL },
	{ "Print", init_Print, op_Print, next_Print },
	{ "Push", init_Push, op_Push, NULL },
	{ "ReadonlyDec", init_ReadonlyDec, op_ReadonlyDec, NULL },
	{ "ReadonlyInc", init_ReadonlyInc, op_ReadonlyInc, NULL },
	{ "Return", init_Return, op_Return, NULL },
	{ "Save", init_Save, op_Save, NULL },
	{ "Sequential", init_Sequential, op_Sequential, NULL },
	{ "SetIntLevel", init_SetIntLevel, op_SetIntLevel, NULL },
	{ "Spawn", init_Spawn, op_Spawn, NULL },
	{ "Split", init_Split, op_Split, NULL },
	{ "Stop", init_Stop, op_Stop, NULL },
	{ "Store", init_Store, op_Store, next_Store },
	{ "StoreVar", init_StoreVar, op_StoreVar, NULL },
	{ "Trap", init_Trap, op_Trap, NULL },

    // Built-in methods
    { "alloc$malloc", NULL, op_Alloc_Malloc, NULL },
    { "bag$add", NULL, op_Bag_Add, NULL },
    { "bag$bmax", NULL, op_Bag_Bmax, NULL },
    { "bag$bmin", NULL, op_Bag_Bmin, NULL },
    { "bag$multiplicity", NULL, op_Bag_Multiplicity, NULL },
    { "bag$remove", NULL, op_Bag_Remove, NULL },
    { "bag$size", NULL, op_Bag_Size, NULL },
    { "list$tail", NULL, op_List_Tail, NULL },

    { "bogus$iq_new", NULL, op_Bogus_iq_new, NULL },
    { "bogus$iq_enqueue", NULL, op_Bogus_iq_enqueue, NULL },
    { "bogus$iq_dequeue", NULL, op_Bogus_iq_dequeue, NULL },

#ifdef BIRDS
    { "bogus$olb_new", NULL, op_Bogus_olb_new, NULL },
    { "bogus$olb_wb_acquire", NULL, op_Bogus_olb_wb_acquire, NULL },
    { "bogus$olb_wb_release", NULL, op_Bogus_olb_wb_release, NULL },
    { "bogus$olb_eb_acquire", NULL, op_Bogus_olb_eb_acquire, NULL },
    { "bogus$olb_eb_release", NULL, op_Bogus_olb_eb_release, NULL },
#endif

    { NULL, NULL, NULL, NULL }
};

struct f_info f_table[] = {
    { "==", f_eq },
    { "!=", f_ne },
    { "<", f_lt },
    { "<=", f_le },
    { ">=", f_ge },
    { ">", f_gt },
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
    { "|", f_union },
    { "&", f_intersection },
    { "^", f_xor },
    { "..", f_range },
    { "AddArg", f_add_arg },
    { "Closure", f_closure },
    { "DictAdd", f_dict_add },
    { "ListAdd", f_list_add },
    { "SetAdd", f_set_add },
    { "abs", f_abs },
    { "all", f_all },
    { "any", f_any },
    { "bin", f_bin },
    { "dict", f_dict },
    { "get_ident", f_get_ident },
    { "hex", f_hex },
    { "in", f_in },
    { "int", f_int },
    { "keys", f_keys },
    { "len", f_len },
    { "list", f_list },
    { "max", f_max },
    { "min", f_min },
	{ "mod", f_mod },
    { "not", f_not },
    { "oct", f_oct },
    { "reversed", f_reversed },
    { "set", f_set },
    { "sorted", f_sorted },
    { "str", f_str },
    { "sum", f_sum },
    { "type", f_type },
    { "zip", f_zip },
    { NULL, NULL }
};

struct op_info *ops_get(char *opname, int size){
    return dict_lookup(ops_map, opname, size);
}

// Initialize the tables that map instruction names (op_X) or Nary function
// names (f_Y).  Also initialize a bunch of handy Harmony value constants.
void ops_init(struct allocator *allocator) {
    ops_map = dict_new("ops", sizeof(struct op_info *), 0, 0, false, false);
    f_map = dict_new("functions", sizeof(struct f_info *), 0, 0, false, false);
	underscore = value_put_atom(allocator, "_", 1);
	this_atom = value_put_atom(allocator, "this", 4);
    type_bool = value_put_atom(allocator, "bool", 4);
    type_int = value_put_atom(allocator, "int", 3);
    type_str = value_put_atom(allocator, "str", 3);
    type_pc = value_put_atom(allocator, "pc", 2);
    type_list = value_put_atom(allocator, "list", 4);
    type_dict = value_put_atom(allocator, "dict", 4);
    type_set = value_put_atom(allocator, "set", 3);
    type_address = value_put_atom(allocator, "address", 7);
    type_context = value_put_atom(allocator, "context", 7);
	alloc_pool_atom = value_put_atom(allocator, "alloc$pool", 10);
	alloc_next_atom = value_put_atom(allocator, "alloc$next", 10);
    mutex_init(&direct_mutex);

    for (struct op_info *oi = op_table; oi->name != NULL; oi++) {
        struct op_info **p = dict_insert(ops_map, NULL, oi->name, strlen(oi->name), NULL);
        *p = oi;
    }
    for (struct f_info *fi = f_table; fi->name != NULL; fi++) {
        struct f_info **p = dict_insert(f_map, NULL, fi->name, strlen(fi->name), NULL);
        *p = fi;
    }
}
