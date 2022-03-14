#ifndef FILTER_H
#define FILTER_H

#include "json.h"

// TODO
struct condition_t {
    int pc;
};

struct filter_t {
    struct condition_t* conditions;
    int len;
};

struct filter_t create_filter(struct json_value* val);

#endif
