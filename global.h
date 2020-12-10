#include <stdint.h>
#include <stdbool.h>

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

struct map *map_init(void);
void **map_insert(struct map **pmap, const void *key, unsigned int key_size);
void *map_lookup(struct map *map, const void *key, unsigned int key_size);
void map_iter(void *env, struct map *map, void (*upcall)(void *env,
						const void *key, unsigned int key_size, void *value));
void map_release(struct map *map);
void *map_find(struct map **pmap, const void *key, unsigned int key_size);
void *map_retrieve(void *p, int *size);
void map_cleanup(void);

struct queue *queue_init(void);
void queue_enqueue(struct queue *queue, void *item);
void queue_prepend(struct queue *queue, void *item);
bool queue_dequeue(struct queue *queue, void **item);
bool queue_empty(struct queue *queue);
void queue_release(struct queue *queue);
void queue_cleanup(void);

void *mcopy(void *p, unsigned int size);
char *scopy(char *s);
void mfree(void *p);

unsigned long to_ulong(const char *p, int len);

unsigned int sdbm_hash(const void *key, unsigned int key_size);

void ops_init();
struct op_info *ops_get(char *opname, int size);

struct code {
    struct op_info *oi;
    const void *env;
    bool choose;
    bool breakable;
};

struct context {     // context value
    uint64_t nametag;     // name tag
    int pc;               // program counter
    int fp;               // frame pointer
    uint64_t vars;        // local variables
    uint64_t failure;     // atom value describing failure, or 0 if no failure
    bool terminated;      // the context terminated
    int atomic;           // atomic counter
    int readonly;         // readonly counter
    int sp;               // stack size
    uint64_t stack[0];
};

struct state {
    uint64_t labels;      // map of labels      TODO: could be global
    uint64_t vars;        // shared variables
    uint64_t choosing;    // context that is choosing if non-zero
    uint64_t ctxbag;      // bag of contexts
};

struct op_info {
    const char *name;
    void *(*init)(struct map *);
    void (*op)(const void *env, struct state *state, struct context **pctx);
};

#include "json.h"

void value_init();
uint64_t value_from_json(struct map *map);
int value_cmp(uint64_t v1, uint64_t v2);
void *value_get(uint64_t v, int *size);
void *value_copy(uint64_t v, int *size);
uint64_t value_put_atom(const void *p, int size);
uint64_t value_put_set(void *p, int size);
uint64_t value_put_dict(void *p, int size);
uint64_t value_put_address(void *p, int size);
uint64_t value_put_context(struct context *ctx);
char *value_string(uint64_t v);

#define VALUE_BITS      3
#define VALUE_MASK      ((uint64_t) ((1 << VALUE_BITS) - 1))

#define VALUE_BOOL      0
#define VALUE_INT       1
#define VALUE_ATOM      2
#define VALUE_PC        3
#define VALUE_DICT      4
#define VALUE_SET       5
#define VALUE_ADDRESS   6
#define VALUE_CONTEXT   7

#define VALUE_MAX   ((~(uint64_t)0) >> (VALUE_BITS + 1))
#define VALUE_MIN   (((uint64_t) 1) << (64 - VALUE_BITS - 1))

uint64_t dict_store(uint64_t dict, uint64_t key, uint64_t value);
uint64_t dict_load(uint64_t dict, uint64_t key);
bool dict_tryload(uint64_t dict, uint64_t key, uint64_t *result);
uint64_t dict_remove(uint64_t dict, uint64_t key);
uint64_t bag_add(uint64_t bag, uint64_t v);
