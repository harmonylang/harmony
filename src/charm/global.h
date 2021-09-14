#include <stdint.h>
#include <stdbool.h>

#ifndef HARMONY_COMBINE
#include "hashdict.h"
#include "json.h"
#include "minheap.h"
#include "code.h"
#include "value.h"
#endif

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

#define CALLTYPE_PROCESS       1
#define CALLTYPE_NORMAL        2
#define CALLTYPE_INTERRUPT     3

void *mcopy(void *p, unsigned int size);
char *scopy(char *s);
void mfree(void *p);

unsigned long to_ulong(const char *p, int len);

void ops_init(struct values_t *values);
struct op_info *ops_get(char *opname, int size);

struct state {
    uint64_t vars;        // shared variables
    uint64_t seqs;        // sequential variables
    uint64_t choosing;    // context that is choosing if non-zero
    uint64_t ctxbag;      // bag of running contexts
    uint64_t stopbag;     // bag of stopped contexts
    uint64_t termbag;     // bag of terminated contexts
    uint64_t invariants;  // set of invariants that must hold
};

struct global_t {
    struct code_t code;
    struct values_t values;
};

struct op_info {
    const char *name;
    void *(*init)(struct dict *, struct values_t *values);
    void (*op)(const void *env, struct state *state, struct context **pctx, struct global_t *global);
};

uint64_t dict_store(struct values_t *values, uint64_t dict, uint64_t key, uint64_t value);
uint64_t dict_load(uint64_t dict, uint64_t key);
bool dict_tryload(uint64_t dict, uint64_t key, uint64_t *result);
uint64_t dict_remove(struct values_t *values, uint64_t dict, uint64_t key);
uint64_t bag_add(struct values_t *values, uint64_t bag, uint64_t v);
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

struct env_Possibly {
    int index;
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

uint64_t ctx_failure(struct context *ctx, struct values_t *values, char *fmt, ...);
void panic(char *s);
void ext_Del(const void *env, struct state *state, struct context **pctx, struct global_t *global,
                                                        struct access_info *ai);
void ext_Load(const void *env, struct state *state, struct context **pctx, struct global_t *global,
                                                        struct access_info *ai);
void ext_Store(const void *env, struct state *state, struct context **pctx, struct global_t *global,
                                                        struct access_info *ai);
