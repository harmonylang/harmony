#ifndef SRC_CALM_H
#define SRC_CALM_H

#define USE_CALM

#include "charm.h" //struct global

#include "json.h"

#include "conqueue.h"
#include "conhashtab.h"

struct calm_para { //arguments for calm 

    unsigned int nworkers;

    struct json_value* jc; // parsed hmy program

};

// Might need to go back and forth between calm_global and global
struct calm_global {

    unsigned int nworkers;  //number of worker threads

    struct conqueue* todo;

    //something todo with engine

    struct graph *graph; // reuse that of global's

};

int calm(struct calm_para *para, struct global *g);

#endif
