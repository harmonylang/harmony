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

// TODO.  Make iterative rather than recursive
// TODO.  free() doesn't work with allocator->alloc
void dict_assoc_delete(struct dict *dict, struct dict_assoc *node) {
	if (node->next) dict_assoc_delete(dict, node->next);
	free(node);
}

struct dict *dict_new(char *whoami, unsigned int value_len, unsigned int initial_size,
        unsigned int nworkers, bool align16) {
	struct dict *dict = new_alloc(struct dict);
    dict->whoami = whoami;
    dict->value_len = value_len;
	if (initial_size == 0) initial_size = 1024;
	if (initial_size == 0) initial_size = 1;
	dict->length = dict->old_length = initial_size;
	dict->count = dict->old_count = 0;
	dict->table = dict->old_table = calloc(sizeof(struct dict_bucket), initial_size);
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
    for (unsigned int i = 0; i < nworkers; i++) {
        dict->workers[i].unstable = calloc(sizeof(struct dict_unstable), nworkers);
    }
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

void dict_delete(struct dict *dict) {
	for (unsigned int i = 0; i < dict->length; i++) {
		if (dict->table[i].stable != NULL)
			dict_assoc_delete(dict, dict->table[i].stable);
		if (dict->table[i].unstable != NULL)
			dict_assoc_delete(dict, dict->table[i].unstable);
	}
	for (unsigned int i = 0; i < dict->nlocks; i++) {
		mutex_destroy(&dict->locks[i]);
    }
	free(dict->table);
	free(dict);
}

static inline void dict_reinsert_when_resizing(struct dict *dict, struct dict_assoc *k) {
    unsigned int n = hash_func((char *) &k[1] + dict->value_len, k->len) % dict->length;
	struct dict_bucket *db = &dict->table[n];
    k->next = db->stable;
    db->stable = k;
}

unsigned long dict_allocated(struct dict *dict) {
    return dict->length * sizeof(struct dict_bucket);
}

static void dict_resize(struct dict *dict, unsigned int newsize) {
	unsigned int o = dict->length;
	struct dict_bucket *old = dict->table;
	dict->table = calloc(sizeof(struct dict_bucket), newsize);
	dict->length = newsize;
	for (unsigned int i = 0; i < o; i++) {
		struct dict_bucket *b = &old[i];
        assert(b->unstable == NULL);
        struct dict_assoc *k = b->stable;
		b->stable = NULL;
		while (k != NULL) {
			struct dict_assoc *next = k->next;
			dict_reinsert_when_resizing(dict, k);
			k = next;
		}
	}
	free(old);
}

// Keep track of this unstable node in the list for the
// worker who's going to look at this bucket
static inline void dict_unstable(struct dict *dict, struct allocator *al,
                    unsigned int index, struct dict_assoc *k){
    unsigned int worker = index * dict->nworkers / dict->length;
    struct dict_worker *dw = &dict->workers[al->worker];
    struct dict_unstable *du = &dw->unstable[worker];
    if (du->next == du->len) {
        if (du->len == 0) {
            du->len = 1024;
        }
        else {
            du->len *= 2;
        }
        du->entries = realloc(du->entries, du->len);
    }
    du->entries[du->next++] = k;
    dw->count++;
}

// Perhaps the most performance critical function in the entire code base
struct dict_assoc *dict_find(struct dict *dict, struct allocator *al,
                const void *key, unsigned int keylen, bool *new){
    uint32_t hash = hash_func(key, keylen);

    // First see if the item is in the stable list, which does not require
    // a lock
    unsigned int index = hash % dict->length;
    struct dict_bucket *db = &dict->table[index];
	struct dict_assoc *k = db->stable;
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
        k = db->unstable;
        while (k != NULL) {
            if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
                mutex_release(&dict->locks[index % dict->nlocks]);
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
	if (!dict->concurrent && db->stable == NULL) {
		double f = (double)dict->count / (double)dict->length;
		if (f > dict->growth_threshold) {
			dict_resize(dict, dict->length * dict->growth_factor - 1);
			return dict_find(dict, al, key, keylen, new);
		}
	}

#ifdef HASHDICT_STATS
    (void) atomic_fetch_add(&dict->nmisses, 1);
#endif
    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    if (dict->concurrent) {
        k->next = db->unstable;
        db->unstable = k;
        mutex_release(&dict->locks[index % dict->nlocks]);
        dict_unstable(dict, al, index, k);
    }
    else {
        k->next = db->stable;
        db->stable = k;
		dict->count++;
    }

    if (new != NULL) {
        *new = true;
    }
	return k;
}

// Similar to dict_find(), but gets a lock on the bucket
struct dict_assoc *dict_find_lock(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keylen, bool *new, mutex_t **lock){
    assert(dict->concurrent);
    assert(al != NULL);
    uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;
    *lock = &dict->locks[index % dict->nlocks];

    struct dict_bucket *db = &dict->table[index];
	struct dict_assoc *k = db->stable;
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
            mutex_acquire(*lock);
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nstable_hits, 1);
#endif
			return k;
		}
		k = k->next;
	}

    mutex_acquire(*lock);
    // See if the item is in the unstable list
    k = db->unstable;
    while (k != NULL) {
        if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
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

    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    k->next = db->unstable;
    db->unstable = k;
    dict_unstable(dict, al, index, k);

    if (new != NULL) {
        *new = true;
    }
#ifdef HASHDICT_STATS
    (void) atomic_fetch_add(&dict->nmisses, 1);
#endif
	return k;
}

// Similar to dict_find_lock(), but gets a lock on the bucket only if it's a new node
struct dict_assoc *dict_find_lock_new(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keylen, bool *new, mutex_t **lock){
    assert(dict->concurrent);
    assert(al != NULL);
    uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;
    *lock = &dict->locks[index % dict->nlocks];

    struct dict_bucket *db = &dict->table[index];
	struct dict_assoc *k = db->stable;
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

    mutex_acquire(*lock);
    // See if the item is in the unstable list
    k = db->unstable;
    while (k != NULL) {
        if (k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
#ifdef HASHDICT_STATS
            (void) atomic_fetch_add(&dict->nunstable_hits, 1);
#endif
            mutex_release(*lock);
            return k;
        }
        k = k->next;
    }

    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    k->next = db->unstable;
    db->unstable = k;
    dict_unstable(dict, al, index, k);

    if (new != NULL) {
        *new = true;
    }
#ifdef HASHDICT_STATS
    (void) atomic_fetch_add(&dict->nmisses, 1);
#endif
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
    unsigned int index = hash % dict->length;
    struct dict_bucket *db = &dict->table[index];
	// __builtin_prefetch(db);

    // First look in the stable list, which does not require a lock
	struct dict_assoc *k = db->stable;
	while (k != NULL) {
		if (k->len == keylen && !memcmp((char *) &k[1] + dict->value_len, key, keylen)) {
            return * (void **) &k[1];
		}
		k = k->next;
	}

    // Look in the unstable list
    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);
        k = db->unstable;
        while (k != NULL) {
            if (k->len == keylen && !memcmp((char *) &k[1] + dict->value_len, key, keylen)) {
                mutex_release(&dict->locks[index % dict->nlocks]);
                return * (void **) &k[1];
            }
            k = k->next;
        }
        mutex_release(&dict->locks[index % dict->nlocks]);
    }

	return NULL;
}

void dict_iter(struct dict *dict, dict_enumfunc f, void *env) {
	for (unsigned int i = 0; i < dict->length; i++) {
        struct dict_bucket *db = &dict->table[i];
        struct dict_assoc *k = db->stable;
        while (k != NULL) {
            (*f)(env, (char *) &k[1] + dict->value_len, k->len, &k[1]);
            k = k->next;
        }
        if (dict->concurrent) {
            mutex_acquire(&dict->locks[i % dict->nlocks]);
            k = db->unstable;
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
    dict->concurrent = true;
}

// When going from concurrent to sequential, need to move over
// the unstable values.
void dict_make_stable(struct dict *dict, unsigned int worker){
    assert(dict->concurrent);

    if (dict->length != dict->old_length) {
#ifdef OLD
        unsigned int first = (uint64_t) worker * dict->old_length / dict->nworkers;
        unsigned int last = (uint64_t) (worker + 1) * dict->old_length / dict->nworkers;
        for (unsigned i = first; i < last; i++) {
            struct dict_bucket *b = &dict->old_table[i];
            struct dict_assoc *k = b->stable;
            while (k != NULL) {
                struct dict_assoc *next = k->next;
                dict_reinsert_when_resizing(dict, k);
                k = next;
            }
        }
#endif
        for (unsigned i = worker; i < dict->old_length; i += dict->nworkers) {
            struct dict_bucket *b = &dict->old_table[i];
            struct dict_assoc *k = b->stable;
            while (k != NULL) {
                struct dict_assoc *next = k->next;
                dict_reinsert_when_resizing(dict, k);
                k = next;
            }
        }
    }

	for (unsigned int i = 0; i < dict->nworkers; i++) {
        struct dict_worker *dw = &dict->workers[i];
        struct dict_unstable *du = &dw->unstable[worker];
        for (unsigned int j = 0; j < du->next; j++) {
            struct dict_assoc *k = du->entries[j];
            uint32_t hash = hash_func((char *) &k[1] + dict->value_len, k->len);
            unsigned int index = hash % dict->length;
            struct dict_bucket *db = &dict->table[index];
            k->next = db->stable;
            db->stable = k;
            if (dict->table == dict->old_table) {   // Maybe place outside loops
                db->unstable = NULL;
            }
        }
        du->next = 0;
    }
}

// Figure out how much this dictionary should grow by adding up the
// unstable entries.  The actual rehashing happens later.
void dict_grow_prepare(struct dict *dict){
    assert(dict->concurrent);

    if (dict->old_table != dict->table) {
        free(dict->old_table);
        dict->old_table = dict->table;
    }
    dict->old_count = dict->count;
    dict->old_length = dict->length;
    dict->old_table = dict->table;

    unsigned int total = 0;
	for (unsigned int i = 0; i < dict->nworkers; i++) {
        struct dict_worker *dw = &dict->workers[i];
        total += dw->count;
        dw->count = 0;
    }
    dict->count += total;
	if ((double) dict->count / dict->length > dict->growth_threshold) {
        int factor = dict->growth_factor;
        while (factor * dict->length < dict->count) {
            factor++;
        }
        dict->length *= factor;
        dict->table = calloc(sizeof(struct dict_bucket), dict->length);
    }
}

void dict_dump(struct dict *dict){
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
