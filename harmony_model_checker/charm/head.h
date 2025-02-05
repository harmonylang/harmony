// #define DEBUGGING

// #define SHORT_PTR

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
#else // _WIN32
#define ALIGNED_ALLOC
#include <stdlib.h>
#if defined(__APPLE__) && defined(__clang__)
void *my_aligned_alloc(size_t alignment, size_t size);
#else
#define my_aligned_alloc(a, s)  aligned_alloc(a, s)
#endif // __APPLE__
#endif // _WIN32

#ifdef __linux__
#ifdef NUMA
#include <numa.h>
#include <numaif.h>
#include <omp.h>
#endif
#endif
