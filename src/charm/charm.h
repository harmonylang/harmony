#ifndef SRC_CHARM_H
#define SRC_CHARM_H

#ifndef HARMONY_COMBINE
#include "minheap.h"
#include "code.h"
#include "value.h"
#include "graph.h"
#endif

struct global_t {
    struct code_t code;
    struct values_t values;
    struct graph_t graph;
    struct minheap *failures;    // queue of "struct failure"  (TODO: make part of struct node "issues")
    struct minheap *warnings;    // queue of "struct failure"  (TODO: make part of struct node "issues")
    uint64_t *processes;         // list of contexts of processes
    int nprocesses;              // the number of processes in the list
    double lasttime;             // since last report printed
    int timecnt;                 // to reduce time overhead
    int enqueued;                // #states enqueued
    int dequeued;                // #states dequeued
    bool dumpfirst;              // for json dumping
    struct access_info *ai_free; // free list of access_info structures
    struct node *tochk;
    struct dict *possibly_cnt;
};

#endif //SRC_CHARM_H
