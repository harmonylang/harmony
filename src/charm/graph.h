#ifndef SRC_GRAPH_H
#define SRC_GRAPH_H

#include <stdint.h>

#ifndef HARMONY_COMBINE
#include "value.h"
#include "minheap.h"
#endif

struct component {
    bool good;              // terminating or out-going edge
    int size;               // #states
    int representative;     // lowest numbered state in the component
};

struct access_info {
    struct access_info *next; // linked list maintenance
    uint64_t *indices;        // address of load/store
    int n;                    // length of address
    bool load;                // store or del if false
    int pc;                   // for debugging
    int multiplicity;         // #identical contexts
    int atomic;               // atomic counter
};

struct edge {
    struct edge *next;       // linked list maintenance
    uint64_t ctx, choice;    // ctx that made the microstep, choice if any
    bool interrupt;          // set if state change is an interrupt
    struct node *node;       // resulting node (state)
    uint64_t after;          // resulting context
    int weight;              // 1 if context switch; 0 otherwise
    struct access_info *ai;  // to detect data races
};

struct node {
    // Information about state
    struct state *state;    // state corresponding to this node
    int id;                 // nodes are numbered starting from 0
    struct edge *fwd;       // forward edges
    struct edge *bwd;       // backward edges

    // How to get here from parent node
    struct node *parent;    // shortest path to initial state
    int len;                // length of path to initial state
    int steps;              // #microsteps from root
    uint64_t before;        // context before state change
    uint64_t after;         // context after state change (current context)
    uint64_t choice;        // choice made if any
    bool interrupt;         // set if gotten here by interrupt

    // SCC
    bool visited;           // for Kosaraju algorithm
    unsigned int component; // strongly connected component id

    bool processed;         // for debugging currently
};

struct failure {
    enum { FAIL_SAFETY, FAIL_INVARIANT, FAIL_TERMINATION, FAIL_BUSYWAIT, FAIL_RACE } type;
    struct node *node;      // failed state
    uint64_t choice;        // choice if any
    uint64_t address;       // in case of data race
};

struct graph_t {
    struct node **nodes;         // vector of all nodes
    int size;                    // to create node identifiers
    int alloc_size;              // size allocated
};

void graph_init(struct graph_t *graph, int initial_size);

struct access_info *graph_ai_alloc(struct access_info **ai_free, int multiplicity, int atomic, int pc);

void graph_check_for_data_race(
    struct node *node,
    struct minheap *warnings,
    struct values_t *values,
    struct access_info **ai_free
);
void graph_add(struct graph_t *graph, struct node *node);
int graph_find_scc(struct graph_t *graph);

#endif //SRC_GRAPH_H
