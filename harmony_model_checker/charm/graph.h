#ifndef SRC_GRAPH_H
#define SRC_GRAPH_H

#include <stdint.h>
#include "value.h"
#include "thread.h"
#include "hashtab.h"

// After the Kripke structure is computed, we run a Strongly Connected Component
// analysis to break the structure into its connected components.  The most major
// use of this is to determine if there is a "non-terminating state".  A component
// with outgoing edges cannot have such a state.  If not, then check if any of
// the states still have non-eternal threads.  If so, that's a problem.
struct component {
    bool good;              // terminating or out-going edge
    unsigned int size;      // #states in the component
    struct node *rep;       // lowest numbered state in the component
    bool all_same;          // shared state in component is the same
    bool final;             // all states in this component are final
};

// We maintain for each step if it loads or stores any variables in a linked
// list.  This is useful to detect race conditions and also plays a role in
// optimizing the counter-example that is produced if there is a failure.
// A variable is identified by a list of "indices" (simply Harmony values),
// representing a path in the hierarchy of dictionaries and lists that form
// the shared state between the threads.
struct access_info {
    struct access_info *next;        // linked list maintenance
    hvalue_t *indices;               // address of load/store

    // TODO.  The following 32 bits could be packed differently
    uint8_t n;                       // length of address
    bool atomic : 1;                 // atomic or not
    bool load : 1;                   // store or del if false
};

// Inputs to onestep
struct step_input {
    hvalue_t vars;           // initial shared variables
    hvalue_t choice;         // choice (-1 for interrupt)
    hvalue_t ctx;            // context at start
};

// Result of onestep().
// We maintain the number of microsteps (Harmony instructions that were executed)
// but, for memory efficiency, not the details of the microsteps themselves.  If
// a failure is found, that information is recovered by re-executing the path to
// the faulty state.
struct step_output {
    hvalue_t vars;             // updated shared variables
    hvalue_t after;            // context at end
    struct access_info *ai;    // to detect data races
    uint16_t nsteps;           // # microsteps
    uint16_t pc;               // program counter at start

    // TODO It would be good if these bits would be crammed into this structure
    //      more efficiently
    bool printing : 1;         // step involves a Print
    bool terminated : 1;       // thread has terminated
    bool stopped : 1;          // thread has stopped
    bool failed : 1;           // context failed
    bool infinite_loop : 1;    // ran into an infinite loop
    uint8_t nlog : 1;          // # values printed

    uint8_t choose_count;      // number of possible choices
    uint8_t nspawned;          // # contexts started
    uint8_t nunstopped;        // # contexts removed from stopbag
    // hvalue_t log[];         // print history (immediately follows this structure)
    // hvalue_t spawned[];     // spawn history (immediately follows log)
    // hvalue_t unstopped[];   // unstop history (immediately follows spawn history)
};
#define step_log(x)          ((hvalue_t *) ((x) + 1))
#define step_spawned(x)      ((hvalue_t *) ((x) + 1) + (x)->nlog)
#define step_unstopped(x)    ((hvalue_t *) ((x) + 1) + (x)->nlog + (x)->nspawned)

// List of node/edge-index pairs that are waiting for a step computation
// to complete.
struct edge_list {
    struct edge_list *next; // linked list
    struct node *node;      // source node
    int edge_index;         // index into edges of the source node
    int ctx_index;          // index of context in state
};

// Each edge points to one of these (by id).  It describes either a
// step in progress or a completed step.  When the step is in progress,
// multiple edges may be ``waiting'' for it to complete in order to
// compute the next state.
struct step_condition {
    bool completed;      // step has been computed
    bool invariant_chk;  // step is part of invariant check
    union {
        struct edge_list *in_progress;
        struct step_output *completed;
    } u;
};

// For each (directed) edge in the Kripke structure (a graph of states), we maintain
// information of how a program can get from the source state to the destination
// state.
struct edge {
#ifdef SHORT_PTR
THIS SHOULD NOT BE DEFINED
    int64_t dest : 37;          // "short" pointer to dst node
    uint32_t stc_id : 25;       // id of step_condition
#define edge_dst(e)          ((struct node *) ((int64_t *) (e) + (e)->dest))
#else
    struct node *dst;           // pointer to destination node
    uint64_t stc_id : 48;       // pointer to step_condition / step_input
#define edge_dst(e)          ((e)->dst)
#endif
    bool multiple : 1;          // multiplicity > 1
    bool failed : 1;            // edge has failed (safety violation)
    bool invariant_chk : 1;     // fake edge for invariant
};

#define edge_sc(e)           ((struct step_condition *) U64_TO_P((e)->stc_id))
#define edge_input(e)        ((struct step_input *) &edge_sc(e)[1])
#define edge_output(e)       (edge_sc(e)->u.completed)

// Charm can detect a variety of failure types:
enum fail_type {
    FAIL_NONE,
    FAIL_SAFETY,            // assertion failure, divide by zero, etc.
    FAIL_BEHAVIOR_BAD,      // output behavior not allowed by input DFA
    FAIL_BEHAVIOR_FINAL,    // DFA should end up in final state
    FAIL_TERMINATION,       // a non-terminating state exists
    FAIL_DEADLOCK,          // all threads are "stuck"
    FAIL_INFLOOP,           // some thread is in an infinite loop
    FAIL_BUSYWAIT,          // the program allows busy waiting
    FAIL_RACE               // the program has a race condition
};

// This is information about a node in the Kripke structure.  The node is directly followed
// by the array of outgoing edges and then the Harmony state corresponding to this node.
struct node {
    struct node *parent;    // path to initial state
    uint32_t id;            // nodes are numbered starting from 0
    uint16_t len;           // length of path to initial state  // TODO 8 bits is probably enough
    uint8_t nedges;         // number of outgoing edges  // TODO also maintained indirectly by hash table
    bool initial : 1;       // initial state
    bool on_stack : 1;      // for Tarjan
    bool eps_on_stack : 1;  // for Tarjan epsilon closure
    bool failed : 1;        // state resulted from failed transition
    bool final : 1;         // final state
    bool visited : 1;       // for busy wait detection
    // struct edge edges[nedges]
};

// The state corresponding to a node
#define node_edges(n)   ((struct edge *) &((n)[1]))
#define node_state(n)   ((struct state *) &node_edges(n)[(n)->nedges])

// Equivalently...
// #define node_assoc(n)   (((struct dict_assoc *) (n))[-1])
// #define node_state(n)   ((struct state *) ((char *) (n) + node_assoc(n).val_len))

// Information about a failure.  Multiple failures may be detected, and these
// are kept in a linked list.
struct failure {
    struct failure *next;   // for linked list maintenance
    enum fail_type type;    // failure type
    struct edge *edge;      // edge->dst is the faulty state
    struct node *node;      // source node of edge
    hvalue_t address;       // in case of data race or invariant failure
};

// A graph is represented by a list of its nodes.  Each node maintains a
// list of its outgoing edges.
struct graph {
    struct node **nodes;         // vector of all nodes
    unsigned int size;           // #valid nodes in this vector
};

void graph_init(struct graph *graph);
void graph_check_for_data_race(
    struct failure **failures,
    struct node *node,
    struct allocator *allocator
);
void graph_add(struct graph *graph, struct node *node);
unsigned int graph_add_multiple(struct graph *graph, unsigned int n);
struct edge *node_to_parent(struct node *n);

#endif //SRC_GRAPH_H
