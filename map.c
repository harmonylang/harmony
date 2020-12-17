/* Implements a map as a binary tree indexed by a hash of the key in
 * order to get some semblance of balancing.  Each node in the tree
 * points to a linked list of keys that hash to the same value.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include "global.h"

#define MAX_CACHE	5000

struct bin_list_node {
	struct bin_list_node *next;
	void *key, *data;
	unsigned int key_size;
};

struct map {
	struct map *children[2];
	unsigned int hash;
	struct bin_list_node *list;
};

static struct bin_list_node *bln_cache;
static unsigned int bln_csize;

// #define my_hash(k,n)     MurmurHash64A(k,n,0)
#define my_hash(k,n)     meiyan(k,n)

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

uint64_t MurmurHash64A ( const void * key, int len, uint64_t seed )
{
  const uint64_t m = 0xc6a4a7935bd1e995LLU;
  const int r = 47;

  uint64_t h = seed ^ (len * m);

  const uint64_t * data = (const uint64_t *)key;
  const uint64_t * end = data + (len/8);

  while(data != end)
  {
    uint64_t k = *data++;

    k *= m;
    k ^= k >> r;
    k *= m;

    h ^= k;
    h *= m;
  }

  const unsigned char * data2 = (const unsigned char*)data;

  switch(len & 7)
  {
  case 7: h ^= ((uint64_t) data2[6]) << 48;
  case 6: h ^= ((uint64_t) data2[5]) << 40;
  case 5: h ^= ((uint64_t) data2[4]) << 32;
  case 4: h ^= ((uint64_t) data2[3]) << 24;
  case 3: h ^= ((uint64_t) data2[2]) << 16;
  case 2: h ^= ((uint64_t) data2[1]) << 8;
  case 1: h ^= ((uint64_t) data2[0]);
          h *= m;
  };

  h ^= h >> r;
  h *= m;
  h ^= h >> r;

  return h;
}

static void *map_list_lookup(struct bin_list_node *bln, const void *key, unsigned int key_size) {
	while (bln != 0) {
		if (bln->key_size == key_size && memcmp(bln->key, key, key_size) == 0) {
			return bln->data;
		}
		bln = bln->next;
	}
	return 0;
}

void *map_lookup(struct map *map, const void *key, unsigned int key_size) {
	unsigned int h = my_hash(key, key_size);

	while (map != 0) {
		if (map->hash == h) {
			return map_list_lookup(map->list, key, key_size);
		}
		map = map->children[h > map->hash];
	}
	return 0;
}

static void bln_release(struct bin_list_node *bln){
	if (bln_csize >= MAX_CACHE) {
		assert(bln_csize == MAX_CACHE);
		free(bln);
	}
	else {
		bln->next = bln_cache;
		bln_cache = bln;
		bln_csize++;
	}
}

static void **map_list_insert(struct bin_list_node **pbln, const void *key, unsigned int key_size) {
	struct bin_list_node *bln = *pbln;

	while (bln != 0) {
		if (bln->key_size == key_size && memcmp(bln->key, key, key_size) == 0) {
			return &bln->data;
		}
		bln = bln->next;
	}

	if ((bln = bln_cache) == 0) {
		assert(bln_csize == 0);
		bln = new_alloc(struct bin_list_node);
	}
	else {
		assert(bln_csize > 0);
		bln_csize--;
		bln_cache = bln->next;
		bln->data = 0;
	}

	bln->key = malloc(key_size);
	memcpy(bln->key, key, key_size);
	bln->key_size = key_size;
	bln->next = *pbln;
	*pbln = bln;
	return &bln->data;
}

static void *map_list_find(struct bin_list_node **pbln, const void *key, unsigned int key_size) {
	struct bin_list_node *bln = *pbln;

	while (bln != 0) {
		if (bln->key_size == key_size && memcmp(bln->key, key, key_size) == 0) {
			return bln;
		}
		bln = bln->next;
	}

	if ((bln = bln_cache) == 0) {
		assert(bln_csize == 0);
		bln = new_alloc(struct bin_list_node);
	}
	else {
		assert(bln_csize > 0);
		bln_csize--;
		bln_cache = bln->next;
		bln->data = 0;
	}

	bln->key = malloc(key_size);
	memcpy(bln->key, key, key_size);
	bln->key_size = key_size;
	bln->next = *pbln;
	*pbln = bln;
	return bln;
}

static void map_list_iter(void *env, struct bin_list_node *list,
				 void (*upcall)(void *env,
						const void *key, unsigned int key_size, void *value)) {
	while (list != 0) {
		(*upcall)(env, list->key, list->key_size, list->data);
		list = list->next;
	}
}

void **map_insert(struct map **pmap, const void *key, unsigned int key_size) {
	unsigned int h = my_hash(key, key_size);
	struct map *map;

	while ((map = *pmap) != 0) {
		if (map->hash == h) {
			return map_list_insert(&map->list, key, key_size);
		}
		pmap = &map->children[h > map->hash];
	}
	*pmap = map = new_alloc(struct map);
	map->hash = h;
	return map_list_insert(&map->list, key, key_size);
}

void *map_find(struct map **pmap, const void *key, unsigned int key_size) {
	unsigned int h = my_hash(key, key_size);
	struct map *map;

	while ((map = *pmap) != 0) {
		if (map->hash == h) {
			return map_list_find(&map->list, key, key_size);
		}
		pmap = &map->children[h > map->hash];
	}
	*pmap = map = new_alloc(struct map);
	map->hash = h;
	return map_list_find(&map->list, key, key_size);
}

void *map_retrieve(void *p, int *size) {
    struct bin_list_node *bln = p;

    if (size != NULL) {
        *size = bln->key_size;
    }
    return bln->key;
}

void map_iter(void *env, struct map *map, void (*upcall)(void *env,
						const void *key, unsigned int key_size, void *value)) {
	if (map == 0) {
		return;
	}
	map_iter(env, map->children[0], upcall);
	map_list_iter(env, map->list, upcall);
	map_iter(env, map->children[1], upcall);
}

struct map *map_init(void) {
	return 0;
}

static void map_list_release(struct bin_list_node **pbln){
	struct bin_list_node *bln;

	while ((bln = *pbln) != 0) {
		*pbln = bln->next;
		free(bln->key);
		bln_release(bln);
	}
}

void map_release(struct map *map){
	if (map == 0) {
		return;
	}
	map_release(map->children[0]);
	map_release(map->children[1]);
	map_list_release(&map->list);
	free(map);
}

void map_cleanup(void){
	struct bin_list_node *bln;

	while ((bln = bln_cache) != 0) {
		assert(bln_csize > 0);
		bln_csize--;
		bln_cache = bln->next;
		free(bln);
	}
	assert(bln_csize == 0);
}
