struct strbuf {
    char *buf;
    int len, allocated;
};

void strbuf_init(struct strbuf *sb);
void strbuf_append(struct strbuf *sb, const char *str, unsigned int len);
void strbuf_vprintf(struct strbuf *sb, const char *fmt, va_list args);
void strbuf_printf(struct strbuf *sb, const char *fmt, ...);
char *strbuf_getstr(struct strbuf *sb);
unsigned int strbuf_getlen(struct strbuf *sb);
void strbuf_deinit(struct strbuf *sb);
char *strbuf_convert(struct strbuf *sb);
