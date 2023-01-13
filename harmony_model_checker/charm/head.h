// #undef NDEBUG

#ifdef _WIN32
#define HEAP_ALLOC
#else
#define ALIGNED_ALLOC
#endif

#ifndef __STDC_NO_ATOMICS__
#define USE_ATOMIC
#endif
