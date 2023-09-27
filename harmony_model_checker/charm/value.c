// This module deals with Harmony values.  A Harmony value is a 64-bit entity
// of type hvalue_t.  The least significant 4 bits are used to store the type
// of value (bool, int, set, list, ...).  In case of basic types (bool, int,
// program counter), the remaining 60 bits contain the actual value.
// Otherwise, the value is a 16-byte aligned pointer to where the actual
// value is stored.  The value is stored in the global.values hash table
// so it can be easily retrieved.  The entry also maintains the size of
// the value.  In the case of a set or list, the value is simply an array
// of Harmony values (sorted in case of a set).  If it's a dictionary,
// it's an array of alternating key/value pairs, sorted by key.  In case
// of an address (thunk), it is an array where the first entry is the
// function and the remaining values are the arguments.  Strings (aka atoms)
// are simply a list of UTF-8 characters, while a context is a struct
// context followed by an array of values representing the stack.
//
// Some important functions in this module are:
//
//  void *value_get(hvalue_t v, unsigned int *psize);
//      Retrieve the value v.  *psize (if not NULL) will contain
//      the size in bytes
//
//  hvalue_t value_put_X(struct engine *engine, const void *p,
//                                            unsigned int size);
//      Store a value pointed to by p (of value size in bytes) and
//      return an hvalue_t.
//
//  int value_cmp(hvalue_t v1, hvalue_t v2);
//      Compare v1 and v2.  Return a negative value if v1 < v2, a
//      positive value if v1 > v2, and 0 if they are the same.
//
//  char *value_string(hvalue_t v);
//      Return a string representation of the given value v.
//
//  char *value_json(hvalue_t v);
//      Return a JSON representation of v.
//
//  hvalue_t value_from_json(struct engine *engine, struct dict *map);
//      Return a value from the JSON encoded in the given map.

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include "head.h"

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
#include "ops.h"
#include "json.h"

// Return the value represented by v.  If psize != NULL, return the size
// in bytes in *psize.  The value should be stored in the global.values
// hash table.
void *value_get(hvalue_t v, unsigned int *psize){
    v &= ~VALUE_MASK;
    if (v == 0) {
        if (psize != NULL) {
            *psize = 0;
        }
        return NULL;
    }
    return dict_retrieve((void *) v, psize);
}

// Like value_get, but allocate dynamic memory for it
// TODO: OBSOLETE
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

// p points to an UTF-8 string of size bytes.  Return an hvalue.
hvalue_t value_put_atom(struct engine *engine, const void *p, unsigned int size){
    if (size == 0) {
        return VALUE_ATOM;
    }
    void *q = dict_find(global.values, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_ATOM;
}

// p points to a sorted list of unique hvalues.  size is the number of
// bytes that the list occupies.  Return an hvalue for the set.
hvalue_t value_put_set(struct engine *engine, void *p, unsigned int size){
    if (size == 0) {
        return VALUE_SET;
    }
    void *q = dict_find(global.values, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_SET;
}

// p points to an array of key/value pairs, sorted by key (which must be
// unique).  Return an hvalue.
hvalue_t value_put_dict(struct engine *engine, void *p, unsigned int size){
    if (size == 0) {
        return VALUE_DICT;
    }
    void *q = dict_find(global.values, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_DICT;
}

// p points to an array of hvalues.  Return an hvalue.
hvalue_t value_put_list(struct engine *engine, void *p, unsigned int size){
    if (size == 0) {
        return VALUE_LIST;
    }
    void *q = dict_find(global.values, engine->allocator, p, size, NULL);
    return (hvalue_t) q | VALUE_LIST;
}

// p points to an array of hvalues.  The first is the function, and the
// rest are the arguments.  Return an hvalue.
hvalue_t value_put_address(struct engine *engine, void *p, unsigned int size){
    if (size == 0) {
        return VALUE_ADDRESS_SHARED;
    }
    assert(size % sizeof(hvalue_t) == 0);
    void *q = dict_find(global.values, engine->allocator, p, size, NULL);
    if (* (hvalue_t *) p == VALUE_PC_SHARED) {
        return (hvalue_t) q | VALUE_ADDRESS_SHARED;
    }
    else {
        return (hvalue_t) q | VALUE_ADDRESS_PRIVATE;
    }
}

// ctx points to a context.  Returns an hvalue.
hvalue_t value_put_context(struct engine *engine, struct context *ctx){
	assert(ctx->pc >= 0);
    void *q = dict_find(global.values, engine->allocator, ctx, ctx_size(ctx), NULL);
    if (ctx->eternal) {
        return (hvalue_t) q | VALUE_CONTEXT | VALUE_CONTEXT_ETERNAL;
    }
    else {
        return (hvalue_t) q | VALUE_CONTEXT;
    }
}

// Helper function for value_cmp.  False < True, for arbitrary reasons.
static int value_cmp_bool(hvalue_t v1, hvalue_t v2){
    assert(v1 != v2);
    return v1 == 0 ? -1 : 1;
}

// Helper function for value_cmp
static int value_cmp_int(hvalue_t v1, hvalue_t v2){
    return (int64_t) v1 < (int64_t) v2 ? -1 : 1;
}

// Helper function for value_cmp
static int value_cmp_atom(hvalue_t v1, hvalue_t v2){
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

// Helper function for value_cmp
static int value_cmp_pc(hvalue_t v1, hvalue_t v2){
    return v1 < v2 ? -1 : 1;
}

// Helper function for value_cmp.  Dictionaries are lexicographically ordered
// by first sorting the key/value pairs by key.  Fortunately, that's exactly
// how we store dictionaries
static int value_cmp_dict(hvalue_t v1, hvalue_t v2){
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

// Helper function for value_cmp.  Sets are first sorted and then lexicographically
// compared.  Fortunately, we keep sets as ordered lists.
static int value_cmp_set(hvalue_t v1, hvalue_t v2){
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

// Helper function for value_cmp.  List are lexicographically compared.
static int value_cmp_list(hvalue_t v1, hvalue_t v2){
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

// Helper function for value_cmp.  Addresses are "thunks" that are represented
// as a list of values, the first of which is a function and the remaining values
// are arguments.  We simply compare the list lexicographically.  By the way,
// None is represented as the empty list, and so is the lowest address.
static int value_cmp_address(hvalue_t v1, hvalue_t v2){
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

// Contexts are kind of compared arbitrarily using memcmp.
// TODO.  Maybe should compare pc, ... to get some sensible order?
static int value_cmp_context(hvalue_t v1, hvalue_t v2){
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

// This function compares two values v1 and v2, and returns a negative value if
// v1 < v2, 0 if  v1 == v2, and a positive value if v1 > v2.  Values are first
// compared by type (i.e., bools go before integer go before ...) and then are
// compared within their type.
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
        return value_cmp_bool(v1 & ~VALUE_LOBITS, v2 & ~VALUE_LOBITS);
    case VALUE_INT:
        return value_cmp_int(v1 & ~VALUE_LOBITS, v2 & ~VALUE_LOBITS);
    case VALUE_ATOM:
        return value_cmp_atom(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_PC:
        return value_cmp_pc(v1 & ~VALUE_LOBITS, v2 & ~VALUE_LOBITS);
    case VALUE_LIST:
        return value_cmp_list(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_DICT:
        return value_cmp_dict(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_SET:
        return value_cmp_set(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_ADDRESS_SHARED:
    case VALUE_ADDRESS_PRIVATE:
        return value_cmp_address(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    case VALUE_CONTEXT:
        return value_cmp_context(v1 & ~VALUE_MASK, v2 & ~VALUE_MASK);
    default:
        panic("value_cmp: bad value type");
        return 0;
    }
}

// Helper function for value_string
static void value_string_bool(struct strbuf *sb, hvalue_t v) {
    v >>= VALUE_BITS;
    if (v != 0 && v != 1) {
        fprintf(stderr, "value_string_bool %"PRI_HVAL"\n", v);
        panic("value_string_bool: bad value");
    }
    assert(v == 0 || v == 1);
    strbuf_printf(sb, v == 0 ? "False" : "True");
}

// Helper function for value_json
static void value_json_bool(struct strbuf *sb, hvalue_t v) {
    v >>= VALUE_BITS;
    if (v != 0 && v != 1) {
        fprintf(stderr, "value_json_bool %"PRI_HVAL"\n", v);
        panic("value_json_bool: bad value");
    }
    assert(v == 0 || v == 1);
    strbuf_printf(sb, "{ \"type\": \"bool\", \"value\": \"%s\" }", v == 0 ? "False" : "True");
}

// Helper function for value_string
static void value_string_int(struct strbuf *sb, hvalue_t v) {
    int64_t w = VALUE_FROM_INT(v);
    strbuf_printf(sb, "%"PRId64"", w);
}

// Helper function for value_json
static void value_json_int(struct strbuf *sb, hvalue_t v) {
    int64_t w = (int64_t) VALUE_FROM_INT(v);
    strbuf_printf(sb, "{ \"type\": \"int\", \"value\": \"%"PRId64"\" }", (int64_t) w);
}

// Helper function for value_string
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

// Helper function for value_json
static void value_json_atom(struct strbuf *sb, hvalue_t v) {
    unsigned int size;
    char *s = value_get(v, &size);
    // TODO.  There should probably be a json_escape function that prints to
    //        a strbuf.  This is easy but inefficient.
    char *esc = json_escape(s, size);

    strbuf_printf(sb, "{ \"type\": \"atom\", \"value\": \"%s\" }", esc);
    free(esc);
}

// Helper function for value_string
static void value_string_pc(struct strbuf *sb, hvalue_t v) {
    assert(VALUE_FROM_PC(v) < 10000);      // debug
    strbuf_printf(sb, "PC(%u)", (unsigned int) VALUE_FROM_PC(v));
}

// Helper function for value_json
static void value_json_pc(struct strbuf *sb, hvalue_t v) {
    strbuf_printf(sb, "{ \"type\": \"pc\", \"value\": \"%d\" }", (int) VALUE_FROM_PC(v));
}

// Helper function for value_string
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

// Helper function for value_json
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

// Helper function for value_string
static void value_string_list(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "[]");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);

    strbuf_printf(sb, "[");
    for (unsigned int i = 0; i < size; i++) {
        if (i != 0) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_string(sb, vals[i]);
    }
    strbuf_printf(sb, "]");
}

// Helper function for value_string
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

// Helper function for value_json
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

// Helper function for value_json
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

// Helper function for value_string
static void strbuf_indices_string(struct strbuf *sb, const hvalue_t *vec, int size) {
    if (size == 0) {
        strbuf_printf(sb, "None");
        return;
    }
    int index = 1;
    if (VALUE_TYPE(vec[0]) == VALUE_PC) {
        int pc = (int) VALUE_FROM_PC(vec[0]);
        if (pc == -1) {                  // shared variable
            char *s = value_string(vec[1]);     // TODO.  Inefficient
            assert(s[0] == '"');
            int len = strlen(s);
            strbuf_printf(sb, "?%.*s", len - 2, s + 1);
            free(s);
            index = 2;
        }
        else if (pc == -2) {            // method variable
            char *s = value_string(vec[1]);     // TODO.  Inefficient
            assert(s[0] == '"');
            int len = strlen(s);
            strbuf_printf(sb, "?@%.*s", len - 2, s + 1);
            free(s);
            index = 2;
        }
    }
    if (index == 1) {
        strbuf_printf(sb, "?");
        strbuf_value_string(sb, vec[0]);
    }
    for (int i = index; i < size; i++) {
        strbuf_printf(sb, "[");
        strbuf_value_string(sb, vec[i]);
        strbuf_printf(sb, "]");
    }
}

// This function takes a list of values representing an address or, more accurately,
// a "thunk".  The first value is a function, and the remaining values are arguments.
// TODO.  Rename to "address_string" or something like that
char *indices_string(const hvalue_t *vec, int size) {
    struct strbuf sb;

    strbuf_init(&sb);
    strbuf_indices_string(&sb, vec, size);
    return strbuf_convert(&sb);
}

// Helper function for value_string
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

// Helper function for value_json
static void value_json_address(struct strbuf *sb, hvalue_t v) {
    if (v == 0) {
        strbuf_printf(sb, "{ \"type\": \"address\" }");
        return;
    }

    void *p = (void *) v;
    unsigned int size;
    hvalue_t *vals = dict_retrieve(p, &size);
    size /= sizeof(hvalue_t);
    assert(size > 0);
    strbuf_printf(sb, "{ \"type\": \"address\", \"func\": ");
    strbuf_value_json(sb, vals[0]);
    strbuf_printf(sb, ", \"args\": [");
    for (unsigned int i = 1; i < size; i++) {
        if (i != 1) {
            strbuf_printf(sb, ", ");
        }
        strbuf_value_json(sb, vals[i]);
    }

    strbuf_printf(sb, " ] }");
}

// Helper function for value_string
static void value_string_context(struct strbuf *sb, hvalue_t v) {
    struct context *ctx = value_get(v, NULL);
    strbuf_printf(sb, "CONTEXT(");
#ifdef SHORT
    strbuf_value_string(sb, ctx->name);
    strbuf_printf(sb, ", %d)", ctx->pc);
    free(name);
#else
    strbuf_printf(sb, "pc=%d", ctx->pc);
    if (ctx->initial || ctx->id != 0) {
        strbuf_printf(sb, ",id=%u", ctx->id);
    }
    strbuf_printf(sb, ",vars=");
    strbuf_value_string(sb, ctx->vars);
    if (ctx->extended) {
        strbuf_printf(sb, ",this=");
        strbuf_value_string(sb, ctx_this(ctx));
        if (ctx_trap_pc(ctx) != 0) {
            strbuf_printf(sb, ",trap_pc=");
            strbuf_value_string(sb, ctx_trap_pc(ctx));
            strbuf_printf(sb, ",trap_arg=");
            strbuf_value_string(sb, ctx_trap_arg(ctx));
        }
        if (ctx_failure(ctx) != 0) {
            strbuf_printf(sb, ",failure=");
            strbuf_value_string(sb, ctx_failure(ctx));
        }
    }

#ifdef OBSOLETE
    strbuf_printf(sb, ",fp=%d", ctx->fp);
#endif
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

// Helper function for print_vars
static void strbuf_print_vars(struct strbuf *sb, hvalue_t v){
    if (VALUE_TYPE(v) == VALUE_DICT) {
        unsigned int size;
        hvalue_t *vars = value_get(v, &size);
        size /= sizeof(hvalue_t);
        strbuf_printf(sb, "{");
        for (unsigned int i = 0; i < size; i += 2) {
            if (i > 0) {
                strbuf_printf(sb, ",");
            }
            char *k = value_string(vars[i]);
            int len = strlen(k);
            char *v = value_json(vars[i+1]);
            strbuf_printf(sb, " \"%.*s\": %s", len - 2, k + 1, v);
            free(k);
            free(v);
        }
        strbuf_printf(sb, " }");
    }
    else {
        strbuf_value_json(sb, v);
    }
}

// v would typically represent a dictionary that maps variable names to values.
// Instead of printing it as a regular dictionary, the output is stylized to
// represent a set of variables and their respective values.
void print_vars(FILE *file, hvalue_t v){
    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_print_vars(&sb, v);
    fwrite(sb.buf, 1, sb.len, file);
    strbuf_deinit(&sb);
}

// Helper function for value_trace
static void value_json_trace(struct strbuf *sb, struct callstack *cs, unsigned int pc, hvalue_t vars){
    if (cs->parent != NULL) {
        value_json_trace(sb, cs->parent, cs->return_address >> CALLTYPE_BITS, cs->vars);
        strbuf_printf(sb, ",");
    }
    const struct env_Frame *ef = global.code.instrs[cs->pc].env;
    char *method = value_string(ef->name);
    char *arg = json_escape_value(cs->arg);
    strbuf_printf(sb, "{\"pc\": \"%u\",", pc);
    strbuf_printf(sb, "\"xpc\": \"%u\",", cs->pc);
    strbuf_printf(sb, "\"method_name\": ");
    strbuf_value_json(sb, ef->name);
    strbuf_printf(sb, ",\n");
    strbuf_printf(sb, "\"method_arg\": ");
    strbuf_value_json(sb, cs->arg);
    strbuf_printf(sb, ",\n");
    if (*arg == '(') {
        strbuf_printf(sb, "\"method\": \"%.*s%s\",", (int) strlen(method) - 2, method + 1, arg);
    }
    else {
        strbuf_printf(sb, "\"method\": \"%.*s(%s)\",", (int) strlen(method) - 2, method + 1, arg);
    }
    switch (cs->return_address & CALLTYPE_MASK) {
    case CALLTYPE_PROCESS:
        strbuf_printf(sb, "\"calltype\": \"process\",");
        break;
    case CALLTYPE_NORMAL:
        strbuf_printf(sb, "\"calltype\": \"normal\",");
        break;
    case CALLTYPE_INTERRUPT:
        strbuf_printf(sb, "\"calltype\": \"interrupt\",");
        break;
    default:
        printf(">>> %x\n", cs->return_address);
        panic("value_json_trace: bad call type");
    }
    strbuf_printf(sb, "\"vars\":");
    strbuf_print_vars(sb, vars);
    strbuf_printf(sb, ",\"sp\": %u}", cs->sp);
    free(arg);
    free(method);
}

// This function prints information about a context (state of a threads) with
// additional information about its callstack which is kept during the re-execution
// of a counter-example.
void value_trace(FILE *file, struct callstack *cs, unsigned int pc, hvalue_t vars, char *prefix){
    struct strbuf sb;
    strbuf_init(&sb);
    value_json_trace(&sb, cs, pc, vars);
    fwrite(sb.buf, 1, sb.len, file);
    strbuf_deinit(&sb);
}

// Helper function for value_json
static void value_json_context(struct strbuf *sb, hvalue_t v) {
    struct context *ctx = value_get(v, NULL);
    
    strbuf_printf(sb, "{ \"type\": \"context\", \"value\": {");
    if (ctx->initial || ctx->id != 0) {
        strbuf_printf(sb, "\"id\": { \"type\": \"int\", \"value\": \"%u\" },", ctx->id);
    }
    strbuf_printf(sb, "\"pc\": { \"type\": \"pc\", \"value\": \"%u\" },", ctx->pc);
#ifdef TODO
    struct callstack *cs = dict_lookup(global.tracemap, &v, sizeof(v));
    if (cs == NULL) {
        strbuf_printf(sb, "\"vars\":");
        strbuf_print_vars(sb, ctx->vars);
        strbuf_printf(sb, ",");
    }
    else {
        strbuf_printf(sb, "\"callstack\":[");
        value_json_trace(sb, cs, ctx->pc, ctx->vars);
        strbuf_printf(sb, "],");
    }
#else
    strbuf_printf(sb, "\"vars\":");
    strbuf_print_vars(sb, ctx->vars);
    strbuf_printf(sb, ",");
#endif

    if (ctx->atomic > 0) {
        strbuf_printf(sb, "\"atomic\": { \"type\": \"int\", \"value\": \"%u\" },", ctx->atomic);
    }
    if (ctx->readonly > 0) {
        strbuf_printf(sb, "\"readonly\": { \"type\": \"int\", \"value\": \"%u\" },", ctx->readonly);
    }
    if (ctx->initial) {
        strbuf_printf(sb, "\"initial\": { \"type\": \"bool\", \"value\": \"True\" },");
    }
    if (ctx->atomicFlag) {
        strbuf_printf(sb, "\"atomicFlag\": { \"type\": \"bool\", \"value\": \"True\" },");
    }
    if (ctx->interruptlevel) {
        strbuf_printf(sb, "\"interruptlevel\": { \"type\": \"int\", \"value\": \"1\" },");
    }
    if (ctx->stopped) {
        strbuf_printf(sb, "\"stopped\": { \"type\": \"bool\", \"value\": \"True\" },");
    }
    if (ctx->terminated) {
        strbuf_printf(sb, "\"mode\": { \"type\": \"atom\", \"value\": \"terminated\" },");
    }
    else if (ctx->failed) {
        strbuf_printf(sb, "\"mode\": { \"type\": \"atom\", \"value\": \"failed\" },");
    }
    if (ctx->eternal) {
        strbuf_printf(sb, "\"eternal\": { \"type\": \"bool\", \"value\": \"True\" },");
    }
    if (ctx->extended) {
        if (ctx_this(ctx) != 0) {
            strbuf_printf(sb, "\"this\": ");
            strbuf_value_json(sb, ctx_this(ctx));
            strbuf_printf(sb, ", ");
        }
        if (ctx_failure(ctx) != 0) {
            strbuf_printf(sb, "\"failure\": ");
            strbuf_value_json(sb, ctx_failure(ctx));
            strbuf_printf(sb, ", ");
        }
        if (ctx_trap_pc(ctx) != 0) {
            strbuf_printf(sb, "\"trap_pc\": ");
            strbuf_value_json(sb, ctx_trap_pc(ctx));
            strbuf_printf(sb, ", ");
        }
        if (ctx_trap_arg(ctx) != 0) {
            strbuf_printf(sb, "\"trap_arg\": ");
            strbuf_value_json(sb, ctx_trap_arg(ctx));
            strbuf_printf(sb, ", ");
        }
    }
    strbuf_printf(sb, "\"sp\": { \"type\": \"int\", \"value\": \"%u\" }", ctx->sp);

    strbuf_printf(sb, " } }");
}

// This function pretty-prints Harmony value v in the given string buffer
void strbuf_value_string(struct strbuf *sb, hvalue_t v){
    switch (VALUE_TYPE(v)) {
    case VALUE_BOOL:
        value_string_bool(sb, v & ~VALUE_LOBITS);
        break;
    case VALUE_INT:
        value_string_int(sb, v & ~VALUE_LOBITS);
        break;
    case VALUE_ATOM:
        value_string_atom(sb, v & ~VALUE_MASK);
        break;
    case VALUE_PC:
        value_string_pc(sb, v & ~VALUE_LOBITS);
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
    case VALUE_ADDRESS_SHARED:
    case VALUE_ADDRESS_PRIVATE:
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

// This function pretty-prints Harmony value v and returns it in a malloc-ed
// null-terminated byte buffer.
char *value_string(hvalue_t v){
    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_value_string(&sb, v);
    return strbuf_convert(&sb);
}

// Print Harmony value v encoded as a JSON object in the given string buffer
void strbuf_value_json(struct strbuf *sb, hvalue_t v){
    switch VALUE_TYPE(v) {
    case VALUE_BOOL:
        value_json_bool(sb, v & ~VALUE_LOBITS);
        break;
    case VALUE_INT:
        value_json_int(sb, v & ~VALUE_LOBITS);
        break;
    case VALUE_ATOM:
        value_json_atom(sb, v & ~VALUE_MASK);
        break;
    case VALUE_PC:
        value_json_pc(sb, v & ~VALUE_LOBITS);
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
    case VALUE_ADDRESS_SHARED:
    case VALUE_ADDRESS_PRIVATE:
        value_json_address(sb, v & ~VALUE_MASK);
        break;
    case VALUE_CONTEXT:
        value_json_context(sb, v);
        break;
    default:
        printf("bad value type: %p\n", (void *) v);
        panic("strbuf_value_json: bad value type");
    }
}

// Encode the given Harmony value v as a JSON value, returned as a string.
char *value_json(hvalue_t v){
    struct strbuf sb;
    strbuf_init(&sb);
    strbuf_value_json(&sb, v);
    return strbuf_convert(&sb);
}

// buf.base points to a non-null terminated character string of length buf.len.
// Compare this lexicographically with the null-terminated string s.
static bool atom_cmp(json_buf_t buf, char *s){
    unsigned int n = strlen(s);
    if (n != buf.len) {
        return false;
    }
    return strncmp(buf.base, s, n) == 0;
}

// Helper function for value_from_json.  A bool has a "value" field that contains
// either the string "False" or "True"
static hvalue_t value_bool(struct dict *map){
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

// Helper function for value_from_json.  An int contains a "value" field
// that contains the integer.
static hvalue_t value_int(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    hvalue_t v;
    // TODO.  I think "inf" and "-inf" are obsolete.
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

// Helper function for value_from_json.  A program counter value contains a
// "value" filed containing the integer representing a program counter
static hvalue_t value_pc(struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    char *copy = malloc(value->u.atom.len + 1);
    memcpy(copy, value->u.atom.base, value->u.atom.len);
    copy[value->u.atom.len] = 0;
    long v = atol(copy);
    free(copy);
    return VALUE_TO_PC(v);
}

// Helper function for value_from_json.  An atom (string) has a "value" field
// containing the string value.
static hvalue_t value_atom(struct engine *engine, struct dict *map){
    struct json_value *value = dict_lookup(map, "value", 5);
    assert(value->type == JV_ATOM);
    if (value->u.atom.len == 0) {
        return VALUE_ATOM;
    }
    void *p = dict_find(global.values, engine->allocator, value->u.atom.base, value->u.atom.len, NULL);
    return (hvalue_t) p | VALUE_ATOM;
}

// Helper function for value_from_json.  A dictionary has a "value" field containing
// a list of "key"/"value" pairs.
static hvalue_t value_dict(struct engine *engine, struct dict *map){
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
    void *p = dict_find(global.values, engine->allocator, vals,
                    value->u.list.nvals * sizeof(hvalue_t) * 2, NULL);
    free(vals);
    return (hvalue_t) p | VALUE_DICT;
}

// Helper function for value_from_json.  A set has a "value" field containing
// a sorted list of the values.
static hvalue_t value_set(struct engine *engine, struct dict *map){
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
    void *p = dict_find(global.values, engine->allocator, vals, value->u.list.nvals * sizeof(hvalue_t), NULL);
    free(vals);
    return (hvalue_t) p | VALUE_SET;
}

// Helper function for value_from_json.  A list has a "value" field containing
// a list of the values.
static hvalue_t value_list(struct engine *engine, struct dict *map){
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
    void *p = dict_find(global.values, engine->allocator, vals, value->u.list.nvals * sizeof(hvalue_t), NULL);
    free(vals);
    return (hvalue_t) p | VALUE_LIST;
}

// Helper function for value_from_json.  An address (or perhaps better, a "thunk")
// has a "func" field containing a function value and an "args" field containing
// a list of arguments.
static hvalue_t value_address(struct engine *engine, struct dict *map){
    struct json_value *func = dict_lookup(map, "func", 4);
    if (func == NULL) {
        return (hvalue_t) VALUE_ADDRESS_SHARED;        // None
    }
    assert(func->type == JV_MAP);
    struct json_value *args = dict_lookup(map, "args", 4);
    assert(args->type == JV_LIST);
    unsigned int size = (1 + args->u.list.nvals) * sizeof(hvalue_t);
    hvalue_t *vals = malloc(size);
    vals[0] = value_from_json(engine, func->u.map);
    for (unsigned int i = 0; i < args->u.list.nvals; i++) {
        struct json_value *jv = args->u.list.vals[i];
        assert(jv->type == JV_MAP);
        vals[1+i] = value_from_json(engine, jv->u.map);
    }
    hvalue_t result = value_put_address(engine, vals, size);
    assert(vals[0] != VALUE_PC_SHARED || VALUE_TYPE(result) == VALUE_ADDRESS_SHARED);
    free(vals);
    return result;
}

// This function takes a JSON dictionary value and turns it into a Harmony value.
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
#ifdef HEAP_ALLOC
            hvalue_t *copy = malloc(size * sizeof(hvalue_t));
#else
            hvalue_t copy[size];
#endif
            memcpy(copy, vals, n);
            copy[i + 1] = value;
            hvalue_t v = value_put_dict(engine, copy, n);
#ifdef HEAP_ALLOC
            free(copy);
#endif
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
#ifdef HEAP_ALLOC
    hvalue_t *nvals = malloc((size + 2) * sizeof(hvalue_t));
#else
    hvalue_t nvals[size + 2];
#endif
    memcpy(nvals, vals, i * sizeof(hvalue_t));
    nvals[i] = key;
    nvals[i+1] = value;
    memcpy(&nvals[i+2], &vals[i], (size - i) * sizeof(hvalue_t));
    hvalue_t v = value_put_dict(engine, nvals, n);
#ifdef HEAP_ALLOC
    free(nvals);
#endif
    *result = v;
    return true;
}

// Like value_dict_trystore, but panics if something goes wrong
hvalue_t value_dict_store(struct engine *engine, hvalue_t dict, hvalue_t key, hvalue_t value){
    hvalue_t result;
    bool r = value_dict_trystore(engine, dict, key, value, true, &result);
    if (!r) {
        fprintf(stderr, "value_dict_store: failed\n");
        exit(1);
    }
    return result;
}

// "root" should be either a dictionary or a key.  This function stores "value"
// under "key" in "root" (i.e., it computes "root[key] = value"), and returns
// a new dictionary or list.  "allow_inserts" specifies if a new value is allowed
// to be inserted, or if only overwrites are allowed.
//
// For a list of size n, note that you can store in root[n] and extend the length
// of the list by 1.
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
#ifdef HEAP_ALLOC
                hvalue_t *nvals = malloc(n * sizeof(hvalue_t));
#else
                hvalue_t nvals[n];
#endif
                memcpy(nvals, vals, size);
                nvals[i + 1] = value;
                hvalue_t v = value_put_dict(engine, nvals, size);
#ifdef HEAP_ALLOC
                free(nvals);
#endif
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
#ifdef HEAP_ALLOC
        hvalue_t *nvals = malloc((n + 2) * sizeof(hvalue_t));
#else
        hvalue_t nvals[n + 2];
#endif
        memcpy(nvals, vals, i * sizeof(hvalue_t));
        nvals[i] = key;
        nvals[i+1] = value;
        memcpy(&nvals[i+2], &vals[i], (n - i) * sizeof(hvalue_t));
        hvalue_t v = value_put_dict(engine, nvals, size);
#ifdef HEAP_ALLOC
        free(nvals);
#endif
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
#ifdef HEAP_ALLOC
        hvalue_t *nvals = malloc(nsize);
#else
        hvalue_t nvals[nsize / sizeof(hvalue_t)];
#endif
        memcpy(nvals, vals, size);
        nvals[index] = value;
        hvalue_t v = value_put_list(engine, nvals, nsize);
#ifdef HEAP_ALLOC
        free(nvals);
#endif
        *result = v;
        return true;
    }
}

// Like value_try_store but panics if something goes wrong
hvalue_t value_store(struct engine *engine, hvalue_t root, hvalue_t key, hvalue_t value){
    hvalue_t result;
    bool r = value_trystore(engine, root, key, value, true, &result);
    if (!r) {
        fprintf(stderr, "value_store: failed\n");
        exit(1);
    }
    return result;
}

// Look up the given key in the given dictionary and return the value.  Returns 0
// if the key does not exist in the dictionary.
//
// TODO.  Is this functionality duplicated by value_tryload()??
hvalue_t value_dict_load(hvalue_t dict, hvalue_t key){
    assert(VALUE_TYPE(dict) == VALUE_DICT);
    if (dict == VALUE_DICT) {       // dictionary is empty
        return 0;
    }

    hvalue_t *vals;
    unsigned int size;
    vals = value_get(dict, &size);
    size /= sizeof(hvalue_t);
    assert(size % 2 == 0);

    unsigned int i;
    for (i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            return vals[i + 1];
        }
        /* TODO.  The following would be correct, but since value_cmp() is an
                  expensive function, I figured it would be better to not use it.
            if (value_cmp(vals[i], key) > 0) {
                break;
            }
        */
    }
    return 0;
}

// Remove the given key from the dictionary and return the new dictionary.
// TODO.  Does this duplicate the work of value_remove()??
hvalue_t value_dict_remove(struct engine *engine, hvalue_t dict, hvalue_t key){
    assert(VALUE_TYPE(dict) == VALUE_DICT);
    if (dict == VALUE_DICT) {       // dictionary is empty
        return VALUE_DICT;
    }

    unsigned int size;
    hvalue_t *vals = value_get(dict, &size);
    size /= sizeof(hvalue_t);
    assert(size % 2 == 0);

    // If there is only one key/value pair, the result is either unchanged
    // or an empty dictionary.
    if (size == 2) {
        return vals[0] == key ? VALUE_DICT : dict;
    }

    assert(size > 2);
    for (unsigned int i = 0; i < size; i += 2) {
        if (vals[i] == key) {
            int n = (size - 2) * sizeof(hvalue_t);
#ifdef HEAP_ALLOC
            hvalue_t *copy = malloc((size - 2) * sizeof(hvalue_t));
#else
            hvalue_t copy[size - 2];
#endif
            memcpy(copy, vals, i * sizeof(hvalue_t));
            memcpy(&copy[i], &vals[i+2],
                   (size - i - 2) * sizeof(hvalue_t));
            hvalue_t v = value_put_dict(engine, copy, n);
#ifdef HEAP_ALLOC
            free(copy);
#endif
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

// Remove the given key from either a dictionary or a list.
// TODO.  Should perhaps also support removing characters from a string.
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

        // Special case: if there is only one key value pair, the result
        // is either unchanged or an empty dictionary.
        if (n == 2) {
            return vals[0] == key ? VALUE_DICT : root;
        }

        assert(n > 2);
        for (unsigned i = 0; i < n; i += 2) {
            if (vals[i] == key) {
                size -= 2 * sizeof(hvalue_t);
#ifdef HEAP_ALLOC
                hvalue_t *copy = malloc(size);
#else
                hvalue_t copy[size / sizeof(hvalue_t)];
#endif
                memcpy(copy, vals, i * sizeof(hvalue_t));
                memcpy(&copy[i], &vals[i+2],
                       (n - i - 2) * sizeof(hvalue_t));
                hvalue_t v = value_put_dict(engine, copy, size);
#ifdef HEAP_ALLOC
                free(copy);
#endif
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

        // TODO.  Should perhaps return an error in this case?
        if (index >= n) {
            return root;
        }

        // TODO. For efficiency should perhaps special case removing entry 0
        //       from a list of size 1 (which will be the empty list).

        size -= sizeof(hvalue_t);
#ifdef HEAP_ALLOC
        hvalue_t *copy = malloc(size);
#else
        hvalue_t copy[size / sizeof(hvalue_t)];
#endif
        memcpy(copy, vals, index * sizeof(hvalue_t));
        memcpy(&copy[index], &vals[index+1],
               (n - index - 1) * sizeof(hvalue_t));
        hvalue_t v = value_put_list(engine, copy, size);
#ifdef HEAP_ALLOC
        free(copy);
#endif
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

// A bag is a dictionary that maps elements to their multiplicity.  This function
// add "multiplicity" copies of v to the given bag and returns a new bag.
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

// Remove a copy of v from the given bag (which must be in there).
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

// Push a copy of the given value on the stack of the given context (state of
// a Harmony thread).  Detects stack overflow.
bool value_ctx_push(struct context *ctx, hvalue_t v){
    if (ctx->sp == MAX_CONTEXT_STACK - ctx_extent) {
        return false;
    }
    ctx_stack(ctx)[ctx->sp++] = v;
    return true;
}

// Pop and return a value from the context stack.
hvalue_t value_ctx_pop(struct context *ctx){
    assert(ctx->sp > 0);
    return ctx_stack(ctx)[--ctx->sp];
}

// For memory efficiency, contexts have some optional values.  If those are
// needed, value_ctx_extend adds them to the context (unless they are already
// there).
void value_ctx_extend(struct context *ctx){
    if (ctx->extended) {
        return;
    }
    memmove(&context_stack(ctx)[ctx_extent], context_stack(ctx), ctx->sp * sizeof(hvalue_t));
    memset(context_stack(ctx), 0, ctx_extent * sizeof(hvalue_t));
    ctx_this(ctx) = VALUE_DICT;
    ctx->extended = true;
}

// A failure has occurred and this is registered with the context.
hvalue_t value_ctx_failure(struct context *ctx, struct engine *engine, char *fmt, ...){
    va_list args;

    assert(!ctx->failed);
    value_ctx_extend(ctx);
    assert(ctx_failure(ctx) == 0);

    struct strbuf sb;
    strbuf_init(&sb);
    va_start(args, fmt);
    strbuf_vprintf(&sb, fmt, args);
    va_end(args);
    // printf("FAIL %.*s\n", strbuf_getlen(&sb), strbuf_getstr(&sb));
    ctx_failure(ctx) = value_put_atom(engine, strbuf_getstr(&sb), strbuf_getlen(&sb));
    ctx->failed = true;
    strbuf_deinit(&sb);

    return 0;
}

// A Harmony state contains a bag (multiset) of contexts.  This function checks
// if all that contexts are of "eternal" threads (threads that are allowed not
// to terminate).
bool value_state_all_eternal(struct state *state) {
    if (state->bagsize == 0) {
        return true;
    }
    for (unsigned int i = 0; i < state->bagsize; i++) {
        assert(VALUE_TYPE(state_contexts(state)[i]) == VALUE_CONTEXT);
        struct context *ctx = value_get(state_contexts(state)[i], NULL);
        if (!ctx->eternal) {
            return false;
        }
    }
    return true;
}

// ctxbag is a Harmony value containing a bag of contexts.  A bag is a
// multiset represented as a dictionary that maps elements to their
// multiplicity.  This function checks if all contexts are of eternal threads.
bool value_ctx_all_eternal(hvalue_t ctxbag) {
    if (ctxbag == VALUE_DICT) {     // optimization
        return true;
    }
    unsigned int size;
    hvalue_t *vals = value_get(ctxbag, &size);
    size /= sizeof(hvalue_t);
    for (unsigned int i = 0; i < size; i += 2) {
        assert(VALUE_TYPE(vals[i]) == VALUE_CONTEXT);
        assert(VALUE_TYPE(vals[i + 1]) == VALUE_INT);
        struct context *ctx = value_get(vals[i], NULL);
        assert(ctx != NULL);
        if (!ctx->eternal) {
            return false;
        }
    }
    return true;
}

// This function takes a Harmony value, represents it as a string, and then
// adds escape characters so it can be used as a JSON string.  If the value
// is a list, it prints it as a tuple (surrounded by parentheses) instead
// of brackets.
char *json_escape_value(hvalue_t v){
    char *s = value_string(v);
    int len = strlen(s);
    if (*s == '[') {
        *s = '(';
        s[len-1] = ')';
    }
    char *r = json_escape(s, len);
    free(s);
    return r;
}

// Remove context 'ctx' from the state.  The multiset of contexts in a state
// is represented as a bag.
void context_remove(struct state *state, hvalue_t ctx){
    for (unsigned int i = 0; i < state->bagsize; i++) {
        if (state_contexts(state)[i] == ctx) {
            if (multiplicities(state)[i] > 1) {
                multiplicities(state)[i]--;
            }
            else {
                state->bagsize--;
                memmove(&state_contexts(state)[i], &state_contexts(state)[i+1],
                        (state->bagsize - i) * sizeof(hvalue_t) + i);
                memmove((char *) &state_contexts(state)[state->bagsize] + i,
                        (char *) &state_contexts(state)[state->bagsize + 1] + i + 1,
                        state->bagsize - i);
            }
            return;
        }
    }
    // TODO. this can happen with invariant contexts
    // panic("context_remove: can't find context");
}

// Add context 'ctx' to the state's context bag.  May fail if there are too
// many different contexts (i.e., >= MAX_CONTEXT_BAG).
int context_add(struct state *state, hvalue_t ctx){
    unsigned int i;
    for (i = 0; i < state->bagsize; i++) {
        if (state_contexts(state)[i] == ctx) {
            multiplicities(state)[i]++;
            return i;
        }
        if (state_contexts(state)[i] > ctx) {
            break;
        }
    }

    if (state->bagsize >= MAX_CONTEXT_BAG) {
        return -1;
    }
 
    // Move the last multiplicities
    memmove((char *) &state_contexts(state)[state->bagsize + 1] + i + 1,
            (char *) &state_contexts(state)[state->bagsize] + i,
            state->bagsize - i);

    // Move the last contexts plus the first multiplicitkes
    memmove(&state_contexts(state)[i+1], &state_contexts(state)[i],
                    (state->bagsize - i) * sizeof(hvalue_t) + i);

    state->bagsize++;
    state_contexts(state)[i] = ctx;
    multiplicities(state)[i] = 1;
    return i;
}
