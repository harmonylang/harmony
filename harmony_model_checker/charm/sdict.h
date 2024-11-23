// Originally downloaded from https://github.com/exebook/hashdict.c

#ifndef SDICTC
#define SDICTC
#include <stdlib.h> /* malloc/calloc */
#include <stdint.h> /* uint32_t */
#include <string.h> /* memcpy/memcmp */
#include <stdbool.h>

#include "hashdict.h"
#include "thread.h"

struct sdict {
    char *whoami;
    unsigned int value_len;
	struct dict_assoc **stable;
	unsigned int length, count;
	struct dict_assoc **old_stable;
	unsigned int old_length, old_count;
	double growth_threshold;
	unsigned int growth_factor;
    unsigned int invoke_count;      // how many time invoked?
    unsigned int depth_count;       // how deep are we searching in the linked list?
    unsigned int depth_max; 
    bool autogrow;
};

static inline void *sdict_retrieve(const void *p, unsigned int *psize){
    const struct dict_assoc *k = p;
    if (psize != NULL) {
        *psize = k->len;
    }
    return (char *) &k[1];
}

struct sdict *sdict_new(char *whoami, unsigned int value_len, unsigned int initial_size);
void sdict_delete(struct sdict *dict);
void *sdict_search(struct sdict *dict, const void *key, unsigned int keylen);
void *sdict_lookup(struct sdict *dict, const void *key, unsigned int keylen);
bool sdict_remove(struct sdict *dict, const void *key, unsigned int keylen);
void *sdict_insert(struct sdict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);
struct dict_assoc *sdict_find_new(struct sdict *dict, struct allocator *al, const void *key, unsigned int keyn, unsigned int extra, bool *is_new, uint32_t hash);
struct dict_assoc *sdict_find(struct sdict *dict, struct allocator *al, const void *key, unsigned int keylen, bool *is_new);
unsigned long sdict_allocated(struct sdict *dict);
bool sdict_exists(struct sdict *dict, const void *key, unsigned int keylen, uint32_t hash);
void sdict_resize(struct sdict *dict, unsigned int newsize);
bool sdict_overload(struct sdict *dict);

#endif
