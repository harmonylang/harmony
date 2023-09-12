#undef NDEBUG

// This file is included at the start of every C source.  It mostly deals with
// architecture dependent stuff

#ifdef _WIN32
#define HEAP_ALLOC
#ifndef __STDC_NO_ATOMICS__     // don't really seem to work yet
#define __STDC_NO_ATOMICS__
#endif
#else
#define ALIGNED_ALLOC

#include <stdlib.h>
#ifdef __APPLE__
void *my_aligned_alloc(size_t alignment, size_t size);
#else
#define my_aligned_alloc(a, s)  aligned_alloc(a, s)
#endif
#endif

#ifndef __STDC_NO_ATOMICS__
#define USE_ATOMIC
#endif
