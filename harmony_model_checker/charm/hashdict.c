#include "head.h"

#include <assert.h>
#include <stdio.h>
#include <stdbool.h>

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
    k->hash = hash;
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
	dict->length = dict->old_length = initial_size;
	dict->count = dict->old_count = 0;
	dict->stable = dict->old_stable = calloc(sizeof(*dict->stable), initial_size);
	dict->unstable = dict->old_unstable = calloc(sizeof(*dict->unstable), initial_size);
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
        dict->workers[i].unstable = calloc(sizeof(struct dict_assoc *), nworkers);
    }
    dict->align16 = align16;
	return dict;
}

bool dict_remove(struct dict *dict, const void *key, unsigned int keylen){
    assert(false);
    return false;
}

void dict_delete(struct dict *dict) {
	for (unsigned int i = 0; i < dict->length; i++) {
		if (dict->stable[i] != NULL)
			dict_assoc_delete(dict, dict->stable[i]);
		if (dict->unstable[i] != NULL)
			dict_assoc_delete(dict, dict->unstable[i]);
	}
	for (unsigned int i = 0; i < dict->nlocks; i++) {
		mutex_destroy(&dict->locks[i]);
    }
	free(dict->stable);
	free(dict->unstable);
	free(dict);
}

static inline void dict_reinsert_when_resizing(struct dict *dict, struct dict_assoc *k) {
    // unsigned int n = hash_func((char *) &k[1] + dict->value_len, k->len) % dict->length;
    unsigned int n = k->hash % dict->length;
	struct dict_assoc **db = &dict->stable[n];
    k->next = *db;
    *db = k;
}

unsigned long dict_allocated(struct dict *dict) {
    return dict->length * (sizeof(*dict->stable) + sizeof(*dict->unstable));
}

static void dict_resize(struct dict *dict, unsigned int newsize) {
	unsigned int o = dict->length;
	struct dict_assoc **old_stable = dict->stable;
	struct dict_assoc **old_unstable = dict->unstable;
	dict->stable = calloc(sizeof(*dict->stable), newsize);
	dict->unstable = calloc(sizeof(*dict->unstable), newsize);
	dict->length = newsize;
	for (unsigned int i = 0; i < o; i++) {
        assert(old_unstable[i] == NULL);
		struct dict_assoc **b = &old_stable[i];
        struct dict_assoc *k = *b;
		*b = NULL;
		while (k != NULL) {
			struct dict_assoc *next = k->next;
			dict_reinsert_when_resizing(dict, k);
			k = next;
		}
	}
	free(old_stable);
	free(old_unstable);
}

// Perhaps the most performance critical function in the entire code base
struct dict_assoc *dict_find(struct dict *dict, struct allocator *al,
                const void *key, unsigned int keylen, bool *new){
    uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;
    struct dict_assoc **db = &dict->stable[index];

    // First see if the item is in the stable list, which does not require
    // a lock
	struct dict_assoc *k = *db;
	while (k != NULL) {
		if (k->hash == hash && k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
			return k;
		}
		k = k->next;
	}

    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);

        // See if the item is in the unstable list
        db = &dict->unstable[index];
        k = *db;
        while (k != NULL) {
            if (k->hash == hash && k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
                mutex_release(&dict->locks[index % dict->nlocks]);
                dict->workers[al->worker].clashes++;
                if (new != NULL) {
                    *new = false;
                }
                return k;
            }
            k = k->next;
        }
    }

    // If not concurrent may have to grow the table now
	if (!dict->concurrent && dict->stable[index] == NULL) {
		double f = (double)dict->count / (double)dict->length;
		if (f > dict->growth_threshold) {
			dict_resize(dict, dict->length * dict->growth_factor - 1);
			return dict_find(dict, al, key, keylen, new);
		}
	}

    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    if (dict->concurrent) {
        db = &dict->unstable[index];
        k->next = *db;
        *db = k;
        mutex_release(&dict->locks[index % dict->nlocks]);

        // Keep track of this unstable node in the list for the
        // worker who's going to look at this bucket
        unsigned int worker = index * dict->nworkers / dict->length;
        struct dict_worker *dw = &dict->workers[al->worker];
        k->unstable_next = dw->unstable[worker];
        dw->unstable[worker] = k;
        dw->count++;
    }
    else {
        db = &dict->stable[index];
        k->next = *db;
        *db = k;
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
    uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;
    struct dict_assoc **db = &dict->stable[index];
    *lock = &dict->locks[index % dict->nlocks];

	struct dict_assoc *k = *db;
	while (k != NULL) {
		if (k->hash == hash && k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
            // mutex_acquire(*lock);
			return k;
		}
		k = k->next;
	}

    unsigned int worker = index * dict->nworkers / dict->length;
    struct dict_worker *dw = &dict->workers[al->worker];

    mutex_acquire(*lock);
    // See if the item is in the unstable list
    db = &dict->unstable[index];
    k = *db;
    while (k != NULL) {
        if (k->hash == hash && k->len == keylen && memcmp((char *) &k[1] + dict->value_len, key, keylen) == 0) {
            dict->workers[al->worker].clashes++;
            if (new != NULL) {
                *new = false;
            }
            mutex_release(*lock);
            return k;
        }
        k = k->next;
    }

    k = dict_assoc_new(dict, al, (char *) key, keylen, hash);
    k->next = *db;
    *db = k;

    // Keep track of this unstable node in the list for the
    // worker who's going to look at this bucket
    k->unstable_next = dw->unstable[worker];
    dw->unstable[worker] = k;
    dw->count++;

    mutex_release(*lock);

    if (new != NULL) {
        *new = true;
    }
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
    struct dict_assoc **db = &dict->stable[index];
	// __builtin_prefetch(db);

    // First look in the stable list, which does not require a lock
	struct dict_assoc *k = *db;
	while (k != NULL) {
		if (k->hash == hash && k->len == keylen && !memcmp((char *) &k[1] + dict->value_len, key, keylen)) {
            return * ((void **) &k[1]);
		}
		k = k->next;
	}

    // Look in the unstable list
    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);
        db = &dict->unstable[index];
        k = *db;
        while (k != NULL) {
            if (k->hash == hash && k->len == keylen && !memcmp((char *) &k[1] + dict->value_len, key, keylen)) {
                mutex_release(&dict->locks[index % dict->nlocks]);
                return * ((void **) &k[1]);
            }
            k = k->next;
        }
        mutex_release(&dict->locks[index % dict->nlocks]);
    }

	return NULL;
}

void dict_iter(struct dict *dict, dict_enumfunc f, void *env) {
	for (unsigned int i = 0; i < dict->length; i++) {
        struct dict_assoc **db = &dict->stable[i];
        struct dict_assoc *k = *db;
        while (k != NULL) {
            (*f)(env, (char *) &k[1] + dict->value_len, k->len, &k[1]);
            k = k->next;
        }
        if (dict->concurrent) {
            mutex_acquire(&dict->locks[i % dict->nlocks]);
            db = &dict->unstable[i];
            k = *db;
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
        unsigned int first = (uint64_t) worker * dict->old_length / dict->nworkers;
        unsigned int last = (uint64_t) (worker + 1) * dict->old_length / dict->nworkers;
        for (unsigned i = first; i < last; i++) {
            struct dict_assoc **b = &dict->old_stable[i];
            struct dict_assoc *k = *b;
            while (k != NULL) {
                struct dict_assoc *next = k->next;
                dict_reinsert_when_resizing(dict, k);
                k = next;
            }
        }
    }

	for (unsigned int i = 0; i < dict->nworkers; i++) {
        struct dict_worker *dw = &dict->workers[i];
        struct dict_assoc *k;
        while ((k = dw->unstable[worker]) != NULL) {
            // uint32_t hash = hash_func((char *) &k[1] + dict->value_len, k->len);
            // unsigned int index = hash % dict->length;
            unsigned int index = k->hash % dict->length;
            struct dict_assoc **db = &dict->stable[index];
            dw->unstable[worker] = k->unstable_next;
            k->next = *db;
            k->unstable_next = NULL;
            *db = k;
            if (dict->stable == dict->old_stable) {
                dict->unstable[index] = NULL;
            }
        }
    }
}

// Figure out how much this dictionary should grow by adding up the
// unstable entries.  The actual rehashing happens later.
void dict_grow_prepare(struct dict *dict){
    assert(dict->concurrent);

    if (dict->old_stable != dict->stable) {
        free(dict->old_stable);
        dict->old_stable = dict->stable;
        free(dict->old_unstable);
        dict->old_unstable = dict->unstable;
    }
    dict->old_count = dict->count;
    dict->old_length = dict->length;
    dict->old_stable = dict->stable;
    dict->old_unstable = dict->unstable;

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
        dict->stable = calloc(sizeof(*dict->stable), dict->length);
        dict->unstable = calloc(sizeof(*dict->unstable), dict->length);
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
