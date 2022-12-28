#ifndef SRC_HASHTAB_H
#define SRC_HASHTAB_H

#ifdef USE_ATOMIC
#include <stdatomic.h>
#define hAtomic(x)  _Atomic(x)
#else

#define hAtomic(t)          t
#define atomic_init(p, v)   do *(p) = (v); while (0)
#define atomic_store(p, v)  do *(p) = (v); while (0)
#define atomic_load(p)      (*(p))

#endif // USE_ATOMIC

#include <stdlib.h>
#include "thread.h"

// followed directly by data of `size' bytes
struct ht_node {
    hAtomic(struct ht_node *) next;
    unsigned int size;
};

// #define USE_SPINLOCK    // TODO

#ifdef USE_SPINLOCK

typedef pthread_spinlock_t ht_lock_t;
#define ht_lock_init(ll) pthread_spin_init(ll, 0)
#define ht_lock_acquire(ll) pthread_spin_lock(ll)
#define ht_lock_try_acquire(ll) (pthread_spin_trylock(ll) == 0)
#define ht_lock_release(ll) pthread_spin_unlock(ll)
#else
typedef mutex_t ht_lock_t;
#define ht_lock_init(ll) mutex_init(ll);
#define ht_lock_acquire(ll) mutex_acquire(ll)
#define ht_lock_try_acquire(ll) mutex_try_acquire(ll)
#define ht_lock_release(ll) mutex_release(ll)
#endif

// #define CACHE_LINE_ALIGNED
struct ht_bucket {
    hAtomic(struct ht_node *) list;
#ifdef CACHE_LINE_ALIGNED
    char padding[64 - sizeof(hAtomic(struct ht_node *))];
#endif
};

struct hashtab {
    char *whoami;
    unsigned int value_size;
    bool align16;
    struct ht_bucket *buckets;
    unsigned int nbuckets;
    ht_lock_t *locks;
    unsigned int nlocks;
    bool concurrent;
    unsigned int nworkers;
    unsigned int *counts;       // 1 per worker
    uint64_t *cycles;           // 1 per worker
    unsigned long nobjects;     // total #items in hash table

#ifndef USE_ATOMIC
    mutex_t mutex;
#endif
    hAtomic(unsigned int) rt_count;     // number of objects in hash table

    // For concurrent resize
    struct ht_bucket *old_buckets;
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
