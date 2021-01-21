// Downloaded from https://github.com/exebook/hashdict.c

#ifndef HASHDICTC
#define HASHDICTC
#include <stdlib.h> /* malloc/calloc */
#include <stdint.h> /* uint32_t */
#include <string.h> /* memcpy/memcmp */

#define HASHDICT_VALUE_TYPE void*

typedef void (*enumFunc)(void *env, const void *key, unsigned int key_size,
                                HASHDICT_VALUE_TYPE value);

struct keynode {
	struct keynode *next;
	char *key;
	unsigned int len;
	HASHDICT_VALUE_TYPE value;
};
		
struct dict {
	struct keynode **table;
	int length, count;
	double growth_treshold;
	double growth_factor;
};

struct dict *dict_new(int initial_size);
void dict_delete(struct dict *dict);
void *dict_lookup(struct dict *dict, const void *key, unsigned int keylen);
void **dict_insert(struct dict *dict, const void *key, unsigned int keylen);
void *dict_find(struct dict *dict, const void *key, unsigned int keylen);
void *dict_retrieve(const void *p, int *psize);
void dict_iter(struct dict *dict, enumFunc f, void *user);
#endif
