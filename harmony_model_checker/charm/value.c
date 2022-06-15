#include "head.h"

#define _GNU_SOURCE

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <inttypes.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#include "global.h"
#include "hashdict.h"
#include "value.h"
#include "strbuf.h"
#include "json.h"

void *value_get(hvalue_t v, unsigned int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        *psize = 0;
        return NULL;
    }
    return dict_retrieve((void *) v, psize);
}

// Like value_get, but allocate dynamic memory for it
void *value_copy(hvalue_t v, unsigned int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        *psize = 0;
        return NULL;
    }
    unsigned int size;
    void *p = dict_retrieve((void *) v, &size);
    void *r = malloc(size);
    memcpy(r, p, size);
    if (psize != NULL) {
        *psize = size;
    }
    return r;
}

// Like value_copy, but extend with given size and return old size
void *value_copy_extend(hvalue_t v, unsigned int inc, unsigned int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        *psize = 0;
        return inc == 0 ? NULL : malloc(inc);
    }
    unsigned int size;
    void *p = dict_retrieve((void *) v, &size);
    void *r = malloc(size + inc);
    memcpy(r, p, size);
    if (psize != NULL) {
        *psize = size;
    }
    return r;
}

hvalue_t value_put_atom(struct engine *engine, const void *p, int size){
    if (size == 0) {
        return VALUE_ATOM;
    }
    void *q = dict_find(engine->values->atoms, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_ATOM;
}

hvalue_t value_put_set(struct engine *engine, void *p, int size){
    if (size == 0) {
        return VALUE_SET;
    }
    void *q = dict_find(engine->values->sets, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_SET;
}

hvalue_t value_put_dict(struct engine *engine, void *p, int size){
    if (size == 0) {
        return VALUE_DICT;
    }
    void *q = dict_find(engine->values->dicts, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_DICT;
}

hvalue_t value_put_list(struct engine *engine, void *p, int size){
    if (size == 0) {
        return VALUE_LIST;
    }
    void *q = dict_find(engine->values->lists, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_LIST;
}

hvalue_t value_put_address(struct engine *engine, void *p, int size){
    if (size == 0) {
        return VALUE_ADDRESS;
    }
    void *q = dict_find(engine->values->addresses, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_ADDRESS;
}

hvalue_t value_put_context(struct engine *engine, struct context *ctx){
	assert(ctx->pc >= 0);
    unsigned int size = sizeof(*ctx) + (ctx->sp * sizeof(hvalue_t));
    if (ctx->extended) {
        size += ctx_extent * sizeof(hvalue_t);
    }
    void *q = dict_find(engine->values->contexts, engine->allocator, ctx, size, NULL);
    return (hvalue_t) q | VALUE_CONTEXT;
}

int value_cmp_bool(hvalue_t v1, hvalue_t v2){
    return v1 == 0 ? -1 : 1;
}

int value_cmp_int(hvalue_t v1, hvalue_t v2){
    return (int64_t) v1 < (int64_t) v2 ? -1 : 1;
}

int value_cmp_atom(hvalue_t v1, hvalue_t v2){
    unsigned int size1, size2;
    char *s1 = value_get(v1, &size1);
    char *s2 = value_get(v2, &size2);
    unsigned int size = size1 < size2 ? size1 : size2;
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
    unsigned int size1, size2;
    hvalue_t *vals1 = dict_retrieve(p1, &size1);
    hvalue_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(hvalue_t);
    size2 /= sizeof(hvalue_t);
    unsigned int size = size1 < size2 ? size1 : size2;
    for (unsigned int i = 0; i < size; i++) {
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
    unsigned int size1, size2;
    hvalue_t *vals1 = dict_retrieve(p1, &size1);
    hvalue_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(hvalue_t);
    size2 /= sizeof(hvalue_t);
    unsigned int size = size1 < size2 ? size1 : size2;
    for (unsigned int i = 0; i < size; i++) {
        int cmp = value_cmp(vals1[i], vals2[i]);
        if (cmp != 0) {
            return cmp;
        }
    }
    return size1 < size2 ? -1 : 1;
}

int value_cmp_list(hvalue_t v1, hvalue_t v2){
    if (v1 == 0) {
        return v2 == 0 ? 0 : -1;
    }
    if (v2 == 0) {
        return 1;
    }
    void *p1 = (void *) v1, *p2 = (void *) v2;
    unsigned int size1, size2;
    hvalue_t *vals1 = dict_retrieve(p1, &size1);
    hvalue_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(hvalue_t);
    size2 /= sizeof(hvalue_t);
    unsigned int size = size1 < size2 ? size1 : size2;
    for (unsigned int i = 0; i < size; i++) {
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
    unsigned int size1, size2;
    hvalue_t *vals1 = dict_retrieve(p1, &size1);
    hvalue_t *vals2 = dict_retrieve(p2, &size2);
    size1 /= sizeof(hvalue_t);
    size2 /= sizeof(hvalue_t);
    unsigned int size = size1 < size2 ? size1 : size2;
    for (unsigned int i = 0; i < size; i++) {
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
    unsigned int size1, size2;
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
    int t1 = VALUE_TYPE(v1);
    int t2 = VALUE_TYPE(v2);
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
    case VALUE_LIST:
        return value_cmp_list(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
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

static void value_string_bool(struct strbuf *sb, hvalue_t v) {
    v >>= VALUE_BITS;
    if (v != 0 && v != 1) {
        fprintf(stderr, "value_string_bool %"PRI_HVAL"\n", v);
        panic("value_string_bool: bad value");
    }
    assert(v == 0 || v == 1);
    strbuf_printf(sb, v == 0 ? "False" : "True");
}

static void value_json_bool(struct strbuf *sb, hvalue_t v) {
    v >>= VALUE_BITS;
    if (v != 0 && v != 1) {
        fprintf(stderr, "value_json_bool %"PRI_HVAL"\n", v);
        panic("value_json_bool: bad value");
    }
    assert(v == 0 || v == 1);
    strbuf_printf(sb, "{ \"type\": \"bool\", \"value\": \"%s\" }", v == 0 ? "False" : "True");
}

static void value_string_int(struct strbuf *sb, hvalue_t v) {
    int64_t w = (int64_t) VALUE_FROM_INT(v);
    strbuf_printf(sb, "%"PRId64"", (int64_t) w);
}

static void value_json_int(struct strbuf *sb, hvalue_t v) {
    int64_t w = (int64_t) VALUE_FROM_INT(v);
    strbuf_printf(sb, "{ \"type\": \"int\", \"value\": \"%"PRId64"\" }", (int64_t) w);
}

static void value_string_atom(struct strbuf *sb, hvalue_t v) {
    unsigned int size;
    char *s = value_get(v, &size);

    strbuf_append(sb, "\"", 1);
	while (size > 0) {
		switch (*s) {
		case '"':
			strbuf_append(sb, "\\\"", 2);
			break;
		case '\\':
			strbuf_append(sb, "\\\\", 2);
			break;
		case '\n':
			strbuf_append(sb, "\\n", 2);
			break;
		case '\r':
			strbuf_append(sb, "\\r", 2);
			break;
		default:
			strbuf_append(sb, s, 1);
		}
		s++;
		size--;
	}
    strbuf_append(sb, "\"", 1);
}

static void value_json_atom(struct strbuf *sb, hvalue_t v) {
    unsigned int size;
    char *s = value_get(v, &size);
    char *esc = json_escape(s, size);

    strbuf_printf(sb, "{ \"type\": \"atom\", \"value\": \"%s\" }", esc);
    free(esc);
}

static void value_string_pc(struct strbuf *sb, hvalue_t v) {
    assert(VALUE_FROM_PC(v) < 10000);      // debug
    strbuf_printf(sb, "PC(%u)", (unsigned int) VALUE_FROM_PC(v));
}

static void value_json_pc(struct strbuf *sb, hvalue_t v) {
    strbuf_printf(sb, "{ \"type\": \"pc\", \"value\": \"%u\" }", (unsigned int) VALUE_FROM_PC(v));
}

static void value_string_dict(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "{:}");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(hvalue_t);
    strbuf_printf(sb, "{ ");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_string(sb, vals[2*i]);
        strbuf_printf(sb, ": ");
        strbuf_value_string(sb, vals[2*i+1]);
    }
    strbuf_printf(sb, " }");
}

static void value_json_dict(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "{ \"type\": \"dict\", \"value\": [] }");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(hvalue_t);

    strbuf_printf(sb, "{ \"type\": \"dict\", \"value\": [");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_printf(sb, "{ \"key\": ");
        strbuf_value_json(sb, vals[2*i]);
        strbuf_printf(sb, ", \"value\": ");
        strbuf_value_json(sb, vals[2*i+1]);
        strbuf_printf(sb, " }");
    }
    strbuf_printf(sb, " ] }");
}

static void value_string_list(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "[]");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);

    strbuf_printf(sb, "[ ");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_string(sb, vals[i]);
    }
    strbuf_printf(sb, " ]");
}

static void value_string_set(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "{}");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);

    strbuf_printf(sb, "{ ");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_string(sb, vals[i]);
    }
    strbuf_printf(sb, " }");
}

static void value_json_list(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "{ \"type\": \"list\", \"value\": [] }");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);

    strbuf_printf(sb, "{ \"type\": \"list\", \"value\": [");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_json(sb, vals[i]);
    }
    strbuf_printf(sb, " ] }");
}

static void value_json_set(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "{ \"type\": \"set\", \"value\": [] }");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);

    strbuf_printf(sb, "{ \"type\": \"set\", \"value\": [");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_json(sb, vals[i]);
    }
    strbuf_printf(sb, " ] }");
}

static void strbuf_indices_string(struct strbuf *sb, const hvalue_t *vec, int size) {
    if (size == 0) {
        strbuf_printf(sb, "None");
        return;
    }
    char *s = value_string(vec[0]);
    assert(s[0] == '"');
	int len = strlen(s);
    strbuf_printf(sb, "%.*s", len - 2, s + 1);
    free(s);

    for (int i = 1; i < size; i++) {
        strbuf_printf(sb, "[");
        strbuf_value_string(sb, vec[i]);
        strbuf_printf(sb, "]");
    }
}

char *indices_string(const hvalue_t *vec, int size) {
    struct strbuf sb;

    strbuf_init(&sb);
    strbuf_indices_string(&sb, vec, size);
    return strbuf_convert(&sb);
}

static void value_string_address(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "None");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *indices = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    strbuf_indices_string(sb, indices, size);
}

static void value_json_address(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "{ \"type\": \"address\", \"value\": [] }");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    strbuf_printf(sb, "{ \"type\": \"address\", \"value\": [");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_json(sb, vals[i]);
    }

    strbuf_printf(sb, " ] }");
}

static void value_string_context(struct strbuf *sb, hvalue_t v) {
    struct context *ctx = value_get(v, NULL);
    strbuf_printf(sb, "CONTEXT(");
#ifdef SHORT
    strbuf_value_string(sb, ctx->name);
    strbuf_printf(sb, ", %d)", ctx->pc);
    free(name);
#else
    // strbuf_printf(sb, "name=");
    // strbuf_value_string(sb, ctx->name);
    strbuf_printf(sb, ",entry=%u", ctx->entry);
    // strbuf_printf(sb, ",arg=");
    // strbuf_value_string(sb, ctx->arg);
    strbuf_printf(sb, ",vars=");
    strbuf_value_string(sb, ctx->vars);
    if (ctx->extended) {
        strbuf_printf(sb, ",this=");
        strbuf_value_string(sb, ctx->ctx_this);
        if (ctx->ctx_trap_pc != 0) {
            strbuf_printf(sb, ",trap_pc=");
            strbuf_value_string(sb, ctx->ctx_trap_pc);
            strbuf_printf(sb, ",trap_arg=");
            strbuf_value_string(sb, ctx->ctx_trap_arg);
        }
        if (ctx->ctx_failure != 0) {
            strbuf_printf(sb, ",failure=");
            strbuf_value_string(sb, ctx->ctx_failure);
        }
    }

    strbuf_printf(sb, ",pc=%d", ctx->pc);
    strbuf_printf(sb, ",fp=%d", ctx->fp);
    strbuf_printf(sb, ",readonly=%d", ctx->readonly);
    strbuf_printf(sb, ",atomic=%d", ctx->atomic);
    strbuf_printf(sb, ",aflag=%d", ctx->atomicFlag);
    strbuf_printf(sb, ",il=%d", ctx->interruptlevel);
    strbuf_printf(sb, ",stopped=%d", ctx->stopped);
    strbuf_printf(sb, ",terminated=%d", ctx->terminated);
    strbuf_printf(sb, ",eternal=%d", ctx->eternal);

    strbuf_printf(sb, ",sp=%d,STACK[", ctx->sp);

    for (int i = 0; i < ctx->sp; i++) {
        if (i != 0) {
            strbuf_printf(sb, ",");
        }
        strbuf_value_string(sb, ctx_stack(ctx)[i]);
    }

    strbuf_printf(sb, "])");
#endif
}

static void value_json_context(struct strbuf *sb, hvalue_t v) {
    struct context *ctx = value_get(v, NULL);
    
    strbuf_printf(sb, "{ \"type\": \"context\", \"value\": {");
    strbuf_printf(sb, "\"entry\": %u", ctx->entry);
    // strbuf_printf(sb, ", \"arg\": ");
    // strbuf_value_json(sb, ctx->arg);
    strbuf_printf(sb, ", \"pc\": { \"type\": \"pc\", \"value\": \"%d\" }", ctx->pc);

    strbuf_printf(sb, " } }");
}

void strbuf_value_string(struct strbuf *sb, hvalue_t v){
    switch (VALUE_TYPE(v)) {
    case VALUE_BOOL:
        value_string_bool(sb, v & ~VALUE_MASK);
        break;
    case VALUE_INT:
        value_string_int(sb, v & ~VALUE_MASK);
        break;
    case VALUE_ATOM:
        value_string_atom(sb, v & ~VALUE_MASK);
        break;
    case VALUE_PC:
        value_string_pc(sb, v & ~VALUE_MASK);
        break;
    case VALUE_LIST:
        value_string_list(sb, v & ~VALUE_MASK);
        break;
    case VALUE_DICT:
        value_string_dict(sb, v & ~VALUE_MASK);
        break;
    case VALUE_SET:
        value_string_set(sb, v & ~VALUE_MASK);
        break;
    case VALUE_ADDRESS:
        value_string_address(sb, v & ~VALUE_MASK);
        break;
    case VALUE_CONTEXT:
        value_string_context(sb, v & ~VALUE_MASK);
        break;
    default:
        printf("bad value type: %p\n", (void *) v);
        panic("strbuf_value_string: bad value type");
    }
}

char *value_string(hvalue_t v){
    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_value_string(&sb, v);
    return strbuf_convert(&sb);
}

void strbuf_value_json(struct strbuf *sb, hvalue_t v){
    switch VALUE_TYPE(v) {
    case VALUE_BOOL:
        value_json_bool(sb, v & ~VALUE_MASK);
        break;
    case VALUE_INT:
        value_json_int(sb, v & ~VALUE_MASK);
        break;
    case VALUE_ATOM:
        value_json_atom(sb, v & ~VALUE_MASK);
        break;
    case VALUE_PC:
        value_json_pc(sb, v & ~VALUE_MASK);
        break;
    case VALUE_LIST:
        value_json_list(sb, v & ~VALUE_MASK);
        break;
    case VALUE_DICT:
        value_json_dict(sb, v & ~VALUE_MASK);
        break;
    case VALUE_SET:
        value_json_set(sb, v & ~VALUE_MASK);
        break;
    case VALUE_ADDRESS:
        value_json_address(sb, v & ~VALUE_MASK);
        break;
    case VALUE_CONTEXT:
        value_json_context(sb, v & ~VALUE_MASK);
        break;
    default:
        panic("strbuf_value_json: bad value type");
    }
}

char *value_json(hvalue_t v){
    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_value_json(&sb, v);
    return strbuf_convert(&sb);
}

bool atom_cmp(json_buf_t buf, char *s){
    unsigned int n = strlen(s);
    if (n != buf.len) {
        return false;
    }
    return strncmp(buf.base, s, n) == 0;
}

hvalue_t value_bool(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    if (atom_cmp(value->u.atom, "False")) {
        return VALUE_FALSE;
    }
    if (atom_cmp(value->u.atom, "True")) {
        return VALUE_TRUE;
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
    return VALUE_TO_INT(v);
}

hvalue_t value_pc(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    char *copy = malloc(value->u.atom.len + 1);
    memcpy(copy, value->u.atom.base, value->u.atom.len);
    copy[value->u.atom.len] = 0;
    long v = atol(copy);
    free(copy);
    return VALUE_TO_PC(v);
}

hvalue_t value_atom(struct engine *engine, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    if (value->u.atom.len == 0) {
        return VALUE_ATOM;
    }
    void *p = dict_find(engine->values->atoms, engine->allocator, value->u.atom.base, value->u.atom.len, NULL);
    return (hvalue_t) p | VALUE_ATOM;
}

hvalue_t value_dict(struct engine *engine, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return VALUE_DICT;
    }
    hvalue_t *vals = malloc(value->u.list.nvals * sizeof(hvalue_t) * 2);
    for (unsigned int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        struct json_value *k = dict_lookup(jv->u.map, "key", 3);
        assert(k->type == JV_MAP);
        struct json_value *v = dict_lookup(jv->u.map, "value", 5);
        assert(v->type == JV_MAP);
        vals[2*i] = value_from_json(engine, k->u.map);
        vals[2*i+1] = value_from_json(engine, v->u.map);
    }

    // vals is sorted already by harmony compiler
    void *p = dict_find(engine->values->dicts, engine->allocator, vals,
                    value->u.list.nvals * sizeof(hvalue_t) * 2, NULL);
    free(vals);
    return (hvalue_t) p | VALUE_DICT;
}

hvalue_t value_set(struct engine *engine, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (hvalue_t) VALUE_SET;
    }
    hvalue_t *vals = malloc(value->u.list.nvals * sizeof(hvalue_t));
    for (unsigned int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(engine, jv->u.map);
    }

    // vals is sorted already by harmony compiler
    void *p = dict_find(engine->values->sets, engine->allocator, vals, value->u.list.nvals * sizeof(hvalue_t), NULL);
    free(vals);
    return (hvalue_t) p | VALUE_SET;
}

hvalue_t value_list(struct engine *engine, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (hvalue_t) VALUE_LIST;
    }
    hvalue_t *vals = malloc(value->u.list.nvals * sizeof(hvalue_t));
    for (unsigned int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(engine, jv->u.map);
    }
    void *p = dict_find(engine->values->lists, engine->allocator, vals, value->u.list.nvals * sizeof(hvalue_t), NULL);
    free(vals);
    return (hvalue_t) p | VALUE_LIST;
}

hvalue_t value_address(struct engine *engine, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (hvalue_t) VALUE_ADDRESS;
    }
    hvalue_t *vals = malloc(value->u.list.nvals * sizeof(hvalue_t));
    for (unsigned int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(engine, jv->u.map);
    }
    void *p = dict_find(engine->values->addresses, engine->allocator, vals,
                            value->u.list.nvals * sizeof(hvalue_t), NULL);
    free(vals);
    return (hvalue_t) p | VALUE_ADDRESS;
}

hvalue_t value_from_json(struct engine *engine, struct dict *map){
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
        return value_atom(engine, map);
    }
    else if (atom_cmp(type->u.atom, "list")) {
        return value_list(engine, map);
    }
    else if (atom_cmp(type->u.atom, "dict")) {
        return value_dict(engine, map);
    }
    else if (atom_cmp(type->u.atom, "set")) {
        return value_set(engine, map);
    }
    else if (atom_cmp(type->u.atom, "pc")) {
        return value_pc(map);
    }
    else if (atom_cmp(type->u.atom, "address")) {
        return value_address(engine, map);
    }
    else {
        panic("value_from_json: bad type");
        return 0;
    }
}

// Memory allocation that returns pointers aligned to 1 << VALUE_BITS
static void *align_alloc(size_t size){
    char *q = malloc(size + (1 << VALUE_BITS));
    size_t offset = (1 << VALUE_BITS) - (((size_t) q) & VALUE_MASK);
    char *p = q + offset;
    p[-1] = offset;
    return p;
}

// Corresponding free
static void align_free(void *p){
    int offset = *((char *) p - 1);
    free(((char *) p) - offset);
}

// Try to figure out the "native" alignment of this machine.  It's
// probably good enough
#define N_ALIGN_TESTS 16
static bool align_test(){
    for (int i = 0; i < N_ALIGN_TESTS; i++) {
        if (((hvalue_t) malloc(1) & VALUE_MASK) != 0) {
            return false;
        }
    }
    return true;
}

void value_init(struct values_t *values, unsigned int nworkers){
    if (align_test()) {
        // printf("malloc appears aligned to %d bytes\n", 1 << VALUE_BITS);
        values->atoms = dict_new("atoms", 0, 0, nworkers, NULL, NULL);
        values->dicts = dict_new("dicts", 0, 0, nworkers, NULL, NULL);
        values->sets = dict_new("sets", 0, 0, nworkers, NULL, NULL);
        values->lists = dict_new("lists", 0, 0, nworkers, NULL, NULL);
        values->addresses = dict_new("addresses", 0, 0, nworkers, NULL, NULL);
        values->contexts = dict_new("contexts", 0, 0, nworkers, NULL, NULL);
    }
    else {
        values->atoms = dict_new("atoms", 0, 0, nworkers, align_alloc, align_free);
        values->dicts = dict_new("dicts", 0, 0, nworkers, align_alloc, align_free);
        values->sets = dict_new("sets", 0, 0, nworkers, align_alloc, align_free);
        values->lists = dict_new("lists", 0, 0, nworkers, align_alloc, align_free);
        values->addresses = dict_new("addresses", 0, 0, nworkers, align_alloc, align_free);
        values->contexts = dict_new("contexts", 0, 0, nworkers, align_alloc, align_free);
    }
}

void value_set_concurrent(struct values_t *values){
    dict_set_concurrent(values->atoms);
    dict_set_concurrent(values->dicts);
    dict_set_concurrent(values->sets);
    dict_set_concurrent(values->lists);
    dict_set_concurrent(values->addresses);
    dict_set_concurrent(values->contexts);
}

void value_make_stable(struct values_t *values, unsigned int worker){
    dict_make_stable(values->atoms, worker);
    dict_make_stable(values->dicts, worker);
    dict_make_stable(values->sets, worker);
    dict_make_stable(values->lists, worker);
    dict_make_stable(values->addresses, worker);
    dict_make_stable(values->contexts, worker);
}

void value_grow_prepare(struct values_t *values) {
    dict_grow_prepare(values->atoms);
    dict_grow_prepare(values->dicts);
    dict_grow_prepare(values->sets);
    dict_grow_prepare(values->lists);
    dict_grow_prepare(values->addresses);
    dict_grow_prepare(values->contexts);
}

void value_set_sequential(struct values_t *values){
    dict_set_sequential(values->atoms);
    dict_set_sequential(values->dicts);
    dict_set_sequential(values->sets);
    dict_set_sequential(values->lists);
    dict_set_sequential(values->addresses);
    dict_set_sequential(values->contexts);
}

// Store key:value in the given dictionary and returns its value code
// in *result.  May fail if allow_inserts is false and key does not exist
bool value_dict_trystore(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result){
    assert(VALUE_TYPE(dict) == VALUE_DICT);

    hvalue_t *vals;
    unsigned int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict, &size);
        size /= sizeof(hvalue_t);
        assert(size % 2 == 0);
    }

    unsigned int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            if (vals[i + 1] == value) {
                *result = dict;
                return true;
            }
            int n = size * sizeof(hvalue_t);
            hvalue_t copy[size];
            memcpy(copy, vals, n);
            copy[i + 1] = value;
            hvalue_t v = value_put_dict(engine, copy, n);
            *result = v;
            return true;
        }
        if (value_cmp(vals[i], key) > 0) {
            break;
        }
    }

    if (!allow_inserts) {
        return false;
    }

    int n = (size + 2) * sizeof(hvalue_t);
    hvalue_t nvals[size + 2];
    memcpy(nvals, vals, i * sizeof(hvalue_t));
    nvals[i] = key;
    nvals[i+1] = value;
    memcpy(&nvals[i+2], &vals[i], (size - i) * sizeof(hvalue_t));
    hvalue_t v = value_put_dict(engine, nvals, n);
    *result = v;
    return true;
}

hvalue_t value_dict_store(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value){
    hvalue_t result;
    bool r = value_dict_trystore(engine, dict, key, value, true, &result);
    if (!r) {
        fprintf(stderr, "value_dict_store: failed\n");
        exit(1);
    }
    return result;
}

bool value_trystore(struct engine *engine, hvalue_t root, hvalue_t key, hvalue_t value, bool allow_inserts, hvalue_t *result){
    assert(VALUE_TYPE(root) == VALUE_DICT || VALUE_TYPE(root) == VALUE_LIST);

    unsigned int size;
    hvalue_t *vals = value_get(root, &size);
    unsigned int n = size / sizeof(hvalue_t);

    if (VALUE_TYPE(root) == VALUE_DICT) {
        assert(n % 2 == 0);
        unsigned int i;
        for (i = 0; i < n; i += 2) {
            if (vals[i] == key) {
                if (vals[i + 1] == value) {
                    *result = root;
                    return true;
                }
                hvalue_t nvals[n];
                memcpy(nvals, vals, size);
                nvals[i + 1] = value;
                hvalue_t v = value_put_dict(engine, nvals, size);
                *result = v;
                return true;
            }
            if (value_cmp(vals[i], key) > 0) {
                break;
            }
        }

        if (!allow_inserts) {
            return false;
        }

        size += 2 * sizeof(hvalue_t);
        hvalue_t nvals[n + 2];
        memcpy(nvals, vals, i * sizeof(hvalue_t));
        nvals[i] = key;
        nvals[i+1] = value;
        memcpy(&nvals[i+2], &vals[i], (n - i) * sizeof(hvalue_t));
        hvalue_t v = value_put_dict(engine, nvals, size);
        *result = v;
        return true;
    }
    else {
        assert(VALUE_TYPE(root) == VALUE_LIST);
        if (VALUE_TYPE(key) != VALUE_INT) {
            return false;
        }
        unsigned int index = (unsigned int) VALUE_FROM_INT(key);
        if (index > n) {
            return false;
        }
        unsigned int nsize;
        if (index == n) {
            if (!allow_inserts) {
                return false;
            }
            nsize = size + sizeof(hvalue_t);
        }
        else {
            if (vals[index] == value) {
                *result = root;
                return true;
            }
            nsize = size;
        }
        hvalue_t nvals[size / sizeof(hvalue_t)];
        memcpy(nvals, vals, size);
        nvals[index] = value;
        hvalue_t v = value_put_list(engine, nvals, nsize);
        *result = v;
        return true;
    }
}

hvalue_t value_store(struct engine *engine, hvalue_t root, hvalue_t key, hvalue_t value){
    hvalue_t result;
    bool r = value_trystore(engine, root, key, value, true, &result);
    if (!r) {
        fprintf(stderr, "value_store: failed\n");
        exit(1);
    }
    return result;
}

hvalue_t value_dict_load(hvalue_t dict, hvalue_t key){
    assert(VALUE_TYPE(dict) == VALUE_DICT);

    hvalue_t *vals;
    unsigned int size;
    if (dict == VALUE_DICT) {
        vals = NULL;
        size = 0;
    }
    else {
        vals = value_get(dict, &size);
        size /= sizeof(hvalue_t);
        assert(size % 2 == 0);
    }

    unsigned int i;
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

hvalue_t value_dict_remove(struct engine *engine, hvalue_t dict, hvalue_t key){
    assert(VALUE_TYPE(dict) == VALUE_DICT);

    hvalue_t *vals;
    unsigned int size;
    if (dict == VALUE_DICT) {
        return VALUE_DICT;
    }
    vals = value_get(dict, &size);
    size /= sizeof(hvalue_t);
    assert(size % 2 == 0);

    if (size == 2) {
        return vals[0] == key ? VALUE_DICT : dict;
    }

    for (unsigned int i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            int n = (size - 2) * sizeof(hvalue_t);
            hvalue_t copy[size - 2];
            memcpy(copy, vals, i * sizeof(hvalue_t));
            memcpy(&copy[i], &vals[i+2],
                   (size - i - 2) * sizeof(hvalue_t));
            hvalue_t v = value_put_dict(engine, copy, n);
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

hvalue_t value_remove(struct engine *engine, hvalue_t root, hvalue_t key){
    assert(VALUE_TYPE(root) == VALUE_DICT || VALUE_TYPE(root) == VALUE_LIST);

    unsigned int size;
    hvalue_t *vals = value_get(root, &size);
    if (size == 0) {
        return root;
    }
    unsigned int n = size / sizeof(hvalue_t);

    if (VALUE_TYPE(root) == VALUE_DICT) {
        assert(size % 2 == 0);

        if (n == 2) {
            return vals[0] == key ? VALUE_DICT : root;
        }

        for (unsigned i = 0; i < n; i += 2) {
            if (vals[i] == key) {
                size -= 2 * sizeof(hvalue_t);
                hvalue_t copy[size / sizeof(hvalue_t)];
                memcpy(copy, vals, i * sizeof(hvalue_t));
                memcpy(&copy[i], &vals[i+2],
                       (n - i - 2) * sizeof(hvalue_t));
                hvalue_t v = value_put_dict(engine, copy, size);
                return v;
            }
            /* Not worth it
                if (value_cmp(vals[i], key) > 0) {
                    assert(false);
                }
            */
        }
    }
    else {
        assert(VALUE_TYPE(root) == VALUE_LIST);
        if (VALUE_TYPE(key) != VALUE_INT) {
            fprintf(stderr, "value_remove: not an int\n");
            return root;
        }
        unsigned int index = (unsigned int) VALUE_FROM_INT(key);
        if (index >= n) {
            return root;
        }
        size -= sizeof(hvalue_t);
        hvalue_t copy[size / sizeof(hvalue_t)];
        memcpy(copy, vals, index * sizeof(hvalue_t));
        memcpy(&copy[index], &vals[index+1],
               (n - index - 1) * sizeof(hvalue_t));
        hvalue_t v = value_put_list(engine, copy, size);
        return v;
    }

    return root;
}

// Try to load from either a dict (by key) or a string or list (by index).
bool value_tryload(
    struct engine *engine,
    hvalue_t root,
    hvalue_t key,
    hvalue_t *result
){
    if (VALUE_TYPE(root) == VALUE_ATOM) {
        if (VALUE_TYPE(key) != VALUE_INT) {
            return false;
        }
        key = VALUE_FROM_INT(key);
        unsigned int size;
        char *chars = value_get(root, &size);
        if (key >= (unsigned int) size) {
            return false;
        }
        *result = value_put_atom(engine, chars + key, 1);
        return true;
    }

    if (VALUE_TYPE(root) == VALUE_LIST) {
        if (VALUE_TYPE(key) != VALUE_INT) {
            return false;
        }
        key = VALUE_FROM_INT(key);
        unsigned int size;
        hvalue_t *vals = value_get(root, &size);
        size /= sizeof(hvalue_t);
        if (key >= (unsigned int) size) {
            return false;
        }
        *result = vals[key];
        return true;
    }

    if (VALUE_TYPE(root) == VALUE_DICT) {
        hvalue_t *vals;
        unsigned int size;
        vals = value_get(root, &size);
        size /= sizeof(hvalue_t);
        assert(size % 2 == 0);

        for (unsigned int i = 0; i < size; i += 2) {
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
    }

    return false;
}

hvalue_t value_bag_add(struct engine *engine, hvalue_t bag, hvalue_t v, int multiplicity){
    hvalue_t count;
    assert(VALUE_TYPE(bag) == VALUE_DICT);
    if (value_tryload(engine, bag, v, &count)) {
        assert(VALUE_TYPE(count) == VALUE_INT);
        assert(count != VALUE_INT);
        count += multiplicity << VALUE_BITS;
        return value_dict_store(engine, bag, v, count);
    }
    else {
        return value_dict_store(engine, bag, v, VALUE_TO_INT(1));
    }
}

hvalue_t value_bag_remove(struct engine *engine, hvalue_t bag, hvalue_t v){
    assert(VALUE_TYPE(bag) == VALUE_DICT);
    hvalue_t count = value_dict_load(bag, v);
    assert(VALUE_TYPE(count) == VALUE_INT);
    count -= 1 << VALUE_BITS;
    if (count == VALUE_INT) {
        return value_dict_remove(engine, bag, v);
    }
    else {
        return value_dict_store(engine, bag, v, count);
    }
}

void value_ctx_push(struct context *ctx, hvalue_t v){
    // TODO.  Check for stack overflow
    ctx_stack(ctx)[ctx->sp++] = v;
}

hvalue_t value_ctx_pop(struct context *ctx){
    assert(ctx->sp > 0);
    return ctx_stack(ctx)[--ctx->sp];
}

void value_ctx_extend(struct context *ctx){
    if (ctx->extended) {
        return;
    }
    memmove(&ctx->thestack[ctx_extent], ctx->thestack, ctx->sp * sizeof(hvalue_t));
    memset(ctx->thestack, 0, ctx_extent * sizeof(hvalue_t));
    ctx->ctx_this = VALUE_DICT;
    ctx->extended = true;
}

hvalue_t value_ctx_failure(struct context *ctx, struct engine *engine, char *fmt, ...){
    va_list args;

    assert(!ctx->failed);
    value_ctx_extend(ctx);
    assert(ctx->ctx_failure == 0);

    struct strbuf sb;
    strbuf_init(&sb);
    va_start(args, fmt);
    strbuf_vprintf(&sb, fmt, args);
    va_end(args);
    ctx->ctx_failure = value_put_atom(engine, strbuf_getstr(&sb), strbuf_getlen(&sb));
    ctx->failed = true;
    strbuf_deinit(&sb);

    return 0;
}

bool value_ctx_all_eternal(hvalue_t ctxbag) {
    if (ctxbag == VALUE_DICT) {     // optimization
        return true;
    }
    unsigned int size;
    hvalue_t *vals = value_get(ctxbag, &size);
    size /= sizeof(hvalue_t);
    bool all = true;
    for (unsigned int i = 0; i < size; i += 2) {
        assert(VALUE_TYPE(vals[i]) == VALUE_CONTEXT);
        assert(VALUE_TYPE(vals[i + 1]) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        assert(ctx != NULL);
        if (!ctx->eternal) {
            all = false;
            break;
        }
    }
    return all;
}
