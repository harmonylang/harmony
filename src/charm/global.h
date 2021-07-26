#include <stdint.h>
#include <stdbool.h>

#ifndef HARMONY_COMBINE
#include "hashdict.h"
#include "json.h"
#include "minheap.h"
#endif

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

#define CALLTYPE_PROCESS       1
#define CALLTYPE_NORMAL        2
#define CALLTYPE_INTERRUPT     3

void *mcopy(void *p, unsigned int size);
char *scopy(char *s);
void mfree(void *p);

unsigned long to_ulong(const char *p, int len);

void ops_init();
struct op_info *ops_get(char *opname, int size);

struct code {
    struct op_info *oi;
    const void *env;
    bool choose, load, store, del, breakable;
};

struct context {     // context value
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

struct state {
    uint64_t vars;        // shared variables
    uint64_t seqs;        // sequential variables
    uint64_t choosing;    // context that is choosing if non-zero
    uint64_t ctxbag;      // bag of running contexts
    uint64_t stopbag;     // bag of stopped contexts
    uint64_t termbag;     // bag of terminated contexts
    uint64_t invariants;  // set of invariants that must hold
};

struct op_info {
    const char *name;
    void *(*init)(struct dict *);
    void (*op)(const void *env, struct state *state, struct context **pctx);
};

void value_init();
uint64_t value_from_json(struct dict *map);
int value_cmp(uint64_t v1, uint64_t v2);
void *value_get(uint64_t v, int *size);
void *value_copy(uint64_t v, int *size);
uint64_t value_put_atom(const void *p, int size);
uint64_t value_put_set(void *p, int size);
uint64_t value_put_dict(void *p, int size);
uint64_t value_put_address(void *p, int size);
uint64_t value_put_context(struct context *ctx);
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

uint64_t dict_store(uint64_t dict, uint64_t key, uint64_t value);
uint64_t dict_load(uint64_t dict, uint64_t key);
bool dict_tryload(uint64_t dict, uint64_t key, uint64_t *result);
uint64_t dict_remove(uint64_t dict, uint64_t key);
uint64_t bag_add(uint64_t bag, uint64_t v);
void ctx_push(struct context **pctx, uint64_t v);

struct access_info {
    struct access_info *next; // linked list maintenance
    uint64_t *indices;        // address of load/store
    int n;                    // length of address
    bool load;                // store or del if false
    int pc;                   // for debugging
    int multiplicity;         // #identical contexts
    int atomic;               // atomic counter
};

struct env_Cut {
    uint64_t set;
    struct var_tree *key, *value;
};

struct env_DelVar {
    uint64_t name;
};

struct env_Frame {
    uint64_t name;
    struct var_tree *args;
};

struct env_AtomicInc {
    bool lazy;
};

struct env_IncVar {
    uint64_t name;
};

struct env_Invariant {
    int end;
};

struct env_Jump {
    int pc;
};

struct env_JumpCond {
    uint64_t cond;
    int pc;
};

struct env_Load {
    uint64_t *indices;
    int n;
};

struct env_LoadVar {
    uint64_t name;
};

struct env_Move {
    int offset;
};

struct env_Nary {
    int arity;
    struct f_info *fi;
};

struct env_Push {
    uint64_t value;
};

struct env_Spawn {
    bool eternal;
};

struct env_Split {
    int count;
};

struct env_Stop {
    uint64_t *indices;
    int n;
};

struct env_Store {
    uint64_t *indices;
    int n;
};

struct env_StoreVar {
    struct var_tree *args;
};

uint64_t ctx_failure(struct context *ctx, char *fmt, ...);
void panic(char *s);
void ext_Del(const void *env, struct state *state, struct context **pctx,
                                                        struct access_info *ai);
void ext_Load(const void *env, struct state *state, struct context **pctx,
                                                        struct access_info *ai);
void ext_Store(const void *env, struct state *state, struct context **pctx,
                                                        struct access_info *ai);
