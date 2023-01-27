#include "conqueue.h"

inline void conqueue_init(struct Conqueue *cq, void *init_e) {
    //TODO
}

inline cq_iter conqueue_claim(struct Conqueue *cq, unsigned int sz) {
    //TODO
    return 0;
}

inline void* conqueue_get(struct Conqueue *cq, cq_iter pt) {
    return NULL;
}

inline bool conqueue_invalid(struct Conqueue *cq, cq_iter pt) {
    //TODO
    return true;
}

inline void conqueue_reset(struct Conqueue *cq) {
    //TODO
}
