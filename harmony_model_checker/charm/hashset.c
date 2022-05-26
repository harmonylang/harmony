#include "head.h"

#include "global.h"
#include "hashset.h"

struct hashset_t hashset_new(int initial_size) {
    struct hashset_t set;
    set.dict = dict_new(0, initial_size, 0, NULL, NULL);
    return set;
}

// returns true iff key was in the set before
bool hashset_insert(struct hashset_t set, const void *key, unsigned int keylen) {
    bool new;
    dict_insert(set.dict, NULL, key, keylen, &new);
    return !new;
}

// returns true iff key was in the set before
bool hashset_remove(struct hashset_t set, const void *key, unsigned int keylen) {
    return dict_remove(set.dict, key, keylen);
}

// TODO.  Need better implementation
bool hashset_contains(struct hashset_t set, const void *key, unsigned int keylen) {
    bool new;
    dict_insert(set.dict, NULL, key, keylen, &new);
    if (new) {
        dict_remove(set.dict, key, keylen);
    }
    return !new;
}

void hashset_delete(struct hashset_t set) {
    dict_delete(set.dict);
}
