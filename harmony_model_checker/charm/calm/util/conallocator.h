#ifndef SRC_CALM_CONALLOCATOR_H
#define SRC_CALM_CONALLOCATOR_H

// Not an abstraction as the allocator in global.h
// Buffered malloc without free for each thread

#define CONALLOC_CHUNK (64 * 1024 * 1024) //64MB chunks

typedef unsigned char byte;

struct Conallocator {
    byte *chunk; //start of the chunk
    byte *ptr; // current position in the chunk

    //TODO: For monitoring
};

void conallocator_init(struct Conallocator *al);
inline void *conallocator_malloc(struct Conallocator *al, unsigned int sz) __attribute__ ((always_inline)); //cannot allocate things larger than CONALLOC_CHUNK

#endif //SRC_CALM_CONALLOCATOR_H