// #undef NDEBUG

#ifdef _WIN32
#define HEAP_ALLOC
#else
// #define USE_ATOMIC
#define ALIGNED_ALLOC
#endif
