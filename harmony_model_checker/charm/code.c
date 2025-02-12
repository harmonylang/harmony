#include "head.h"

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#ifndef HARMONY_COMBINE
#include "value.h"
#include "code.h"
#include "hashdict.h"
#include "ops.h"
#endif

static struct instr code_instr_parse(struct allocator *allocator, struct json_value *jv) {
    assert(jv->type == JV_MAP);
    struct json_value *op = dict_lookup(jv->u.map, "op", 2);
    assert(op->type == JV_ATOM);
    struct op_info *oi = ops_get(op->u.atom.base, op->u.atom.len);
    if (oi == NULL) {
        fprintf(stderr, "Unknown HVM instruction: %.*s\n", op->u.atom.len, op->u.atom.base);
        exit(1);
    }
    struct instr i;
    memset(&i, 0, sizeof(i));
    i.oi = oi;
    i.env = (*oi->init)(jv->u.map, allocator);
    i.frame = strcmp(oi->name, "Frame") == 0;
    i.choose = strcmp(oi->name, "Choose") == 0;
    i.load = strcmp(oi->name, "Load") == 0;
    i.store = strcmp(oi->name, "Store") == 0;
    i.del = strcmp(oi->name, "Del") == 0;
    i.print = strcmp(oi->name, "Print") == 0;
    i.retop = strcmp(oi->name, "Return") == 0;
    i.atomicinc = strcmp(oi->name, "AtomicInc") == 0;
    i.atomicdec = strcmp(oi->name, "AtomicDec") == 0;
    i.setintlevel = strcmp(oi->name, "SetIntLevel") == 0;
    i.breakable = i.load || i.store || i.del || i.print;
    if (strcmp(oi->name, "AtomicInc") == 0) {
        const struct env_AtomicInc *ea = i.env;
        if (ea->lazy) {
            i.is_assert = true;
        }
        else {
            i.breakable = true;
        }
    }
    return i;
}

struct code code_init_parse(struct allocator *allocator, struct json_value *json_code) {
    assert(json_code->type == JV_LIST);

    struct code code;
    code.len = json_code->u.list.nvals;
    code.instrs = malloc(code.len * sizeof(struct instr));

    for (unsigned int i = 0; i < json_code->u.list.nvals; i++) {
        code.instrs[i] = code_instr_parse(allocator, json_code->u.list.vals[i]);
    }

    code.code_map = dict_new("code", sizeof(char *), 0, 0, false, false);

    return code;
}
