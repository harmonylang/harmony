// #define DEBUGGING

// #define SHORT_POINTER

#ifdef DEBUGGING
# undef NDEBUG
#else
# ifndef NDEBUG
#  define NDEBUG
# endif
#endif

// This file is included at the start of every C source.  It mostly deals with
// architecture dependent stuff

#ifdef _WIN32
#define HEAP_ALLOC
#ifndef __STDC_NO_ATOMICS__     // don't really seem to work yet
#define __STDC_NO_ATOMICS__
#endif
#else // _WIN32
#define ALIGNED_ALLOC

#include <stdlib.h>
#ifdef __APPLE__
void *my_aligned_alloc(size_t alignment, size_t size);
#else
#define my_aligned_alloc(a, s)  aligned_alloc(a, s)
#endif // __APPLE__
#endif // _WIN32

#ifndef __STDC_NO_ATOMICS__
#define USE_ATOMIC
#include <stdatomic.h>
#define hAtomic(x)  _Atomic(x)
#endif
