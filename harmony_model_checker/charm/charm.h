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
    hvalue_t print;             // the value that was printed (0 if none)
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
};

// All global variables of Charm should be in here, at least the ones that
// are used across multiple modules.
struct global {
    struct code code;               // code of the Harmony program
    struct dict *values;            // dictionary of values
    struct dict *computations;      // evaluated Harmony byte code
    hvalue_t seqs;                  // sequential variables

    // invariants
    mutex_t inv_lock;               // lock on list of invariants and finals
    unsigned int ninvs;             // number of invariants
    struct invariant *invs;         // list of invariants
    bool inv_pre;                   // some invariant uses "pre"
    unsigned int nfinals;           // #finally predicates
    hvalue_t *finals;               // contexts of finally preds

    struct graph graph;             // the Kripke structure but also the todo list

    bool layer_done;                // all states in a layer completed
    bool printed_something;         // see if anything was printed

    unsigned int nshards;           // total number of Kripke structure shards
    struct shard *shards;           // array of shards
#ifdef notdef
    _Atomic(unsigned int) sh_index1; // shard index for phase 1
    _Atomic(unsigned int) sh_index2; // shard index for phase 2
#endif

    unsigned int nworkers;          // total number of threads
    unsigned int ncomponents;       // to generate component identifiers
    struct failure *failures;       // queue of "struct failure"  (TODO: make part of struct node "issues")
    hvalue_t *processes;            // array of contexts of processes
    struct callstack **callstacks;  // array of callstacks of processes
    unsigned int nprocesses;        // the number of processes in the list
    double lasttime;                // since last report printed
    unsigned int last_nstates;      // to measure #states / second
    struct dfa *dfa;                // for tracking correct behaviors
    unsigned int diameter;          // graph diameter
    struct json_value *pretty;      // for output
    bool run_direct;                // non-model-checked mode
    unsigned long allocated;        // allocated table space
    unsigned int oldpid;            // for thread id computation

    // Reconstructed error trace stored here
    unsigned int nmacrosteps, alloc_macrosteps;
    struct macrostep **macrosteps;

    mutex_t stc_lock;
    struct step_condition **stc_table;
    unsigned int nstc, stc_allocated;
};

extern struct global global;

void add_failure(struct failure **failures, struct failure *f);

#endif //SRC_CHARM_H
