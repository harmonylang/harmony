#include "head.h"

#ifdef _WIN32
#include <windows.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <assert.h>

#ifndef HARMONY_COMBINE
#include "global.h"
#endif

// Convert a string representation of an integer to an unsigned long value.
unsigned long to_ulong(const char *p, int len){
	unsigned long r = 0;

	while (len > 0) {
		assert(isdigit(*p));
		r *= 10;
		r += *p - '0';
		len--;
		p++;
	}
	return r;
}

// Something went terribly wrong.  Print a message and exit.
void panic(char *s){
    fprintf(stderr, "Panic: %s\n", s);
    exit(1);
}

#ifdef __APPLE__
void *my_aligned_alloc(size_t alignment, size_t size){
    if (__builtin_available(macOS 10.15, *)) {
        return aligned_alloc(alignment, size);
    }
    panic("aligned_alloc not available in current version of MacOSX");
    return NULL;
}
#endif
