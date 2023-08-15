#ifndef JSON_H
#define JSON_H

// A JSON "atom" is a list of characters which may or may not be quoted.
typedef struct json_buf {
    char *base;
    unsigned int len;
    bool quoted;
} json_buf_t;

// A JSON "value" is either an atom, a map, or a list.
struct json_value { 
	enum { JV_ATOM, JV_MAP, JV_LIST } type;
	union {
		json_buf_t atom;
		struct dict *map;		// maps atoms to json_values
		struct {
			struct json_value **vals;
			unsigned int nvals;
		} list;
	} u;
};

struct json_value *json_parse_value(json_buf_t *buf);
struct json_value *json_string(char *s, unsigned int len);
void json_value_free(struct json_value *jv);
void json_dump(struct json_value *jv, FILE *fp, unsigned int indent);
void json_list_append(struct json_value *list, struct json_value *jv);
void json_map_append(struct json_value *map, json_buf_t key, struct json_value *jv);
char *json_lookup_string(struct dict *map, char *key);
struct json_value *json_lookup_map(struct dict *map, char *key);
struct json_value *json_lookup_value(struct dict *map, char *key);
char *json_escape(const char *s, unsigned int len);

#endif /* JSON_H */
