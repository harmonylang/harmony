// Originally downloaded from https://github.com/exebook/hashdict.c

#ifndef HASHDICTC
#define HASHDICTC
#include <stdlib.h> /* malloc/calloc */
#include <stdint.h> /* uint32_t */
#include <string.h> /* memcpy/memcmp */
#include <stdbool.h>

#include "thread.h"

typedef void (*dict_enumfunc)(void *env, const void *key,
                        unsigned int key_size, void *value);
typedef bool (*dict_enumfunc_bool)(void *env, const void *key,
                        unsigned int key_size, void *value);

// This header is followed directly by first the data and then the key.
struct dict_assoc {
	struct dict_assoc *next;
	uint16_t len;               // key length
    uint16_t val_len;           // value length
};

struct dict_list {
    unsigned int next;               // points into array of entries
    unsigned int len;
    struct dict_assoc **entries;     // array of len entries
};

struct dict_worker {
    struct dict_list *unstable;      // one for each of the other workers
    unsigned int count;              // #unstable entries added
};
		
struct dict {
    char *whoami;
    unsigned int value_len;
	struct dict_assoc **stable, **unstable;
	unsigned int length, count;
	struct dict_assoc **old_stable, **old_unstable;
	unsigned int old_length, old_count;
    struct dict_worker *workers;
    unsigned int nworkers;
    mutex_t *locks;
    unsigned int nlocks;
	double growth_threshold;
	unsigned int growth_factor;
    unsigned int invoke_count;      // how many time invoked?
    unsigned int depth_count;       // how deep are we searching in the linked list?
    unsigned int depth_max; 
    bool concurrent;
    bool align16;            // entries must be aligned to 16 bytes
    struct dict_list list;   // to make dict_iter more efficient
    bool autogrow;
};

static inline void *dict_retrieve(const void *p, unsigned int *psize){
    const struct dict_assoc *k = p;
    if (psize != NULL) {
        *psize = k->len;
    }
    return (char *) &k[1];
}

struct dict *dict_new(char *whoami, unsigned int value_len, unsigned int initial_size,
    unsigned int nworkers, bool align16, bool concurrent);
void dict_delete(struct dict *dict);
void *dict_search(struct dict *dict, const void *key, unsigned int keylen);
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen);
bool dict_remove(struct dict *dict, const void *key, unsigned int keylen);
void *dict_insert(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);
struct dict_assoc *dict_find_lock(struct dict *dict, struct allocator *al, const void *key, unsigned int keyn, bool *is_new, mutex_t **lock);
struct dict_assoc *dict_find_new(struct dict *dict, struct allocator *al, const void *key, unsigned int keyn, unsigned int extra, bool *is_new, uint32_t hash);
struct dict_assoc *dict_find(struct dict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);
// void *dict_retrieve(const void *p, unsigned int *psize);
void dict_iter(struct dict *dict, dict_enumfunc f, void *env);
bool dict_iter_bool(struct dict *dict, dict_enumfunc_bool f, void *env);
void dict_set_concurrent(struct dict *dict);
void dict_make_stable(struct dict *dict, unsigned int worker);
void dict_set_sequential(struct dict *dict);
void dict_grow_prepare(struct dict *dict);
unsigned long dict_allocated(struct dict *dict);
bool dict_exists(struct dict *dict, const void *key, unsigned int keylen, uint32_t hash);
void dict_resize(struct dict *dict, unsigned int newsize);
void dict_set_iter(struct dict *dict, unsigned int size);
bool dict_overload(struct dict *dict);

#endif
