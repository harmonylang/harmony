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

// Codomain of onestep()
struct step_input {
    hvalue_t vars;           // initial shared variables
    hvalue_t choice;         // choice (-1 for interrupt)
    hvalue_t ctx;            // context at start
};

// Result of onestep()
struct step_output {
    hvalue_t vars;           // updated shared variables
    hvalue_t after;          // context at end
    struct access_info *ai;  // to detect data races
    uint16_t nsteps;         // # microsteps

    // TODO.  The following 4 can be capture in 2 bits, I think
    bool choosing : 1;       // destination state is choosing
    bool terminated : 1;     // thread has terminated
    bool stopped : 1;        // thread has stopped
    bool failed : 1;         // context failed

    uint16_t nlog : 3;       // # values printed
    uint16_t nspawned : 6;   // # contexts started
    uint16_t nunstopped : 3; // # contexts removed from stopbag
    // hvalue_t log[];       // print history (immediately follows this structure)
    // hvalue_t spawned[];   // spawn history (immediately follows log)
    // hvalue_t unstopped[]; // unstop history (immediately follows spawn history)
};
#define step_log(x)          ((hvalue_t *) ((x) + 1))
#define step_spawned(x)      ((hvalue_t *) ((x) + 1) + (x)->nlog)
#define step_unstopped(x)    ((hvalue_t *) ((x) + 1) + (x)->nlog + (x)->nspawned)

struct node_list {
    struct node_list *next;
    struct node *node;
    unsigned int multiplicity;
};

struct step_condition {
    enum { SC_IN_PROGRESS, SC_COMPLETED } type;
    union {
        struct node_list *in_progress;
        struct step_output *completed;
    } u;
};

// For each (directed) edge in the Kripke structure (a graph of states), we maintain
// information of how a program can get from the source state to the destination
// state.  This structure is directly followed by an array of Harmony values that
// were printed in this transition.
//
// We maintain the number of microsteps (Harmony instructions that were executed)
// but, for memory efficiency, not the details of the microsteps themselves.  If
// a failure is found, that information is recovered by re-executing the path to
// the faulty state.
struct edge {
    struct edge *fwdnext;        // forward linked list maintenance

    // TODO. The following three can be struct dict_assoc *
    hvalue_t ctx;                //< ctx that made the microstep
    hvalue_t choice;             //< choice if any (-1 indicates interrupt)
    struct step_output *so;      // result of onestep()

    struct node *src;            // source node (TODO. Do we need this?)
    struct node *dst;            // destination node

    // TODO.  The multiplicity can be looked up in the source state
    unsigned short multiplicity; // multiplicity of context
    bool failed : 1;             // transition failed
    bool invariant_chk : 1;      // this is an invariant check
};

// Charm can detect a variety of failure types:
enum fail_type {
    FAIL_NONE,
    FAIL_SAFETY,            // assertion failure, divide by zero, etc.
    FAIL_BEHAVIOR,          // output behavior not allowed by input DFA
    FAIL_INVARIANT,         // some invariant failed
    FAIL_FINALLY,           // some "finally" predicate failed
    FAIL_TERMINATION,       // a non-terminating state exists
    FAIL_BUSYWAIT,          // the program allows busy waiting
    FAIL_RACE               // the program has a race condition
};

// This is information about a node in the Kripke structure.  The Harmony state
// corresponding to this node is stored directly behind this node.
struct node {
    // Carefully packed data...
    union {
        // Data we only need while creating the Kripke structure
        struct {
            struct node *next;		// for linked list
            ht_lock_t *lock;        // points to lock for forward edges
        } ph1;
        // Data we only need when analyzing the Kripke structure
        struct {
            uint32_t component;     // strongly connected component id
            uint32_t len;           // length of shortest path to initial state
            union {
                struct {
                    int32_t index, lowlink; // only needed for Tarjan
                } tarjan;
                struct edge *to_parent; // path to initial state
            } u;
        } ph2;
    } u;

    struct edge *fwd;       // forward edges
    uint32_t id;            // nodes are numbered starting from 0
    bool on_stack : 1;      // for Tarjan
    bool initialized : 1;   // this node structure has been initialized
    bool failed : 1;        // a thread has failed
    bool final : 1;         // only eternal threads left (TODO: need this?)
    bool visited : 1;       // for busy wait detection

    // NFA compression
    bool reachable : 1;     // TODO.  Maybe obsolete at this time
};

// The state corresponding to a node, directly following the node
#define node_state(n)   ((struct state *) &(n)[1])

// Information about a failure.  Multiple failures may be detected, and these
// are kept in a linked list.
struct failure {
    struct failure *next;   // for linked list maintenance
    enum fail_type type;    // failure type
    struct edge *edge;      // edge->dst is the faulty state
    hvalue_t address;       // in case of data race or invariant failure
};

// A graph is represented by a list of its nodes.  Each node maintains a linked
// list of its outgoing edges.
struct graph {
    struct node **nodes;         // vector of all nodes
    unsigned int size;           // #valid nodes in this vector
    unsigned int alloc_size;     // #nodes allocated
};

void graph_init(struct graph *graph, unsigned int initial_size);
void graph_check_for_data_race(
    struct failure **failures,
    struct node *node,
    struct engine *engine
);
void graph_add(struct graph *graph, struct node *node);
unsigned int graph_add_multiple(struct graph *graph, unsigned int n);
unsigned int graph_find_scc(struct graph *graph);
struct scc *graph_find_scc_one(struct graph *graph, struct scc *scc, unsigned int component, void **scc_cache);
struct scc *scc_alloc(unsigned int start, unsigned int finish, struct scc *next, void **scc_cache);

#endif //SRC_GRAPH_H
