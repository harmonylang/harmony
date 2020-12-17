#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>
#include "global.h"
#include "json.h"

#define buf_adv(b)		do { assert((b)->len > 0); (b)->base++; (b)->len--; } while (false)

static void json_map_cleanup(void *env, const void *key, unsigned int keylen, void *val){
	json_value_free(val);
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
			int i;

			for (i = 0; i < jv->u.list.nvals; i++) {
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
	void **p = dict_insert(map->u.map, key.base, key.len);
	if (*p != 0) {
		fprintf(stderr, "json_map_append: duplicate key: '%.*s'\n",
							(int) key.len, key.base);
	}
	assert(*p == 0);
	*p = jv;
}

static struct json_value *json_parse_struct(json_buf_t *buf){
	assert(buf->len > 0);
	assert(*buf->base == '{');
	buf_adv(buf);

	struct json_value *jv = new_alloc(struct json_value);
	jv->type = JV_MAP;
	jv->u.map = dict_new(0);
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
			case 'e':
				json_string_add(&jv->u.atom, '\e');
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
			fprintf(stderr, "--> '%.*s'\n", (int) buf->len, buf->base);
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
	jv->u.atom.len = len;
	jv->u.atom.base = malloc(len);
	memcpy(jv->u.atom.base, s, len);
	return jv;
}

static void json_indent(unsigned int ind){
	while (ind > 0) {
		putchar(' ');
		ind--;
	}
}

static void json_dump_ind(struct json_value *jv, unsigned int ind);

static void json_dump_map(void *env, const void *key, unsigned int keylen, void *val){
	unsigned int ind = (size_t) env;
	json_indent(ind);
	printf("%.*s: ", keylen, (char *) key);
	json_dump_ind(val, ind + 2);
}

static void json_dump_string(json_buf_t buf){
	int i;

	/* See if we should quote it.
	 */
	for (i = 0; i < buf.len; i++) {
		if (!is_atom_char(buf.base[i])) {
			break;
		}
	}
	if (i == buf.len) {
		printf("%.*s\n", (int) buf.len, buf.base);
		return;
	}

	putchar('"');
	for (i = 0; i < buf.len; i++) {
		switch (buf.base[i]) {
		case 0:
			printf("\\0");
			break;
		case '"':
			printf("\\\"");
			break;
		default:
			putchar(buf.base[i]);
		}
	}
	printf("\"\n");
}

static void json_dump_ind(struct json_value *jv, unsigned int ind){
	switch (jv->type) {
	case JV_ATOM:
		json_dump_string(jv->u.atom);
		break;
	case JV_MAP:
		printf("{\n");
		dict_iter(jv->u.map, json_dump_map, (void *) (size_t) (ind + 2));
		json_indent(ind); printf("}\n");
		break;
	case JV_LIST:
		printf("[\n");
		int i;
		for (i = 0; i < jv->u.list.nvals; i++) {
			json_indent(ind + 2);
			json_dump_ind(jv->u.list.vals[i], ind + 4);
		}
		json_indent(ind); printf("]\n");
		break;
	default:
		assert(0);
	}
}

void json_dump(struct json_value *jv){
	json_dump_ind(jv, 0);
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
