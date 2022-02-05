#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#ifndef HARMONY_COMBINE
#include "code.h"
#include "hashdict.h"
#include "ops.h"
#endif

static struct instr_t code_instr_parse(struct values_t *values, struct json_value *jv) {
    assert(jv->type == JV_MAP);
    struct json_value *op = dict_lookup(jv->u.map, "op", 2);
    assert(op->type == JV_ATOM);
    struct op_info *oi = ops_get(op->u.atom.base, op->u.atom.len);
    if (oi == NULL) {
        fprintf(stderr, "Unknown HVM instruction: %.*s\n", op->u.atom.len, op->u.atom.base);
        exit(1);
    }
    struct instr_t i;
    i.oi = oi;
    i.env = (*oi->init)(jv->u.map, values);
    i.choose = strcmp(oi->name, "Choose") == 0;
    i.load = strcmp(oi->name, "Load") == 0;
    i.store = strcmp(oi->name, "Store") == 0;
    i.del = strcmp(oi->name, "Del") == 0;
    i.print = strcmp(oi->name, "Print") == 0;
    i.retop = strcmp(oi->name, "Return") == 0;
    i.breakable = i.load || i.store || i.del || i.print;
    if (strcmp(oi->name, "AtomicInc") == 0) {
        const struct env_AtomicInc *ea = i.env;
        if (!ea->lazy) {
            i.breakable = true;
        }
    }
    return i;
}

struct code_t code_init_parse(struct values_t *values, struct json_value *json_code) {
    assert(json_code->type == JV_LIST);

    struct code_t code;
    code.len = json_code->u.list.nvals;
    code.instrs = malloc(code.len * sizeof(struct instr_t));

    for (unsigned int i = 0; i < json_code->u.list.nvals; i++) {
        code.instrs[i] = code_instr_parse(values, json_code->u.list.vals[i]);
    }

    code.code_map = dict_new(0);

    return code;
}
