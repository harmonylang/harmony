#ifndef SRC_CALM_MYBARRIER_H
#define SRC_CALM_MYBARRIER_H

#include "thread.h"

typedef int pthread_barrierattr_t;
typedef barrier_t pthread_barrier_t;

static inline int pthread_barrier_init(pthread_barrier_t *barrier, const pthread_barrierattr_t *attr, unsigned count) {
    barrier_init(barrier, count);
    return 0;
}

static inline int pthread_barrier_wait(pthread_barrier_t *barrier) {
    barrier_wait(barrier);
    return 0;
}

static inline int pthread_barrier_destroy(pthread_barrier_t *barrier) {
    barrier_destroy(barrier);
    return 0;
}

#endif //SRC_CALM_MYBARRIER_H
