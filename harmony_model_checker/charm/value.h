#ifndef SRC_VALUE_H
#define SRC_VALUE_H

#include <stdbool.h>
#include "global.h"
#include "strbuf.h"
#include "charm.h"

#define MAX_CONTEXT_STACK   250        // maximum size of context stack
#define MAX_CONTEXT_BAG       32        // maximum number of distinct contexts

// This contains the state in a Harmony execution.
//
// TODO.  State can be reduced in size in various ways;
//  - pre and stopbag are not always used
//  - contexts could be represented more efficiently
//  - the entire thing could be replaced with a collision-resistant hash
typedef struct state {
    hvalue_t vars;        // shared variables
    // hvalue_t pre;         // "pre" state (same as vars in non-choosing states)
    hvalue_t stopbag;     // bag of stopped contexts (to detect deadlock)
    uint32_t dfa_state;   // state of input dfa
    int8_t chooser;       // context that is choosing, -1 if none

    // The state includes a variable-size bag of contexts.  This is represented
    // by an array of contexts of type hvalue_t, which is followed by an array
    // of multiplicities (of type uint8_t) with the same number of elements.
    uint8_t bagsize;
    // hvalue_t contexts[VAR_SIZE];   // context/multiplicity pairs
} state;
#define state_contexts(s)   ((hvalue_t *) ((s) + 1))
#define multiplicities(s)   ((uint8_t *) &state_contexts(s)[(s)->bagsize])
#define state_size(s)       (sizeof(struct state) + (s)->bagsize * (sizeof(hvalue_t) + 1))

// A context is the state of a Harmony thread.  The state, which is part of the
// state of a thread, immediately follows this structure.
typedef struct context {   // context value
    hvalue_t vars;            // method-local variables
    uint16_t pc;              // program counter
    uint16_t id;              // thread identifier
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
    uint8_t sp;               // stack size
    // hvalue_t thestack[VAR_SIZE];     // growing stack

// Context can be extended with the following additional values
// TODO.  ctx_trap_pc/ctx_trap_arg can be combined as ctx_closure
#define ctx_this(c)     (context_stack(c)[0])
#define ctx_failure(c)  (context_stack(c)[1])
#define ctx_trap_pc(c)  (context_stack(c)[2])
#define ctx_trap_arg(c) (context_stack(c)[3])
#define ctx_extent      4

} context;
#define context_stack(c)    ((hvalue_t *) ((c) + 1))
#define ctx_size(c)     (sizeof(struct context) + (c)->sp * sizeof(hvalue_t) + ((c)->extended ? (ctx_extent*sizeof(hvalue_t)) : 0))
#define ctx_stack(c)    ((c)->extended ? &context_stack(c)[ctx_extent] : context_stack(c))

hvalue_t value_from_json(struct engine *engine, struct dict *map);
int value_cmp(hvalue_t v1, hvalue_t v2);
void *value_get(hvalue_t v, unsigned int *size);
void *value_copy(hvalue_t v, unsigned int *size);
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

// A Harmony value is represented by a 64 bit representation.  Currently the
// low 4 bits indicate the type of the value.  We sometimes also use the top 16
// bits which are not typically used by the underlying hardware if the value
// represents a memory address.
//
// TODO.  Perhaps we should put everything in the top 16 bits.
#define VALUE_BITS      4
#define VALUE_HIBITS    ((hvalue_t) 0xFF << 48)
#define VALUE_LOBITS    ((hvalue_t) ((1 << VALUE_BITS) - 1))
#define VALUE_MASK      (VALUE_HIBITS | VALUE_LOBITS)

// Value types
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

#define VALUE_CONTEXT_ETERNAL   ((hvalue_t) 1 << 48)

#define VALUE_FALSE     VALUE_BOOL
#define VALUE_TRUE      ((1 << VALUE_BITS) | VALUE_BOOL)

#define VALUE_MAX   ((int64_t) ((~(hvalue_t)0) >> (VALUE_BITS + 1)))
#define VALUE_MIN   ((int64_t) ((~(hvalue_t)0) << (64 - (VALUE_BITS + 1))))

#define VALUE_TYPE(v)      ((v) & VALUE_LOBITS)

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
int context_add(struct state *state, hvalue_t ctx);
char *json_escape_value(hvalue_t v);
void value_trace(struct global *global, FILE *file, struct callstack *cs, unsigned int pc, hvalue_t vars, char *prefix);
void print_vars(struct global *global, FILE *file, hvalue_t v);

#endif //SRC_VALUE_H
