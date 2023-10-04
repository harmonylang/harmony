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

struct dict_worker {
    unsigned int unstable_count;    // #unstable entries added
    unsigned int clashes;           // some profiling
};

struct dict_table {
    unsigned int count;                 // #entries total
    unsigned int length;                // #buckets
    struct dict_assoc **buckets;        // each bucket points to a linked list of entries
};

struct dict {
    char *whoami;
    unsigned int value_len;
    struct dict_table stable;           // stable entries (do not need lock)
    struct dict_table unstable;         // unstable entries (require lock))
    struct dict_table old_stable;
    struct dict_table old_unstable;
    struct dict_worker *workers;
    unsigned int nworkers;
    mutex_t *locks;
    unsigned int nlocks;
	double growth_threshold;
	unsigned int growth_factor;
    bool concurrent;         // 0 = not concurrent
    bool align16;            // entries must be aligned to 16 bytes

#ifdef HASHDICT_STATS
    // stats
    hAtomic(unsigned int) nmisses;
    hAtomic(unsigned int) nunstable_hits;
    hAtomic(unsigned int) nstable_hits;
#endif
};

struct dict *dict_new(char *whoami, unsigned int value_len, unsigned int initial_size,
    unsigned int nworkers, bool align16);
void dict_delete(struct dict *dict);
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen);
bool dict_remove(struct dict *dict, const void *key, unsigned int keylen);
void *dict_insert(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);
struct dict_assoc *dict_find_lock(struct dict *dict, struct allocator *al, const void *key, unsigned int keyn, bool *is_new, mutex_t **lock);
struct dict_assoc *dict_find_lock_new(struct dict *dict, struct allocator *al, const void *key, unsigned int keyn, bool *is_new, mutex_t **lock);
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
