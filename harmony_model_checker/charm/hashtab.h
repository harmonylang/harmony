#ifndef SRC_HASHTAB_H
#define SRC_HASHTAB_H

#include <stdlib.h>
#include <stdatomic.h>
#include "thread.h"

// followed directly by data of `size' bytes
struct ht_node {
    _Atomic(struct ht_node *) next;
    unsigned int size;
};

#ifdef __APPLE__
typedef int pthread_spinlock_t;

int pthread_spin_init(pthread_spinlock_t *lock, int pshared);
int pthread_spin_lock(pthread_spinlock_t *lock);
int pthread_spin_trylock(pthread_spinlock_t *lock);
int pthread_spin_unlock(pthread_spinlock_t *lock);
#else
#include <pthread.h>
#endif // __APPLE__

// #define USE_SPINLOCK    // TODO

#ifdef USE_SPINLOCK

typedef pthread_spinlock_t ht_lock_t;
#define ht_lock_init(ll) pthread_spin_init(ll, 0)
#define ht_lock_acquire(ll) pthread_spin_lock(ll)
#define ht_lock_try_acquire(ll) pthread_spin_trylock(ll)
#define ht_lock_release(ll) pthread_spin_unlock(ll)
#else
typedef pthread_mutex_t ht_lock_t;
#define ht_lock_init(ll) pthread_mutex_init(ll, NULL);
#define ht_lock_acquire(ll) pthread_mutex_lock(ll)
#define ht_lock_try_acquire(ll) pthread_mutex_trylock(ll)
#define ht_lock_release(ll) pthread_mutex_unlock(ll)
#endif

struct hashtab {
    unsigned int value_size;
    bool align16;
    _Atomic(struct ht_node *) *buckets;
    unsigned int nbuckets;
    ht_lock_t *locks;
    unsigned int nlocks;
    bool concurrent;
    unsigned int nworkers;
    unsigned int *counts;       // 1 per worker
    unsigned long nobjects;     // total #items in hash table

    _Atomic(unsigned int) rt_count;     // number of objects in hash table

    // For concurrent resize
    _Atomic(struct ht_node *) *old_buckets;
    unsigned int old_nbuckets;
};

struct hashtab *ht_new(char *whoami, unsigned int value_size, unsigned int nbuckets,
        unsigned int nworkers, bool align16);
void ht_resize(struct hashtab *ht, unsigned int nbuckets);
void *ht_retrieve(struct ht_node *n, unsigned int *psize);
struct ht_node *ht_find(struct hashtab *ht, struct allocator *al, const void *key, unsigned int size, bool *is_new);
struct ht_node *ht_find_lock(struct hashtab *ht, struct allocator *al, const void *key, unsigned int size, bool *is_new, ht_lock_t **plock);
void *ht_insert(struct hashtab *ht, struct allocator *al,
                        const void *key, unsigned int size, bool *new);
void ht_set_concurrent(struct hashtab *ht);
void ht_make_stable(struct hashtab *ht, unsigned int worker);
void ht_set_sequential(struct hashtab *ht);
void ht_grow_prepare(struct hashtab *ht);
unsigned long ht_allocated(struct hashtab *ht);
bool ht_needs_to_grow(struct hashtab *ht);

#endif //SRC_HASHTAB_H
