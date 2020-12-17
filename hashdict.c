#include "hashdict.h"
#define hash_func meiyan

static inline uint32_t meiyan(const char *key, int count) {
	typedef uint32_t* P;
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

struct dictionary* dic_new(int initial_size) {
	struct dictionary* dic = malloc(sizeof(struct dictionary));
	if (initial_size == 0) initial_size = 1024;
	dic->length = initial_size;
	dic->count = 0;
	dic->table = calloc(sizeof(struct keynode*), initial_size);
	dic->growth_treshold = 2.0;
	dic->growth_factor = 10;
	return dic;
}

void dic_delete(struct dictionary* dic) {
	for (int i = 0; i < dic->length; i++) {
		if (dic->table[i])
			keynode_delete(dic->table[i]);
	}
	free(dic->table);
	dic->table = 0;
	free(dic);
}

void dic_reinsert_when_resizing(struct dictionary* dic, struct keynode *k2) {
	int n = hash_func(k2->key, k2->len) % dic->length;
	if (dic->table[n] == 0) {
		dic->table[n] = k2;
		return;
	}
	struct keynode *k = dic->table[n];
	k2->next = k;
	dic->table[n] = k2;
}

void dic_resize(struct dictionary* dic, int newsize) {
	int o = dic->length;
	struct keynode **old = dic->table;
	dic->table = calloc(sizeof(struct keynode*), newsize);
	dic->length = newsize;
	for (int i = 0; i < o; i++) {
		struct keynode *k = old[i];
		while (k) {
			struct keynode *next = k->next;
			k->next = 0;
			dic_reinsert_when_resizing(dic, k);
			k = next;
		}
	}
	free(old);
}

void *dic_find(struct dictionary* dic, const void *key, int keyn) {
	int n = hash_func((const char*)key, keyn) % dic->length;
	if (dic->table[n] == 0) {
		double f = (double)dic->count / (double)dic->length;
		if (f > dic->growth_treshold) {
			dic_resize(dic, dic->length * dic->growth_factor);
			return dic_find(dic, key, keyn);
		}
		dic->table[n] = keynode_new((char*)key, keyn);
		dic->count++;
		return dic->table[n];
	}
	struct keynode *k = dic->table[n];
	while (k) {
		if (k->len == keyn && memcmp(k->key, key, keyn) == 0) {
			return k;
		}
		k = k->next;
	}
	dic->count++;
	struct keynode *k2 = keynode_new((char*)key, keyn);
	k2->next = dic->table[n];
	dic->table[n] = k2;
	return k2;
}

void **dic_insert(struct dictionary *dic, const void *key, int keyn){
    struct keynode *k = dic_find(dic, key, keyn);
    return &k->value;
}

void *dic_retrieve(const void *p, int *psize){
    const struct keynode *k = p;
    if (psize != NULL) {
        *psize = k->len;
    }
    return k->key;
}

void *dic_lookup(struct dictionary* dic, const void *key, int keyn) {
	int n = hash_func((const char*)key, keyn) % dic->length;
	__builtin_prefetch(dic->table[n]);
	struct keynode *k = dic->table[n];
	if (!k) return 0;
	while (k) {
		if (k->len == keyn && !memcmp(k->key, key, keyn)) {
			return k->value;
		}
		k = k->next;
	}
	return 0;
}

void dic_iter(struct dictionary* dic, enumFunc f, void *env) {
	for (int i = 0; i < dic->length; i++) {
		if (dic->table[i] != 0) {
			struct keynode *k = dic->table[i];
			while (k) {
				(*f)(env, k->key, k->len, k->value);
				k = k->next;
			}
		}
	}
}
