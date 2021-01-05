#define _GNU_SOURCE

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include <assert.h>
#include "global.h"
#include "json.h"

static struct dict *atom_map;
static struct dict *dict_map;
static struct dict *set_map;
static struct dict *address_map;
static struct dict *context_map;

void *value_get(uint64_t v, int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        *psize = 0;
        return NULL;
    }
    return dict_retrieve((void *) v, psize);
}

void *value_copy(uint64_t v, int *psize){
    int size;
    void *p = dict_retrieve((void *) (v & ~VALUE_MASK), &size);
    void *r = malloc(size);
    memcpy(r, p, size);
    if (psize != NULL) {
        *psize = size;
    }
    return r;
}

uint64_t value_put_atom(const void *p, int size){
    assert(size > 0);
    void *q = dict_find(atom_map, p, size);
    return (uint64_t) q | VALUE_ATOM;
}

uint64_t value_put_set(void *p, int size){
    if (size == 0) {
        return VALUE_SET;
    }
    void *q = dict_find(set_map, p, size);
    return (uint64_t) q | VALUE_SET;
}

uint64_t value_put_dict(void *p, int size){
    if (size == 0) {
        return VALUE_DICT;
    }
    void *q = dict_find(dict_map, p, size);
    return (uint64_t) q | VALUE_DICT;
}

uint64_t value_put_address(void *p, int size){
    if (size == 0) {
        return VALUE_ADDRESS;
    }
    void *q = dict_find(address_map, p, size);
    return (uint64_t) q | VALUE_ADDRESS;
}

uint64_t value_put_context(struct context *ctx){
    int size = sizeof(*ctx) + (ctx->sp * sizeof(uint64_t));
    void *q = dict_find(context_map, ctx, size);
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
    assert(0);
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
        assert(0);
    }
}

void append_printf(char **p, char *fmt, ...){
    char *r;
    va_list args;

    va_start(args, fmt);
    vasprintf(&r, fmt, args);
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
        fprintf(stderr, "value_string_bool %llx\n", v);
    }
    assert(v == 0 || v == (1 << VALUE_BITS));
    asprintf(&r, v == 0 ? "False" : "True");
    return r;
}

static char *value_json_bool(uint64_t v) {
    char *r;
    if (v != 0 && v != (1 << VALUE_BITS)) {
        fprintf(stderr, "value_string_bool %llx\n", v);
    }
    assert(v == 0 || v == (1 << VALUE_BITS));
    asprintf(&r, "{ \"type\": \"bool\", \"value\": \"%s\" }", v == 0 ? "False" : "True");
    return r;
}

static char *value_string_int(uint64_t v) {
    char *r;

    if ((v >> VALUE_BITS) == VALUE_MAX) {
        asprintf(&r, "inf");
    }
    else if ((v >> VALUE_BITS) == VALUE_MIN) {
        asprintf(&r, "-inf");
    }
    else {
        asprintf(&r, "%"PRId64"", ((int64_t) v) >> VALUE_BITS);
    }
    return r;
}

static char *value_json_int(uint64_t v) {
    char *r;

    if ((v >> VALUE_BITS) == VALUE_MAX) {
        asprintf(&r, "{ \"type\": \"int\", \"value\": \"inf\" }");
    }
    else if ((v >> VALUE_BITS) == VALUE_MIN) {
        asprintf(&r, "{ \"type\": \"int\", \"value\": \"-inf\" }");
    }
    else {
        asprintf(&r, "{ \"type\": \"int\", \"value\": \"%"PRId64"\" }",
                            ((int64_t) v) >> VALUE_BITS);
    }
    return r;
}

static char *value_string_atom(uint64_t v) {
    void *p = (void *) v;
    int size;
    char *s = dict_retrieve(p, &size), *r;
    asprintf(&r, ".%.*s", size, s);
    return r;
}

static char *value_json_atom(uint64_t v) {
    void *p = (void *) v;
    int size;
    char *s = dict_retrieve(p, &size), *r;
    asprintf(&r, "{ \"type\": \"atom\", \"value\": \"%.*s\" }", size, s);
    return r;
}

static char *value_string_pc(uint64_t v) {
    char *r;
    assert((v >> VALUE_BITS) < 10000);      // debug
    asprintf(&r, "PC(%"PRIu64")", v >> VALUE_BITS);
    return r;
}

static char *value_json_pc(uint64_t v) {
    char *r;
    asprintf(&r, "\"type\": \"pc\", \"value\": \"%"PRIu64"\" }", v >> VALUE_BITS);
    return r;
}

static char *value_string_dict(uint64_t v) {
    char *r;

    if (v == 0) {
        asprintf(&r, "()");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(uint64_t);

    asprintf(&r, "dict{ ");
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
    return r;
}

static char *value_json_dict(uint64_t v) {
    char *r;

    if (v == 0) {
        asprintf(&r, "{ \"type\": \"dict\", \"value\": [] }");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= 2 * sizeof(uint64_t);

    asprintf(&r, "{ \"type\": \"dict\", \"value\": [");
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
        asprintf(&r, "{}");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);

    asprintf(&r, "{ ");
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
        asprintf(&r, "{ \"type\": \"set\", \"value\": [] }");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);

    asprintf(&r, "{ \"type\": \"set\", \"value\": [");
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

static char *value_string_address(uint64_t v) {
    char *r;
    if (v == 0) {
        asprintf(&r, "None");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *indices = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);
    assert(size > 0);
    char *s = value_string(indices[0]);
    assert(s[0] == '.');
    asprintf(&r, "?%s", s + 1);
    free(s);

    for (int i = 1; i < size; i++) {
        s = value_string(indices[i]);
        if (*s == '.') {
            append_printf(&r, "%s", s);
        }
        else {
            append_printf(&r, "[%s]", s);
        }
    }

    return r;
}

static char *value_json_address(uint64_t v) {
    char *r;
    if (v == 0) {
        asprintf(&r, "{ \"type\": \"address\", \"value\": [] }");
        return r;
    }

    void *p = (void *) v;
    int size;
    uint64_t *vals = dict_retrieve(p, &size);
    size /= sizeof(uint64_t);
    assert(size > 0);
    asprintf(&r, "{ \"type\": \"address\", \"value\": [");
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
    char *name = value_string(ctx->name);
    char *r;
    asprintf(&r, "CONTEXT(%s, %d)", name, ctx->pc);
    free(name);
    return r;
}

static char *value_json_context(uint64_t v) {
    struct context *ctx = value_get(v, NULL);
    char *r, *val;
    asprintf(&r, "{ \"type\": \"context\", \"value\": {");

    val = value_json(ctx->name);
    append_printf(&r, "\"name\": \"%s\"", val);
    free(val);

    val = value_json(ctx->arg);
    append_printf(&r, ", \"arg\": \"%s\"", val);
    free(val);

    val = value_json(ctx->pc);
    append_printf(&r, ", \"pc\": \"%s\"", val);
    free(val);

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
        assert(0);
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
        assert(0);
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
    assert(0);
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

uint64_t value_atom(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    void *p = dict_find(atom_map, value->u.atom.base, value->u.atom.len);
    return (uint64_t) p | VALUE_ATOM;
}

uint64_t value_dict(struct dict *map){
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
        vals[2*i] = value_from_json(k->u.map);
        vals[2*i+1] = value_from_json(v->u.map);
    }

    // vals is sorted already by harmony compiler
    void *p = dict_find(dict_map, vals,
                    value->u.list.nvals * sizeof(uint64_t) * 2);
    free(vals);
    return (uint64_t) p | VALUE_DICT;
}

uint64_t value_set(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (uint64_t) VALUE_SET;
    }
    uint64_t *vals = malloc(value->u.list.nvals * sizeof(uint64_t));
    for (int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(jv->u.map);
    }

    // vals is sorted already by harmony compiler
    void *p = dict_find(set_map, vals, value->u.list.nvals * sizeof(uint64_t));
    free(vals);
    return (uint64_t) p | VALUE_SET;
}

uint64_t value_address(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_LIST);
    if (value->u.list.nvals == 0) {
        return (uint64_t) VALUE_ADDRESS;
    }
    uint64_t *vals = malloc(value->u.list.nvals * sizeof(uint64_t));
    for (int i = 0; i < value->u.list.nvals; i++) {
        struct json_value *jv = value->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[i] = value_from_json(jv->u.map);
    }
    void *p = dict_find(address_map, vals,
                            value->u.list.nvals * sizeof(uint64_t));
    free(vals);
    return (uint64_t) p | VALUE_ADDRESS;
}

uint64_t value_from_json(struct dict *map){
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
        return value_atom(map);
    }
    else if (atom_cmp(type->u.atom, "dict")) {
        return value_dict(map);
    }
    else if (atom_cmp(type->u.atom, "set")) {
        return value_set(map);
    }
    else if (atom_cmp(type->u.atom, "pc")) {
        return value_pc(map);
    }
    else if (atom_cmp(type->u.atom, "address")) {
        return value_address(map);
    }
    else {
        assert(0);
    }
}

void value_init(){
    atom_map = dict_new(0);
    dict_map = dict_new(0);
    set_map = dict_new(0);
    address_map = dict_new(0);
    context_map = dict_new(0);
}
