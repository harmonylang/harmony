#ifndef SRC_HASHTAB_H
#define SRC_HASHTAB_H

#include <stdlib.h>
#include <stdatomic.h>
#include "thread.h"

// followed directly by data
struct ht_node {
    _Atomic(struct ht_node *) next;
    unsigned int size;
};

struct hashtab {
    unsigned int value_size;
    bool align16;
    _Atomic(struct ht_node *) *buckets;
    unsigned int nbuckets;
    mutex_t *locks;
    unsigned int nlocks;
    bool concurrent;
    unsigned int nworkers;
    unsigned int *counts;       // 1 per worker
    unsigned long nobjects;     // total #items in hash table

    // For concurrent resize
    _Atomic(struct ht_node *) *old_buckets;
    unsigned int old_nbuckets;
};

struct hashtab *ht_new(char *whoami, unsigned int value_size, unsigned int nbuckets,
        unsigned int nworkers, bool align16);
void ht_resize(struct hashtab *ht, unsigned int nbuckets);
void *ht_retrieve(struct ht_node *n, unsigned int *psize);
struct ht_node *ht_find(struct hashtab *ht, struct allocator *al, const void *key, unsigned int size, bool *is_new);
struct ht_node *ht_find_lock(struct hashtab *ht, struct allocator *al, const void *key, unsigned int size, bool *is_new, mutex_t **plock);
void *ht_insert(struct hashtab *ht, struct allocator *al,
                        const void *key, unsigned int size, bool *new);
void ht_set_concurrent(struct hashtab *ht);
void ht_make_stable(struct hashtab *ht, unsigned int worker);
void ht_set_sequential(struct hashtab *ht);
void ht_grow_prepare(struct hashtab *ht);
unsigned long ht_allocated(struct hashtab *ht);

#endif //SRC_HASHTAB_H
