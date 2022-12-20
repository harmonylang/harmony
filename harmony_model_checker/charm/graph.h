#ifndef SRC_GRAPH_H
#define SRC_GRAPH_H

#include <stdint.h>
#include "value.h"
#include "minheap.h"
#include "thread.h"
#include "hashtab.h"

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

    // TODO.  The following 32 bits could be packed differently
    uint8_t n;                       // length of address
    uint8_t multiplicity;            // #identical contexts
    bool atomic : 1;                 // atomic or not
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
    uint32_t nsteps;         // # microsteps
    bool interrupt : 1;      // set if state change is an interrupt
    uint8_t weight : 1;      // context switch or not
    bool choosing : 1;       // destination state is choosing
    bool failed : 1;         // context failed
    uint16_t nlog : 12;      // size of print history
    // hvalue_t log[];       // print history (immediately follows edge)
};
#define edge_log(x)     ((hvalue_t *) ((x) + 1))

enum fail_type {
    FAIL_NONE,
    FAIL_SAFETY,
    FAIL_BEHAVIOR,
    FAIL_INVARIANT,
    FAIL_FINALLY,
    FAIL_TERMINATION,
    FAIL_BUSYWAIT,
    FAIL_RACE
};

struct node {
	struct node *next;		// for linked list

    // Information about state
    // TODO.  state contiguous to this node, so don't need pointer
    struct state *state;    // state corresponding to this node
    struct edge *bwd;       // backward edges
    struct edge *fwd;       // forward edges
    ht_lock_t *lock;         // lock for forward edges

    struct edge *to_parent; // pointer towards initial state
    uint32_t id;            // nodes are numbered starting from 0
    uint32_t component;     // strongly connected component id
    uint16_t len;           // length of path to initial state
    uint16_t steps;         // #microsteps from root
    bool initialized : 1;   // this node structure has been initialized
    bool final : 1;         // only eternal threads left (TODO: need this?)
    bool visited : 1;       // for busy wait detection

    // NFA compression
    bool reachable : 1;
};

struct failure {
    struct failure *next;   // for linked list maintenance
    enum fail_type type;    // failure type
    struct edge *edge;      // edge->dst is the faulty state
    hvalue_t address;       // in case of data race or invariant failure
};

struct graph {
    struct node **nodes;         // vector of all nodes
    unsigned int size;           // to create node identifiers
    unsigned int alloc_size;     // size allocated
};

void graph_init(struct graph *graph, unsigned int initial_size);

void graph_check_for_data_race(
    struct node *node,
    struct minheap *warnings,
    struct engine *engine
);
void graph_add(struct graph *graph, struct node *node);
unsigned int graph_add_multiple(struct graph *graph, unsigned int n);
unsigned int graph_find_scc(struct graph *graph);
struct scc *graph_find_scc_one(struct graph *graph, struct scc *scc, unsigned int component, void **scc_cache);
struct scc *scc_alloc(unsigned int start, unsigned int finish, struct scc *next, void **scc_cache);

#endif //SRC_GRAPH_H
