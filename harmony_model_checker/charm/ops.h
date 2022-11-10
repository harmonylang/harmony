#ifndef SRC_OPS_H
#define SRC_OPS_H

#include <inttypes.h>

#include "charm.h"
#include "value.h"
#include "global.h"

#define MAX_PRINT       64

void ops_init(struct global *global, struct engine *engine);
struct op_info *ops_get(char *opname, int size);

struct step {
    struct engine engine;
    struct context *ctx;
    struct access_info *ai;
    struct dfa_trie *dfa_trie;
    bool keep_callstack;
    struct strbuf explain;
    struct callstack *callstack;
    unsigned int nlog;
    hvalue_t log[MAX_PRINT];
};

struct op_info {
    const char *name;
    void *(*init)(struct dict *, struct engine *engine);
    void (*op)(const void *env, struct state *state, struct step *step, struct global *global);
    void (*next)(const void *env, struct context *ctx, struct global *global, FILE *fp);
};

struct env_Builtin {
    hvalue_t method;
};

struct env_Cut {
    struct var_tree *key, *value;
};

struct env_Del {
    hvalue_t *indices;
    unsigned int n;
};

struct env_DelVar {
    hvalue_t name;
};

struct env_Frame {
    hvalue_t name;
    struct var_tree *args;
};

struct env_AtomicInc {
    bool lazy;
};

struct env_Invariant {
    int end;
    bool pre;
};

struct env_Jump {
    int pc;
};

struct env_JumpCond {
    hvalue_t cond;
    int pc;
};

struct env_Load {
    hvalue_t *indices;
    unsigned int n;
};

struct env_LoadVar {
    hvalue_t name;
};

struct env_Move {
    int offset;
};

struct env_Nary {
    unsigned int arity;
    struct f_info *fi;
};

struct env_Push {
    hvalue_t value;
};

struct env_Spawn {
    bool eternal;
};

struct env_Split {
    unsigned int count;
};

struct env_Stop {
    hvalue_t *indices;
    unsigned int n;
};

struct env_Store {
    hvalue_t *indices;
    unsigned int n;
};

struct env_StoreVar {
    struct var_tree *args;
};

void interrupt_invoke(struct step *step);

#endif //SRC_OPS_H
