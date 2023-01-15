// Originally downloaded from https://github.com/exebook/hashdict.c

#ifndef HASHDICTC
#define HASHDICTC
#include <stdlib.h> /* malloc/calloc */
#include <stdint.h> /* uint32_t */
#include <string.h> /* memcpy/memcmp */

#include "thread.h"

typedef void (*dict_enumfunc)(void *env, const void *key, unsigned int key_size,
                                void *value);

// This header is followed directly by first the data and then the key.
// The value is of length dict->value_len.
struct dict_assoc {
	struct dict_assoc *next;
    struct dict_assoc *unstable_next;
	unsigned int len;               // key length
};

// TODO.  Split into two tables, one for stable, one for unstable.
struct dict_bucket {
    struct dict_assoc *stable, *unstable;
};

struct dict_worker {
    struct dict_assoc **unstable;   // one for each of the workers
    unsigned int count;             // #unstable entries added
    unsigned int clashes;           // some profiling
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
    bool align16;            // entries must be aligned to 16 bytes
};

struct dict *dict_new(char *whoami, unsigned int value_len, unsigned int initial_size,
    unsigned int nworkers, bool align16);
void dict_delete(struct dict *dict);
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen);
bool dict_remove(struct dict *dict, const void *key, unsigned int keylen);
void *dict_insert(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);
struct dict_assoc *dict_find_lock(struct dict *dict, struct allocator *al, const void *key, unsigned int keyn, bool *is_new, mutex_t **lock);
struct dict_assoc *dict_find(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);
void *dict_retrieve(const void *p, unsigned int *psize);
void dict_iter(struct dict *dict, dict_enumfunc f, void *user);
void dict_set_concurrent(struct dict *dict);
void dict_make_stable(struct dict *dict, unsigned int worker);
void dict_set_sequential(struct dict *dict);
void dict_grow_prepare(struct dict *dict);
unsigned long dict_allocated(struct dict *dict);
void dict_dump(struct dict *dict);

#endif
