#include "head.h"

#include <assert.h>
#include <stdio.h>
#include <stdbool.h>

#ifdef USE_ATOMIC
#include <stdatomic.h>
#endif

#include "global.h"
#include "hashdict.h"
#include "thread.h"

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

static inline struct dict_assoc *dict_assoc_new(struct dict *dict,
        struct allocator *al, char *key, unsigned int len, uint32_t hash){
    unsigned int total = sizeof(struct dict_assoc) + dict->value_len + len;
	struct dict_assoc *k = al == NULL ?  malloc(total) :
                        (*al->alloc)(al->ctx, total, false, dict->align16);
    memset(k, 0, sizeof(*k) + dict->value_len);
	k->len = len;
	memcpy((char *) &k[1] + dict->value_len, key, len);
	return k;
}

// TODO.  free() doesn't work with allocator->alloc
void dict_assoc_delete(struct dict_assoc *k) {
    while (k != NULL) {
        struct dict_assoc *next = k->next;
        free(k);
        k = next;
    }
}

struct dict *dict_new(char *whoami, unsigned int value_len, unsigned int initial_size,
        unsigned int nworkers, bool align16) {
	struct dict *dict = new_alloc(struct dict);
    dict->whoami = whoami;
    dict->value_len = value_len;
	if (initial_size == 0) initial_size = 1024;
	if (initial_size == 0) initial_size = 1;
	dict->stable.length = dict->unstable.length = initial_size;
	dict->old_stable.length = dict->old_unstable.length = 0;
    dict->stable.buckets = calloc(sizeof(struct dict_assoc *), initial_size);
    dict->unstable.buckets = calloc(sizeof(struct dict_assoc *), initial_size);
    dict->nlocks = nworkers * 64;        // TODO: how much?
    dict->locks = malloc(dict->nlocks * sizeof(mutex_t));
	for (unsigned int i = 0; i < dict->nlocks; i++) {
		mutex_init(&dict->locks[i]);
	}
	dict->growth_threshold = 2;
	dict->growth_factor = 10;
	dict->concurrent = false;
    dict->workers = calloc(sizeof(struct dict_worker), nworkers);
    dict->nworkers = nworkers;
    dict->align16 = align16;
#ifdef HASHDICT_STATS
    atomic_init(&dict->nstable_hits, 0);
    atomic_init(&dict->nunstable_hits, 0);
    atomic_init(&dict->nmisses, 0);
#endif
	return dict;
}

bool dict_remove(struct dict *dict, const void *key, unsigned int keylen){
    assert(false);
    return false;
}

static void dict_table_delete(struct dict_table *dt) {
	for (unsigned int i = 0; i < dt->length; i++) {
        dict_assoc_delete(dt->buckets[i]);
    }
    free(dt->buckets);
}

void dict_delete(struct dict *dict) {
    dict_table_delete(&dict->stable);
    dict_table_delete(&dict->unstable);
    dict_table_delete(&dict->old_stable);
    dict_table_delete(&dict->old_unstable);
	for (unsigned int i = 0; i < dict->nlocks; i++) {
		mutex_destroy(&dict->locks[i]);
    }
	free(dict);
}

static inline void dict_reinsert_when_resizing(struct dict *dict, struct dict_table *dt, struct dict_assoc *k) {
    unsigned int n = hash_func((char *) &k[1] + dict->value_len, k->len) % dt->length;
	struct dict_assoc **bucket = &dt->buckets[n];
    k->next = *bucket;
    *bucket = k;
}

static unsigned long dict_table_allocated(struct dict_table *dt) {
    if (dt == NULL) {
        return 0;
    }
    return dt->length * sizeof(*dt->buckets);
}

unsigned long dict_allocated(struct dict *dict) {
    return dict_table_allocated(&dict->stable)
         + dict_table_allocated(&dict->unstable)
         + dict_table_allocated(&dict->old_stable)
         + dict_table_allocated(&dict->old_unstable);
}

static void dict_resize(struct dict *dict, struct dict_table *dt, unsigned int newsize) {
	unsigned int oldsize = dt->length;
	struct dict_assoc **old = dt->buckets;
	dt->buckets = calloc(sizeof(*dt->buckets), newsize);
	dt->length = newsize;
	for (unsigned int i = 0; i < oldsize; i++) {
        struct dict_assoc *k = old[i];
		while (k != NULL) {
			struct dict_assoc *next = k->next;
			dict_reinsert_when_resizing(dict, dt, k);
			k = next;
		}
	}
	free(old);
}

// Perhaps the most performance critical function in the entire code base
struct dict_assoc *dict_find(struct dict *dict, struct allocator *al,
                const void *key, unsigned int keylen, bool *new){
    uint32_t hash = hash_func(key, keylen);

    // First see if the item is in the stable list, which does not require
    // a lock
    unsigned int index = hash % dict->stable.length;
    struct dict_assoc *k = dict->stable.buckets[index];
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nstable_hits, 1);
#endif
			return k;
		}
		k = k->next;
	}

    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);

        // See if the item is in the unstable list
        index = hash % dict->unstable.length;
        k = dict->unstable.buckets[index];
        while (k != NULL) {
            if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
                mutex_release(&dict->locks[index % dict->nlocks]);
                dict->workers[al->worker].clashes++;
                if (new != NULL) {
                    *new = false;
                }
#ifdef HASHDICT_STATS
                (void) atomic_fetch_add(&dict->nunstable_hits, 1);
#endif
                return k;
            }
            k = k->next;
        }
    }

    // If not concurrent may have to grow the table now
	else {
        struct dict_table *dt = &dict->stable;
		double f = (double) dt->count / (double) dt->length;
		if (f > dict->growth_threshold) {
			dict_resize(dict, dt, dt->length * dict->growth_factor - 1);
			return dict_find(dict, al, key, keylen, new);
		}
	}

#ifdef HASHDICT_STATS
    (void) atomic_fetch_add(&dict->nmisses, 1);
#endif
    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    k->next = dict->unstable.buckets[index];
    dict->unstable.buckets[index] = k;
    if (dict->concurrent) {
        dict->workers[al->worker].unstable_count++;
        mutex_release(&dict->locks[index % dict->nlocks]);
    }
    else {
		dict->stable.count++;
    }

    if (new != NULL) {
        *new = true;
    }
	return k;
}

// Similar to dict_find(), but gets a lock on the bucket
struct dict_assoc *dict_find_lock(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keylen, bool *new, mutex_t **lock){
    uint32_t hash = hash_func(key, keylen);

    // First see if the item is in the stable list, which does not require
    // a lock
    unsigned int index = hash % dict->stable.length;
    struct dict_assoc *k = dict->stable.buckets[index];
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nstable_hits, 1);
#endif
            mutex_acquire(&dict->locks[index % dict->nlocks]);
			return k;
		}
		k = k->next;
	}

    mutex_acquire(&dict->locks[index % dict->nlocks]);

    // See if the item is in the unstable list
    index = hash % dict->unstable.length;
    k = dict->unstable.buckets[index];
    while (k != NULL) {
        if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            dict->workers[al->worker].clashes++;
            if (new != NULL) {
                *new = false;
            }
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nunstable_hits, 1);
#endif
            return k;
        }
        k = k->next;
    }

#ifdef HASHDICT_STATS
    (void) atomic_fetch_add(&dict->nmisses, 1);
#endif
    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    k->next = dict->unstable.buckets[index];
    dict->unstable.buckets[index] = k;
    dict->workers[al->worker].unstable_count++;

    if (new != NULL) {
        *new = true;
    }
	return k;
}

// Similar to dict_find_lock(), but gets a lock on the bucket only if it's a new node
struct dict_assoc *dict_find_lock_new(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keylen, bool *new, mutex_t **lock){
    uint32_t hash = hash_func(key, keylen);

    // First see if the item is in the stable list, which does not require
    // a lock
    unsigned int index = hash % dict->stable.length;
    struct dict_assoc *k = dict->stable.buckets[index];
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            *new = false;
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nstable_hits, 1);
#endif
			return k;
		}
		k = k->next;
	}

    mutex_acquire(&dict->locks[index % dict->nlocks]);

    // See if the item is in the unstable list
    index = hash % dict->unstable.length;
    k = dict->unstable.buckets[index];
    while (k != NULL) {
        if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            mutex_release(&dict->locks[index % dict->nlocks]);
            dict->workers[al->worker].clashes++;
            *new = false;
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nunstable_hits, 1);
#endif
            return k;
        }
        k = k->next;
    }

#ifdef HASHDICT_STATS
    (void) atomic_fetch_add(&dict->nmisses, 1);
#endif
    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    k->next = dict->unstable.buckets[index];
    dict->unstable.buckets[index] = k;
    dict->workers[al->worker].unstable_count++;

    *new = true;
	return k;
}

// Returns a pointer to the value
void *dict_insert(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keylen, bool *new){
    struct dict_assoc *k = dict_find(dict, al, key, keylen, new);
    return (char *) &k[1];
}

void *dict_retrieve(const void *p, unsigned int *psize){
    const struct dict_assoc *k = p;
    if (psize != NULL) {
        *psize = k->len;
    }
    return (char *) &k[1];
}

// This assumes that the value is a pointer.  Returns NULL if there is
// no entry but does not create an entry.
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen) {
    uint32_t hash = hash_func(key, keylen);

    // First see if the item is in the stable list, which does not require
    // a lock
    unsigned int index = hash % dict->stable.length;
    struct dict_assoc *k = dict->stable.buckets[index];
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nstable_hits, 1);
#endif
			return k;
		}
		k = k->next;
	}

    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);

        // See if the item is in the unstable list
        index = hash % dict->unstable.length;
        k = dict->unstable.buckets[index];
        while (k != NULL) {
            if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
                mutex_release(&dict->locks[index % dict->nlocks]);
#ifdef HASHDICT_STATS
                (void) atomic_fetch_add(&dict->nunstable_hits, 1);
#endif
                return k;
            }
            k = k->next;
        }
    }

	return NULL;
}

void dict_iter(struct dict *dict, dict_enumfunc f, void *env) {
	for (unsigned int i = 0; i < dict->stable.length; i++) {
        struct dict_assoc *k = dict->stable.buckets[i];
        while (k != NULL) {
            (*f)(env, (char *) &k[1] + dict->value_len, k->len, &k[1]);
            k = k->next;
        }
    }

    if (dict->concurrent) {
        for (unsigned int i = 0; i < dict->unstable.length; i++) {
            mutex_acquire(&dict->locks[i % dict->nlocks]);
            struct dict_assoc *k = dict->unstable.buckets[i];
            while (k != NULL) {
                (*f)(env, (char *) &k[1] + dict->value_len, k->len, &k[1]);
                k = k->next;
            }
            mutex_release(&dict->locks[i % dict->nlocks]);
        }
	}
}

// Switch to concurrent mode
void dict_set_concurrent(struct dict *dict) {
    assert(!dict->concurrent);

    // Free any old tables
    if (dict->old_stable.buckets != NULL) {
        free(dict->old_stable.buckets);
        dict->old_stable.buckets = NULL;
    }
    if (dict->old_unstable.buckets != NULL) {
        free(dict->old_unstable.buckets);
        dict->old_unstable.buckets = NULL;
    }
    dict->old_stable.count = dict->old_stable.length = 0;
    dict->old_unstable.count = dict->old_unstable.length = 0;

    dict->concurrent = true;
}

// Move entries from one table into the other.
static void dict_reinsert(struct dict *dict, unsigned int worker,
                        struct dict_table *src, struct dict_table *dst) {
    // Figure out which part this worker is going to redistribute
    unsigned int first = (uint64_t) worker * src->length / dict->nworkers;
    unsigned int last = (uint64_t) (worker + 1) * src->length / dict->nworkers;
    for (unsigned i = first; i < last; i++) {
        struct dict_assoc *k = src->buckets[i];
        while (k != NULL) {
            struct dict_assoc *next = k->next;
            dict_reinsert_when_resizing(dict, dst, k);
            k = next;
        }
        src->buckets[i] = NULL;
    }
}

// When going from concurrent to sequential, need to move over
// the unstable values.  Each worker calls this function.
void dict_make_stable(struct dict *dict, unsigned int worker){
    assert(dict->concurrent);

    // See if the table was grown
    struct dict_table *dt = &dict->old_stable;
    if (dt->buckets != NULL) {
        dict_reinsert(dict, worker, dt, &dict->stable);
    }

    // Now move unstable entries into the stable table
    dict_reinsert(dict, worker, &dict->unstable, &dict->stable);
}

// Figure out how much this dictionary should grow by adding up the
// unstable entries.  The actual rehashing happens later.
void dict_grow_prepare(struct dict *dict){
    assert(dict->concurrent);

    // Update the #entries in the unstable table
    unsigned int unstable_count = 0;
	for (unsigned int i = 0; i < dict->nworkers; i++) {
        struct dict_worker *dw = &dict->workers[i];
        unstable_count += dw->unstable_count;
        dw->unstable_count = 0;
    }
    dict->unstable.count = unstable_count;

    // See if we need to grow the stable table
    unsigned int total = dict->stable.count + dict->unstable.count;
	if ((double) total / dict->stable.length > dict->growth_threshold) {
        int factor = dict->growth_factor;
        while (factor * dict->stable.length < total) {
            factor++;
        }
        dict->old_stable.buckets = dict->stable.buckets;
        dict->old_stable.length = dict->stable.length;
        dict->old_stable.count = dict->stable.count;
        dict->stable.length *= factor;
        dict->stable.buckets = calloc(sizeof(*dict->stable.buckets), dict->stable.length);
        dict->stable.count = total;
    }
}

void dict_dump(struct dict *dict){
    unsigned int clashes = 0;
    for (unsigned int i = 0; i < dict->nworkers; i++) {
        struct dict_worker *dw = &dict->workers[i];
        clashes += dw->clashes;
    }
    printf("%s: %u clashes\n", dict->whoami, clashes);
}

void dict_set_sequential(struct dict *dict) {
    assert(dict->concurrent);

#ifdef notdef
    // check integrity
    struct dict_bucket *db = dict->table;
    unsigned int total = 0;
	for (unsigned int i = 0; i < dict->length; i++, db++) {
        if (db->unstable != NULL) {
            printf("BAD DICT %s\n", dict->whoami);
        }
        for (struct dict_assoc *k = db->stable; k != NULL; k = k->next) {
            total++;
        }
    }
    if (total != dict->count) {
        printf("DICT: bad total %s\n", dict->whoami);
    }
#endif

    dict->concurrent = false;
}
