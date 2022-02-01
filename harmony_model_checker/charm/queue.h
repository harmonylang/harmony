#include "stdint.h"

struct queue {
	struct element *first, **last;
	int nelts;
};

void queue_init(struct queue *q);
void queue_insert(struct queue *q, void *item);
void queue_append(struct queue *q, void *, char *file, int line);
unsigned int queue_size(struct queue *q);
void queue_add(struct queue *q, void *);
void queue_add_uint(struct queue *q, uint64_t);
void *queue_get(struct queue *q);
bool queue_tget(struct queue *q, void **item);
bool queue_get_uint(struct queue *q, uint64_t *);
bool queue_empty(struct queue *q);
void queue_release(struct queue *q);
