#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include "global.h"
#include "hashtab.h"

#ifdef USE_SPINLOCK

#ifdef __APPLE__

#include <pthread.h>
#include <errno.h>

int pthread_spin_init(pthread_spinlock_t *lock, int pshared) {
    __asm__ __volatile__ ("" ::: "memory");
    *lock = 0;
    return 0;
}

int pthread_spin_destroy(pthread_spinlock_t *lock) {
    return 0;
}

int pthread_spin_lock(pthread_spinlock_t *lock) {
    while (1) {
        int i;
        for (i=0; i < 10000; i++) {
            if (__sync_bool_compare_and_swap(lock, 0, 1)) {
                return 0;
            }
        }
        sched_yield();
    }
}

int pthread_spin_trylock(pthread_spinlock_t *lock) {
    if (__sync_bool_compare_and_swap(lock, 0, 1)) {
        return 0;
    }
    return EBUSY;
}

int pthread_spin_unlock(pthread_spinlock_t *lock) {
    __asm__ __volatile__ ("" ::: "memory");
    *lock = 0;
    return 0;
}

#endif // __APPLE__

#endif // USE_SPINLOCK

#define hash_func meiyan

static inline uint32_t meiyan(const char *key, int count) {
	typedef uint32_t *P;
	uint32_t h = 0x811c9dc5;
	while (count >= 8) {
		h = (h ^ ((((*(P)key) << 5) | ((*(P)key) >> 27)) ^ *(P)(key + 4))) * 0xad3e7;
		count -= 8;
		key += 8;
	}
	#define tmp h = (h ^ *(uint16_t*)key) * 0xad3e7; key += 2;
	if (count & 4) { tmp tmp }
	if (count & 2) { tmp }
	if (count & 1) { h = (h ^ *key) * 0xad3e7; }
	#undef tmp
	return h ^ (h >> 16);
}

struct hashtab *ht_new(char *whoami, unsigned int value_size, unsigned int nbuckets,
        unsigned int nworkers, bool align16) {
    struct hashtab *ht = new_alloc(struct hashtab);
    ht->align16 = align16;
    ht->value_size = value_size;
	if (nbuckets == 0) {
        nbuckets = 1024;
    }
    nbuckets = 1024;
    ht->nbuckets = nbuckets;
    ht->buckets = malloc(nbuckets * sizeof(*ht->buckets));
    for (unsigned int i = 0; i < nbuckets; i++) {
        atomic_init(&ht->buckets[i], NULL);
    }
    ht->nlocks = nworkers * 64;        // TODO: how much?
    ht->locks = malloc(ht->nlocks * sizeof(ht->locks));
	for (unsigned int i = 0; i < ht->nlocks; i++) {
		ht_lock_init(&ht->locks[i]);
	}
    ht->nworkers = nworkers;
    ht->counts = calloc(nworkers, sizeof(*ht->counts));
    atomic_init(&ht->rt_count, 0);
    return ht;
}

void ht_do_resize(struct hashtab *ht, unsigned int old_nbuckets, _Atomic(struct ht_node *) *old_buckets, unsigned int first, unsigned int last){
    unsigned int factor = ht->nbuckets / old_nbuckets;
    if (factor == 0) {      // deal with shrinking tables
        factor = 1;
    }
    for (unsigned int i = first; i < last; i++) {
        unsigned int k = i;
        for (unsigned int j = 0; j < factor; j++) {
            atomic_init(&ht->buckets[k], NULL);
            k += old_nbuckets;
        }
        struct ht_node *n = atomic_load(&old_buckets[i]), *next;
        for (; n != NULL; n = next) {
            next = atomic_load(&n->next);
            unsigned int hash = hash_func((char *) &n[1] + ht->value_size, n->size) % ht->nbuckets;
            atomic_store(&n->next, atomic_load(&ht->buckets[hash]));
            atomic_store(&ht->buckets[hash], n);
        }
    }
}

void ht_resize(struct hashtab *ht, unsigned int nbuckets){
    _Atomic(struct ht_node *) *old_buckets = ht->buckets;
    unsigned int old_nbuckets = ht->nbuckets;
    ht->buckets = malloc(nbuckets * sizeof(*ht->buckets));
    ht->nbuckets = nbuckets;
    ht_do_resize(ht, old_nbuckets, old_buckets, 0, old_nbuckets);
}

// TODO.  is_new is not terribly useful.
struct ht_node *ht_find_with_hash(struct hashtab *ht, struct allocator *al, unsigned int hash, const void *key, unsigned int size, bool *is_new){
    // First do a search
    _Atomic(struct ht_node *) *chain = &ht->buckets[hash];
    for (;;) {
        struct ht_node *expected = atomic_load(chain);
        if (expected == NULL) {
            break;
        }
        if (expected->size == size && memcmp((char *) &expected[1] + ht->value_size, key, size) == 0) {
            if (is_new != NULL) {
                *is_new = false;
            }
            return expected;
        }
        chain = &expected->next;
    }

    // Allocated a new node
    unsigned int total = sizeof(struct ht_node) + ht->value_size + size;
	struct ht_node *desired = al == NULL ?
            malloc(total) : (*al->alloc)(al->ctx, total, false, ht->align16);
    atomic_init(&desired->next, NULL);
    desired->size = size;
    if (ht->value_size > 0) {
        memset(&desired[1], 0, ht->value_size);
    }
    memcpy((char *) &desired[1] + ht->value_size, key, size);

    // Insert the node
    for (;;) {
        struct ht_node *expected = NULL;
        if (atomic_compare_exchange_strong(chain, &expected, desired)) {
            atomic_fetch_add(&ht->rt_count, 1);
            if (ht->concurrent) {
                assert(al != NULL);
                ht->counts[al->worker]++;
            }
            if (is_new != NULL) {
                *is_new = true;
            }
            return desired;
        }
        else if (expected->size == size && memcmp((char *) &expected[1] + ht->value_size, key, size) == 0) {
            // somebody else beat me to it
            if (al == NULL) {
                free(desired);
            }
            else {
                (*al->free)(al->ctx, desired, ht->align16);
            }
            if (is_new != NULL) {
                *is_new = false;
            }
            return expected;
        }
        chain = &expected->next;
    }
}

struct ht_node *ht_find(struct hashtab *ht, struct allocator *al, const void *key, unsigned int size, bool *is_new){
    unsigned int hash = hash_func(key, size) % ht->nbuckets;

    return ht_find_with_hash(ht, al, hash, key, size, is_new);
}

struct ht_node *ht_find_lock(struct hashtab *ht, struct allocator *al,
                            const void *key, unsigned int size, bool *new, ht_lock_t **lock){
    unsigned int hash = hash_func(key, size) % ht->nlocks;
    struct ht_node *n = ht_find_with_hash(ht, al, hash, key, size, new);
    *lock = &ht->locks[hash];
    ht_lock_acquire(*lock);
    return n;
}

void *ht_retrieve(struct ht_node *n, unsigned int *psize){
    if (psize != NULL) {
        *psize = n->size;
    }
    return &n[1];
}

// Returns a pointer to the value
void *ht_insert(struct hashtab *ht, struct allocator *al,
                        const void *key, unsigned int size, bool *new){
    struct ht_node *n = ht_find(ht, al, key, size, new);
    return &n[1];
}

void ht_set_concurrent(struct hashtab *ht){
    assert(!ht->concurrent);
    ht->concurrent = true;
}

void ht_set_sequential(struct hashtab *ht){
    assert(ht->concurrent);
    ht->concurrent = false;
}

void ht_make_stable(struct hashtab *ht, unsigned int worker){
    assert(ht->concurrent);
    if (ht->old_buckets != NULL) {
        unsigned int first = (uint64_t) worker * ht->old_nbuckets / ht->nworkers;
        unsigned int last = (uint64_t) (worker + 1) * ht->old_nbuckets / ht->nworkers;
        ht_do_resize(ht, ht->old_nbuckets, ht->old_buckets, first, last);
    }
}

void ht_grow_prepare(struct hashtab *ht){
    assert(ht->concurrent);
    free(ht->old_buckets);
    for (unsigned int i = 0; i < ht->nworkers; i++) {
        ht->nobjects += ht->counts[i];
        ht->counts[i] = 0;
    }
    if (ht->nbuckets < ht->nobjects * 2) {
        ht->old_buckets = ht->buckets;
        ht->old_nbuckets = ht->nbuckets;
        ht->nbuckets = ht->nbuckets * 8;
        while (ht->nbuckets < ht->nobjects * 16) {
            ht->nbuckets *= 2;
        }
        ht->buckets = malloc(ht->nbuckets * sizeof(*ht->buckets));
    }
    else {
        ht->old_buckets = NULL;
        ht->old_nbuckets = 0;
    }
}

unsigned long ht_allocated(struct hashtab *ht){
    return ht->nbuckets * sizeof(*ht->buckets) +
            ht->nlocks * sizeof(*ht->locks);
}

bool ht_needs_to_grow(struct hashtab *ht){
    return 2 * atomic_load(&ht->rt_count) > ht->nbuckets;
}
