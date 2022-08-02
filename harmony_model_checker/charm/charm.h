#ifndef SRC_CHARM_H
#define SRC_CHARM_H

#include "minheap.h"
#include "code.h"
#include "graph.h"
#include "json.h"

struct scc {        // Strongly Connected Component
    struct scc *next;
    unsigned int start, finish;
};

struct values {
    struct dict *atoms;
    struct dict *dicts;
    struct dict *sets;
    struct dict *lists;
    struct dict *addresses;
    struct dict *contexts;
};

struct global {
    struct code code;               // code of the Harmony program
    struct values values;           // dictionaries of values
    hvalue_t seqs;                  // sequential variables
    hvalue_t invariants;            // set of invariants that must hold
    struct graph graph;             // the Kripke structure
    unsigned int todo;              // points into graph->nodes
    unsigned int goal;              // points into graph->nodes
    bool layer_done;                // all states in a layer completed
    mutex_t todo_lock;              // to access the todo list
    mutex_t todo_wait;              // to wait for SCC tasks
    unsigned int nworkers;          // total number of threads
    unsigned int scc_nwaiting;      // # workers waiting for SCC work
    unsigned int ncomponents;       // to generate component identifiers
    struct minheap *failures;       // queue of "struct failure"  (TODO: make part of struct node "issues")
    hvalue_t *processes;            // list of contexts of processes
    struct callstack **callstacks;  // list of callstacks of processes
    unsigned int nprocesses;        // the number of processes in the list
    double lasttime;                // since last report printed
    unsigned int last_nstates;      // to measure #states / second
    bool dumpfirst;                 // for json dumping
    struct dfa *dfa;                // for tracking correct behaviors
    unsigned int diameter;          // graph diameter
    bool phase2;                    // when model checking is done and graph analysis starts
    struct scc *scc_todo;           // SCC search
    struct json_value *pretty;      // for output
    bool run_direct;                // non-model-checked mode
};

#endif //SRC_CHARM_H
