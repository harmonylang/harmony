#include <assert.h>
#include <stdlib.h>
#include "vector.h"

struct int_vector int_vector_init(int capacity) {
    struct int_vector vec;
    vec.capacity = capacity;
    vec.len = 0;
    vec.v = malloc(sizeof(int) * vec.capacity);
    return vec;
}


void int_vector_push(struct int_vector* vec, int v) {
    if (vec->len >= vec->capacity) {
        vec->v = realloc(vec->v, sizeof(int) * (vec->capacity * 2));
    }
    vec->v[vec->len] = v;
    ++ vec->len;
}


int int_vector_get(struct int_vector* vec, int i) {
    assert(i < vec->len);
    return vec->v[i];
}


void int_vector_free(struct int_vector* vec) {
    free(vec->v);
}
