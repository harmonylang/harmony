#ifndef SRC_CALM_ALLOCATOR_H
#define SRC_CALM_ALLOCATOR_H

// Not an abstraction as the allocator in global.h
// Buffered malloc without free for each thread

#include<stdlib.h>

#define HEAP_ALLOC_CHUNK (64 * 1024 * 1024) //64MB chunks

typedef unsigned char byte;

struct Allocator {
    byte *chunk; //start of the chunk
    byte *ptr; // current position in the chunk

    //TODO: For monitoring
};

static inline void allocator_init(struct Allocator *al) __attribute__ ((always_inline)) {
    al->chunk = (byte*)malloc(HEAP_ALLOC_CHUNK);
    al->ptr = al->chunk;
}

static inline void* allocator_malloc(struct Allocator *al, unsigned int sz) __attribute__ ((always_inline)) {
    void *ret = al->ptr;
    al->ptr += sz;
    return ret;
}

#define STACK_ALLOC_CHUNK (8 * 1024 * 1024) //8MB stack

struct ManualStack {
    byte *bot;
    byte *top;
};

static inline void manualstack_init(struct ManualStack *ms) __attribute__ ((always_inline)) {
    ms->bot = ms->top = (byte*)malloc(STACK_ALLOC_CHUNK);
}

static inline void* manualstack_alloca(struct ManualStack *ms, unsigned int sz) __attribute__ ((always_inline)) {
    void *ret = ms->top;
    ms->top += sz;
    return ret;
}

static inline void manualstack_reset(struct ManualStack *ms) __attribute__ ((always_inline)) {
    ms->top = ms->bot;
}

#endif //SRC_CALM_CONALLOCATOR_H