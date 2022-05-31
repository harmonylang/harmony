// Originally downloaded from https://github.com/exebook/hashdict.c

#ifndef HASHDICTC
#define HASHDICTC
#include <stdlib.h> /* malloc/calloc */
#include <stdint.h> /* uint32_t */
#include <string.h> /* memcpy/memcmp */

#define DICT_ALIGN      sizeof(void *)

#include "thread.h"

typedef void (*enumFunc)(void *env, const void *key, unsigned int key_size,
                                void *value);

// This header is followed directly by first the key and
// then the value (aligned to DICT_ALIGN).
// The value is of length dict->value_len.
struct keynode {
	struct keynode *next;
    struct keynode *unstable_next;
	unsigned int len;                   // key length
};

struct dict_bucket {
    struct keynode *stable, *unstable;
};

struct dict_worker {
    struct keynode **unstable;   // one for each of the workers
    unsigned int count;          // #unstable entries added
};
		
struct dict {
    char *whoami;
    unsigned int value_len;
	struct dict_bucket *table;
	unsigned int length, count;
	struct dict_bucket *old_table;
	unsigned int old_length, old_count;
    struct dict_worker *workers;
    unsigned int nworkers;
    mutex_t *locks;
    unsigned int nlocks;
	double growth_threshold;
	unsigned int growth_factor;
    bool concurrent;         // 0 = not concurrent
    void *(*malloc)(size_t size);
    void (*free)(void *);
};

struct dict *dict_new(char *whoami, unsigned int value_len, unsigned int initial_size,
    unsigned int nworkers, void *(*malloc)(size_t size), void (*free)(void *));
void dict_delete(struct dict *dict);
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen);
bool dict_remove(struct dict *dict, const void *key, unsigned int keylen);
void *dict_insert(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *new);
void *dict_insert_lock(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *new);
struct keynode *dict_find_lock(struct dict *dict, struct allocator *al,
                            const void *key, unsigned int keyn, bool *new);
void dict_insert_release(struct dict *dict, const void *key, unsigned int keylen);
struct keynode *dict_find(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *new);
void *dict_retrieve(const void *p, unsigned int *psize);
void dict_iter(struct dict *dict, enumFunc f, void *user);
void dict_set_concurrent(struct dict *dict);
void dict_make_stable(struct dict *dict, unsigned int worker);
void dict_set_sequential(struct dict *dict);
void dict_grow_prepare(struct dict *dict);

#endif
