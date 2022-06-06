#ifndef SRC_CODE_H
#define SRC_CODE_H

#include "json.h"
#include "value.h"

struct instr_t {
    struct op_info *oi;
    const void *env;
    bool choose, load, store, del, retop, print;
    bool atomicinc, atomicdec, setintlevel, breakable;
};

struct code_t {
    struct instr_t *instrs;
    unsigned int len;
    struct dict *code_map;       // maps pc to file:line
};

struct code_t code_init_parse(struct engine *engine, struct json_value *json_code);

#endif //SRC_CODE_H
