#include <stdlib.h>
#include <assert.h>
#include "global.h"

#define MAX_CACHE	5000

static struct q_elt *queue_cache;
static unsigned int queue_csize;

struct q_elt {
	struct q_elt *next;
	void *item;
};

struct queue {
	struct q_elt *first, **last;
};

void queue_enqueue(struct queue *queue, void *item){
	struct q_elt *qe;

	if ((qe = queue_cache) == 0) {
		assert(queue_csize == 0);
		qe = new_alloc(struct q_elt);
	}
	else {
		assert(queue_csize > 0);
		queue_csize--;
		queue_cache = qe->next;
		qe->next = 0;
	}

	qe->item = item;
	*queue->last = qe;
	queue->last = &qe->next;
}

void queue_prepend(struct queue *queue, void *item){
	struct q_elt *qe;

	if ((qe = queue_cache) == 0) {
		assert(queue_csize == 0);
		qe = new_alloc(struct q_elt);
	}
	else {
		assert(queue_csize > 0);
		queue_csize--;
		queue_cache = qe->next;
	}

	qe->item = item;
    if ((qe->next = queue->first) == 0) {
        queue->last = &qe->next;
    }
    queue->first = qe;
}

bool queue_dequeue(struct queue *queue, void **item){
	struct q_elt *qe;

	if ((qe = queue->first) == 0) {
		return false;
	}
	if ((queue->first = qe->next) == 0) {
		queue->last = &queue->first;
	}
	*item = qe->item;

	if (queue_csize >= MAX_CACHE) {
		assert(queue_csize == MAX_CACHE);
		free(qe);
	}
	else {
		qe->next = queue_cache;
		queue_cache = qe;
		queue_csize++;
	}
	return true;
}

bool queue_empty(struct queue *queue){
    return queue->first == 0;
}

struct queue *queue_init(void){
	struct queue *q = new_alloc(struct queue);

	q->last = &q->first;
	return q;
}

void queue_release(struct queue *queue){
	assert(queue->last == &queue->first);
	free(queue);
}

void queue_cleanup(void){
	struct q_elt *qe;

	while ((qe = queue_cache) != 0) {
		assert(queue_csize > 0);
		queue_csize--;
		queue_cache = qe->next;
		free(qe);
	}
	assert(queue_csize == 0);
}
