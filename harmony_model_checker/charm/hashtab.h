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
    union {
        struct ht_node *stable;
        hAtomic(struct ht_node *) unstable;
    } next;
    uint32_t size;
    uint32_t hash;
};

struct ht_worker {
    unsigned int first, last;
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

#define CACHE_LINE_ALIGNED
struct ht_unstable {
    hAtomic(struct ht_node *) list;
#ifdef CACHE_LINE_ALIGNED
    char padding[64 - sizeof(hAtomic(struct ht_node *))];
#endif
};

// The hash table is "grow-only" and has two arrays of buckets:
// unstable and stable buckets.  The array of unstable buckets
// is used to add new items and uses a lock-free mechanism
// based on cas, and for cache efficiency each bucket is
// aligned to 64 bytes and the number of buckets is fixed.
// The array of stable buckets is (usually) read-only.  Both
// have a power of 2 buckets.  Let U be the number of unstable
// buckets.  Then the array of stable buckets is subdivided
// into U contiguous segments.  There is a mechanism to grow
// the array of stable buckets and to flush the unstable items
// into the stable corresponding stable segments.
// log_unstable below gives the number of unstable buckets or
// segments in that U == (1 << log_unstable).  log_stable
// gives the number of stable buckets per segment.

struct hashtab {
    char *whoami;
    unsigned int value_size;
    bool align16;
    unsigned int log_stable, log_unstable;
    struct ht_node **stable;
    struct ht_unstable *unstable;
    bool needs_flush;
    hAtomic(unsigned int) todo;
    ht_lock_t *locks;
    unsigned int nlocks;
    bool concurrent;
    unsigned int nworkers;
    struct ht_worker *workers;
    unsigned int *counts;       // 1 per worker
    unsigned long nobjects;     // total #items in hash table

#ifndef USE_ATOMIC
    mutex_t mutex;
#endif
    unsigned int stable_count;  // #objects in stable buckets
    hAtomic(unsigned int) unstable_count;     // #objects in unstable buckets

    // For concurrent resize
    struct ht_node **old_stable;
    unsigned int old_log_stable;
};

struct hashtab *ht_new(char *whoami, unsigned int value_size, unsigned int log_buckets, unsigned int nworkers, bool align16);
void ht_resize(struct hashtab *ht, unsigned int log_buckets);
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
