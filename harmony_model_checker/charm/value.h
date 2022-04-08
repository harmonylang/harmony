#ifndef SRC_VALUE_H
#define SRC_VALUE_H

#include "global.h"
#include "strbuf.h"
#include <stdbool.h>

typedef struct state {
    hvalue_t vars;        // shared variables
    hvalue_t seqs;        // sequential variables
    hvalue_t choosing;    // context that is choosing if non-zero
    hvalue_t ctxbag;      // bag of running contexts
    hvalue_t stopbag;     // bag of stopped contexts
    hvalue_t termbag;     // bag of terminated contexts
    hvalue_t invariants;  // set of invariants that must hold
    hvalue_t dfa_state;
} state;

typedef struct context {          // context value
    hvalue_t name;        // name of method
    hvalue_t entry;       // entry point of main method
    hvalue_t arg;         // argument provided to spawn
    hvalue_t this;        // thread-local state
    hvalue_t vars;        // method-local variables
    hvalue_t trap_pc;     // trap program counter
    hvalue_t trap_arg;    // trap argument
    hvalue_t failure;     // atom value describing failure, or 0 if no failure
    int pc;               // program counter
    int fp;               // frame pointer
    int readonly;         // readonly counter
    int atomic;           // atomic counter
    bool atomicFlag;      // to implement lazy atomicity
    bool interruptlevel;  // interrupt level
    bool stopped;         // context is stopped
    bool terminated;      // context has terminated
    bool eternal;         // context runs indefinitely
    int sp;               // stack size
    hvalue_t stack[0];    // growing stack
} context;

typedef struct combined {           // combination of current state and current context
    struct state state;
    struct context context;
} combined;

typedef struct values_t {
    struct dict *atoms;
    struct dict *dicts;
    struct dict *sets;
    struct dict *addresses;
    struct dict *contexts;
} values_t;

void value_init(struct values_t *values);
void value_set_concurrent(struct values_t *values, int concurrent);
hvalue_t value_from_json(struct values_t *values, struct dict *map);
int value_cmp(hvalue_t v1, hvalue_t v2);
void *value_get(hvalue_t v, int *size);
void *value_copy(hvalue_t v, int *size);
hvalue_t value_put_atom(struct values_t *values, const void *p, int size);
hvalue_t value_put_set(struct values_t *values, void *p, int size);
hvalue_t value_put_dict(struct values_t *values, void *p, int size);
hvalue_t value_put_list(struct values_t *values, void *p, int size);
hvalue_t value_put_address(struct values_t *values, void *p, int size);
hvalue_t value_put_context(struct values_t *values, struct context *ctx);
char *value_string(hvalue_t v);
char *indices_string(const hvalue_t *vec, int size);
char *value_json(hvalue_t v);

void strbuf_value_string(strbuf *sb, hvalue_t v);
void strbuf_value_json(strbuf *sb, hvalue_t v);

#define VALUE_BITS      3
#define VALUE_MASK      ((hvalue_t) ((1 << VALUE_BITS) - 1))

#define VALUE_BOOL      0
#define VALUE_INT       1
#define VALUE_ATOM      2
#define VALUE_PC        3
#define VALUE_DICT      4
#define VALUE_SET       5
#define VALUE_ADDRESS   6
#define VALUE_CONTEXT   7

#define VALUE_LIST      VALUE_ADDRESS       // HACK for introducing lists

#define VALUE_FALSE     VALUE_BOOL
#define VALUE_TRUE      ((1 << VALUE_BITS) | VALUE_BOOL)

#define VALUE_MAX   ((int64_t) ((~(hvalue_t)0) >> (VALUE_BITS + 1)))
#define VALUE_MIN   ((int64_t) ((~(hvalue_t)0) << (64 - (VALUE_BITS + 1))))

#define VALUE_TYPE(v)      ((v) & VALUE_MASK)
#define VALUE_POINTER(v)   ((void *) ((v) & ~VALUE_MASK))

#define VALUE_TO_INT(i)    (((hvalue_t) (i) << VALUE_BITS) | VALUE_INT)
#define VALUE_TO_BOOL(i)   (((hvalue_t) (i) << VALUE_BITS) | VALUE_BOOL)
#define VALUE_TO_PC(i)     (((hvalue_t) (i) << VALUE_BITS) | VALUE_PC)
#define VALUE_FROM_INT(i)  ((i) >> VALUE_BITS)
#define VALUE_FROM_BOOL(i) ((i) >> VALUE_BITS)
#define VALUE_FROM_PC(i)   ((i) >> VALUE_BITS)

hvalue_t value_dict_store(struct values_t *values, hvalue_t dict, hvalue_t key, hvalue_t value);
bool value_dict_trystore(struct values_t *values, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result);
hvalue_t value_dict_load(hvalue_t dict, hvalue_t key);
bool value_dict_tryload(struct values_t *values, hvalue_t dict, hvalue_t key, hvalue_t *result);
hvalue_t value_dict_remove(struct values_t *values, hvalue_t dict, hvalue_t key);
hvalue_t value_bag_add(struct values_t *values, hvalue_t bag, hvalue_t v, int multiplicity);
void value_ctx_push(struct context **pctx, hvalue_t v);
hvalue_t value_ctx_pop(struct context **pctx);
hvalue_t value_ctx_failure(struct context *ctx, struct values_t *values, char *fmt, ...);
bool value_ctx_all_eternal(hvalue_t ctxbag);


#endif //SRC_VALUE_H
