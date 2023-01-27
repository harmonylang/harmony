#include <stdio.h>
#include <pthread.h>

#include "calm.h"
//#include "graph.h"
#include "conallocator.h"
#include "conhashtab.h"
#include "conqueue.h"
#include "engine.h"

unsigned int nworkers;

struct Conhashtab values;
struct Conhashtab states;

struct Conqueue todo;

struct Engine engine;

struct pthread_barrier_t barrier_computation, barrier_sequential, barrier_concurrent;

atomic_bool interrupt_computation;

struct worker {
    //TODO

    unsigned int id;

    struct Conallocator al;
};

struct worker *workers;

//worker's alloca

//worker's steps

//worker do work (phase 1)

void work_computation(struct worker *this) {

    #define TODO_GRAB_SIZE 256

    while(true) {
        cq_iter next = conqueue_grab(&todo, TODO_GRAB_SIZE);
        
        for (int i = 0; i < TODO_GRAB_SIZE; ++i, ++next) {
            if (conqueue_invalid(&todo, next)) {
                break;
            }
            struct Node* node = conqueue_get(&todo, next);

            struct State* s = &node->s;

            for (int cid = 0; cid < s->bagsize; ++cid) {

                struct Node* next = engine_compute(&engine, &this->al, s, cid);

                //TODO: do things when the two nodes are connected

            }

        }

        if (atomic_load(&interrupt_computation)) {
            break;
        }
    }

}

void work_sequential(struct worker *this) {
    //reset conqueue
    //reset interrupt_computation

}

void work_concurrent(struct worker *this) {

}

void work(struct worker *this) {
    if (this->id != 0) {
        conallocator_init(&this->al);
    }
    pthread_barrier_wait(&barrier_concurrent);

    while(true) {

        //TODO: add measurements and reports
        work_computation(this);

        pthread_barrier_wait(&barrier_computation);

        work_sequential(this);

        pthread_barrier_wait(&barrier_sequential);

        work_concurrent(this);

        pthread_barrier_wait(&barrier_concurrent);

    }
}

//foreman

void foreman(struct calm_para *para, struct Conallocator *al0) {

    atomic_store(&interrupt_computation, false);
    pthread_barrier_init(&barrier_computation, NULL, nworkers);
    pthread_barrier_init(&barrier_sequential, NULL, nworkers);
    pthread_barrier_init(&barrier_concurrent, NULL, nworkers);

    workers = malloc(nworkers * sizeof(struct worker)); //workers[0] = foreman

    for (unsigned int i = 0; i < nworkers; ++i) {
        workers[i].id = i;
        if (i == 0) {
            workers[i].al = *al0;
        } else {
            pthread_t pt;
            pthread_create(&pt, NULL, work, &workers[i]);
        }
    }

    work(&workers[0]);

}

int calm(struct calm_para *para, struct global *g) {

    fprintf(stderr, "Calm main reporting\n");

//    struct Graph graph;
//    graph_init(&graph);

    nworkers = para->nworkers;

    conhashtab_init(&values, &interrupt_computation);
    conhashtab_init(&states, &interrupt_computation);


    struct Conallocator al0; //will be used for the allocator of worker 0
    conallocator_init(&al0);

    engine_init(&engine, para->jc, &values, &states, &al0);

    struct Node *init_n = engine_create_initial_node(&engine, &al0);

    conqueue_init(&todo, init_n);

    foreman(para, &al0);

    //Warning: al0 is now obsolete

    //TODO: clean up: translate everything back to what charm.c can understand in global *g

    return 0;
}