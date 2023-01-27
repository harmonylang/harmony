#include <stdio.h>

#include "engine.h"

void engine_init(struct Engine *engine, struct json_value *jc, struct Conhashtab *value, struct Conhashtab *states, struct Conallocator *al) {
    //TODO
}

struct Node* engine_create_initial_node(struct Engine *engine, struct Conallocator *al) {
    //TODO
}

struct Node* engine_compute(struct Engine *engine, struct Conallocator *al, struct State *s, unsigned cid) {
    //DANGER: everything alloca + force inline now
    //TODO
}