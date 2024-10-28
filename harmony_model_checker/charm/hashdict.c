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
        struct allocator *al, char *key, unsigned int len, unsigned int extra){
    unsigned int total = sizeof(struct dict_assoc) + dict->value_len + extra + len;
	struct dict_assoc *k = al == NULL ?  malloc(total) :
                        (*al->alloc)(al->ctx, total, false, dict->align16);
    k->len = len;
    k->val_len = dict->value_len + extra;
	memcpy((char *) &k[1] + k->val_len, key, len);
	return k;
}

// TODO.  Make iterative rather than recursive
// TODO.  free() doesn't work with allocator->alloc
void dict_assoc_delete(struct dict *dict, struct dict_assoc *k) {
	if (k->next) dict_assoc_delete(dict, k->next);
	free(k);
}

struct dict *dict_new(char *whoami, unsigned int value_len, unsigned int initial_size,
        unsigned int nworkers, bool align16, bool concurrent) {
	struct dict *dict = new_alloc(struct dict);
    dict->whoami = whoami;
    dict->value_len = value_len;
	if (initial_size == 0) initial_size = 1024;
	dict->length = dict->old_length = initial_size;
	dict->count = dict->old_count = 0;
	dict->growth_threshold = 2;
	dict->growth_factor = 10;
	dict->concurrent = concurrent;
    dict->align16 = align16;
	dict->stable = dict->old_stable = calloc(sizeof(*dict->stable), initial_size);
    if (concurrent) {
        dict->unstable = dict->old_unstable = calloc(sizeof(*dict->unstable), initial_size);
        dict->nlocks = nworkers * 64;        // TODO: how much?
        dict->locks = malloc(dict->nlocks * sizeof(mutex_t));
        for (unsigned int i = 0; i < dict->nlocks; i++) {
            mutex_init(&dict->locks[i]);
        }
        dict->workers = calloc(sizeof(struct dict_worker), nworkers);
        dict->nworkers = nworkers;
        for (unsigned int i = 0; i < nworkers; i++) {
            dict->workers[i].unstable = calloc(sizeof(struct dict_unstable), nworkers);
        }
    }
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
		if (dict->concurrent && dict->unstable[i] != NULL)
			dict_assoc_delete(dict, dict->unstable[i]);
	}
	for (unsigned int i = 0; i < dict->nlocks; i++) {
		mutex_destroy(&dict->locks[i]);
    }
	free(dict->stable);
	free(dict->unstable);
	free(dict);
}

static inline void dict_reinsert(struct dict *dict, struct dict_assoc *k) {
    unsigned int n = hash_func((char *) &k[1] + k->val_len, k->len) % dict->length;
	struct dict_assoc **sdb = &dict->stable[n];
    k->next = *sdb;
    *sdb = k;
}

unsigned long dict_allocated(struct dict *dict) {
    if (dict->concurrent) {
        return dict->length * (sizeof(*dict->stable) + sizeof(*dict->unstable));
    }
    return dict->length * sizeof(*dict->stable);
}

void dict_resize(struct dict *dict, unsigned int newsize) {
	unsigned int o = dict->length;
	struct dict_assoc **old = dict->stable;
	dict->stable = calloc(sizeof(*dict->stable), newsize);
	dict->length = newsize;
	for (unsigned int i = 0; i < o; i++) {
		struct dict_assoc **b = &old[i];
        struct dict_assoc *k = *b;
		// *b = NULL;
		while (k != NULL) {
			struct dict_assoc *next = k->next;
			dict_reinsert(dict, k);
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
            du->len = 4096;
            assert(du->entries == NULL);
        }
        else {
            du->len *= 2;
            assert(du->entries != NULL);
        }
        du->entries = realloc(du->entries, du->len * sizeof(*du->entries));
    }
    assert(du->next < du->len);
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
    struct dict_assoc **sdb = &dict->stable[index];
	struct dict_assoc *k = *sdb;
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + k->val_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
			return k;
		}
		k = k->next;
	}

    struct dict_assoc **udb = &dict->unstable[index];
    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);

        // See if the item is in the unstable list
        k = *udb;
        while (k != NULL) {
            if (k->len == keylen && memcmp((char *) &k[1] + k->val_len, key, keylen) == 0) {
                mutex_release(&dict->locks[index % dict->nlocks]);
                if (new != NULL) {
                    *new = false;
                }
                return k;
            }
            k = k->next;
        }
    }

    // If not concurrent may have to grow the table now
	// if (!dict->concurrent && db->stable == NULL) {
	if (!dict->concurrent) {
		double f = (double) dict->count / (double) dict->length;
		if (f > dict->growth_threshold) {
			dict_resize(dict, dict->length * dict->growth_factor - 1);
			return dict_find(dict, al, key, keylen, new);
		}
	}

    k = dict_assoc_new(dict, al, (char *) key, keylen, 0);
    if (dict->concurrent) {
        k->next = *udb;
        *udb = k;
        mutex_release(&dict->locks[index % dict->nlocks]);
        dict_unstable(dict, al, index, k);
    }
    else {
        k->next = *sdb;
        *sdb = k;
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
    // TODO assert(dict->concurrent);
    assert(al != NULL);
    uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;
    *lock = &dict->locks[index % dict->nlocks];

	struct dict_assoc *k = dict->stable[index];
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + k->val_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
            mutex_acquire(*lock);
			return k;
		}
		k = k->next;
	}

    // See if the item is in the unstable list
    struct dict_assoc **udb = &dict->unstable[index];
    mutex_acquire(*lock);
    k = *udb;
    while (k != NULL) {
        if (k->len == keylen && memcmp((char *) &k[1] + k->val_len, key, keylen) == 0) {
            if (new != NULL) {
                *new = false;
            }
            return k;
        }
        k = k->next;
    }

    k = dict_assoc_new(dict, al, (char *) key, keylen, 0);
    k->next = *udb;
    *udb = k;
    dict_unstable(dict, al, index, k);

    if (new != NULL) {
        *new = true;
    }
	return k;
}

// Returns in *new if this is a new entry or not.
// 'extra' is an additional number of bytes added to the value.
struct dict_assoc *dict_find_new(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keylen,
                            unsigned int extra, bool *new, uint32_t hash){
    assert(al != NULL);
    assert(!dict->concurrent);
    // uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;

    struct dict_assoc **sdb = &dict->stable[index];
	struct dict_assoc *k = *sdb;
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + k->val_len, key, keylen) == 0) {
            *new = false;
			return k;
		}
		k = k->next;
	}

    // See if we need to grow the table
    double f = (double) dict->count / (double) dict->length;
    if (f > dict->growth_threshold) {
        dict_resize(dict, dict->length * dict->growth_factor - 1);
        return dict_find_new(dict, al, key, keylen, extra, new, hash);
    }

    // Add new entry
    k = dict_assoc_new(dict, al, (char *) key, keylen, extra);
    k->next = *sdb;
    *sdb = k;
    dict->count++;
    *new = true;
	return k;
}

// Returns a pointer to the value
void *dict_insert(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keylen, bool *new){
    struct dict_assoc *k = dict_find(dict, al, key, keylen, new);
    return (char *) &k[1];
}

// Search for but do not create an entry in the hash table.
void *dict_search(struct dict *dict, const void *key, unsigned int keylen) {
    uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;
	// __builtin_prefetch(db);

    // First look in the stable list, which does not require a lock
	struct dict_assoc *k = dict->stable[index];
	while (k != NULL) {
		if (k->len == keylen && !memcmp((char *) &k[1] + k->val_len, key, keylen)) {
            return &k[1];
		}
		k = k->next;
	}

    // Look in the unstable list
    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);
        k = dict->unstable[index];
        while (k != NULL) {
            if (k->len == keylen && !memcmp((char *) &k[1] + k->val_len, key, keylen)) {
                mutex_release(&dict->locks[index % dict->nlocks]);
                return &k[1];
            }
            k = k->next;
        }
        mutex_release(&dict->locks[index % dict->nlocks]);
    }

	return NULL;
}

// This assumes that the value is a pointer.  Returns NULL if there is
// no entry but does not create an entry.
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen) {
    uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;
	// __builtin_prefetch(db);

    // First look in the stable list, which does not require a lock
	struct dict_assoc *k = dict->stable[index];
	while (k != NULL) {
		if (k->len == keylen && !memcmp((char *) &k[1] + k->val_len, key, keylen)) {
            return * (void **) &k[1];
		}
		k = k->next;
	}

    // Look in the unstable list
    if (dict->concurrent) {
        mutex_acquire(&dict->locks[index % dict->nlocks]);
        k = dict->unstable[index];
        while (k != NULL) {
            if (k->len == keylen && !memcmp((char *) &k[1] + k->val_len, key, keylen)) {
                mutex_release(&dict->locks[index % dict->nlocks]);
                return * (void **) &k[1];
            }
            k = k->next;
        }
        mutex_release(&dict->locks[index % dict->nlocks]);
    }

	return NULL;
}

bool dict_exists(struct dict *dict, const void *key, unsigned int keylen, uint32_t hash) {
    unsigned int index = hash % dict->length;
    struct dict_assoc **sdb = &dict->stable[index];
	assert(!dict->concurrent);

	struct dict_assoc *k = *sdb;
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + k->val_len, key, keylen) == 0) {
            return true;
		}
		k = k->next;
	}
    return false;
}

void dict_iter(struct dict *dict, dict_enumfunc f, void *env) {
	for (unsigned int i = 0; i < dict->length; i++) {
        struct dict_assoc *k = dict->stable[i];
        while (k != NULL) {
            (*f)(env, (char *) &k[1] + k->val_len, k->len, &k[1]);
            k = k->next;
        }
        if (dict->concurrent) {
            mutex_acquire(&dict->locks[i % dict->nlocks]);
            k = dict->unstable[i];
            while (k != NULL) {
                (*f)(env, (char *) &k[1] + k->val_len, k->len, &k[1]);
                k = k->next;
            }
            mutex_release(&dict->locks[i % dict->nlocks]);
        }
	}
}

// Returns true iff all f() invocations return true.
bool dict_iter_bool(struct dict *dict, dict_enumfunc_bool f, void *env) {
    assert(!dict->concurrent);
	for (unsigned int i = 0; i < dict->length; i++) {
        struct dict_assoc *k = dict->stable[i];
        while (k != NULL) {
            if (!(*f)(env, (char *) &k[1] + k->val_len, k->len, &k[1])) {
                return false;
            }
            k = k->next;
        }
	}
    return true;
}

// Switch to concurrent mode
// TODO.  Obsolete
void dict_set_concurrent(struct dict *dict) {
    assert(false);
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
            struct dict_assoc *k = dict->old_stable[i];
            while (k != NULL) {
                struct dict_assoc *next = k->next;
                dict_reinsert(dict, k);
                k = next;
            }
        }
    }

    // Stabilization: move all unstable entries into the stable lists.
    if (dict->stable == dict->old_stable) {
        for (unsigned int i = 0; i < dict->nworkers; i++) {
            struct dict_worker *dw = &dict->workers[i];
            struct dict_unstable *du = &dw->unstable[worker];
            for (unsigned int j = 0; j < du->next; j++) {
                struct dict_assoc *k = du->entries[j];
                uint32_t hash = hash_func((char *) &k[1] + k->val_len, k->len);
                unsigned int index = hash % dict->length;
                struct dict_assoc **sdb = &dict->stable[index];
                k->next = *sdb;
                *sdb = k;
                dict->unstable[index] = NULL;
            }
            du->next = 0;
        }
    }
    else {
        for (unsigned int i = 0; i < dict->nworkers; i++) {
            struct dict_worker *dw = &dict->workers[i];
            struct dict_unstable *du = &dw->unstable[worker];
            for (unsigned int j = 0; j < du->next; j++) {
                struct dict_assoc *k = du->entries[j];
                uint32_t hash = hash_func((char *) &k[1] + k->val_len, k->len);
                unsigned int index = hash % dict->length;
                struct dict_assoc **sdb = &dict->stable[index];
                k->next = *sdb;
                *sdb = k;
                assert(dict->unstable[index] == NULL);
            }
            du->next = 0;
        }
    }
}

// Figure out how much this dictionary should grow by adding up the
// unstable entries.  The actual rehashing happens later.
void dict_grow_prepare(struct dict *dict){
    assert(dict->concurrent);

    if (dict->old_stable != dict->stable) {
        free(dict->old_stable);
        free(dict->old_unstable);
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
}

void dict_set_sequential(struct dict *dict) {
    assert(dict->concurrent);

#ifdef notdef
    // check integrity
    struct dict_assoc **sdb = dict->stable;
    struct dict_assoc **udb = dict->unstable;
    unsigned int total = 0;
	for (unsigned int i = 0; i < dict->length; i++, sdb++, udb++) {
        if (*udb != NULL) {
            printf("BAD DICT %s\n", dict->whoami);
        }
        for (struct dict_assoc *k = *sdb; k != NULL; k = k->next) {
            total++;
        }
    }
    if (total != dict->count) {
        printf("DICT: bad total %s\n", dict->whoami);
    }
    else {
        printf("DICT: good total %s\n", dict->whoami);
    }
#endif

    dict->concurrent = false;
}
