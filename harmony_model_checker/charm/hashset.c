#include "head.h"

#include "global.h"
#include "hashset.h"

struct hashset_t hashset_new(int initial_size) {
    struct hashset_t set;
    set.dict = dict_new(initial_size, NULL, NULL);
    return set;
}

static int DUMMY;

// returns true iff key was in the set before
bool hashset_insert(struct hashset_t set, const void *key, unsigned int keylen) {
    void **value = dict_insert(set.dict, NULL, key, keylen);
    bool result = *value != NULL;
    *value = &DUMMY;
    return result;
}

// returns true iff key was in the set before
bool hashset_remove(struct hashset_t set, const void *key, unsigned int keylen) {
    void **value = dict_insert(set.dict, NULL, key, keylen);
    bool result = *value != NULL;
    *value = NULL;
    return result;
}

bool hashset_contains(struct hashset_t set, const void *key, unsigned int keylen) {
    return dict_lookup(set.dict, key, keylen) != NULL;
}

void hashset_delete(struct hashset_t set) {
    dict_delete(set.dict);
}
