#include "head.h"

#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include "global.h"
#include "sdict.h"
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

static inline struct dict_assoc *sdict_assoc_new(struct sdict *dict,
        struct allocator *al, char *key, unsigned int len, unsigned int extra){
    unsigned int total = sizeof(struct dict_assoc) + dict->value_len + extra + len;
	struct dict_assoc *k = al == NULL ? malloc(total) :
                        (*al->alloc)(al->ctx, total, false, false);
    k->len = len;
    k->val_len = dict->value_len + extra;
	memcpy((char *) &k[1] + k->val_len, key, len);
	return k;
}

// TODO.  Make iterative rather than recursive
// TODO.  free() doesn't work with allocator->alloc
void sdict_assoc_delete(struct sdict *dict, struct dict_assoc *k) {
	if (k->next) sdict_assoc_delete(dict, k->next);
	free(k);
}

struct sdict *sdict_new(char *whoami, unsigned int value_len, unsigned int initial_size){
	struct sdict *dict = new_alloc(struct sdict);
    dict->whoami = whoami;
    dict->value_len = value_len;
	if (initial_size == 0) initial_size = 1024;
	dict->length = dict->old_length = initial_size;
	dict->count = dict->old_count = 0;
	dict->growth_threshold = 2;
	dict->growth_factor = 10;
	dict->stable = dict->old_stable = calloc(sizeof(*dict->stable), initial_size);
	return dict;
}

bool sdict_remove(struct sdict *dict, const void *key, unsigned int keylen){
    assert(false);
    return false;
}

void sdict_delete(struct sdict *dict) {
	for (unsigned int i = 0; i < dict->length; i++) {
		if (dict->stable[i] != NULL)
			sdict_assoc_delete(dict, dict->stable[i]);
	}
	free(dict->stable);
	free(dict);
}

static inline void sdict_reinsert(struct sdict *dict, struct dict_assoc *k) {
    unsigned int n = hash_func((char *) &k[1] + k->val_len, k->len) % dict->length;
	struct dict_assoc **sdb = &dict->stable[n];
    k->next = *sdb;
    *sdb = k;
}

unsigned long sdict_allocated(struct sdict *dict) {
    return dict->length * sizeof(*dict->stable);
}

void sdict_resize(struct sdict *dict, unsigned int newsize) {
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
			sdict_reinsert(dict, k);
			k = next;
		}
	}
	free(old);
}

// See if the dictionary needs growing
bool sdict_overload(struct sdict *dict){
    double f = (double) dict->count / (double) dict->length;
    return f > dict->growth_threshold;
}

// Returns in *new if this is a new entry or not.
// 'extra' is an additional number of bytes added to the value.
struct dict_assoc *sdict_find_new(struct sdict *dict, struct allocator *al,
                            const void *key, unsigned int keylen,
                            unsigned int extra, bool *new, uint32_t hash){
    assert(al != NULL);
    // uint32_t hash = hash_func(key, keylen);
    unsigned int index = hash % dict->length;

    dict->invoke_count++;
    unsigned int depth = 0;

    struct dict_assoc **sdb = &dict->stable[index];
	struct dict_assoc *k = *sdb;
	while (k != NULL) {
		if (k->len == keylen && memcmp((char *) &k[1] + k->val_len, key, keylen) == 0) {
            *new = false;
            if (depth > dict->depth_max) {
                dict->depth_max = depth;
            }
			return k;
		}
        dict->depth_count++;
        depth++;
		k = k->next;
	}

    // See if we need to grow the table
    if (dict->autogrow) {
        double f = (double) dict->count / (double) dict->length;
        if (f > dict->growth_threshold) {
            sdict_resize(dict, dict->length * dict->growth_factor - 1);
            return sdict_find_new(dict, al, key, keylen, extra, new, hash);
        }
    }

    // Add new entry
    k = sdict_assoc_new(dict, al, (char *) key, keylen, extra);
    k->next = *sdb;
    *sdb = k;
    dict->count++;
    *new = true;
    if (depth > dict->depth_max) {
        dict->depth_max = depth;
    }
	return k;
}
