#ifndef SRC_CHARM_H
#define SRC_CHARM_H

#include "minheap.h"
#include "code.h"
#include "value.h"
#include "graph.h"

struct global_t {
    struct code_t code;
    struct values_t values;
    struct graph_t graph;
    struct minheap *failures;    // queue of "struct failure"  (TODO: make part of struct node "issues")
    hvalue_t *processes;         // list of contexts of processes
    int nprocesses;              // the number of processes in the list
    double lasttime;             // since last report printed
    int enqueued;                // #states enqueued
    int dequeued;                // #states dequeued
    bool dumpfirst;              // for json dumping
    struct dfa *dfa;             // for tracking correct behaviors
    hvalue_t init_name;          // "__init__" atom
    unsigned int diameter;       // graph diameter
    bool run_direct;             // non-model-checked mode
};

#endif //SRC_CHARM_H
