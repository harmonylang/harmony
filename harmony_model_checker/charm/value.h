#ifndef SRC_VALUE_H
#define SRC_VALUE_H

#include <stdbool.h>
#include "global.h"
#include "strbuf.h"
#include "charm.h"

#define MAX_CONTEXT_STACK   1000        // maximum size of context stack
#define MAX_CONTEXT_BAG       32        // maximum number of distinct contexts

typedef struct state {
    hvalue_t vars;        // shared variables
    hvalue_t pre;         // "pre" state (same as vars in non-choosing states)
    hvalue_t choosing;    // context that is choosing if non-zero
    hvalue_t stopbag;     // bag of stopped contexts (to detect deadlock)
    uint32_t dfa_state;

    // The state includes a variable-size bag of contexts.  This is represented
    // by an array of contexts of type hvalue_t, which is followed by an array
    // of multiplicities (of type uint8_t) with the same number of elements.
    uint32_t bagsize;
    // hvalue_t contexts[VAR_SIZE];   // context/multiplicity pairs
} state;
#define state_contexts(s)   ((hvalue_t *) ((s) + 1))
#define multiplicities(s)   ((uint8_t *) &state_contexts(s)[(s)->bagsize])
#define state_size(s)       (sizeof(struct state) + (s)->bagsize * (sizeof(hvalue_t) + 1))

typedef struct context {   // context value
    hvalue_t vars;            // method-local variables
    bool initial : 1;         // __init__ context
    bool atomicFlag : 1;      // to implement lazy atomicity
    bool interruptlevel : 1;  // interrupt level
    bool stopped : 1;         // context is stopped
    bool terminated : 1;      // context has terminated
    bool failed : 1;          // context has failed
    bool eternal : 1;         // context runs indefinitely
    bool extended : 1;        // context extended with more values
    uint8_t readonly;         // readonly counter
    uint8_t atomic;           // atomic counter
    uint16_t pc;              // program counter
    uint16_t sp;              // stack size
    // hvalue_t thestack[VAR_SIZE];     // growing stack

// Context can be extended with the following additional values
#define ctx_this(c)     (context_stack(c)[0])
#define ctx_failure(c)  (context_stack(c)[1])
#define ctx_trap_pc(c)  (context_stack(c)[2])
#define ctx_trap_arg(c) (context_stack(c)[3])
#define ctx_extent      4

} context;
#define context_stack(c)    ((hvalue_t *) ((c) + 1))
#define ctx_size(c)     (sizeof(struct context) + (c)->sp * sizeof(hvalue_t) + ((c)->extended ? (ctx_extent*sizeof(hvalue_t)) : 0))
#define ctx_stack(c)    ((c)->extended ? &context_stack(c)[ctx_extent] : context_stack(c))

void value_init(struct values *values, unsigned int nworkers);
void value_set_concurrent(struct values *values);
void value_make_stable(struct values *values, unsigned int worker);
void value_set_sequential(struct values *values);
hvalue_t value_from_json(struct engine *engine, struct dict *map);
int value_cmp(hvalue_t v1, hvalue_t v2);
void *value_get(hvalue_t v, unsigned int *size);
// void *value_copy(hvalue_t v, unsigned int *size);
void *value_copy_extend(hvalue_t v, unsigned int inc, unsigned int *psize);
hvalue_t value_put_atom(struct engine *engine, const void *p, unsigned int size);
hvalue_t value_put_set(struct engine *engine, void *p, unsigned int size);
hvalue_t value_put_dict(struct engine *engine, void *p, unsigned int size);
hvalue_t value_put_list(struct engine *engine, void *p, unsigned int size);
hvalue_t value_put_address(struct engine *engine, void *p, unsigned int size);
hvalue_t value_put_context(struct engine *engine, struct context *ctx);
char *value_string(hvalue_t v);
char *indices_string(const hvalue_t *vec, int size);
char *value_json(hvalue_t v, struct global *global);

void strbuf_value_string(strbuf *sb, hvalue_t v);
void strbuf_value_json(strbuf *sb, hvalue_t v, struct global *global);

#define VALUE_BITS      4
#define VALUE_MASK      ((hvalue_t) ((1 << VALUE_BITS) - 1))

#define VALUE_BOOL      1
#define VALUE_INT       2
#define VALUE_ATOM      3
#define VALUE_PC        4
#define VALUE_LIST      5
#define VALUE_DICT      6
#define VALUE_SET       7
#define VALUE_ADDRESS_SHARED    8
#define VALUE_ADDRESS_PRIVATE   9
#define VALUE_CONTEXT  10

#define VALUE_FALSE     VALUE_BOOL
#define VALUE_TRUE      ((1 << VALUE_BITS) | VALUE_BOOL)

#define VALUE_MAX   ((int64_t) ((~(hvalue_t)0) >> (VALUE_BITS + 1)))
#define VALUE_MIN   ((int64_t) ((~(hvalue_t)0) << (64 - (VALUE_BITS + 1))))

#define VALUE_TYPE(v)      ((v) & VALUE_MASK)

#define VALUE_TO_INT(i)    (((hvalue_t) (i) << VALUE_BITS) | VALUE_INT)
#define VALUE_TO_BOOL(i)   (((hvalue_t) (i) << VALUE_BITS) | VALUE_BOOL)
#define VALUE_TO_PC(i)     (((hvalue_t) (i) << VALUE_BITS) | VALUE_PC)
#define VALUE_FROM_INT(i)  ((int64_t) (i) >> VALUE_BITS)
#define VALUE_FROM_BOOL(i) ((bool) ((i) >> VALUE_BITS))
#define VALUE_FROM_PC(i)   ((int64_t) (i) >> VALUE_BITS)

#define VALUE_PC_SHARED    VALUE_TO_PC(-1)
#define VALUE_PC_LOCAL     VALUE_TO_PC(-2)

bool value_trystore(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result);
hvalue_t value_store(struct engine *engine, hvalue_t root, hvalue_t key, hvalue_t value);
hvalue_t value_dict_store(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value);
bool value_dict_trystore(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result);
hvalue_t value_dict_load(hvalue_t dict, hvalue_t key);
bool value_tryload(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t *result);
hvalue_t value_remove(struct engine *engine, hvalue_t root, hvalue_t key);
hvalue_t value_dict_remove(struct engine *engine, hvalue_t dict, hvalue_t key);
hvalue_t value_bag_add(struct engine *engine, hvalue_t bag, hvalue_t v, int multiplicity);
hvalue_t value_bag_remove(struct engine *engine, hvalue_t bag, hvalue_t v);
bool value_ctx_push(struct context *ctx, hvalue_t v);
hvalue_t value_ctx_pop(struct context *ctx);
void value_ctx_extend(struct context *ctx);
hvalue_t value_ctx_failure(struct context *ctx, struct engine *engine, char *fmt, ...);
bool value_ctx_all_eternal(hvalue_t ctxbag);
bool value_state_all_eternal(struct state *state);
void context_remove(struct state *state, hvalue_t ctx);
bool context_add(struct state *state, hvalue_t ctx);
char *json_escape_value(hvalue_t v);
void value_trace(struct global *global, FILE *file, struct callstack *cs, unsigned int pc, hvalue_t vars, char *prefix);
void value_grow_prepare(struct values *values);
unsigned long value_allocated(struct values *values);
void print_vars(struct global *global, FILE *file, hvalue_t v);

#endif //SRC_VALUE_H
