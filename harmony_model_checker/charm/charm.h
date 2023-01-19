#ifndef SRC_CHARM_H
#define SRC_CHARM_H

#include "minheap.h"
#include "code.h"
#include "graph.h"
#include "json.h"
#include "hashtab.h"

struct scc {        // Strongly Connected Component
    struct scc *next;
    unsigned int start, finish;
};

struct invariant {
    unsigned int pc;                // location of invariant code
    // TODO.  May not need the following since we can get it from env
    bool pre;                       // uses "pre" or not
};

// Info about a microstep
struct microstep {
    struct microstep *next;
    struct state *state;
    struct context *ctx;
    bool interrupt, choose;
    hvalue_t choice, print;
    struct callstack *cs;
    char *explain;
};

// Info about a macrostep (edge in Kripke structure)
struct macrostep {
    struct macrostep *next;
    struct edge *edge;
    unsigned int tid;
    hvalue_t name, arg;
    struct callstack *cs;
    unsigned int nmicrosteps, alloc_microsteps;
    struct microstep **microsteps;
    struct instr *trim;             // first instruction if trimmed
    hvalue_t value;                 // corresponding value

    hvalue_t *processes;            // array of contexts of processes
    struct callstack **callstacks;  // array of callstacks of processes
    unsigned int nprocesses;        // the number of processes in the list
};

struct global {
    struct code code;               // code of the Harmony program
    struct dict *values;            // dictionary of values
    hvalue_t seqs;                  // sequential variables

    // invariants
    mutex_t inv_lock;               // lock on list of invariants and finals
    unsigned int ninvs;             // number of invariants
    struct invariant *invs;         // list of invariants
    bool inv_pre;                   // some invariant uses "pre"
    unsigned int nfinals;           // #finally predicates
    unsigned int *finals;           // program counters of finally preds

    unsigned int n_numa;            // splitting state across sockets
    struct {
        struct graph graph;             // the Kripke structure
        struct dict *visited;           // hash map for states
#ifdef USE_ATOMIC
        hAtomic(unsigned int) atodo;
#else
        mutex_t todo_lock;              // to access the todo list
        unsigned int todo;
#endif
        unsigned int goal;
        bool layer_done;                // all states in a layer completed
    } *numa;

    mutex_t todo_enter;             // entry semaphore for SCC tasks
    mutex_t todo_wait;              // wait semaphore for SCC tasks
    unsigned int nworkers;          // total number of threads
    unsigned int scc_nwaiting;      // # workers waiting for SCC work
    unsigned int ncomponents;       // to generate component identifiers
    struct minheap *failures;       // queue of "struct failure"  (TODO: make part of struct node "issues")
    hvalue_t *processes;            // array of contexts of processes
    struct callstack **callstacks;  // array of callstacks of processes
    unsigned int nprocesses;        // the number of processes in the list
    double lasttime;                // since last report printed
    unsigned int last_nstates;      // to measure #states / second
    struct dfa *dfa;                // for tracking correct behaviors
    unsigned int diameter;          // graph diameter
    bool phase2;                    // when model checking is done and graph analysis starts
    struct scc *scc_todo;           // SCC search
    struct json_value *pretty;      // for output
    bool run_direct;                // non-model-checked mode
    unsigned long allocated;        // allocated table space
    unsigned int numa_rand;         // for distribution across chips

    // Reconstructed error trace stored here
    unsigned int nmacrosteps, alloc_macrosteps;
    struct macrostep **macrosteps;
};

#endif //SRC_CHARM_H
