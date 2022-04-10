#import "head.h"

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "minheap.h"

#define parent(k)   (int) (((k) - 1) / 2)
#define leftc(k)    (2 * (k) + 1)
#define rightc(k)    (2 * (k) + 2)

struct minheap {
    int (*cmp)(void *v1, void *v2);
    void **array;
    int alloc_size, size;
};

bool minheap_check(struct minheap *mh, void *key) {
    for (int i = 0; i < mh->size; i++) {
        if (mh->array[i] == key) {
            return true;
        }
    }
    return false;
}

struct minheap *minheap_create(int (*cmp)(void *, void *)) {
    struct minheap *mh = malloc(sizeof(struct minheap));
    if (mh == NULL) {
        fprintf(stderr, "minheap_create: out of memory\n");
        exit(1);
    }
    mh->cmp = cmp;
    mh->size = 0;
    mh->alloc_size = 1024;
    mh->array = malloc(sizeof(void *) * mh->alloc_size);
    if (mh->array == NULL) {
        fprintf(stderr, "minheap_create: out of memory\n");
        exit(1);
    }
    return mh;
}

static void minheap_swap(struct minheap *mh, int i, int j) {
    void *tmp = mh->array[i];
    mh->array[i] = mh->array[j];
    mh->array[j] = tmp;
}

static void minheap_fixup(struct minheap *mh, int k) {
    while (k > 0 && (*mh->cmp)(mh->array[k], mh->array[parent(k)]) < 0) {
        minheap_swap(mh, parent(k), k);
        k = parent(k);
    }
}

static void minheap_fixdown(struct minheap *mh, int k) {
    int j;

    while ((j = leftc(k)) < mh->size) {
        assert(j > 0);
        if (j < mh->size - 1 && (*mh->cmp)(mh->array[j+1], mh->array[j]) < 0) {
            j++;
        }
        if ((*mh->cmp)(mh->array[k], mh->array[j]) <= 0) {
            break;
        }
        minheap_swap(mh, k, j);
        k = j;
    }
}

void minheap_insert(struct minheap *mh, void *key) {
    if (mh->size == mh->alloc_size) {
        mh->alloc_size *= 2;
        mh->array = realloc(mh->array, sizeof(void *) * mh->alloc_size);
    }
    mh->array[mh->size++] = key;
    minheap_fixup(mh, mh->size - 1);
}

void minheap_decrease(struct minheap *mh, void *key) {
    for (int i = 0; i < mh->size; i++) {
        if (mh->array[i] == key) {
            minheap_fixup(mh, i);
            break;
        }
    }
}

bool minheap_empty(struct minheap *mh) {
    return mh->size == 0;
}

void *minheap_getmin(struct minheap *mh) {
    if (minheap_empty(mh)) {
        fprintf(stderr, "minheap_getmin: heap is empty\n");
        exit(1);
    }
    void *result = mh->array[0];
    mh->array[0] = mh->array[--mh->size];
    minheap_fixdown(mh, 0);
    return result;
}

int minheap_size(struct minheap *mh) {
    return mh->size;
}

// TODO: make more efficient
// Move everything from mh1 into mh2
void minheap_move(struct minheap *mh1, struct minheap *mh2){
    while (!minheap_empty(mh1)) {
        void *v = minheap_getmin(mh1);
        minheap_insert(mh2, v);
    }
}

void minheap_destroy(struct minheap *mh) {
    free(mh->array);
    free(mh);
}
