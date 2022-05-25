#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "hashdict.h"
#include "filter.h"

struct filter_t create_filter(struct json_value* val) {
    assert(val->type == JV_LIST);

    struct filter_t filter;
    filter.len = val->u.list.nvals;
    filter.conditions = malloc(filter.len * sizeof(struct condition_t));

    for (unsigned int i = 0; i < val->u.list.nvals; i++) {
        struct condition_t cond;
        struct json_value* cond_map = val->u.list.vals[i];
        struct json_value* pc = dict_lookup(cond_map->u.map, "pc", 2);
        assert(pc->type == JV_ATOM);
        
        char *copy = malloc(pc->u.atom.len + 1);
        memcpy(copy, pc->u.atom.base, pc->u.atom.len);
        copy[pc->u.atom.len] = 0;
        cond.pc = atoi(copy);
        free(copy);

        filter.conditions[i] = cond;
    }
    return filter;
}
