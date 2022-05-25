// Originally downloaded from https://github.com/exebook/hashdict.c

#ifndef HASHDICTC
#define HASHDICTC
#include <stdlib.h> /* malloc/calloc */
#include <stdint.h> /* uint32_t */
#include <string.h> /* memcpy/memcmp */

#include "thread.h"

#define HASHDICT_VALUE_TYPE void*

typedef void (*enumFunc)(void *env, const void *key, unsigned int key_size,
                                HASHDICT_VALUE_TYPE value);

// key directly follows this header
struct keynode {
	struct keynode *next;
    struct keynode *unstable_next;
	unsigned int len;
	HASHDICT_VALUE_TYPE value;
};

struct dict_bucket {
    struct keynode *stable, *unstable;
};

struct dict_worker {
    struct keynode **unstable;   // one for each of the workers
};
		
struct dict {
	struct dict_bucket *table;
	unsigned int length, count;
    struct dict_worker *workers;
    unsigned int nworkers;
    mutex_t *locks;
    unsigned int nlocks;
	double growth_threshold;
	double growth_factor;
    int concurrent;         // 0 = not concurrent
    void *(*malloc)(size_t size);
    void (*free)(void *);
};

struct dict *dict_new(unsigned int initial_size, unsigned int nworkers, void *(*malloc)(size_t size), void (*free)(void *));
void dict_delete(struct dict *dict);
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen);
void **dict_insert(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen);
struct keynode *dict_find_lock(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keyn);
void dict_find_release(struct dict *dict, struct keynode *k);
void *dict_find(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen);
void *dict_retrieve(const void *p, unsigned int *psize);
void dict_iter(struct dict *dict, enumFunc f, void *user);
void dict_set_concurrent(struct dict *dict);
int dict_make_stable(struct dict *dict, unsigned int worker);
void dict_set_sequential(struct dict *dict, int n);
#endif
