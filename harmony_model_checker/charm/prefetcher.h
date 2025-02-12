#ifndef PREFETCHER_H
#define PREFETCHER_H

#include <stdint.h>

#if defined(__GNUC__) || defined(__clang__)
    #define PREFETCH(addr, rw, locality) __builtin_prefetch((addr), (rw), (locality))
#elif defined(_WIN32)
    #include <xmmintrin.h>
    #define PREFETCH(addr, rw, locality) _mm_prefetch((const char*)(addr), _MM_HINT_T0)
#else
    #define PREFETCH(addr, rw, locality) // No prefetch available
#endif

#endif // PREFETCHER_H