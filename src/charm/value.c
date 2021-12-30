#define _GNU_SOURCE

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#ifndef HARMONY_COMBINE
#include "global.h"
#endif

void *value_get(uint64_t v, int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        *psize = 0;
        return NULL;
    }
    return dict_retrieve((void *) v, psize);
}

void *value_copy(uint64_t v, int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        *psize = 0;
        return NULL;
    }
    int size;
    void *p = dict_retrieve((void *) v, &size);
    void *r = malloc(size);
    memcpy(r, p, size);
    if (psize != NULL) {
        *psize = size;
    }
    return r;
}

uint64_t value_put_atom(struct values_t *values, const void *p, int size){
    assert(size > 0);
    void *q = dict_find(values->atoms, p, size);
    return (uint64_t) q | VALUE_ATOM;
}

uint64_t value_put_set(struct values_t *values, void *p, int size){
    if (size == 0) {
        return VALUE_SET;
    }
    void *q = dict_find(values->sets, p, size);
    return (uint64_t) q | VALUE_SET;
}

uint64_t value_put_dict(struct values_t *values, void *p, int size){
    if (size == 0) {
        return VALUE_DICT;
    }
    void *q = dict_find(values->dicts, p, size);
    return (uint64_t) q | VALUE_DICT;
}

uint64_t value_put_address(struct values_t *values, void *p, int size){
    if (size == 0) {
        return VALUE_ADDRESS;
    }
    void *q = dict_find(values->addresses, p, size);
    return (uint64_t) q | VALUE_ADDRESS;
}

uint64_t value_put_context(struct values_t *values, struct context *ctx){
	assert(ctx->pc >= 0);
    int size = sizeof(*ctx) + (ctx->sp * sizeof(uint64_t));
    void *q = dict_find(values->contexts, ctx, size);
    return (uint64_t) q | VALUE_CONTEXT;
}

int value_cmp_bool(uint64_t v1, uint64_t v2){
    return v1 == 0 ? -1 : 1;
}

int value_cmp_int(uint64_t v1, uint64_t v2){
    return (int64_t) v1 < (int64_t) v2 ? -1 : 1;
}

int value_cmp_atom(uint64_t v1, uint64_t v2){
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    char *s1 = dict_retrieve(p1, &size1);
    char *s2 = dict_retrieve(p2, &size2);
    int size = size1 < size2 ? size1 : size2;
    int cmp = strncmp(s1, s2, size);
    if (cmp != 0) {
        return cmp;
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp_pc(uint64_t v1, uint64_t v2){
    return v1 < v2 ? -1 : 1;
}

int value_cmp_dict(uint64_t v1, uint64_t v2){
    if (v1 == 0) {
        return v2 == 0 ? 0 : -1;
    }
    if (v2 == 0) {
        return 1;
    }
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    uint64_t *vals1 = dict_retrieve(p1, &size1);
    uint64_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(uint64_t);
    size2 /= sizeof(uint64_t);
    int size = size1 < size2 ? size1 : size2;
    for (int i = 0; i < size; i++) {
        int cmp = value_cmp(vals1[i], vals2[i]);
        if (cmp != 0) {
            return cmp;
        }
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp_set(uint64_t v1, uint64_t v2){
    if (v1 == 0) {
        return v2 == 0 ? 0 : -1;
    }
    if (v2 == 0) {
        return 1;
    }
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    uint64_t *vals1 = dict_retrieve(p1, &size1);
    uint64_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(uint64_t);
    size2 /= sizeof(uint64_t);
    int size = size1 < size2 ? size1 : size2;
    for (int i = 0; i < size; i++) {
        int cmp = value_cmp(vals1[i], vals2[i]);
        if (cmp != 0) {
            return cmp;
        }
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp_address(uint64_t v1, uint64_t v2){
    if (v1 == 0) {
        return v2 == 0 ? 0 : -1;
    }
    if (v2 == 0) {
        return 1;
    }
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    uint64_t *vals1 = dict_retrieve(p1, &size1);
    uint64_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(uint64_t);
    size2 /= sizeof(uint64_t);
    int size = size1 < size2 ? size1 : size2;
    for (int i = 0; i < size; i++) {
        int cmp = value_cmp(vals1[i], vals2[i]);
        if (cmp != 0) {
            return cmp;
        }
    }
    return size1 < size2 ? -1 : 1;
}

// TODO.  Maybe should compare name tag, pc, ...
int value_cmp_context(uint64_t v1, uint64_t v2){
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    char *s1 = dict_retrieve(p1, &size1);
    char *s2 = dict_retrieve(p2, &size2);
    int size = size1 < size2 ? size1 : size2;
    int cmp = memcmp(s1, s2, size);
    if (cmp != 0) {
        return cmp < 0 ? -1 : 1;
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp(uint64_t v1, uint64_t v2){
    if (v1 == v2) {
        return 0;
    }
    int t1 = v1 & VALUE_MASK;
    int t2 = v2 & VALUE_MASK;
    if (t1 != t2) {
        return t1 < t2 ? -1 : 1;
    }
    switch (t1) {
    case VALUE_BOOL:
        return value_cmp_bool(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_INT:
        return value_cmp_int(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_ATOM:
        return value_cmp_atom(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_PC:
        return value_cmp_pc(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_DICT:
        return value_cmp_dict(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_SET:
        return value_cmp_set(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_ADDRESS:
        return value_cmp_address(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_CONTEXT:
        return value_cmp_context(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    default:
        panic("value_cmp: bad value type");
        return 0;
    }
}

void alloc_printf(char **r, char *fmt, ...){
    va_list args;

    va_start(args, fmt);
    if (vasprintf(r, fmt, args) < 0) {
		panic("alloc_printf: vasprintf");
	}
    va_end(args);
}

void append_printf(char **p, char *fmt, ...){
    char *r;
    va_list args;

    va_start(args, fmt);
    if (vasprintf(&r, fmt, args) < 0) {
		panic("append_printf: vasprintf");
	}
    va_end(args);

    if (*p == 0) {
        *p = r;
    }
    else {
        int n = strlen(*p);
        int m = strlen(r);
        *p = realloc(*p, n + m + 1);
        strcpy(*p + n, r);
        free(r);
    }
}

static char *value_string_bool(uint64_t v) {
    char *r;
    if (v != 0 && v != (1 << VALUE_BITS)) {
        fprintf(stderr, "value_string_bool %"PRIu64"\n", v);
        panic("value_string_bool: bad value");
    }
    assert(v == 0 || v == (1 << VALUE_BITS));
    alloc_printf(&r, v == 0 ? "False" : "True");
    return r;
}

static char *value_json_bool(uint64_t v) {
    char *r;
    if (v != 0 && v != (1 << VALUE_BITS)) {
        fprintf(stderr, "value_json_bool %"PRIu64"\n", v);
        panic("value_json_bool: bad value");
    }
    assert(v == 0 || v == (1 << VALUE_BITS));
    alloc_printf(&r, "{ \"type\": \"bool\", \"value\": \"%s\" }", v == 0 ? "False" : "True");
    return r;
}

static char *value_string_int(uint64_t v) {
    int64_t w = ((int64_t) v) >> VALUE_BITS;
    char *r;

    if (w == VALUE_MAX) {
        alloc_printf(&r, "inf");
    }
    else if (w == VALUE_MIN) {
        alloc_printf(&r, "-inf");
    }
    else {
        alloc_printf(&r, "%"PRId64"", w);
    }
    return r;
}

static char *value_json_int(uint64_t v) {
    int64_t w = ((int64_t) v) >> VALUE_BITS;
    char *r;

    if (w == VALUE_MAX) {
        alloc_printf(&r, "{ \"type\": \"int\", \"value\": \"inf\" }");
    }
    else if (w == VALUE_MIN) {
        alloc_printf(&r, "{ \"type\": \"int\", \"value\": \"-inf\" }");
    }
    else {
        alloc_printf(&r, "{ \"type\": \"int\", \"value\": \"%"PRId64"\" }", w);
    }
    return r;
}

static char *value_string_atom(uint64_t v) {
    void *p = (void *) v;
    int size;
    char *s = dict_retrieve(p, &size), *r;
	struct strbuf sb;

	strbuf_init(&sb);
    strbuf_append(&sb, "\"", 1);
	while (size > 0) {
		switch (*s) {
		case '"':
			strbuf_append(&sb, "\\\"", 2);
			break;
		case '\\':
			strbuf_append(&sb, "\\\\", 2);
			break;
		case '\n':
			strbuf_append(&sb, "\\n", 2);
			break;
		case '\r':
			strbuf_append(&sb, "\\r", 2);
			break;
		default:
			strbuf_append(&sb, s, 1);
		}
		s++;
		size--;
	}
    strbuf_append(&sb, "\"", 1);
	return strbuf_getstr(&sb);
}

static char *value_json_atom(uint64_t v) {
    void *p = (void *) v;
    int size;
    char *s = dict_retrieve(p, &size), *r;
    assert(size > 0);
    if (size > 1 || (isprint(s[0]) && s[0] != '"' && s[0] != '\\')) {
        char *esc = json_escape(s, size);
        alloc_printf(&r, "{ \"type\": \"atom\", \"value\": \"%s\" }", esc);
        free(esc);
    }
    else {
        alloc_printf(&r, "{ \"type\": \"char\", \"value\": \"%02x\" }", s[0]);
    }
    return r;
}

static char *value_string_pc(uint64_t v) {
    char *r;
    assert((v >> VALUE_BITS) < 10000);      // debug
    alloc_printf(&r, "PC(%"PRIu64")", v >> VALUE_BITS);
    return r;
}

static char *value_json_pc(uint64_t v) {
    char *r;
    alloc_printf(&r, "{ \"type\": \"pc\", \"value\": \"%"PRIu64"\" }", v >> VALUE_BITS);
    return r;
}

static char *value_string_dict(uint64_t v) {
    char *r;

    if (v == 0) {
        alloc_printf(&r, "()");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(uint64_t);

    bool islist = true;
    for (uint64_t i = 0; i < size; i++) {
        if (vals[2*i] != ((i << VALUE_BITS) | VALUE_INT)) {
            islist = false;
            break;
        }
    }

    if (islist) {
        alloc_printf(&r, "(");
        for (int i = 0; i < size; i++) {
            if (i != 0) {
                append_printf(&r, ", ");
            }
            char *val = value_string(vals[2*i+1]);
            append_printf(&r, "%s", val);
            free(val);
        }
        append_printf(&r, ")");
    }
    else {
        alloc_printf(&r, "{ ");
        for (int i = 0; i < size; i++) {
            if (i != 0) {
                append_printf(&r, ", ");
            }
            char *key = value_string(vals[2*i]);
            char *val = value_string(vals[2*i+1]);
            append_printf(&r, "%s: %s", key, val);
            free(key);
            free(val);
        }
        append_printf(&r, " }");
    }
    return r;
}

static char *value_json_dict(uint64_t v) {
    char *r;

    if (v == 0) {
        alloc_printf(&r, "{ \"type\": \"dict\", \"value\": [] }");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(uint64_t);

    alloc_printf(&r, "{ \"type\": \"dict\", \"value\": [");
    for (int i = 0; i < size; i++) {
        if (i != 0) {
            append_printf(&r, ", ");
        }
        char *key = value_json(vals[2*i]);
        char *val = value_json(vals[2*i+1]);
        append_printf(&r, "{ \"key\": %s, \"value\": %s }", key, val);
        free(key);
        free(val);
    }
    append_printf(&r, " ] }");
    return r;
}

static char *value_string_set(uint64_t v) {
    char *r;

    if (v == 0) {
        alloc_printf(&r, "{}");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);

    alloc_printf(&r, "{ ");
    for (int i = 0; i < size; i++) {
        char *val = value_string(vals[i]);
        if (i == 0) {
            append_printf(&r, "%s", val);
        }
        else {
            append_printf(&r, ", %s", val);
        }
        free(val);
    }
    append_printf(&r, " }");
    return r;
}

static char *value_json_set(uint64_t v) {
    char *r;

    if (v == 0) {
        alloc_printf(&r, "{ \"type\": \"set\", \"value\": [] }");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);

    alloc_printf(&r, "{ \"type\": \"set\", \"value\": [");
    for (int i = 0; i < size; i++) {
        char *val = value_json(vals[i]);
        if (i == 0) {
            append_printf(&r, "%s", val);
        }
        else {
            append_printf(&r, ", %s", val);
        }
        free(val);
    }
    append_printf(&r, " ] }");
    return r;
}

char *indices_string(const uint64_t *vec, int size) {
    char *r;
    if (size == 0) {
        alloc_printf(&r, "None");
        return r;
    }
    char *s = value_string(vec[0]);
    assert(s[0] == '"');
	int len = strlen(s);
    alloc_printf(&r, "?%.*s", len - 2, s + 1);
    free(s);

    for (int i = 1; i < size; i++) {
        s = value_string(vec[i]);
        append_printf(&r, "[%s]", s);
    }

    return r;
}

static char *value_string_address(uint64_t v) {
    if (v == 0) {
        char *r;
        alloc_printf(&r, "None");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *indices = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);
    assert(size > 0);
    return indices_string(indices, size);
}

static char *value_json_address(uint64_t v) {
    char *r;
    if (v == 0) {
        alloc_printf(&r, "{ \"type\": \"address\", \"value\": [] }");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);
    assert(size > 0);
    alloc_printf(&r, "{ \"type\": \"address\", \"value\": [");
    for (int i = 0; i < size; i++) {
        char *val = value_json(vals[i]);
        if (i == 0) {
            append_printf(&r, "%s", val);
        }
        else {
            append_printf(&r, ", %s", val);
        }
        free(val);
    }

    append_printf(&r, " ] }");
    return r;
}

static char *value_string_context(uint64_t v) {
    struct context *ctx = value_get(v, NULL);
    char *r;
#ifdef SHORT
    char *name = value_string(ctx->name);
    alloc_printf(&r, "CONTEXT(%s, %d)", name, ctx->pc);
    free(name);
#else
    char *s;
    alloc_printf(&r, "CONTEXT(");

    s = value_string(ctx->name);
    append_printf(&r, "name=%s", s);
    free(s);

    s = value_string(ctx->entry);
    append_printf(&r, ",entry=%s", s);
    free(s);

    s = value_string(ctx->arg);
    append_printf(&r, ",arg=%s", s);
    free(s);

    s = value_string(ctx->this);
    append_printf(&r, ",this=%s", s);
    free(s);

    s = value_string(ctx->vars);
    append_printf(&r, ",vars=%s", s);
    free(s);

    s = value_string(ctx->trap_pc);
    append_printf(&r, ",trap_pc=%s", s);
    free(s);

    s = value_string(ctx->trap_arg);
    append_printf(&r, ",trap_arg=%s", s);
    free(s);

    s = value_string(ctx->failure);
    append_printf(&r, ",failure=%s", s);
    free(s);

    append_printf(&r, ",pc=%d", ctx->pc);

    append_printf(&r, ",fp=%d", ctx->fp);

    append_printf(&r, ",readonly=%d", ctx->readonly);

    append_printf(&r, ",atomic=%d", ctx->atomic);

    append_printf(&r, ",aflag=%d", ctx->atomicFlag);

    append_printf(&r, ",il=%d", ctx->interruptlevel);

    append_printf(&r, ",stopped=%d", ctx->stopped);

    append_printf(&r, ",terminated=%d", ctx->terminated);

    append_printf(&r, ",eternal=%d", ctx->eternal);

    append_printf(&r, ",sp=%d,STACK[", ctx->sp);

    for (int i = 0; i < ctx->sp; i++) {
        s = value_string(ctx->stack[i]);
        append_printf(&r, ",%s", s);
        free(s);
    }

    append_printf(&r, "]");

    append_printf(&r, ")");
#endif
    return r;
}

static char *value_json_context(uint64_t v) {
    struct context *ctx = value_get(v, NULL);
    char *r, *val;
    alloc_printf(&r, "{ \"type\": \"context\", \"value\": {");

    val = value_json(ctx->name);
    append_printf(&r, "\"name\": %s", val);
    free(val);

    val = value_json(ctx->arg);
    append_printf(&r, ", \"arg\": %s", val);
    free(val);

    append_printf(&r, ", \"pc\": { \"type\": \"pc\", \"value\": \"%d\" }", ctx->pc);

    append_printf(&r, " } }");
    return r;
}

char *value_string(uint64_t v){
    switch (v & VALUE_MASK) {
    case VALUE_BOOL:
        return value_string_bool(v & ~VALUE_MASK);
    case VALUE_INT:
        return value_string_int(v & ~VALUE_MASK);
    case VALUE_ATOM:
        return value_string_atom(v & ~VALUE_MASK);
    case VALUE_PC:
        return value_string_pc(v & ~VALUE_MASK);
    case VALUE_DICT:
        return value_string_dict(v & ~VALUE_MASK);
    case VALUE_SET:
        return value_string_set(v & ~VALUE_MASK);
    case VALUE_ADDRESS:
        return value_string_address(v & ~VALUE_MASK);
    case VALUE_CONTEXT:
        return value_string_context(v & ~VALUE_MASK);
    default:
        panic("value_string: bad value type");
        return NULL;
    }
}

char *value_json(uint64_t v){
    switch (v & VALUE_MASK) {
    case VALUE_BOOL:
        return value_json_bool(v & ~VALUE_MASK);
    case VALUE_INT:
        return value_json_int(v & ~VALUE_MASK);
    case VALUE_ATOM:
        return value_json_atom(v & ~VALUE_MASK);
    case VALUE_PC:
        return value_json_pc(v & ~VALUE_MASK);
    case VALUE_DICT:
        return value_json_dict(v & ~VALUE_MASK);
    case VALUE_SET:
        return value_json_set(v & ~VALUE_MASK);
    case VALUE_ADDRESS:
        return value_json_address(v & ~VALUE_MASK);
    case VALUE_CONTEXT:
        return value_json_context(v & ~VALUE_MASK);
    default:
        panic("value_json: bad value type");
        return NULL;
    }
}

bool atom_cmp(json_buf_t buf, char *s){
    int n = strlen(s);
    if (n != buf.len) {
        return false;
    }
    return strncmp(buf.base, s, n) == 0;
}

uint64_t value_bool(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    if (atom_cmp(value->u.atom, "False")) {
        return VALUE_BOOL;
    }
    if (atom_cmp(value->u.atom, "True")) {
        return (1 << VALUE_BITS) | VALUE_BOOL;
    }
    panic("value_bool: bad value");
    return 0;
}

uint64_t value_int(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    uint64_t v;
    if (atom_cmp(value->u.atom, "inf")) {
        v = VALUE_MAX;
    }
    else if (atom_cmp(value->u.atom, "-inf")) {
        v = VALUE_MIN;
    }
    else {
        char *copy = malloc(value->u.atom.len + 1);
        memcpy(copy, value->u.atom.base, value->u.atom.len);
        copy[value->u.atom.len] = 0;
        v = atol(copy);
        free(copy);
    }
    return (v << VALUE_BITS) | VALUE_INT;
}

uint64_t value_pc(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    char *copy = malloc(value->u.atom.len + 1);
    memcpy(copy, value->u.atom.base, value->u.atom.len);
    copy[value->u.atom.len] = 0;
    long v = atol(copy);
    free(copy);
    return (v << VALUE_BITS) | VALUE_PC;
}

uint64_t value_atom(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
	assert(value->u.atom.len > 0);
    void *p = dict_find(values->atoms, value->u.atom.base, value->u.atom.len);
    return (uint64_t) p | VALUE_ATOM;
}

uint64_t value_char(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    char *copy = malloc(value->u.atom.len + 1);
    memcpy(copy, value->u.atom.base, value->u.atom.len);
    copy[value->u.atom.len] = 0;
    unsigned long x;
    sscanf(copy, "%lx", &x);
    free(copy);
    if (x == 0) {
        printf("value_char: can't handle null characters yet\n");
    }
    else if (x != (x & 0x7F)) {
        printf("value_char: can only handle ASCII characters right now\n");
    }
    char v = x & 0x7F;
    void *p = dict_find(values->atoms, &v, 1);
    return (uint64_t) p | VALUE_ATOM;
}

uint64_t value_dict(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return VALUE_DICT;
    }
    uint64_t *vals = malloc(value->u.list.nvals * sizeof(uint64_t) * 2);
    for (int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        struct json_value *k = dict_lookup(jv->u.map, "key", 3);
        assert(k->type == JV_MAP);
        struct json_value *v = dict_lookup(jv->u.map, "value", 5);
        assert(v->type == JV_MAP);
        vals[2*i] = value_from_json(values, k->u.map);
        vals[2*i+1] = value_from_json(values, v->u.map);
    }

    // vals is sorted already by harmony compiler
    void *p = dict_find(values->dicts, vals,
                    value->u.list.nvals * sizeof(uint64_t) * 2);
    free(vals);
    return (uint64_t) p | VALUE_DICT;
}

uint64_t value_set(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (uint64_t) VALUE_SET;
    }
    uint64_t *vals = malloc(value->u.list.nvals * sizeof(uint64_t));
    for (int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(values, jv->u.map);
    }

    // vals is sorted already by harmony compiler
    void *p = dict_find(values->sets, vals, value->u.list.nvals * sizeof(uint64_t));
    free(vals);
    return (uint64_t) p | VALUE_SET;
}

uint64_t value_address(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (uint64_t) VALUE_ADDRESS;
    }
    uint64_t *vals = malloc(value->u.list.nvals * sizeof(uint64_t));
    for (int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(values, jv->u.map);
    }
    void *p = dict_find(values->addresses, vals,
                            value->u.list.nvals * sizeof(uint64_t));
    free(vals);
    return (uint64_t) p | VALUE_ADDRESS;
}

uint64_t value_from_json(struct values_t *values, struct dict *map){
    struct json_value *type = dict_lookup(map, "type", 4);
    assert(type != 0);
    assert(type->type == JV_ATOM);
    if (atom_cmp(type->u.atom, "bool")) {
        return value_bool(map);
    }
    else if (atom_cmp(type->u.atom, "int")) {
        return value_int(map);
    }
    else if (atom_cmp(type->u.atom, "atom")) {
        return value_atom(values, map);
    }
    else if (atom_cmp(type->u.atom, "char")) {
        return value_char(values, map);
    }
    else if (atom_cmp(type->u.atom, "dict")) {
        return value_dict(values, map);
    }
    else if (atom_cmp(type->u.atom, "set")) {
        return value_set(values, map);
    }
    else if (atom_cmp(type->u.atom, "pc")) {
        return value_pc(map);
    }
    else if (atom_cmp(type->u.atom, "address")) {
        return value_address(values, map);
    }
    else {
        panic("value_from_json: bad type");
        return 0;
    }
}

void value_init(struct values_t *values){
    values->atoms = dict_new(0);
    values->dicts = dict_new(0);
    values->sets = dict_new(0);
    values->addresses = dict_new(0);
    values->contexts = dict_new(0);
}

void value_set_concurrent(struct values_t *values, int concurrent){
    dict_set_concurrent(values->atoms, concurrent);
    dict_set_concurrent(values->dicts, concurrent);
    dict_set_concurrent(values->sets, concurrent);
    dict_set_concurrent(values->addresses, concurrent);
    dict_set_concurrent(values->contexts, concurrent);
}

// Store key:value in the given dictionary and returns its value code
uint64_t value_dict_store(struct values_t *values, uint64_t dict, uint64_t key, uint64_t value){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    if (false) {
        char *p = value_string(value);
        char *q = value_string(dict);
        char *r = value_string(key);
        printf("DICT_STORE %s %s %s\n", p, q, r);
        free(p);
        free(q);
        free(r);
    }

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(uint64_t);
        assert(size % 2 == 0);
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            if (vals[i + 1] == value) {
                return dict;
            }
            int n = size * sizeof(uint64_t);
            uint64_t *copy = malloc(n);
            memcpy(copy, vals, n);
            copy[i + 1] = value;
            uint64_t v = value_put_dict(values, copy, n);
            free(copy);
            return v;
        }
        if (value_cmp(vals[i], key) > 0) {
            break;
        }
    }

    int n = (size + 2) * sizeof(uint64_t);
    uint64_t *nvals = malloc(n);
    memcpy(nvals, vals, i * sizeof(uint64_t));
    nvals[i] = key;
    nvals[i+1] = value;
    memcpy(&nvals[i+2], &vals[i], (size - i) * sizeof(uint64_t));
    uint64_t v = value_put_dict(values, nvals, n);
    free(nvals);
    return v;
}

uint64_t value_dict_load(uint64_t dict, uint64_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(uint64_t);
        assert(size % 2 == 0);
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            return vals[i + 1];
        }
        /*
            if (value_cmp(vals[i], key) > 0) {
                break;
            }
        */
    }

    printf("CAN'T FIND %s in %s\n", value_string(key), value_string(dict));
    panic("dict_load");
    return 0;
}

uint64_t value_dict_remove(struct values_t *values, uint64_t dict, uint64_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        return VALUE_DICT;
    }
    vals = value_get(dict & ~VALUE_MASK, &size);
    size /= sizeof(uint64_t);
    assert(size % 2 == 0);

    if (size == 2) {
        return vals[0] == key ? VALUE_DICT : dict;
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            int n = (size - 2) * sizeof(uint64_t);
            uint64_t *copy = malloc(n);
            memcpy(copy, vals, i * sizeof(uint64_t));
            memcpy(&copy[i], &vals[i+2],
                   (size - i - 2) * sizeof(uint64_t));
            uint64_t v = value_put_dict(values, copy, n);
            free(copy);
            return v;
        }
        /*
            if (value_cmp(vals[i], key) > 0) {
                assert(false);
            }
        */
    }

    return dict;
}

bool value_dict_tryload(uint64_t dict, uint64_t key, uint64_t *result){
    if ((dict & VALUE_MASK) != VALUE_DICT) {
        return false;
    }

    uint64_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(uint64_t);
        assert(size % 2 == 0);
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            *result = vals[i + 1];
            return true;
        }
        /*
            if (value_cmp(vals[i], key) > 0) {
                break;
            }
        */
    }
    return false;
}

uint64_t value_bag_add(struct values_t *values, uint64_t bag, uint64_t v, int multiplicity){
    uint64_t count;
    if (value_dict_tryload(bag, v, &count)) {
        assert((count & VALUE_MASK) == VALUE_INT);
        assert(count != VALUE_INT);
        count += multiplicity << VALUE_BITS;
        return value_dict_store(values, bag, v, count);
    }
    else {
        return value_dict_store(values, bag, v, (1 << VALUE_BITS) | VALUE_INT);
    }
}

void value_ctx_push(struct context **pctx, uint64_t v){
    assert(*pctx != NULL);
    struct context *ctx = realloc(*pctx, sizeof(struct context) +
                                         ((*pctx)->sp + 1) * sizeof(uint64_t));

    ctx->stack[ctx->sp++] = v;
    *pctx = ctx;
}

uint64_t value_ctx_pop(struct context **pctx){
    struct context *ctx = *pctx;

    assert(ctx->sp > 0);
    return ctx->stack[--ctx->sp];
}

uint64_t value_ctx_failure(struct context *ctx, struct values_t *values, char *fmt, ...){
    char *r;
    va_list args;

    assert(ctx->failure == 0);

    va_start(args, fmt);
    if (vasprintf(&r, fmt, args) < 0) {
        panic("ctx_failure: vasprintf");
    }
    va_end(args);

    ctx->failure = value_put_atom(values, r, strlen(r));
    free(r);

    return 0;
}

bool value_ctx_all_eternal(uint64_t ctxbag) {
    if (ctxbag == VALUE_DICT) {     // optimization
        return true;
    }
    int size;
    uint64_t *vals = value_get(ctxbag, &size);
    size /= sizeof(uint64_t);
    bool all = true;
    for (int i = 0; i < size; i += 2) {
        assert((vals[i] & VALUE_MASK) == VALUE_CONTEXT);
        assert((vals[i + 1] & VALUE_MASK) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        assert(ctx != NULL);
        if (!ctx->eternal) {
            all = false;
            break;
        }
    }
    return all;
}
