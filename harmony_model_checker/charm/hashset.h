#ifndef SRC_HASHSET_H
#define SRC_HASHSET_H

#include <stdbool.h>
#include <assert.h>
#include "hashdict.h"

struct hashset_t {
    struct dict *dict;  // a dict from values to DUMMY
};

struct hashset_t hashset_new(int initial_size);

// returns true iff key was in the set before
bool hashset_insert(struct hashset_t set, const void *key, unsigned int keylen);

// returns true iff key was in the set before
bool hashset_remove(struct hashset_t set, const void *key, unsigned int keylen);

bool hashset_contains(struct hashset_t set, const void *key, unsigned int keylen);

void hashset_delete(struct hashset_t set);

#endif //SRC_HASHSET_H
