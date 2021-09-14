#ifndef SRC_VALUE_H
#define SRC_VALUE_H

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

struct values_t {
    struct dict *atoms;
    struct dict *dicts;
    struct dict *sets;
    struct dict *addresses;
    struct dict *contexts;
};

void value_init(struct values_t *values);
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

#endif //SRC_VALUE_H
