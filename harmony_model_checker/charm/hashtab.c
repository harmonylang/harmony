#include "head.h"
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include "global.h"
#include "hashtab.h"
// #include "komihash.h"

#define GROW_THRESHOLD   2
#define GROW_FACTOR      8

#ifdef _WIN32

#include <intrin.h>
static inline uint64_t get_cycles(){
    return __rdtsc();
}

//  Linux/GCC
#else

#ifdef notdef
static inline uint64_t get_cycles(){
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t) hi << 32) | lo;
}

static inline uint64_t get_cycles(){
    uint64_t msr;
    asm volatile ( "rdtsc\n\t"    // Returns the time in EDX:EAX.
               "shl $32, %%rdx\n\t"  // Shift the upper bits left.
               "or %%rdx, %0"        // 'Or' in the lower bits.
               : "=a" (msr)
               :
               : "rdx");
    return msr;
}
#endif

static inline void rdtscp(uint64_t *cycles, uint64_t *pid) {
  // rdtscp
  // high cycles : edx
  // low cycles  : eax
  // processor id: ecx

  asm volatile
    (
     // Assembleur
     "rdtscp;\n"
     "shl $32, %%rdx;\n"
     "or %%rdx, %%rax;\n"
     "mov %%rax, (%[_cy]);\n"
     "mov %%ecx, (%[_pid]);\n"

     // outputs
     :

     // inputs
     :
     [_cy] "r" (cycles),
     [_pid] "r" (pid)

     // clobbers
     :
     "cc", "memory", "%eax", "%edx", "%ecx"
     );

  return;
}

static inline uint64_t get_cycles(){
    uint64_t cycles, pid;

    rdtscp(&cycles, &pid);
    return cycles;
}

#endif

// #define hash_func(key, size) komihash(key, size, 0)
#define hash_func(key, size) meiyan(key, size)
// #define hash_func(key, size) djb2(key, size)

#ifdef NOT_NEEDED
static inline unsigned long djb2(const char *key, int count) {
     unsigned long hash = 0;

     while (count-- > 0) {
          hash = (hash * 33) ^ *key++;
     }
     return hash;
}
#endif

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
if (true) return 0; // TODO
	return h ^ (h >> 16);
}

struct hashtab *ht_new(char *whoami, unsigned int value_size, unsigned int nbuckets,
        unsigned int nworkers, bool align16) {
#ifdef CACHE_LINE_ALIGNED
    assert(sizeof(struct ht_unstable) == 64);
#endif
    struct hashtab *ht = new_alloc(struct hashtab);
    ht->whoami = whoami;
    ht->align16 = align16;
    ht->value_size = value_size;
	if (nbuckets == 0) {
        nbuckets = 1024;
    }
nbuckets = 1;  // TODO
    ht->nbuckets = nbuckets;
    ht->stable = calloc(nbuckets, sizeof(*ht->stable));
#ifdef ALIGNED_ALLOC
    ht->unstable = aligned_alloc(64, nbuckets * sizeof(*ht->unstable));
#else
    ht->unstable = malloc(nbuckets * sizeof(*ht->unstable));
#endif
    for (unsigned int i = 0; i < nbuckets; i++) {
        atomic_init(&ht->unstable[i].list, NULL);
    }
    ht->nlocks = nworkers * 256;        // TODO: how much?
#ifdef ALIGNED_ALLOC
    ht->locks = aligned_alloc(sizeof(*ht->locks), ht->nlocks * sizeof(*ht->locks));
#else
    ht->locks = malloc(ht->nlocks * sizeof(*ht->locks));
#endif
	for (unsigned int i = 0; i < ht->nlocks; i++) {
		ht_lock_init(&ht->locks[i]);
	}
    ht->nworkers = nworkers;
    ht->counts = calloc(nworkers, sizeof(*ht->counts));
    ht->cycles = calloc(nworkers, sizeof(*ht->cycles));
#ifndef USE_ATOMIC
    mutex_init(&ht->mutex);
#endif
    atomic_init(&ht->unstable_count, 0);
    return ht;
}

struct ht_node *ht_quick(struct hashtab *ht, const void *key, unsigned int size, unsigned int hs) {
    unsigned int hash = hash_func(key, size) % ht->nbuckets;
    assert(hash == hs);
    struct ht_node *hn = ht->stable[hash % ht->nbuckets];
    while (hn != NULL) {
        if (hn->size == size && memcmp((char *) &hn[1] + ht->value_size, key, size) == 0) {
            return hn;
        }
        hn = hn->next.stable;
    }
    assert(false);
}

void ht_do_resize(struct hashtab *ht,
        unsigned int old_nbuckets,
        struct ht_node **old_stable,
        struct ht_unstable *old_unstable,
        unsigned int first, unsigned int last){
    unsigned int factor = ht->nbuckets / old_nbuckets;
    if (factor == 0) {      // deal with shrinking tables
        factor = 1;
    }
    for (unsigned int i = first; i < last; i++) {
        unsigned int k = i;
        for (unsigned int j = 0; j < factor; j++) {
            ht->stable[k] = NULL;
            atomic_init(&ht->unstable[k].list, NULL);
            k += old_nbuckets;
        }

        // Move the old stable entries into the new stable buckets
        struct ht_node *n = old_stable[i], *next;
        for (; n != NULL; n = next) {
            next = n->next.stable;
            unsigned int hash = hash_func((char *) &n[1] + ht->value_size, n->size) % ht->nbuckets;
            n->next.stable = ht->stable[hash];
            ht->stable[hash] = n;
        }

        // Move the old unstable entries over into the new stable buckets
        n = atomic_load(&old_unstable[i].list);
        for (; n != NULL; n = next) {
            next = atomic_load(&n->next.unstable);
            unsigned int hash = hash_func((char *) &n[1] + ht->value_size, n->size) % ht->nbuckets;
            n->next.stable = ht->stable[hash];
            ht->stable[hash] = n;
        }
    }
}

void ht_resize(struct hashtab *ht, unsigned int nbuckets){
    struct ht_node **old_stable = ht->stable;
    struct ht_unstable *old_unstable = ht->unstable;
    unsigned int old_nbuckets = ht->nbuckets;
    ht->stable = malloc(nbuckets * sizeof(*ht->stable));
#ifdef ALIGNED_ALLOC
    ht->unstable = aligned_alloc(64, nbuckets * sizeof(*ht->unstable));
#else
    ht->unstable = malloc(nbuckets * sizeof(*ht->unstable));
#endif
    ht->nbuckets = nbuckets;
    ht_do_resize(ht, old_nbuckets, old_stable, old_unstable, 0, old_nbuckets);
}

// TODO.  is_new is not terribly useful.
struct ht_node *ht_find_with_hash(struct hashtab *ht, struct allocator *al, unsigned int hash, const void *key, unsigned int size, bool *is_new){
    uint64_t before = get_cycles();

    // First check the (read-only at this point) stable list
    struct ht_node *hn = ht->stable[hash % ht->nbuckets];
    while (hn != NULL) {
        if (hn->size == size && memcmp((char *) &hn[1] + ht->value_size, key, size) == 0) {
            if (is_new != NULL) {
                *is_new = false;
            }
            if (al != NULL) {
                uint64_t after = get_cycles();
                ht->cycles[al->worker] += after - before;
            }
            return hn;
        }
        hn = hn->next.stable;
    }

#ifdef USE_ATOMIC

    // First do a search
    hAtomic(struct ht_node *) *chain = &ht->unstable[hash % ht->nbuckets].list;

    assert(atomic_load(chain) == 0 || atomic_load(chain) != 0);
    for (;;) {
        struct ht_node *expected = atomic_load(chain);
        if (expected == NULL) {
            break;
        }
        if (expected->size == size && memcmp((char *) &expected[1] + ht->value_size, key, size) == 0) {
            if (is_new != NULL) {
                *is_new = false;
            }
            if (al != NULL) {
                uint64_t after = get_cycles();
                ht->cycles[al->worker] += after - before;
            }
            return expected;
        }
        chain = &expected->next.unstable;
    }

    // Allocate a new node
    unsigned int total = sizeof(struct ht_node) + ht->value_size + size;
	struct ht_node *desired = al == NULL ?
            malloc(total) : (*al->alloc)(al->ctx, total, false, ht->align16);
    atomic_init(&desired->next.unstable, NULL);
    desired->size = size;
    if (ht->value_size > 0) {
        memset(&desired[1], 0, ht->value_size);
    }
    memcpy((char *) &desired[1] + ht->value_size, key, size);

    // Insert the node
    for (;;) {
        struct ht_node *expected = NULL;
        if (atomic_compare_exchange_strong(chain, &expected, desired)) {
            atomic_fetch_add(&ht->unstable_count, 1);
            if (ht->concurrent) {
                assert(al != NULL);
                ht->counts[al->worker]++;
            }
            if (is_new != NULL) {
                *is_new = true;
            }
            if (al != NULL) {
                assert(ht->concurrent);
                uint64_t after = get_cycles();
                ht->cycles[al->worker] += after - before;
            }
            else {
                assert(!ht->concurrent);
                ht->nobjects++;
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
            if (al != NULL) {
                uint64_t after = get_cycles();
                ht->cycles[al->worker] += after - before;
            }
            return expected;
        }
        chain = &expected->next.unstable;
    }

#else // USE_ATOMIC

    mutex_acquire(&ht->locks[hash % ht->nlocks]);
    struct ht_node **pn = &ht->unstable[hash % ht->nbuckets].list, *n;
    while ((n = *pn) != NULL) {
        if (n->size == size && memcmp((char *) &n[1] + ht->value_size, key, size) == 0) {
            break;
        }
        pn = &n->next.unstable;
    }
    if (n == NULL) {
        // Allocate a new node
        unsigned int total = sizeof(struct ht_node) + ht->value_size + size;
        n = al == NULL ? malloc(total) :
                (*al->alloc)(al->ctx, total, false, ht->align16);
        n->next.unstable = NULL;
        n->size = size;
        if (ht->value_size > 0) {
            memset(&n[1], 0, ht->value_size);
        }
        memcpy((char *) &n[1] + ht->value_size, key, size);
        *pn = n;
        ht->unstable_count++;
        if (ht->concurrent) {
            assert(al != NULL);
            ht->counts[al->worker]++;
        }
        mutex_release(&ht->locks[hash % ht->nlocks]);
        if (is_new != NULL) {
            *is_new = true;
        }
    }
    else {
        mutex_release(&ht->locks[hash % ht->nlocks]);
        if (is_new != NULL) {
            *is_new = false;
        }
    }
    if (al != NULL) {
        uint64_t after = get_cycles();
        ht->cycles[al->worker] += after - before;
    }
    return n;

#endif // USE_ATOMIC
}

struct ht_node *ht_find(struct hashtab *ht, struct allocator *al, const void *key, unsigned int size, bool *is_new){
    unsigned int hash = hash_func(key, size);
    return ht_find_with_hash(ht, al, hash, key, size, is_new);
}

struct ht_node *ht_find_lock(struct hashtab *ht, struct allocator *al,
                            const void *key, unsigned int size, bool *new, ht_lock_t **lock){
    unsigned int hash = hash_func(key, size);
    struct ht_node *n = ht_find_with_hash(ht, al, hash, key, size, new);
    *lock = &ht->locks[hash % ht->nlocks];
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
    assert(memcmp((char *) &n[1] + ht->value_size, key, size) == 0);
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
    if (ht->old_unstable != NULL) {
        unsigned int first = (uint64_t) worker * ht->old_nbuckets / ht->nworkers;
        unsigned int last = (uint64_t) (worker + 1) * ht->old_nbuckets / ht->nworkers;
        ht_do_resize(ht, ht->old_nbuckets, ht->old_stable, ht->old_unstable, first, last);
    }
}

void ht_grow_prepare(struct hashtab *ht){
    assert(ht->concurrent);
    free(ht->old_stable);
    free(ht->old_unstable);

    unsigned int n_unstable = atomic_load(&ht->unstable_count);
    printf("GROW %s %u %u %u\n", ht->whoami, n_unstable, ht->nbuckets, n_unstable * GROW_THRESHOLD);
    if (ht->nbuckets < n_unstable * GROW_THRESHOLD) {
        printf("DO GROW\n");
        ht->old_nbuckets = ht->nbuckets;
        ht->old_stable = ht->stable;
        ht->old_unstable = ht->unstable;
        ht->nbuckets = ht->nbuckets * 4;
        while (ht->nbuckets < n_unstable * GROW_FACTOR) {
            ht->nbuckets *= 2;
        }
        ht->stable = malloc(ht->nbuckets * sizeof(*ht->stable));
#ifdef ALIGNED_ALLOC
        ht->unstable = aligned_alloc(64, ht->nbuckets * sizeof(*ht->unstable));
#else
        ht->unstable = malloc(ht->nbuckets * sizeof(*ht->unstable));
#endif
        ht->stable_count += atomic_load(&ht->unstable_count);
        atomic_store(&ht->unstable_count, 0);
        printf("PREP DONE\n");
    }
    else {
        printf("SKIP GROW\n");
        ht->old_nbuckets = 0;
        ht->old_stable = NULL;
        ht->old_unstable = NULL;
    }
}

unsigned long ht_allocated(struct hashtab *ht){
    return ht->nbuckets * (sizeof(*ht->stable) +
                            sizeof(*ht->unstable)) +
            ht->nlocks * sizeof(*ht->locks);
}

bool ht_needs_to_grow(struct hashtab *ht){
#ifdef USE_ATOMIC
    return GROW_THRESHOLD * atomic_load(&ht->unstable_count) > ht->nbuckets;
#else
    mutex_acquire(&ht->mutex);
    bool r =  GROW_THRESHOLD * ht->unstable_count > ht->nbuckets;
    mutex_release(&ht->mutex);
    return r;
#endif
}
