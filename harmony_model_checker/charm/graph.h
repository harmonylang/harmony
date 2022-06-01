#ifndef SRC_GRAPH_H
#define SRC_GRAPH_H

#include <stdint.h>
#include "value.h"
#include "minheap.h"
#include "thread.h"

struct component {
    bool good;              // terminating or out-going edge
    unsigned int size;      // #states
    struct node *rep;       // lowest numbered state in the component
    bool all_same;          // shared state in component is the same
    bool final;             // all states in this component are final
};

struct access_info {
    struct access_info *next;        // linked list maintenance
    hvalue_t *indices;               // address of load/store
    uint8_t n;                       // length of address
    uint8_t atomic;                  // atomic counter
    uint16_t pc;                     // for debugging
    unsigned int multiplicity : 15;  // #identical contexts
    bool load : 1;                   // store or del if false
};

struct edge {
    struct edge *fwdnext;    // forward linked list maintenance
    struct edge *bwdnext;    // backward linked list maintenance
    hvalue_t ctx, choice;    // ctx that made the microstep, choice if any
    struct node *src;        // source node
    struct node *dst;        // destination node
    hvalue_t after;          // resulting context
    struct access_info *ai;  // to detect data races
    hvalue_t *log;           // print history
    uint16_t nsteps;         // # microsteps
    uint16_t nlog : 15;      // size of print history
    bool interrupt : 1;      // set if state change is an interrupt
};

enum fail_type {
    FAIL_NONE,
    FAIL_SAFETY,
    FAIL_BEHAVIOR,
    FAIL_INVARIANT,
    FAIL_TERMINATION,
    FAIL_BUSYWAIT,
    FAIL_RACE
};

struct node {
	struct node *next;		// for linked list

    // Information about state
    struct state state;     // state corresponding to this node
    struct edge *fwd;       // forward edges
    struct edge *bwd;       // backward edges

    struct edge *to_parent; // pointer towards initial state
    uint32_t id;            // nodes are numbered starting from 0
    uint16_t len;           // length of path to initial state
    uint16_t steps;         // #microsteps from root
    bool final: 1;          // only eternal threads left (TODO: need this?)

    // TODO.  Allocate the rest after model checking, or use union?

    // NFA compression
    bool reachable : 1;

    // SCC
    bool visited : 1;       // for Kosaraju algorithm
    uint32_t component;     // strongly connected component id
};

struct failure {
    struct failure *next;   // for linked list maintenance
    enum fail_type type;    // failure type
    struct edge *edge;      // edge->dst is the faulty state
    hvalue_t address;       // in case of data race
};

struct graph_t {
    struct node **nodes;         // vector of all nodes
    unsigned int size;           // to create node identifiers
    unsigned int alloc_size;     // size allocated
};

void graph_init(struct graph_t *graph, unsigned int initial_size);

struct access_info *graph_ai_alloc(int multiplicity, int atomic, int pc);

void graph_check_for_data_race(
    struct node *node,
    struct minheap *warnings,
    struct engine *engine
);
void graph_add(struct graph_t *graph, struct node *node);
unsigned int graph_add_multiple(struct graph_t *graph, unsigned int n);
int graph_find_scc(struct graph_t *graph);

#endif //SRC_GRAPH_H
