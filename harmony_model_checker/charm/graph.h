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
    struct access_info *next; // linked list maintenance
    hvalue_t *indices;        // address of load/store
    unsigned int n;           // length of address
    bool load;                // store or del if false
    int pc;                   // for debugging
    int multiplicity;         // #identical contexts
    int atomic;               // atomic counter
};

struct edge {
    struct edge *fwdnext;    // forward linked list maintenance
    struct edge *bwdnext;    // backward linked list maintenance
    hvalue_t ctx, choice;    // ctx that made the microstep, choice if any
    bool interrupt;          // set if state change is an interrupt
    struct node *src;        // source node
    struct node *dst;        // destination node
    hvalue_t after;          // resulting context
    struct access_info *ai;  // to detect data races
    hvalue_t *log;           // print history
    unsigned int nlog;       // size of print history
    int probability_numerator;  // Probability to node as rational number
    int probability_denominator;
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
    unsigned int id;        // nodes are numbered starting from 0
    struct edge *fwd;       // forward edges
    struct edge *bwd;       // backward edges

    // How to get here from parent node
    struct node *parent;    // shortest path to initial state
    int len;                // length of path to initial state
    int steps;              // #microsteps from root
    hvalue_t before;        // context before state change
    hvalue_t after;         // context after state change (current context)
    hvalue_t choice;        // choice made if any
    int choice_size;        // Helper to get size of choice
    bool interrupt;         // set if gotten here by interrupt
    bool final;             // only eternal threads left

    // SCC
    bool visited;           // for Kosaraju algorithm
    unsigned int component; // strongly connected component id

    // NFA compression
    bool reachable;
};

struct failure {
    struct failure *next;   // for linked list maintenance
    enum fail_type type;
    struct node *node;      // failed state
    struct node *parent;    // if NULL, use node->parent
    hvalue_t choice;        // choice if any
    bool interrupt;         // interrupt transition
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
int graph_find_scc(struct graph_t *graph);

#endif //SRC_GRAPH_H
