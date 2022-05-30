#ifndef SRC_VALUE_H
#define SRC_VALUE_H

#include "global.h"
#include "strbuf.h"
#include <stdbool.h>

#define MAX_CONTEXT_STACK   1000

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

typedef struct context {   // context value
    hvalue_t vars;            // method-local variables
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
    uint16_t fp;              // frame pointer
    uint16_t sp;              // stack size
    uint16_t entry;           // pc of method
    hvalue_t thestack[0];     // growing stack

// Context can be extended with the following additional values
#define ctx_this        thestack[0]
#define ctx_failure     thestack[1]
#define ctx_trap_pc     thestack[2]
#define ctx_trap_arg    thestack[3]
#define ctx_extent      4

} context;

#define ctx_stack(c)    ((c)->extended ? &(c)->thestack[ctx_extent] : (c)->thestack)

typedef struct combined {           // combination of current state and current context
    struct state state;
    struct context context;
} combined;

typedef struct values_t {
    struct dict *atoms;
    struct dict *dicts;
    struct dict *sets;
    struct dict *lists;
    struct dict *addresses;
    struct dict *contexts;
} values_t;

// For value_make_stable and value_set_sequential
struct value_stable {
    int atom;
    int dict;
    int set;
    int list;
    int address;
    int context;
};

struct engine {
    struct allocator *allocator;
    struct values_t *values;
};

void value_init(struct values_t *values, unsigned int nworkers);
void value_set_concurrent(struct values_t *values);
void value_stable_add(struct value_stable *vs, struct value_stable *vs2);
void value_make_stable(struct values_t *values,
            unsigned int worker, struct value_stable *vs);
void value_set_sequential(struct values_t *values, struct value_stable *vs);
hvalue_t value_from_json(struct engine *engine, struct dict *map);
int value_cmp(hvalue_t v1, hvalue_t v2);
void *value_get(hvalue_t v, unsigned int *size);
// void *value_copy(hvalue_t v, unsigned int *size);
void *value_copy_extend(hvalue_t v, unsigned int inc, unsigned int *psize);
hvalue_t value_put_atom(struct engine *engine, const void *p, int size);
hvalue_t value_put_set(struct engine *engine, void *p, int size);
hvalue_t value_put_dict(struct engine *engine, void *p, int size);
hvalue_t value_put_list(struct engine *engine, void *p, int size);
hvalue_t value_put_address(struct engine *engine, void *p, int size);
hvalue_t value_put_context(struct engine *engine, struct context *ctx);
char *value_string(hvalue_t v);
char *indices_string(const hvalue_t *vec, int size);
char *value_json(hvalue_t v);

void strbuf_value_string(strbuf *sb, hvalue_t v);
void strbuf_value_json(strbuf *sb, hvalue_t v);

#define VALUE_BITS      4
#define VALUE_MASK      ((hvalue_t) ((1 << VALUE_BITS) - 1))

#define VALUE_BOOL      1
#define VALUE_INT       2
#define VALUE_ATOM      3
#define VALUE_PC        4
#define VALUE_LIST      5
#define VALUE_DICT      6
#define VALUE_SET       7
#define VALUE_ADDRESS   8
#define VALUE_CONTEXT   9

#define VALUE_FALSE     VALUE_BOOL
#define VALUE_TRUE      ((1 << VALUE_BITS) | VALUE_BOOL)

#define VALUE_MAX   ((int64_t) ((~(hvalue_t)0) >> (VALUE_BITS + 1)))
#define VALUE_MIN   ((int64_t) ((~(hvalue_t)0) << (64 - (VALUE_BITS + 1))))

#define VALUE_TYPE(v)      ((v) & VALUE_MASK)

#define VALUE_TO_INT(i)    (((hvalue_t) (i) << VALUE_BITS) | VALUE_INT)
#define VALUE_TO_BOOL(i)   (((hvalue_t) (i) << VALUE_BITS) | VALUE_BOOL)
#define VALUE_TO_PC(i)     (((hvalue_t) (i) << VALUE_BITS) | VALUE_PC)
#define VALUE_FROM_INT(i)  ((int64_t) (i) >> VALUE_BITS)
#define VALUE_FROM_BOOL(i) ((i) >> VALUE_BITS)
#define VALUE_FROM_PC(i)   ((i) >> VALUE_BITS)

bool value_trystore(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result);
hvalue_t value_store(struct engine *engine, hvalue_t root, hvalue_t key, hvalue_t value);
hvalue_t value_dict_store(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value);
bool value_dict_trystore(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result);
hvalue_t value_dict_load(hvalue_t dict, hvalue_t key);
bool value_tryload(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t *result);
hvalue_t value_remove(struct engine *engine, hvalue_t root, hvalue_t key);
hvalue_t value_dict_remove(struct engine *engine, hvalue_t dict, hvalue_t key);
hvalue_t value_bag_add(struct engine *engine, hvalue_t bag, hvalue_t v, int multiplicity);
void value_ctx_push(struct context *ctx, hvalue_t v);
hvalue_t value_ctx_pop(struct context *ctx);
void value_ctx_extend(struct context *ctx);
hvalue_t value_ctx_failure(struct context *ctx, struct engine *engine, char *fmt, ...);
bool value_ctx_all_eternal(hvalue_t ctxbag);


#endif //SRC_VALUE_H
