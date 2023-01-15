#ifndef SRC_CODE_H
#define SRC_CODE_H

#include "json.h"
#include "value.h"

struct instr {
    struct op_info *oi;
    const void *env;
    bool choose, load, store, del, retop, print;
    bool atomicinc, atomicdec, setintlevel, breakable;
};

struct code {
    struct instr *instrs;
    unsigned int len;
    struct dict *code_map;       // maps pc to file:line
};

struct engine {
    struct allocator *allocator;
    struct dict *values;
};

struct callstack {
    struct callstack *parent;
    unsigned int pc;
    unsigned int sp;
    unsigned int return_address;
    hvalue_t arg;
    hvalue_t vars;
};

struct code code_init_parse(struct engine *engine, struct json_value *json_code);

#endif //SRC_CODE_H
