#ifdef _WIN32
#include <windows.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <assert.h>
#include <time.h>

#ifndef TIME_UTC
#include <sys/time.h>
#endif

#ifndef HARMONY_COMBINE
#include "global.h"
#endif

#define CHUNK_SIZE	4096

double gettime(){
#if defined(TIME_UTC) && !defined(__APPLE__)
    struct timespec ts;
    timespec_get(&ts, TIME_UTC);
    return ts.tv_sec + (double) ts.tv_nsec / 1000000000;
#else
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + (double) tv.tv_usec / 1000000;
#endif
}

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

void panic(char *s){
    fprintf(stderr, "Panic: %s\n", s);
    exit(1);
}

#ifdef notdef
bool file_read(char *filename, /* OUT */ json_buf_t *buf){
	FILE *fp;

	if ((fp = fopen(filename, "r")) == NULL) {
		perror(filename);
		return false;
	}

	*buf = uv_buf_init(0, 0);
	int n;
	for (;;) {
		buf->base = realloc(buf->base, buf->len + CHUNK_SIZE);
		n = fread(buf->base + buf->len, 1, CHUNK_SIZE, fp);
		if (n < CHUNK_SIZE) {
			if (ferror(fp)) {
				perror(filename);
				fclose(fp);
				return false;
			}
			assert(feof(fp));
			assert(n >= 0);
			fclose(fp);
			buf->len += n;
			break;
		}
		assert(n == CHUNK_SIZE);
		buf->len += CHUNK_SIZE;
	}
	return true;
}
#endif // notdef
