#include "head.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>
#include <stdbool.h>

#include "global.h"
#include "hashdict.h"
#include "json.h"
#include "strbuf.h"

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

#define buf_adv(b)		do { assert((b)->len > 0); (b)->base++; (b)->len--; } while (false)

static void json_map_cleanup(void *env, const void *key, unsigned int keylen, void *val){
    struct json_value **pjv = val;

	json_value_free(*pjv);
}

void json_value_free(struct json_value *jv){
	switch (jv->type) {
	case JV_ATOM:
		free(jv->u.atom.base);
		break;
	case JV_MAP:
		dict_iter(jv->u.map, json_map_cleanup, jv);
		dict_delete(jv->u.map);
		break;
	case JV_LIST:
		{
			for (unsigned int i = 0; i < jv->u.list.nvals; i++) {
				json_value_free(jv->u.list.vals[i]);
			}
			free(jv->u.list.vals);
		}
		break;
	default:
		assert(0);
	}
	free(jv);
}

static void json_string_add(json_buf_t *buf, char c){
	/* Grow efficiently, doubling at powers of 2.
	 */
	if (((buf->len + 1) & buf->len) == 0) {
		buf->base = realloc(buf->base, (buf->len + 1) * 2);
	}
	buf->base[buf->len++] = c;
}

static void json_skip_blanks(json_buf_t *buf){
	while (buf->len > 0) {
		if (!isspace(*buf->base)) {
			return;
		}
		buf_adv(buf);
	}
}

static bool is_atom_char(char c){
	return isalnum(c) || c == '.' || c == '-' || c == '_' || c == '/';
}

static void json_parse_atom(json_buf_t *buf, json_buf_t *atom){
	assert(buf->len > 0);
	assert(is_atom_char(*buf->base));
    atom->quoted = false;
	while (buf->len > 0) {
		if (!is_atom_char(*buf->base)) {
			return;
		}
		json_string_add(atom, *buf->base);
		buf_adv(buf);
	}
}

void json_map_append(struct json_value *map, json_buf_t key, struct json_value *jv){
	assert(map->type == JV_MAP);
    bool new;
	struct json_value **p = dict_insert(map->u.map, NULL, key.base, key.len, &new);
	if (!new) {
		fprintf(stderr, "json_map_append: duplicate key: '%.*s'\n",
							(int) key.len, key.base);
	}
	*p = jv;
}

static struct json_value *json_parse_struct(json_buf_t *buf){
	assert(buf->len > 0);
	assert(*buf->base == '{');
	buf_adv(buf);

	struct json_value *jv = new_alloc(struct json_value);
	jv->type = JV_MAP;
	jv->u.map = dict_new("json", sizeof(struct json_value *), 0, 0, NULL, NULL);
	for (;;) {
		json_skip_blanks(buf);
		assert(buf->len > 0);
		if (*buf->base == '}') {
			buf_adv(buf);
			return jv;
		}

		struct json_value *key = json_parse_value(buf);
		assert(key->type == JV_ATOM);
		json_skip_blanks(buf);
		assert(buf->len > 0);
		assert(*buf->base == '=' || *buf->base == ':');
		buf_adv(buf);
		struct json_value *val = json_parse_value(buf);
		json_map_append(jv, key->u.atom, val);
		json_value_free(key);

		json_skip_blanks(buf);
		assert(buf->len > 0);
		if (*buf->base == ',' || *buf->base == ';') {
			buf_adv(buf);
		}
	}
}

/* Append a value to the list.
 */
void json_list_append(struct json_value *list, struct json_value *jv){
	assert(list->type == JV_LIST);
	list->u.list.vals = realloc(list->u.list.vals,
				(list->u.list.nvals + 1) * sizeof(*list->u.list.vals));
	list->u.list.vals[list->u.list.nvals++] = jv;
}

static struct json_value *json_parse_list(json_buf_t *buf){
	assert(buf->len > 0);
	assert(*buf->base == '[');
	buf_adv(buf);

	struct json_value *jv = new_alloc(struct json_value);
	jv->type = JV_LIST;
	unsigned int index;
	for (index = 0;; index++) {
		json_skip_blanks(buf);
		assert(buf->len > 0);
		if (*buf->base == ']') {
			buf_adv(buf);
			return jv;
		}
		json_list_append(jv, json_parse_value(buf));
		json_skip_blanks(buf);
		assert(buf->len > 0);
		if (*buf->base == ',' || *buf->base == ';') {
			buf_adv(buf);
		}
	}
}

static struct json_value *json_parse_string(json_buf_t *buf){
	assert(buf->len > 0);
	assert(*buf->base == '"' || *buf->base == '\'');
	char delim = *buf->base;
	buf_adv(buf);

	struct json_value *jv = new_alloc(struct json_value);
	jv->type = JV_ATOM;
    jv->u.atom.quoted = true;

	while (buf->len > 0) {
		if (*buf->base == '\\') {
			buf_adv(buf);
			assert(buf->len > 0);
			switch (*buf->base) {
			case 0:
				json_string_add(&jv->u.atom, 0);
				break;
			case '\\':
				json_string_add(&jv->u.atom, '\\');
				break;
			case '\'':
				json_string_add(&jv->u.atom, '\'');
				break;
			case '\"':
				json_string_add(&jv->u.atom, '\"');
				break;
			case '\?':
				json_string_add(&jv->u.atom, '\?');
				break;
			case 'a':
				json_string_add(&jv->u.atom, '\a');
				break;
			case 'b':
				json_string_add(&jv->u.atom, '\b');
				break;
			case 'f':
				json_string_add(&jv->u.atom, '\f');
				break;
			case 'n':
				json_string_add(&jv->u.atom, '\n');
				break;
			case 'r':
				json_string_add(&jv->u.atom, '\r');
				break;
			case 't':
				json_string_add(&jv->u.atom, '\t');
				break;
			case 'v':
				json_string_add(&jv->u.atom, '\v');
				break;
			default:
				json_string_add(&jv->u.atom, *buf->base);
			}
		}
		else if (*buf->base == delim) {
			buf_adv(buf);
			return jv;
		}
		else {
			json_string_add(&jv->u.atom, *buf->base);
		}
		buf_adv(buf);
	}
	assert(0);
	return 0;
}

struct json_value *json_parse_value(json_buf_t *buf){
	json_skip_blanks(buf);
	assert(buf->len > 0);
	switch (*buf->base) {
	case '{':
		return json_parse_struct(buf);
	case '[':
		return json_parse_list(buf);
	case '"': case '\'':
		return json_parse_string(buf);
	default:
		if (!is_atom_char(*buf->base)) {
            int n = buf->len;
            if (n > 100) n = 100;
			fprintf(stderr, "JSON PROBLEM --> '%.*s'\n", n, buf->base);
		}
		assert(is_atom_char(*buf->base));
		struct json_value *jv = new_alloc(struct json_value);
		jv->type = JV_ATOM;
		json_parse_atom(buf, &jv->u.atom);
		return jv;
	}
}

struct json_value *json_string(char *s, unsigned int len){
	struct json_value *jv = new_alloc(struct json_value);
	jv->type = JV_ATOM;
    jv->u.atom.quoted = true;
	jv->u.atom.len = len;
	jv->u.atom.base = malloc(len);
	memcpy(jv->u.atom.base, s, len);
	return jv;
}

static void json_indent(FILE *fp, unsigned int ind){
	while (ind > 0) {
		putc(' ', fp);
		ind--;
	}
}

struct json_dump_map_env {
    FILE *fp;
    unsigned int ind;       // indent
    bool first;
};

static void json_dump_map(void *env, const void *key, unsigned int keylen, void *val){
    struct json_dump_map_env *jdme = env;
    if (jdme->first) {
        jdme->first = false;
    }
    else {
        fprintf(jdme->fp, ",\n");
    }
	json_indent(jdme->fp, jdme->ind);
	fprintf(jdme->fp, "\"%.*s\": ", keylen, (char *) key);
    struct json_value **pjv = val;
	json_dump(*pjv, jdme->fp, jdme->ind + 2);
}

static void json_dump_string(json_buf_t buf, FILE *fp){
	unsigned int i;

    if (buf.quoted) putc('"', fp);
	for (i = 0; i < buf.len; i++) {
		switch (buf.base[i]) {
		case 0:
			fprintf(fp, "\\0");
			break;
		case '"':
			fprintf(fp, "\\\"");
			break;
		default:
			putc(buf.base[i], fp);
		}
	}
	if (buf.quoted) putc('"', fp);
}

void json_dump(struct json_value *jv, FILE *fp, unsigned int ind){
	switch (jv->type) {
	case JV_ATOM:
		json_dump_string(jv->u.atom, fp);
		break;
	case JV_MAP:
		fprintf(fp, "{\n");
        struct json_dump_map_env jdme = { .ind = ind + 2, .fp = fp, .first = true };
		dict_iter(jv->u.map, json_dump_map, &jdme);
		putc('\n', fp); json_indent(fp, ind); fprintf(fp, "}");
		break;
	case JV_LIST:
		fprintf(fp, "[\n");
		for (unsigned int i = 0; i < jv->u.list.nvals; i++) {
            if (i > 0) {
                fprintf(fp, ",\n");
            }
			json_indent(fp, ind + 2);
			json_dump(jv->u.list.vals[i], fp, ind + 4);
		}
		putc('\n', fp); json_indent(fp, ind); fprintf(fp, "]");
		break;
	default:
		assert(0);
	}
}

/* Allocate and get a string out of an atom identified by string key.
 */
char *json_lookup_string(struct dict *map, char *key){
	struct json_value *jv = dict_lookup(map, key, strlen(key));
	if (jv == 0) {
		return 0;
	}
	assert(jv->type == JV_ATOM);
	char *p = malloc(jv->u.atom.len + 1);
	memcpy(p, jv->u.atom.base, jv->u.atom.len);
	p[jv->u.atom.len] = 0;
	return p;
}

/* Find a map inside the map by string key.
 */
struct json_value *json_lookup_map(struct dict *map, char *key){
	struct json_value *jv = dict_lookup(map, key, strlen(key));
	if (jv == 0) {
		return 0;
	}
	assert(jv->type == JV_MAP);
	return jv;
}

/* Find a json_value (can be either a JV_MAP or JV_ATOM) 
 * inside the map by string key.
 */
struct json_value *json_lookup_value(struct dict *map, char *key){
	struct json_value *jv = dict_lookup(map, key, strlen(key));
	if (jv == 0) {
		return 0;
	}
	return jv;
}

char *json_escape(const char *s, unsigned int len){
	struct strbuf sb;

	strbuf_init(&sb);
	while (len > 0) {
		switch (*s) {		// TODO.  More cases
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
		len--;
	}
	return strbuf_getstr(&sb);
}
