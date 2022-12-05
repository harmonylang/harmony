#ifndef SRC_HASHTAB_H
#define SRC_HASHTAB_H

#include <stdlib.h>
#include <stdatomic.h>

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
    _Atomic(uint32_t) nobjects;
};

struct hashtab *ht_new(char *whoami, unsigned int value_size, unsigned int nbuckets,
        unsigned int nworkers, bool align16);
void ht_resize(struct hashtab *ht, unsigned int nbuckets);
void *ht_retrieve(struct ht_node *n, unsigned int *psize);

struct ht_node *ht_find(struct hashtab *ht, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);

#endif //SRC_HASHTAB_H
