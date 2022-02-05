#ifndef SRC_STRBUF_H
#define SRC_STRBUF_H

#include <stdarg.h>

typedef struct strbuf {
    char *buf;
    unsigned int len, allocated;
} strbuf;

void strbuf_init(strbuf *sb);
void strbuf_append(strbuf *sb, const char *str, unsigned int len);
void strbuf_vprintf(strbuf *sb, const char *fmt, va_list args);
void strbuf_printf(strbuf *sb, const char *fmt, ...);
char *strbuf_getstr(strbuf *sb);
unsigned int strbuf_getlen(strbuf *sb);
void strbuf_deinit(strbuf *sb);
char *strbuf_convert(strbuf *sb);

#endif // SRC_STRBUF_H
