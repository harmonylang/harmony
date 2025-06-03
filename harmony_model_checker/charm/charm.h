#ifndef SRC_CHARM_H
#define SRC_CHARM_H

#include "code.h"
#include "graph.h"
#include "json.h"
#include "hashtab.h"

// Invariants are compiled into Harmony code (terminated by an Assert instruction)
// Invariants are allowed to pairs of states (pre and post).  Since this comes at
// a cost that we do not want to level against all invariants, we keep track of
// whether an invariant refers to the pre state of a transition.
struct invariant {
    hvalue_t context;
    unsigned int pc;                // location of invariant code
    // TODO.  May not need the following since we can get it from env
    bool pre;                       // uses "pre" or not
};

// Info about a microstep, which is the execution of a single Harmony instruction
// by some thread during the re-execution of a counter-example.
struct microstep {
    struct microstep *next;     // linked list maintenance
    struct state *state;        // state before the microstep
    struct context *ctx;        // context (thread state) before the microstep
    bool interrupt;             // the instruction was interrupted
    bool choose;                // the instruction is a "choose"
    hvalue_t choice;            // the value that was chosen
    hvalue_t print, attrs;      // the value that was printed (0 if none)
    struct callstack *cs;       // the callstack of the execution
    char *explain;              // a string explaining the execution
    hvalue_t *args;             // arguments to explanation
    unsigned int nargs;         // the number of argument
};

// Info about a macrostep (edge in Kripke structure representing a sequence
// of microsteps)
struct macrostep {
    struct edge *edge;              // the edge this macrostep corresponds to
    unsigned int tid;               // thread identifier
#ifdef notdef
    unsigned int tid2;               // thread identifier
#endif
    hvalue_t name, arg;             // name and argument of the thread (first method)
    struct callstack *cs;           // callstack of the thread at the beginning

    // An array of microsteps.  nmicrosteps is the actual number of microsteps,
    // which alloc_microsteps is how many entries were allocated
    unsigned int nmicrosteps, alloc_microsteps;
    struct microstep **microsteps;

    struct instr *trim;             // first instruction if trimmed
    hvalue_t value;                 // corresponding value
    hvalue_t *processes;            // array of contexts of processes
    struct callstack **callstacks;  // array of callstacks of processes
    unsigned int nprocesses;        // the number of processes in the list

    // bool last;                      // to find the last macrostep
};

struct node_set {
    unsigned int nnodes;
    unsigned int nallocated;
    uint32_t *list;
};

// TODO.  Probably don't need both node_set and eps_component
struct eps_component {
    struct node_set ns;
};

// TODO. Could this be a union?
struct eps_scc {
    struct eps_component *component;
    int32_t index, lowlink; // only needed for Tarjan
};

// TODO. Could this be a union?
struct scc {
    uint32_t component;     // strongly connected component id
    int32_t index, lowlink; // only needed for Tarjan
};

#define MAX_PHASES  20

struct phase {
    char *descr;
    double start, finish;
    bool in_progress;
};

// All global variables of Charm should be in here, at least the ones that
// are used across multiple modules.
struct global {
    struct code code;               // code of the Harmony program
    struct json_value *locs;        // from hvm file
    struct json_value *modules;     // from hvm file
    struct json_value *pretty;      // from hvm file
    struct dict *values;            // dictionary of values
    struct dict *computations;      // evaluated Harmony byte code
    hvalue_t *seqs;                 // sequential variables
    unsigned int nseqs;             // number of sequential variables
    struct worker *workers;         // points to array of workers
    unsigned int nworkers;          // total number of workers
    struct phase phases[MAX_PHASES];// for reporting
    unsigned int nphases;           // ditto
    bool no_race_detect;            // do not detect data races
    bool do_not_pin;                // don't pin workers
    double last_report;             // used for periodic reporting
    char *lazy_header;              // report header
    double start_model_checking;    // time when model checking started

    // The worker thread loops through three phases:
    //  1: evaluate states on the todo list
    //  2: look up states and add to the todo list if new
    //  3: resize tables
    // The barriers are to synchronize these three phases.
    barrier_t barrier;

    // invariants
#ifdef OBSOLETE
    mutex_t inv_lock;               // lock on list of invariants and finals
#endif
    unsigned int ninvs;             // number of invariants
    struct invariant *invs;         // list of invariants
    bool inv_pre;                   // some invariant uses "pre"
    unsigned int nfinals;           // #finally predicates
    hvalue_t *finals;               // contexts of finally preds

    struct graph graph;             // the Kripke structure but also the todo list
    struct node *initial;           // initial node
    uint8_t *neps;                  // #epsilon edges for each node
    bool printed_something;         // set if anything was printed
    struct failure *failures;       // queue of "struct failure"  (TODO: make part of struct node "issues")
    hvalue_t *processes;            // array of contexts of processes
    struct callstack **callstacks;  // array of callstacks of processes
    unsigned int nprocesses;        // the number of processes in the list
    struct dfa *dfa;                // for tracking correct behaviors
    bool run_direct;                // non-model-checked mode
    unsigned long allocated;        // allocated table space
    unsigned int oldpid;            // for thread id computation
    struct scc *scc;                // strongly connected components
    unsigned int ncomponents;       // number of components
    struct eps_scc *eps_scc;        // same as above two for epsilon
    unsigned int eps_ncomponents;   //    closure computation

    hvalue_t *symbols;              // list of symbols
    unsigned int nsymbols;

    // Reconstructed error trace stored here
    unsigned int nmacrosteps;
    struct macrostep **macrosteps;
};

extern struct global global;

void add_failure(struct failure **failures, struct failure *f);

#endif //SRC_CHARM_H
