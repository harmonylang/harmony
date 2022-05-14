#include "head.h"

#include <assert.h>
#include <stdio.h>
#include <stdbool.h>

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

uint32_t dict_hash(const void *key, int size){
	return hash_func(key, size);
}

static inline struct keynode *keynode_new(struct dict *dict,
        char *key, unsigned int len, uint32_t hash, void *(*alloc)(void)) {
	struct keynode *node = (*dict->malloc)(sizeof(struct keynode) + len);
	node->len = len;
	node->key = (char *) &node[1];
	memcpy(node->key, key, len);
    node->hash = hash;
	node->next = 0;
	node->value = alloc == NULL ? NULL : (*alloc)();
	return node;
}

// TODO.  Make iterative rather than recursive
void keynode_delete(struct dict *dict, struct keynode *node) {
	if (node->next) keynode_delete(dict, node->next);
	(*dict->free)(node);
}

struct dict *dict_new(int initial_size, void *(*m)(size_t size), void (*f)(void *)) {
	struct dict *dict = malloc(sizeof(struct dict));
	if (initial_size == 0) initial_size = 1024;
	dict->length = initial_size;
	dict->count = 0;
	dict->table = calloc(sizeof(struct dict_bucket), initial_size);
	for (int i = 0; i < dict->length; i++) {
		mutex_init(&dict->table[i].lock);
	}
	dict->growth_treshold = 2;
	dict->growth_factor = 5;
	dict->concurrent = 0;
    dict->malloc = m == NULL ? malloc : m;
    dict->free = f == NULL ? free : f;
	return dict;
}

void dict_delete(struct dict *dict) {
	for (int i = 0; i < dict->length; i++) {
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
	int n = k->hash % dict->length;
	struct dict_bucket *db = &dict->table[n];
    k->next = db->stable;
    db->stable = k;
}

static void dict_resize(struct dict *dict, int newsize) {
	int o = dict->length;
	struct dict_bucket *old = dict->table;
	dict->table = calloc(sizeof(struct dict_bucket), newsize);
	dict->length = newsize;
	for (int i = 0; i < newsize; i++) {
		mutex_init(&dict->table[i].lock);
	}
	for (int i = 0; i < o; i++) {
		struct dict_bucket *b = &old[i];
        assert(b->unstable == NULL);
        struct keynode *k = b->stable;
		while (k != NULL) {
			struct keynode *next = k->next;
			dict_reinsert_when_resizing(dict, k);
			k = next;
		}
		mutex_destroy(&b->lock);
	}
	free(old);
}

static inline void *dict_find_alloc(struct dict *dict, const void *key, unsigned int keyn, void *(*alloc)(void)) {
	// assert(keyn > 0);
    uint32_t hash = hash_func(key, keyn);
	int n = hash % dict->length;
    struct dict_bucket *db = &dict->table[n];

    // First see if the item is in the stable list, which does not require
    // a lock
	struct keynode *k = db->stable;
	while (k != NULL) {
		if (k->len == keyn && memcmp(k->key, key, keyn) == 0) {
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
            if (k->len == keyn && memcmp(k->key, key, keyn) == 0) {
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
		if (f > dict->growth_treshold) {
            printf("GROW 2\n");
			dict_resize(dict, dict->length * dict->growth_factor - 1);
			return dict_find_alloc(dict, key, keyn, alloc);
		}
	}

    k = keynode_new(dict, (char *) key, keyn, hash, alloc);
    if (dict->concurrent) {
#ifdef notdef
        struct keynode *k2;
        for (k2 = db->unstable; k2 != NULL; k2 = k2->next) {
            if (k2->len == k->len && memcmp(k2->key, k->key, k->len) == 0) {
                fprintf(stderr, "DUPLICATE\n");
                exit(1);
            }
        }
#endif
        if (db->last == NULL) {
            db->unstable = k;
        }
        else {
            db->last->next = k;
        }
        db->last = k;
		db->count++;
        mutex_release(&db->lock);
    }
    else {
        k->next = db->stable;
        db->stable = k;
		dict->count++;
    }
	return k;
}

void *dict_find(struct dict *dict, const void *key, unsigned int keyn) {
	return dict_find_alloc(dict, key, keyn, NULL);
}

void **dict_insert_alloc(struct dict *dict, const void *key, unsigned int keyn, void *(*alloc)(void)){
    struct keynode *k = dict_find_alloc(dict, key, keyn, alloc);
    return &k->value;
}

void **dict_insert(struct dict *dict, const void *key, unsigned int keyn){
    struct keynode *k = dict_find(dict, key, keyn);
    return &k->value;
}

void *dict_retrieve(const void *p, unsigned int *psize){
    const struct keynode *k = p;
    if (psize != NULL) {
        *psize = k->len;
    }
    return k->key;
}

void *dict_lookup(struct dict *dict, const void *key, unsigned int keyn) {
	int n = hash_func((const char*)key, keyn) % dict->length;
    struct dict_bucket *db = &dict->table[n];
	// __builtin_prefetch(db);

    // First look in the stable list, which does not require a lock
	struct keynode *k = db->stable;
	while (k != NULL) {
		if (k->len == keyn && !memcmp(k->key, key, keyn)) {
			return k->value;
		}
		k = k->next;
	}

    // Look in the unstable list
    if (dict->concurrent) {
        mutex_acquire(&db->lock);
        k = db->unstable;
        while (k != NULL) {
            if (k->len == keyn && !memcmp(k->key, key, keyn)) {
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
	for (int i = 0; i < dict->length; i++) {
        struct dict_bucket *db = &dict->table[i];
        struct keynode *k = db->stable;
        while (k != NULL) {
            (*f)(env, k->key, k->len, k->value);
            k = k->next;
        }
        if (dict->concurrent) {
            mutex_acquire(&db->lock);
            k = db->unstable;
            while (k != NULL) {
                (*f)(env, k->key, k->len, k->value);
                k = k->next;
            }
            mutex_release(&db->lock);
        }
	}
}

// To switch between concurrent and sequential modes
void dict_set_concurrent(struct dict *dict, int concurrent) {
	if (dict->concurrent == concurrent) {
        assert(false);      // Shouldn't normally happen
		return;
	}
    dict->concurrent = concurrent;
    if (concurrent) {
        return;
    }

    // When going from concurrent to sequential, need to move over
    // the unstable values and possibly grow the table
	for (int i = 0; i < dict->length; i++) {
        struct dict_bucket *db = &dict->table[i];
        if (db->unstable != NULL) {
            db->last->next = db->stable;
            db->stable = db->unstable;
            db->unstable = db->last = NULL;
        }
		dict->count += db->count;
        db->count = 0;
    }

    struct keynode *k;
    int count = 0;
	for (int i = 0; i < dict->length; i++) {
        struct dict_bucket *db = &dict->table[i];
        for (k = db->stable; k != 0; k = k->next) {
            count++;
        }
    }

	double f = (double)dict->count / (double)dict->length;
	if (f > dict->growth_treshold) {
        int min = dict->length * dict->growth_factor;
        if (min < dict->count) {
            min = dict->count * 2;
        }
		dict_resize(dict, min);
	}
}
