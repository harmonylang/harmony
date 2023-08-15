#include "head.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#include "strbuf.h"

// Initializes a string buffer
void strbuf_init(struct strbuf *sb){
    sb->allocated = 64;               // random constant
    sb->buf = malloc(sb->allocated);  // initial size;
    *sb->buf = 0;                     // always keep buf \0-terminated
    sb->len = '\0';
};

// Append the given string to the string buffer
// len does not include the terminal \0 byte if any
void strbuf_append(struct strbuf *sb, const char *str, unsigned int len){
    if (sb->len + len + 1 > sb->allocated) {
        sb->allocated += len + 1;   // include room for \0
        sb->allocated *= 2;         // add some buffer space
        sb->buf = realloc(sb->buf, sb->allocated);
    }
    memcpy(&sb->buf[sb->len], str, len);
    sb->len += len;
    sb->buf[sb->len] = '\0';
}

// Formatted vprint, appended to string buffer
void strbuf_vprintf(struct strbuf *sb, const char *fmt, va_list args) {
    va_list copy;
    va_copy(copy, args);
    int len = vsnprintf(NULL, 0, fmt, copy);
    if (len < 0) {
		fprintf(stderr, "strbuf_vprintf: vsnprintf failed\n");
        exit(1);
    }

    // allocate enough space also for the null byte
    if (sb->len + len + 1 > sb->allocated) {
        sb->allocated += len + 1;   // include room for \0
        sb->allocated *= 2;         // add some buffer space
        sb->buf = realloc(sb->buf, sb->allocated);
    }

    // print into the buffer, including null byte
    if (vsprintf(&sb->buf[sb->len], fmt, args) < 0) {
		fprintf(stderr, "strbuf_vprintf: vsprintf failed\n");
        exit(1);
	}
    sb->len += len;
}

// Formatted print, appended to string buffer
void strbuf_printf(struct strbuf *sb, const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    strbuf_vprintf(sb, fmt, args);
    va_end(args);
}

// Get a pointer to the current string, which is \0-terminated
char *strbuf_getstr(struct strbuf *sb){
    return sb->buf;
}

// Get the length of the current string (not including terminal \0 byte)
unsigned int strbuf_getlen(struct strbuf *sb){
    return sb->len;
}

// Frees the buffer of a string buffer
void strbuf_deinit(struct strbuf *sb){
    free(sb->buf);
    sb->buf = (char *) 1;       // simplifies finding bugs
}

// alternative to strbuf_deinit
char *strbuf_convert(struct strbuf *sb){
    return sb->buf;
}
