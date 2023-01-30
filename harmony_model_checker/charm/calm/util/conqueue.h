#ifndef SRC_CALM_CONQUEUE_H
#define SRC_CALM_CONQUEUE_H

#include <stdatomic.h>
#include <stdbool.h>

//Concurrent queue abstraction for the todo list

typedef unsigned int cq_iter;

struct Conqueue {
    atomic_uint head;
    unsigned int tail;
};

static inline void conqueue_init(struct Conqueue *cq, void *init_e) __attribute__ ((always_inline)) {

}

inline cq_iter conqueue_claim(struct Conqueue *cq, unsigned int sz)  __attribute__ ((always_inline)) {

}

inline bool conqueue_invalid(struct Conqueue *cq, cq_iter pt)  __attribute__ ((always_inline)) {

}

inline void* conqueue_get(struct Conqueue *cq, cq_iter pt)  __attribute__ ((always_inline)) {

}

inline void conqueue_reset(struct Conqueue *cq)  __attribute__ ((always_inline)) {
    
}

#endif //SRC_CALM_CONQUEUE_H