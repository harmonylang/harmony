#ifndef SRC_GLOBAL_H
#define SRC_GLOBAL_H

#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

#define CALLTYPE_BITS          4
#define CALLTYPE_MASK          ((1 << CALLTYPE_BITS) - 1)
#define CALLTYPE_PROCESS       1
#define CALLTYPE_NORMAL        2
#define CALLTYPE_INTERRUPT     3

#define PRI_HVAL            PRIx64
typedef uint64_t            hvalue_t;

void panic(char *s);
unsigned long to_ulong(const char *p, int len);
double gettime();

#define CHUNKSIZE   (1 << 12)

struct allocator {
    void *(*alloc)(void *ctx, unsigned int size, bool zero, bool align16);
    void *ctx;
    unsigned int worker;        // identifies worker thread
};

#endif // SRC_GLOBAL_H
