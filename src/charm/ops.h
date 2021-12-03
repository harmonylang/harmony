#ifndef SRC_OPS_H
#define SRC_OPS_H

#include <inttypes.h>

#ifndef HARMONY_COMBINE
#include "charm.h"
#include "value.h"
#include "global.h"
#endif

void ops_init(struct global_t* global);
struct op_info *ops_get(char *opname, int size);

struct step {
    struct context *ctx;
    struct access_info *ai;
    uint64_t *log;
    int nlog;
};

struct op_info {
    const char *name;
    void *(*init)(struct dict *, struct values_t *values);
    void (*op)(const void *env, struct state *state, struct step *step, struct global_t *global);
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

void interrupt_invoke(struct step *step);

#endif //SRC_OPS_H
