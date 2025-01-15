#ifndef SRC_VALUE_H
#define SRC_VALUE_H

#include <stdbool.h>
#include "global.h"
#include "strbuf.h"
#include "charm.h"
#include "hashdict.h"

#define MAX_CONTEXT_STACK   250        // maximum size of context stack
#define MAX_CONTEXT_BAG      32        // maximum number of distinct contexts

#define STATE_NORMAL        1
#define STATE_CHOOSE        2
#define STATE_PRINT         3

// This contains the state in a Harmony execution.
//
// TODO.  State can be reduced in size in various ways;
//  - vars can probably be reduce to just 48 bits as we know it's a dict
//  - type only needs 2 bits
//  - contexts could be represented more efficiently
//  - the entire thing could be replaced with a collision-resistant hash
typedef struct state {
    hvalue_t vars;        // shared variables
    uint32_t dfa_state;   // state of input dfa
    uint8_t type;         // NORMAL, CHOOSE, or PRINT
    uint8_t chooser;      // context that is choosing or printing, 0 otherwise

    // The state includes two variable-sized bag of contexts.  A context is
    // of type hvalue_t.  We use bits 48..55 (8 bits total) to contain the
    // multiplicity of the context.  The context bag is of size bagsize,
    // while the stopbag is of size total - bagsize.
    // TODO.  Currently the stopbag is behind the context bag, but if we want
    //        to support more than 256 contexts, maybe the other way around is better
    uint8_t bagsize;      // size of context bag
    uint8_t total;        // bagsize + size of bag of stopped contexts
    // hvalue_t contexts[VAR_SIZE];   // context/multiplicity pairs
} state;
#define state_size_nctx(n)       (sizeof(struct state) + (n) * sizeof(hvalue_t))
#define state_size(s)            state_size_nctx((s)->total)
#define state_ctxlist(s)         ((hvalue_t *) ((s) + 1))
#define STATE_M_SHIFT            48
#define STATE_MULTIPLICITY       ((hvalue_t) 0xFF << STATE_M_SHIFT)
#define state_ctx(s, i)          (state_ctxlist(s)[i] & ~STATE_MULTIPLICITY)
#define state_multiplicity(s, i) ((unsigned int) ((state_ctxlist(s)[i] & STATE_MULTIPLICITY) >> STATE_M_SHIFT))

// A context is the state of a Harmony thread.  The stack, which is part of the
// state of a thread, immediately follows this structure.
//
// TODO.  Some of this info should be kept in the ctx pointer itself.
//        In fact, the eternal bit already is.
struct context {   // context value
    hvalue_t vars;            // method-local variables
    uint16_t pc;              // program counter
    uint16_t id;              // thread identifier
    bool initial : 1;         // __init__ context
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

};
#define context_stack(c)    ((hvalue_t *) ((c) + 1))
#define ctx_size(c)     (sizeof(struct context) + (c)->sp * sizeof(hvalue_t) + ((c)->extended ? (ctx_extent*sizeof(hvalue_t)) : 0))
#define ctx_stack(c)    ((c)->extended ? &context_stack(c)[ctx_extent] : context_stack(c))

// Descriptor for external values.
struct external_descriptor {
    char *type_name;
    void (*print)(struct strbuf *sb, void *ref);
    int (*compare)(void *ref1, void *ref2);
};

// External value
struct val_external {
    struct external_descriptor *descr;
    void *ref;
};

hvalue_t value_from_json(struct allocator *allocator, struct dict *map);
int value_cmp(hvalue_t v1, hvalue_t v2);
int value_order(struct context *ctx, struct allocator *allocator, hvalue_t v1, hvalue_t v2);
bool value_subset(hvalue_t v1, hvalue_t v2);
// void *value_get(hvalue_t v, unsigned int *size);
struct val_external *value_get_external(hvalue_t v);
void *value_copy(hvalue_t v, unsigned int *size);
void *value_copy_extend(hvalue_t v, unsigned int inc, unsigned int *psize);
hvalue_t value_put_atom(struct allocator *allocator, const void *p, unsigned int size);
hvalue_t value_put_set(struct allocator *allocator, void *p, unsigned int size);
hvalue_t value_put_dict(struct allocator *allocator, void *p, unsigned int size);
hvalue_t value_put_list(struct allocator *allocator, void *p, unsigned int size);
hvalue_t value_put_address(struct allocator *allocator, void *p, unsigned int size);
hvalue_t value_put_context(struct allocator *allocator, struct context *ctx);
hvalue_t value_put_external(struct allocator *allocator, struct external_descriptor *descr, void *ref);
char *value_string(hvalue_t v);
char *indices_string(const hvalue_t *vec, int size);
char *value_json(hvalue_t v);

void strbuf_value_string(strbuf *sb, hvalue_t v);
void strbuf_value_json(strbuf *sb, hvalue_t v);

// A Harmony value is represented by a 64 bit representation.  Currently the
// low 4 bits indicate the type of the value.  We sometimes also use the top 16
// bits which are not typically used by the underlying hardware if the value
// represents a memory address.
//
// TODO.  Perhaps we should put everything in the top 16 bits.
#define VALUE_BITS      4
#define VALUE_HIBITS    ((hvalue_t) 0xFFFF << 48)
#define VALUE_LOBITS    ((hvalue_t) ((1 << VALUE_BITS) - 1))
#define VALUE_MASK      (VALUE_HIBITS | VALUE_LOBITS)

// Value types
#define VALUE_BOOL                1
#define VALUE_INT                 2
#define VALUE_ATOM                3
#define VALUE_PC                  4
#define VALUE_LIST                5
#define VALUE_DICT                6
#define VALUE_SET                 7
#define VALUE_ADDRESS_SHARED      8
#define VALUE_ADDRESS_PRIVATE     9
#define VALUE_CONTEXT            10
#define VALUE_EXTERNAL           11
#define VALUE_RACE               12

#define VALUE_CONTEXT_ETERNAL         ((hvalue_t) 1 << 56)
#define VALUE_CONTEXT_INTERRUPTABLE   ((hvalue_t) 1 << 57)

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

// Return the value represented by v.  If psize != NULL, return the size
// in bytes in *psize.  The value should be stored in the global.values
// hash table.
static inline void *value_get(hvalue_t v, unsigned int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        if (psize != NULL) {
            *psize = 0;
        }
        return NULL;
    }
    return dict_retrieve((void *) v, psize);
}

bool value_trystore(struct allocator *allocator, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, bool *is_append, hvalue_t *result);
hvalue_t value_store(struct allocator *allocator, hvalue_t root, hvalue_t key, hvalue_t value);
hvalue_t value_dict_store(struct allocator *allocator, hvalue_t dict, hvalue_t key, hvalue_t value);
bool value_dict_trystore(struct allocator *allocator, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result);
hvalue_t value_dict_load(hvalue_t dict, hvalue_t key);
bool value_tryload(struct allocator *allocator, hvalue_t dict, hvalue_t key, hvalue_t *result);
hvalue_t value_remove(struct context *ctx, struct allocator *allocator, hvalue_t root, hvalue_t key);
hvalue_t value_dict_remove(struct allocator *allocator, hvalue_t dict, hvalue_t key);
hvalue_t value_bag_add(struct allocator *allocator, hvalue_t bag, hvalue_t v, int multiplicity);
hvalue_t value_bag_remove(struct allocator *allocator, hvalue_t bag, hvalue_t v);
bool value_ctx_push(struct context *ctx, hvalue_t v);
hvalue_t value_ctx_pop(struct context *ctx);
void value_ctx_extend(struct context *ctx);
hvalue_t value_ctx_failure(struct context *ctx, struct allocator *allocator, char *fmt, ...);
bool value_state_all_eternal(struct state *state);
void context_remove(struct state *state, hvalue_t ctx);
int context_add(struct state *state, hvalue_t ctx);
int stopped_context_add(struct state *state, hvalue_t ctx);
char *json_escape_value(hvalue_t v);
void value_trace(FILE *file, struct callstack *cs, unsigned int pc, hvalue_t vars);
void print_vars(FILE *file, hvalue_t v);

#endif //SRC_VALUE_H
