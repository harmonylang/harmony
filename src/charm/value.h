#ifndef SRC_VALUE_H
#define SRC_VALUE_H

#include <stdbool.h>

struct state {
    uint64_t vars;        // shared variables
    uint64_t seqs;        // sequential variables
    uint64_t choosing;    // context that is choosing if non-zero
    uint64_t ctxbag;      // bag of running contexts
    uint64_t stopbag;     // bag of stopped contexts
    uint64_t termbag;     // bag of terminated contexts
    uint64_t invariants;  // set of invariants that must hold
};

struct context {          // context value
    uint64_t name;        // name of method
    uint64_t entry;       // entry point of main method
    uint64_t arg;         // argument provided to spawn
    uint64_t this;        // thread-local state
    uint64_t vars;        // method-local variables
    uint64_t trap_pc;     // trap program counter
    uint64_t trap_arg;    // trap argument
    uint64_t failure;     // atom value describing failure, or 0 if no failure
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
    uint64_t stack[0];    // growing stack
};

struct combined {           // combination of current state and current context
    struct state state;
    struct context context;
};

struct values_t {
    struct dict *atoms;
    struct dict *dicts;
    struct dict *sets;
    struct dict *addresses;
    struct dict *contexts;
};

void value_init(struct values_t *values);
void value_set_concurrent(struct values_t *values, int concurrent);
uint64_t value_from_json(struct values_t *values, struct dict *map);
int value_cmp(uint64_t v1, uint64_t v2);
void *value_get(uint64_t v, int *size);
void *value_copy(uint64_t v, int *size);
uint64_t value_put_atom(struct values_t *values, const void *p, int size);
uint64_t value_put_set(struct values_t *values, void *p, int size);
uint64_t value_put_dict(struct values_t *values, void *p, int size);
uint64_t value_put_address(struct values_t *values, void *p, int size);
uint64_t value_put_context(struct values_t *values, struct context *ctx);
char *value_string(uint64_t v);
char *indices_string(const uint64_t *vec, int size);
char *value_json(uint64_t v);

#define VALUE_BITS      3
#define VALUE_MASK      ((uint64_t) ((1 << VALUE_BITS) - 1))

#define VALUE_BOOL      0
#define VALUE_INT       1
#define VALUE_ATOM      2
#define VALUE_PC        3
#define VALUE_DICT      4
#define VALUE_SET       5
#define VALUE_ADDRESS   6
#define VALUE_CONTEXT   7

#define VALUE_FALSE     VALUE_BOOL
#define VALUE_TRUE      ((1 << VALUE_BITS) | VALUE_BOOL)

#define VALUE_MAX   ((int64_t) ((~(uint64_t)0) >> (VALUE_BITS + 1)))
#define VALUE_MIN   ((int64_t) ((~(uint64_t)0) << (64 - (VALUE_BITS + 1))))

uint64_t value_dict_store(struct values_t *values, uint64_t dict, uint64_t key, uint64_t value);
uint64_t value_dict_load(uint64_t dict, uint64_t key);
bool value_dict_tryload(uint64_t dict, uint64_t key, uint64_t *result);
uint64_t value_dict_remove(struct values_t *values, uint64_t dict, uint64_t key);
uint64_t value_bag_add(struct values_t *values, uint64_t bag, uint64_t v, int multiplicity);
void value_ctx_push(struct context **pctx, uint64_t v);
uint64_t value_ctx_pop(struct context **pctx);
uint64_t value_ctx_failure(struct context *ctx, struct values_t *values, char *fmt, ...);
bool value_ctx_all_eternal(uint64_t ctxbag);


#endif //SRC_VALUE_H
