#ifndef SRC_CALM_ENGINE_H
#define SRC_CALM_ENGINE_H

#include "json.h"
//#include "graph.h"
#include "conallocator.h"
#include "conhashtab.h"


typedef uint64_t Fixsize_v;

struct Varsize_v {
    uint64_t h;
    // byte buf[0];
};

//Constants and macros needed for value types

struct Context {
    struct Varsize_v *vars;
    uint16_t pc;
    uint8_t flags, readonly, atomic, sp;
    //struct Fixsize_v stack[sp];
};

struct State {
    struct Varsize_v *vars;
    //...
    uint32_t bagsize;
    //struct Fixsize_v context[bagsize];
    //uint8_t multiplicity[bagsize]
};

struct Node {
    //...
    struct State s;
};

struct Engine {

};

void engine_init(struct Engine *engine, struct json_value *jc, struct Conhashtab *value, struct Conhashtab *state, struct Conallocator *al);

struct Node* engine_create_initial_node(struct Engine *engine, struct Conallocator *al);
struct Node* engine_compute(struct Engine *engine, struct Conallocator *al, struct State *s, unsigned cid);

#endif //SRC_CALM_ENGINE_H