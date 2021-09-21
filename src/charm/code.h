#ifndef SRC_CODE_H
#define SRC_CODE_H

#ifndef HARMONY_COMBINE
#include "json.h"
#include "value.h"
#endif

struct instr_t {
    struct op_info *oi;
    const void *env;
    bool choose, load, store, del, breakable;
};

struct code_t {
    struct instr_t *instrs;
    int len;
    struct dict *code_map;       // maps pc to file:line
};

struct code_t code_init_parse(struct values_t *values, struct json_value *json_code);

#endif //SRC_CODE_H
