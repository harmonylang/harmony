#include "conallocator.h"

void conallocator_init(struct Conallocator *al) {
    al->chunk = malloc(CONALLOC_CHUNK);
    al->ptr = al->chunk;
}

void* conallocator_malloc(struct Conallocator *al, unsigned int sz) {
    //TODO
}