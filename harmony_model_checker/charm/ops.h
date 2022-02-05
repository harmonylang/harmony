#ifndef SRC_OPS_H
#define SRC_OPS_H

#include <inttypes.h>

#include "charm.h"
#include "value.h"
#include "global.h"

void ops_init(struct global_t* global);
struct op_info *ops_get(char *opname, int size);

struct step {
    struct context *ctx;
    struct access_info *ai;
    hvalue_t *log;
    int nlog;
    struct dfa_trie *dfa_trie;
};

struct op_info {
    const char *name;
    void *(*init)(struct dict *, struct values_t *values);
    void (*op)(const void *env, struct state *state, struct step *step, struct global_t *global);
};

struct env_Cut {
    hvalue_t set;
    struct var_tree *key, *value;
};

struct env_Del {
    hvalue_t *indices;
    int n;
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

struct env_IncVar {
    hvalue_t name;
};

struct env_Invariant {
    int end;
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
    int n;
};

struct env_LoadVar {
    hvalue_t name;
};

struct env_Move {
    int offset;
};

struct env_Nary {
    int arity;
    struct f_info *fi;
};

struct env_Push {
    hvalue_t value;
};

struct env_Spawn {
    bool eternal;
};

struct env_Split {
    int count;
};

struct env_Stop {
    hvalue_t *indices;
    int n;
};

struct env_Store {
    hvalue_t *indices;
    int n;
};

struct env_StoreVar {
    struct var_tree *args;
};

void interrupt_invoke(struct step *step);

#endif //SRC_OPS_H
