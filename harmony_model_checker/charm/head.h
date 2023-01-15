// #undef NDEBUG

#ifdef _WIN32
#define HEAP_ALLOC
#ifndef __STDC_NO_ATOMICS__     // don't really seem to work yet
#define __STDC_NO_ATOMICS__
#endif
#else
#define ALIGNED_ALLOC
#endif

#ifndef __STDC_NO_ATOMICS__
#define USE_ATOMIC
#endif
