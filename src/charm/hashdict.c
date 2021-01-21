#ifndef HARMONY_COMBINE
#include "hashdict.h"
#endif

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

struct keynode *keynode_new(char*k, int l) {
	struct keynode *node = malloc(sizeof(struct keynode));
	node->len = l;
	node->key = malloc(l);
	memcpy(node->key, k, l);
	node->next = 0;
	node->value = 0;
	return node;
}

void keynode_delete(struct keynode *node) {
	free(node->key);
	if (node->next) keynode_delete(node->next);
	free(node);
}

struct dict *dict_new(int initial_size) {
	struct dict *dict = malloc(sizeof(struct dict));
	if (initial_size == 0) initial_size = 1024;
	dict->length = initial_size;
	dict->count = 0;
	dict->table = calloc(sizeof(struct keynode*), initial_size);
	dict->growth_treshold = 2.0;
	dict->growth_factor = 10;
	return dict;
}

void dict_delete(struct dict *dict) {
	for (int i = 0; i < dict->length; i++) {
		if (dict->table[i])
			keynode_delete(dict->table[i]);
	}
	free(dict->table);
	dict->table = 0;
	free(dict);
}

void dict_reinsert_when_resizing(struct dict *dict, struct keynode *k2) {
	int n = hash_func(k2->key, k2->len) % dict->length;
	if (dict->table[n] == 0) {
		dict->table[n] = k2;
		return;
	}
	struct keynode *k = dict->table[n];
	k2->next = k;
	dict->table[n] = k2;
}

void dict_resize(struct dict *dict, int newsize) {
	int o = dict->length;
	struct keynode **old = dict->table;
	dict->table = calloc(sizeof(struct keynode*), newsize);
	dict->length = newsize;
	for (int i = 0; i < o; i++) {
		struct keynode *k = old[i];
		while (k) {
			struct keynode *next = k->next;
			k->next = 0;
			dict_reinsert_when_resizing(dict, k);
			k = next;
		}
	}
	free(old);
}

void *dict_find(struct dict *dict, const void *key, unsigned int keyn) {
	int n = hash_func((const char*)key, keyn) % dict->length;
	if (dict->table[n] == 0) {
		double f = (double)dict->count / (double)dict->length;
		if (f > dict->growth_treshold) {
			dict_resize(dict, dict->length * dict->growth_factor);
			return dict_find(dict, key, keyn);
		}
		dict->table[n] = keynode_new((char*)key, keyn);
		dict->count++;
		return dict->table[n];
	}
	struct keynode *k = dict->table[n];
	while (k) {
		if (k->len == keyn && memcmp(k->key, key, keyn) == 0) {
			return k;
		}
		k = k->next;
	}
	dict->count++;
	struct keynode *k2 = keynode_new((char*)key, keyn);
	k2->next = dict->table[n];
	dict->table[n] = k2;
	return k2;
}

void **dict_insert(struct dict *dict, const void *key, unsigned int keyn){
    struct keynode *k = dict_find(dict, key, keyn);
    return &k->value;
}

void *dict_retrieve(const void *p, int *psize){
    const struct keynode *k = p;
    if (psize != NULL) {
        *psize = k->len;
    }
    return k->key;
}

void *dict_lookup(struct dict *dict, const void *key, unsigned int keyn) {
	int n = hash_func((const char*)key, keyn) % dict->length;
	// __builtin_prefetch(dict->table[n]);
	struct keynode *k = dict->table[n];
	if (!k) return 0;
	while (k) {
		if (k->len == keyn && !memcmp(k->key, key, keyn)) {
			return k->value;
		}
		k = k->next;
	}
	return 0;
}

void dict_iter(struct dict *dict, enumFunc f, void *env) {
	for (int i = 0; i < dict->length; i++) {
		if (dict->table[i] != 0) {
			struct keynode *k = dict->table[i];
			while (k) {
				(*f)(env, k->key, k->len, k->value);
				k = k->next;
			}
		}
	}
}
