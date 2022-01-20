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

void *value_get(hvalue_t v, int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        *psize = 0;
        return NULL;
    }
    return dict_retrieve((void *) v, psize);
}

void *value_copy(hvalue_t v, int *psize){
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

hvalue_t value_put_atom(struct values_t *values, const void *p, int size){
    if (size == 0) {
        return VALUE_ATOM;
    }
    void *q = dict_find(values->atoms, p, size);
    return (hvalue_t) q | VALUE_ATOM;
}

hvalue_t value_put_set(struct values_t *values, void *p, int size){
    if (size == 0) {
        return VALUE_SET;
    }
    void *q = dict_find(values->sets, p, size);
    return (hvalue_t) q | VALUE_SET;
}

hvalue_t value_put_dict(struct values_t *values, void *p, int size){
    if (size == 0) {
        return VALUE_DICT;
    }
    void *q = dict_find(values->dicts, p, size);
    return (hvalue_t) q | VALUE_DICT;
}

hvalue_t value_put_address(struct values_t *values, void *p, int size){
    if (size == 0) {
        return VALUE_ADDRESS;
    }
    void *q = dict_find(values->addresses, p, size);
    return (hvalue_t) q | VALUE_ADDRESS;
}

hvalue_t value_put_context(struct values_t *values, struct context *ctx){
	assert(ctx->pc >= 0);
    int size = sizeof(*ctx) + (ctx->sp * sizeof(hvalue_t));
    void *q = dict_find(values->contexts, ctx, size);
    return (hvalue_t) q | VALUE_CONTEXT;
}

int value_cmp_bool(hvalue_t v1, hvalue_t v2){
    return v1 == 0 ? -1 : 1;
}

int value_cmp_int(hvalue_t v1, hvalue_t v2){
    return (int64_t) v1 < (int64_t) v2 ? -1 : 1;
}

int value_cmp_atom(hvalue_t v1, hvalue_t v2){
    int size1, size2;
    char *s1 = value_get(v1, &size1);
    char *s2 = value_get(v2, &size2);
    int size = size1 < size2 ? size1 : size2;
    int cmp = strncmp(s1, s2, size);
    if (cmp != 0) {
        return cmp;
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp_pc(hvalue_t v1, hvalue_t v2){
    return v1 < v2 ? -1 : 1;
}

int value_cmp_dict(hvalue_t v1, hvalue_t v2){
    if (v1 == 0) {
        return v2 == 0 ? 0 : -1;
    }
    if (v2 == 0) {
        return 1;
    }
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    hvalue_t *vals1 = dict_retrieve(p1, &size1);
    hvalue_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(hvalue_t);
    size2 /= sizeof(hvalue_t);
    int size = size1 < size2 ? size1 : size2;
    for (int i = 0; i < size; i++) {
        int cmp = value_cmp(vals1[i], vals2[i]);
        if (cmp != 0) {
            return cmp;
        }
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp_set(hvalue_t v1, hvalue_t v2){
    if (v1 == 0) {
        return v2 == 0 ? 0 : -1;
    }
    if (v2 == 0) {
        return 1;
    }
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    hvalue_t *vals1 = dict_retrieve(p1, &size1);
    hvalue_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(hvalue_t);
    size2 /= sizeof(hvalue_t);
    int size = size1 < size2 ? size1 : size2;
    for (int i = 0; i < size; i++) {
        int cmp = value_cmp(vals1[i], vals2[i]);
        if (cmp != 0) {
            return cmp;
        }
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp_address(hvalue_t v1, hvalue_t v2){
    if (v1 == 0) {
        return v2 == 0 ? 0 : -1;
    }
    if (v2 == 0) {
        return 1;
    }
    void *p1 = (void *) v1, *p2 = (void *) v2;
    int size1, size2;
    hvalue_t *vals1 = dict_retrieve(p1, &size1);
    hvalue_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(hvalue_t);
    size2 /= sizeof(hvalue_t);
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
int value_cmp_context(hvalue_t v1, hvalue_t v2){
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

int value_cmp(hvalue_t v1, hvalue_t v2){
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

static char *value_string_bool(hvalue_t v) {
    if (v != 0 && v != (1 << VALUE_BITS)) {
        fprintf(stderr, "value_string_bool %"PRI_HVAL"\n", v);
        panic("value_string_bool: bad value");
    }
    assert(v == 0 || v == (1 << VALUE_BITS));

    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, v == 0 ? "False" : "True");
    return strbuf_convert(&sb);
}

static char *value_json_bool(hvalue_t v) {
    if (v != 0 && v != (1 << VALUE_BITS)) {
        fprintf(stderr, "value_json_bool %"PRI_HVAL"\n", v);
        panic("value_json_bool: bad value");
    }
    assert(v == 0 || v == (1 << VALUE_BITS));

    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, "{ \"type\": \"bool\", \"value\": \"%s\" }", v == 0 ? "False" : "True");
    return strbuf_convert(&sb);
}

static char *value_string_int(hvalue_t v) {
    int64_t w = ((int64_t) v) >> VALUE_BITS;

    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, "%"PRId64"", (int64_t) w);
    return strbuf_convert(&sb);
}

static char *value_json_int(hvalue_t v) {
    int64_t w = ((int64_t) v) >> VALUE_BITS;

    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, "{ \"type\": \"int\", \"value\": \"%"PRId64"\" }", (int64_t) w);
    return strbuf_convert(&sb);
}

static char *value_string_atom(hvalue_t v) {
    int size;
    char *s = value_get(v, &size), *r;
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

static char *value_json_atom(hvalue_t v) {
    int size;
    char *s = value_get(v, &size);
    char *esc = json_escape(s, size);

    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, "{ \"type\": \"atom\", \"value\": \"%s\" }", esc);
    free(esc);
    return strbuf_convert(&sb);
}

static char *value_string_pc(hvalue_t v) {
    assert((v >> VALUE_BITS) < 10000);      // debug

    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, "PC(%u)", (unsigned int) (v >> VALUE_BITS));
    return strbuf_convert(&sb);
}

static char *value_json_pc(hvalue_t v) {
    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_printf(&sb, "{ \"type\": \"pc\", \"value\": \"%u\" }", (unsigned int) (v >> VALUE_BITS));
    return strbuf_convert(&sb);
}

static char *value_string_dict(hvalue_t v) {
    if (v == 0) {
        char *r = malloc(3);
        strcpy(r, "()");
        return r;
    }

    void *p = (void *) v;
    int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(hvalue_t);

    bool islist = true;
    for (hvalue_t i = 0; i < size; i++) {
        if (vals[2*i] != ((i << VALUE_BITS) | VALUE_INT)) {
            islist = false;
            break;
        }
    }

    struct strbuf sb;
    strbuf_init(&sb);

    if (islist) {
        strbuf_printf(&sb, "(");
        for (int i = 0; i < size; i++) {
            if (i != 0) {
                strbuf_printf(&sb, ", ");
            }
            char *val = value_string(vals[2*i+1]);
            strbuf_printf(&sb, "%s", val);
            free(val);
        }
        strbuf_printf(&sb, ")");
    }
    else {
        strbuf_printf(&sb, "{ ");
        for (int i = 0; i < size; i++) {
            if (i != 0) {
                strbuf_printf(&sb, ", ");
            }
            char *key = value_string(vals[2*i]);
            char *val = value_string(vals[2*i+1]);
            strbuf_printf(&sb, "%s: %s", key, val);
            free(key);
            free(val);
        }
        strbuf_printf(&sb, " }");
    }
    return strbuf_convert(&sb);
}

static char *value_json_dict(hvalue_t v) {
    struct strbuf sb;
    strbuf_init(&sb);

    if (v == 0) {
        strbuf_printf(&sb, "{ \"type\": \"dict\", \"value\": [] }");
        return strbuf_convert(&sb);
    }

    void *p = (void *) v;
    int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(hvalue_t);

    strbuf_printf(&sb, "{ \"type\": \"dict\", \"value\": [");
    for (int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(&sb, ", ");
        }
        char *key = value_json(vals[2*i]);
        char *val = value_json(vals[2*i+1]);
        strbuf_printf(&sb, "{ \"key\": %s, \"value\": %s }", key, val);
        free(key);
        free(val);
    }
    strbuf_printf(&sb, " ] }");
    return strbuf_convert(&sb);
}

static char *value_string_set(hvalue_t v) {
    struct strbuf sb;
    strbuf_init(&sb);

    if (v == 0) {
        strbuf_printf(&sb, "{}");
        return strbuf_convert(&sb);
    }

    void *p = (void *) v;
    int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);

    strbuf_printf(&sb, "{ ");
    for (int i = 0; i < size; i++) {
        char *val = value_string(vals[i]);
        if (i == 0) {
            strbuf_printf(&sb, "%s", val);
        }
        else {
            strbuf_printf(&sb, ", %s", val);
        }
        free(val);
    }
    strbuf_printf(&sb, " }");
    return strbuf_convert(&sb);
}

static char *value_json_set(hvalue_t v) {
    struct strbuf sb;
    strbuf_init(&sb);

    if (v == 0) {
        strbuf_printf(&sb, "{ \"type\": \"set\", \"value\": [] }");
        return strbuf_convert(&sb);
    }

    void *p = (void *) v;
    int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);

    strbuf_printf(&sb, "{ \"type\": \"set\", \"value\": [");
    for (int i = 0; i < size; i++) {
        char *val = value_json(vals[i]);
        if (i == 0) {
            strbuf_printf(&sb, "%s", val);
        }
        else {
            strbuf_printf(&sb, ", %s", val);
        }
        free(val);
    }
    strbuf_printf(&sb, " ] }");
    return strbuf_convert(&sb);
}

char *indices_string(const hvalue_t *vec, int size) {
    struct strbuf sb;
    strbuf_init(&sb);

    if (size == 0) {
        strbuf_printf(&sb, "None");
        return strbuf_convert(&sb);
    }
    char *s = value_string(vec[0]);
    assert(s[0] == '"');
	int len = strlen(s);
    strbuf_printf(&sb, "?%.*s", len - 2, s + 1);
    free(s);

    for (int i = 1; i < size; i++) {
        s = value_string(vec[i]);
        strbuf_printf(&sb, "[%s]", s);
    }

    return strbuf_convert(&sb);
}

static char *value_string_address(hvalue_t v) {
    if (v == 0) {
        struct strbuf sb;
        strbuf_init(&sb);
        strbuf_printf(&sb, "None");
        return strbuf_convert(&sb);
    }

    void *p = (void *) v;
    int size;
    hvalue_t *indices = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    return indices_string(indices, size);
}

static char *value_json_address(hvalue_t v) {
    struct strbuf sb;
    strbuf_init(&sb);

    if (v == 0) {
        strbuf_printf(&sb, "{ \"type\": \"address\", \"value\": [] }");
        return strbuf_convert(&sb);
    }

    void *p = (void *) v;
    int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    strbuf_printf(&sb, "{ \"type\": \"address\", \"value\": [");
    for (int i = 0; i < size; i++) {
        char *val = value_json(vals[i]);
        if (i == 0) {
            strbuf_printf(&sb, "%s", val);
        }
        else {
            strbuf_printf(&sb, ", %s", val);
        }
        free(val);
    }

    strbuf_printf(&sb, " ] }");
    return strbuf_convert(&sb);
}

static char *value_string_context(hvalue_t v) {
    struct context *ctx = value_get(v, NULL);
    struct strbuf sb;
    strbuf_init(&sb);
#ifdef SHORT
    char *name = value_string(ctx->name);
    strbuf_printf(&sb, "CONTEXT(%s, %d)", name, ctx->pc);
    free(name);
#else
    char *s;
    strbuf_printf(&sb, "CONTEXT(");

    s = value_string(ctx->name);
    strbuf_printf(&sb, "name=%s", s);
    free(s);

    s = value_string(ctx->entry);
    strbuf_printf(&sb, ",entry=%s", s);
    free(s);

    s = value_string(ctx->arg);
    strbuf_printf(&sb, ",arg=%s", s);
    free(s);

    s = value_string(ctx->this);
    strbuf_printf(&sb, ",this=%s", s);
    free(s);

    s = value_string(ctx->vars);
    strbuf_printf(&sb, ",vars=%s", s);
    free(s);

    s = value_string(ctx->trap_pc);
    strbuf_printf(&sb, ",trap_pc=%s", s);
    free(s);

    s = value_string(ctx->trap_arg);
    strbuf_printf(&sb, ",trap_arg=%s", s);
    free(s);

    s = value_string(ctx->failure);
    strbuf_printf(&sb, ",failure=%s", s);
    free(s);

    strbuf_printf(&sb, ",pc=%d", ctx->pc);

    strbuf_printf(&sb, ",fp=%d", ctx->fp);

    strbuf_printf(&sb, ",readonly=%d", ctx->readonly);

    strbuf_printf(&sb, ",atomic=%d", ctx->atomic);

    strbuf_printf(&sb, ",aflag=%d", ctx->atomicFlag);

    strbuf_printf(&sb, ",il=%d", ctx->interruptlevel);

    strbuf_printf(&sb, ",stopped=%d", ctx->stopped);

    strbuf_printf(&sb, ",terminated=%d", ctx->terminated);

    strbuf_printf(&sb, ",eternal=%d", ctx->eternal);

    strbuf_printf(&sb, ",sp=%d,STACK[", ctx->sp);

    for (int i = 0; i < ctx->sp; i++) {
        s = value_string(ctx->stack[i]);
        strbuf_printf(&sb, ",%s", s);
        free(s);
    }

    strbuf_printf(&sb, "]");

    strbuf_printf(&sb, ")");
#endif
    return strbuf_convert(&sb);
}

static char *value_json_context(hvalue_t v) {
    struct context *ctx = value_get(v, NULL);
    char *val;
    struct strbuf sb;
    
    strbuf_init(&sb);
    strbuf_printf(&sb, "{ \"type\": \"context\", \"value\": {");

    val = value_json(ctx->name);
    strbuf_printf(&sb, "\"name\": %s", val);
    free(val);

    val = value_json(ctx->arg);
    strbuf_printf(&sb, ", \"arg\": %s", val);
    free(val);

    strbuf_printf(&sb, ", \"pc\": { \"type\": \"pc\", \"value\": \"%d\" }", ctx->pc);

    strbuf_printf(&sb, " } }");
    return strbuf_convert(&sb);
}

char *value_string(hvalue_t v){
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

char *value_json(hvalue_t v){
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

hvalue_t value_bool(struct dict *map){
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

hvalue_t value_int(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    hvalue_t v;
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

hvalue_t value_pc(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    char *copy = malloc(value->u.atom.len + 1);
    memcpy(copy, value->u.atom.base, value->u.atom.len);
    copy[value->u.atom.len] = 0;
    long v = atol(copy);
    free(copy);
    return (v << VALUE_BITS) | VALUE_PC;
}

hvalue_t value_atom(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    if (value->u.atom.len == 0) {
        return VALUE_ATOM;
    }
    void *p = dict_find(values->atoms, value->u.atom.base, value->u.atom.len);
    return (hvalue_t) p | VALUE_ATOM;
}

hvalue_t value_dict(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return VALUE_DICT;
    }
    hvalue_t *vals = malloc(value->u.list.nvals * sizeof(hvalue_t) * 2);
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
                    value->u.list.nvals * sizeof(hvalue_t) * 2);
    free(vals);
    return (hvalue_t) p | VALUE_DICT;
}

hvalue_t value_set(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (hvalue_t) VALUE_SET;
    }
    hvalue_t *vals = malloc(value->u.list.nvals * sizeof(hvalue_t));
    for (int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(values, jv->u.map);
    }

    // vals is sorted already by harmony compiler
    void *p = dict_find(values->sets, vals, value->u.list.nvals * sizeof(hvalue_t));
    free(vals);
    return (hvalue_t) p | VALUE_SET;
}

hvalue_t value_address(struct values_t *values, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (hvalue_t) VALUE_ADDRESS;
    }
    hvalue_t *vals = malloc(value->u.list.nvals * sizeof(hvalue_t));
    for (int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(values, jv->u.map);
    }
    void *p = dict_find(values->addresses, vals,
                            value->u.list.nvals * sizeof(hvalue_t));
    free(vals);
    return (hvalue_t) p | VALUE_ADDRESS;
}

hvalue_t value_from_json(struct values_t *values, struct dict *map){
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
hvalue_t value_dict_store(struct values_t *values, hvalue_t dict, hvalue_t key, hvalue_t value){
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

    hvalue_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(hvalue_t);
        assert(size % 2 == 0);
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            if (vals[i + 1] == value) {
                return dict;
            }
            int n = size * sizeof(hvalue_t);
            hvalue_t *copy = malloc(n);
            memcpy(copy, vals, n);
            copy[i + 1] = value;
            hvalue_t v = value_put_dict(values, copy, n);
            free(copy);
            return v;
        }
        if (value_cmp(vals[i], key) > 0) {
            break;
        }
    }

    int n = (size + 2) * sizeof(hvalue_t);
    hvalue_t *nvals = malloc(n);
    memcpy(nvals, vals, i * sizeof(hvalue_t));
    nvals[i] = key;
    nvals[i+1] = value;
    memcpy(&nvals[i+2], &vals[i], (size - i) * sizeof(hvalue_t));
    hvalue_t v = value_put_dict(values, nvals, n);
    free(nvals);
    return v;
}

hvalue_t value_dict_load(hvalue_t dict, hvalue_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    hvalue_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(hvalue_t);
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

hvalue_t value_dict_remove(struct values_t *values, hvalue_t dict, hvalue_t key){
    assert((dict & VALUE_MASK) == VALUE_DICT);

    hvalue_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        return VALUE_DICT;
    }
    vals = value_get(dict & ~VALUE_MASK, &size);
    size /= sizeof(hvalue_t);
    assert(size % 2 == 0);

    if (size == 2) {
        return vals[0] == key ? VALUE_DICT : dict;
    }

    int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            int n = (size - 2) * sizeof(hvalue_t);
            hvalue_t *copy = malloc(n);
            memcpy(copy, vals, i * sizeof(hvalue_t));
            memcpy(&copy[i], &vals[i+2],
                   (size - i - 2) * sizeof(hvalue_t));
            hvalue_t v = value_put_dict(values, copy, n);
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

bool value_dict_tryload(
    struct values_t *values,
    hvalue_t dict,
    hvalue_t key,
    hvalue_t *result
){
    if ((dict & VALUE_MASK) == VALUE_ATOM) {
        if ((key & VALUE_MASK) != VALUE_INT) {
            return false;
        }
        key >>= VALUE_BITS;
        int size;
        char *chars = value_get(dict, &size);
        if (key >= size) {
            return false;
        }
        *result = value_put_atom(values, chars + key, 1);
        return true;
    }

    if ((dict & VALUE_MASK) != VALUE_DICT) {
        return false;
    }

    hvalue_t *vals;
    int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict & ~VALUE_MASK, &size);
        size /= sizeof(hvalue_t);
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

hvalue_t value_bag_add(struct values_t *values, hvalue_t bag, hvalue_t v, int multiplicity){
    hvalue_t count;
    if (value_dict_tryload(values, bag, v, &count)) {
        assert((count & VALUE_MASK) == VALUE_INT);
        assert(count != VALUE_INT);
        count += multiplicity << VALUE_BITS;
        return value_dict_store(values, bag, v, count);
    }
    else {
        return value_dict_store(values, bag, v, (1 << VALUE_BITS) | VALUE_INT);
    }
}

void value_ctx_push(struct context **pctx, hvalue_t v){
    assert(*pctx != NULL);
    struct context *ctx = realloc(*pctx, sizeof(struct context) +
                                         ((*pctx)->sp + 1) * sizeof(hvalue_t));

    ctx->stack[ctx->sp++] = v;
    *pctx = ctx;
}

hvalue_t value_ctx_pop(struct context **pctx){
    struct context *ctx = *pctx;

    assert(ctx->sp > 0);
    return ctx->stack[--ctx->sp];
}

hvalue_t value_ctx_failure(struct context *ctx, struct values_t *values, char *fmt, ...){
    char *r;
    va_list args;

    assert(ctx->failure == 0);

    struct strbuf sb;
    strbuf_init(&sb);
    va_start(args, fmt);
    strbuf_vprintf(&sb, fmt, args);
    va_end(args);
    ctx->failure = value_put_atom(values, strbuf_getstr(&sb), strbuf_getlen(&sb));
    strbuf_deinit(&sb);

    return 0;
}

bool value_ctx_all_eternal(hvalue_t ctxbag) {
    if (ctxbag == VALUE_DICT) {     // optimization
        return true;
    }
    int size;
    hvalue_t *vals = value_get(ctxbag, &size);
    size /= sizeof(hvalue_t);
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
