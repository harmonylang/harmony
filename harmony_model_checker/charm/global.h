#ifndef SRC_GLOBAL_H
#define SRC_GLOBAL_H

#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

// This is a handy definition for memory allocation.  In particular,
// new_alloc(t) returns a dynamically allocated of type t that has been
// zero initialized.  It avoids a lot of bugs resulting from using malloc()
// directly.
#define new_alloc(t)	(t *) calloc(1, sizeof(t))

// There are three type of method invocations:
//      NORMAL:     a normal method call
//      PROCESS:    the top level method of a thread
//      INTERRUPT:  the method is an interrupt handler
// When a method is invoked, its calltype is pushed onto the stack.  Moreover,
// the calltype also includes the return address.
#define CALLTYPE_BITS          4
#define CALLTYPE_MASK          ((1 << CALLTYPE_BITS) - 1)
#define CALLTYPE_PROCESS       1
#define CALLTYPE_NORMAL        2
#define CALLTYPE_INTERRUPT     3

// This can be used for printing Harmony values as hexadecimal values.
// For example:   printf("This is a value: %"PRI_HVAL"\n", v);
#define PRI_HVAL            PRIx64

// Harmony values are 64 bit values described in more details in value.c.
typedef uint64_t            hvalue_t;

void panic(char *s);
unsigned long to_ulong(const char *p, int len);
double gettime();

// Sometimes during allocation it is more efficient to allocate in "chunks".
// Here is a chunk size that some Charm functions use.
#define CHUNKSIZE   (1 << 12)

// Different Charm worker threads can have their own allocator.  Worker threads
// tend to allocate in large chunks and then use a pointer into these chunks.
// Worker threads can only "free" the last thing that they allocate.
//
// 'ctx' here has nothing to do with the state of a thread.  It keeps some
// information on behalf of the allocator code, and is passed as first
// argument to its alloc and free methods.
struct allocator {
    void *(*alloc)(void *ctx, unsigned int size, bool zero, bool align16);
    void (*free)(void *ctx, void *p, bool align16);
    void *ctx;
    unsigned int worker;        // identifies worker thread
};

#endif // SRC_GLOBAL_H
