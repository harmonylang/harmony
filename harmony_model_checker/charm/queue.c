#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#include "queue.h"

/* An element in a queue.
 */
struct element {
	struct element *next;
	void *item;
};

void queue_init(struct queue *q){
	q->first = 0;
	q->last = &q->first;
	q->nelts = 0;
}

/* Put it on the wrong side of the queue.  I.e., make it the next
 * item to be returned.  Sort of like a stack...
 */
void queue_insert(struct queue *q, void *item){
	struct element *e = calloc(1, sizeof(*e));

	e->item = item;
	if (q->first == 0) {
		q->last = &e->next;
	}
	e->next = q->first;
	q->first = e;
	q->nelts++;
}

void queue_add(struct queue *q, void *item){
	struct element *e = calloc(1, sizeof(*e));

	e->item = item;
	e->next = 0;
	*q->last = e;
	q->last = &e->next;
	q->nelts++;
}

void queue_add_uint(struct queue *q, uint64_t item){
	queue_add(q, (void *) item);
}

void *queue_get(struct queue *q){
	void *item;
	struct element *e;

	if ((e = q->first) == 0) {
		return 0;
	}
	if ((q->first = e->next) == 0) {
		q->last = &q->first;
	}
	item = e->item;
	free(e);
	q->nelts--;
	return item;
}

bool queue_tget(struct queue *q, void **item){
	struct element *e;

	if ((e = q->first) == 0) {
		return false;
	}
	if ((q->first = e->next) == 0) {
		q->last = &q->first;
	}
	*item = e->item;
	free(e);
	q->nelts--;
	return true;
}

bool queue_get_uint(struct queue *q, uint64_t *item){
	void *x;
	bool r = queue_tget(q, &x);
	if (!r) {
		return false;
	}
	*item = (uint64_t) x;
	return true;
}

bool queue_empty(struct queue *q){
	return q->first == 0;
}

unsigned int queue_size(struct queue *q){
	return q->nelts;
}

void queue_release(struct queue *q){
	assert(q->first == 0);
	assert(q->nelts == 0);
}
