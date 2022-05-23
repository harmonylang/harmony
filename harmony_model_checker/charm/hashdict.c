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

static inline struct keynode *keynode_new(struct dict *dict,
        struct allocator *al,
        char *key, unsigned int len, uint32_t hash,
        void *(*alloc)(void *), void *ctx) {
	struct keynode *node = al == NULL ?
            malloc(sizeof(struct keynode) + len) :
            (*al->alloc)(al->ctx, sizeof(struct keynode) + len, false);
	node->len = len;
	memcpy(node + 1, key, len);
    node->hash = hash;
	node->next = 0;
	node->value = alloc == NULL ? NULL : (*alloc)(ctx);
	return node;
}

// TODO.  Make iterative rather than recursive
void keynode_delete(struct dict *dict, struct keynode *node) {
	if (node->next) keynode_delete(dict, node->next);
	(*dict->free)(node);
}

struct dict *dict_new(unsigned int initial_size, unsigned int nworkers,
                void *(*m)(size_t size), void (*f)(void *)) {
	struct dict *dict = new_alloc(struct dict);
	if (initial_size == 0) initial_size = 256;
	dict->length = initial_size;
	dict->count = 0;
	dict->table = calloc(sizeof(struct dict_bucket), initial_size);
	for (unsigned int i = 0; i < dict->length; i++) {
		mutex_init(&dict->table[i].lock);
	}
	dict->growth_threshold = 2;
	dict->growth_factor = 10;
	dict->concurrent = 0;
    dict->workers = calloc(sizeof(struct dict_worker), nworkers);
    dict->nworkers = nworkers;
    for (unsigned int i = 0; i < nworkers; i++) {
        dict->workers[i].unstable = calloc(sizeof(struct keynode *), nworkers);
    }
    dict->malloc = m == NULL ? malloc : m;
    dict->free = f == NULL ? free : f;
	return dict;
}

void dict_delete(struct dict *dict) {
	for (unsigned int i = 0; i < dict->length; i++) {
		if (dict->table[i].stable != NULL)
			keynode_delete(dict, dict->table[i].stable);
		if (dict->table[i].unstable != NULL)
			keynode_delete(dict, dict->table[i].unstable);
		mutex_destroy(&dict->table[i].lock);
	}
	free(dict->table);
	free(dict);
}

static inline void dict_reinsert_when_resizing(struct dict *dict, struct keynode *k) {
	unsigned int n = k->hash % dict->length;
	struct dict_bucket *db = &dict->table[n];
    k->next = db->stable;
    db->stable = k;
}

static void dict_resize(struct dict *dict, unsigned int newsize) {
	unsigned int o = dict->length;
	struct dict_bucket *old = dict->table;
	dict->table = calloc(sizeof(struct dict_bucket), newsize);
	dict->length = newsize;
	for (unsigned int i = 0; i < newsize; i++) {
		mutex_init(&dict->table[i].lock);
	}
	for (unsigned int i = 0; i < o; i++) {
		struct dict_bucket *b = &old[i];
        assert(b->unstable == NULL);
        struct keynode *k = b->stable;
		b->stable = NULL;
		while (k != NULL) {
			struct keynode *next = k->next;
			dict_reinsert_when_resizing(dict, k);
			k = next;
		}
		mutex_destroy(&b->lock);
	}
	free(old);
}

// Perhaps the most performance critical function in the entire code base
static inline void *dict_find_alloc(struct dict *dict, struct allocator *al,
        const void *key, unsigned int keyn, void *(*alloc)(void *), void *ctx) {
    uint32_t hash = hash_func(key, keyn);
    struct dict_bucket *db = &dict->table[hash % dict->length];

    // First see if the item is in the stable list, which does not require
    // a lock
	struct keynode *k = db->stable;
	while (k != NULL) {
		if (k->len == keyn && memcmp(k+1, key, keyn) == 0) {
			assert(alloc == NULL || k->value != NULL);
			return k;
		}
		k = k->next;
	}

    if (dict->concurrent) {
        mutex_acquire(&db->lock);

        // See if the item is in the unstable list
        k = db->unstable;
        while (k != NULL) {
            if (k->len == keyn && memcmp(k+1, key, keyn) == 0) {
				assert(alloc == NULL || k->value != NULL);
                mutex_release(&db->lock);
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
			return dict_find_alloc(dict, al, key, keyn, alloc, ctx);
		}
	}

    k = keynode_new(dict, al, (char *) key, keyn, hash, alloc, ctx);
    if (dict->concurrent) {
#ifdef notdef
        struct keynode *k2;
        for (k2 = db->unstable; k2 != NULL; k2 = k2->next) {
            if (k2->len == k->len && memcmp(k2+1, k+1, k->len) == 0) {
                fprintf(stderr, "DUPLICATE\n");
                exit(1);
            }
        }
#endif
        k->next = db->unstable;
        db->unstable = k;
        mutex_release(&db->lock);

        // Keep track of this unstable node in the list for the
        // worker who's going to look at this bucket
        k->bucket = db;
        int worker = (hash % dict->length) * dict->nworkers / dict->length;
        k->unstable_next = dict->workers[al->worker].unstable[worker];
        dict->workers[al->worker].unstable[worker] = k;
    }
    else {
        k->next = db->stable;
        db->stable = k;
		dict->count++;
    }
	return k;
}

void *dict_find(struct dict *dict, struct allocator *al,
                        const void *key, unsigned int keyn) {
	return dict_find_alloc(dict, al, key, keyn, NULL, NULL);
}

void **dict_insert_alloc(struct dict *dict, struct allocator *al,
        const void *key, unsigned int keyn, void *(*alloc)(void *), void *ctx){
    struct keynode *k = dict_find_alloc(dict, al, key, keyn, alloc, ctx);
    return &k->value;
}

void **dict_insert(struct dict *dict, struct allocator *al,
        const void *key, unsigned int keyn){
    struct keynode *k = dict_find(dict, al, key, keyn);
    return &k->value;
}

void *dict_retrieve(const void *p, unsigned int *psize){
    const struct keynode *k = p;
    if (psize != NULL) {
        *psize = k->len;
    }
    return (void *) (k+1);
}

void *dict_lookup(struct dict *dict, const void *key, unsigned int keyn) {
    uint32_t hash = hash_func(key, keyn);
    struct dict_bucket *db = &dict->table[hash % dict->length];
	// __builtin_prefetch(db);

    // First look in the stable list, which does not require a lock
	struct keynode *k = db->stable;
	while (k != NULL) {
		if (k->len == keyn && !memcmp(k+1, key, keyn)) {
			return k->value;
		}
		k = k->next;
	}

    // Look in the unstable list
    if (dict->concurrent) {
        mutex_acquire(&db->lock);
        k = db->unstable;
        while (k != NULL) {
            if (k->len == keyn && !memcmp(k+1, key, keyn)) {
                mutex_release(&db->lock);
                return k->value;
            }
            k = k->next;
        }
        mutex_release(&db->lock);
    }

	return NULL;
}

void dict_iter(struct dict *dict, enumFunc f, void *env) {
	for (unsigned int i = 0; i < dict->length; i++) {
        struct dict_bucket *db = &dict->table[i];
        struct keynode *k = db->stable;
        while (k != NULL) {
            (*f)(env, k+1, k->len, k->value);
            k = k->next;
        }
        if (dict->concurrent) {
            mutex_acquire(&db->lock);
            k = db->unstable;
            while (k != NULL) {
                (*f)(env, k+1, k->len, k->value);
                k = k->next;
            }
            mutex_release(&db->lock);
        }
	}
}

// Switch to concurrent mode
void dict_set_concurrent(struct dict *dict) {
    assert(!dict->concurrent);
    dict->concurrent = 1;
}

// When going from concurrent to sequential, need to move over
// the unstable values.
int dict_make_stable(struct dict *dict, unsigned int worker){
    assert(dict->concurrent);
    int n = 0;
	for (unsigned int i = 0; i < dict->nworkers; i++) {
        struct dict_worker *w = &dict->workers[i];
        struct keynode *k;
        while ((k = w->unstable[worker]) != NULL) {
            w->unstable[worker] = k->unstable_next;
            k->next = k->bucket->stable;
            k->bucket->stable = k;
            k->bucket->unstable = NULL;
            n++;
        }
    }
    return n;
}

void dict_set_sequential(struct dict *dict, int n) {
    assert(dict->concurrent);
    dict->count += n;

#ifdef notdef
    // check integrity
    struct dict_bucket *db = dict->table;
    unsigned int total = 0;
	for (unsigned int i = 0; i < dict->length; i++, db++) {
        if (db->unstable != NULL) {
            printf("BAD DICT\n");
        }
        for (struct keynode *k = db->stable; k != NULL; k = k->next) {
            total++;
        }
    }
    if (total != dict->count) {
        printf("DICT: bad total\n");
    }
#endif

	double f = (double)dict->count / (double)dict->length;
	if (f > dict->growth_threshold) {
        unsigned int min = dict->length * dict->growth_factor;
        if (min < dict->count) {
            min = dict->count * 2;
        }
		dict_resize(dict, min);
	}
    dict->concurrent = 0;
}
