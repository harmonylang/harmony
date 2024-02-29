// Bounded circular concurrent queue used by FUSE
// Each element on the queue is a struct request.
// After a request is processed, result will be put in-place and the request's 
// status will be updated from UNHANDLED to REPLIED.
// After the result is processed, the request's will be updated from REPLIED to
// DONE to be garbaged collected.

#include "fuse_queue.h"
#include <assert.h>

void fuse_queue_init(struct fuse_queue *q)
{
  // mutex_attr is used to make a mutex shared across processes
  pthread_mutexattr_t mutex_attr;
  pthread_mutexattr_init(&mutex_attr);
  pthread_mutexattr_setpshared(&mutex_attr, PTHREAD_PROCESS_SHARED);

  // cond_var_attr is used to make a cond var shared across processes
  pthread_condattr_t cond_var_attr;
  pthread_condattr_init(&cond_var_attr);
  pthread_condattr_setpshared(&cond_var_attr, PTHREAD_PROCESS_SHARED);

  // initialize the queue
  for (int i = 0; i < QUEUE_LEN; i++) {
    q->requests[i].status = EMPTY;
    pthread_mutex_init(&q->requests[i].req_lk, &mutex_attr);
    pthread_cond_init(&q->requests[i].replied_cond, &cond_var_attr);
  }
  q->in = 0;
  q->out = 0;
  q->gc = 0;
  q->size = 0;
  pthread_mutex_init(&q->queue_lk, &mutex_attr);
  pthread_cond_init(&q->not_full_cond, &cond_var_attr);
}

// Allocate a request to be filled by the client
// Request won't be handled by the server until the caller has filled
// the request and called fuse_queue_req_ready()
void fuse_queue_alloc_req(struct fuse_queue *q, struct request **req)
{
  // wait until the queue is not full
  pthread_mutex_lock(&q->queue_lk);
  while (q->size == QUEUE_LEN)
    pthread_cond_wait(&q->not_full_cond, &q->queue_lk);
  
  // allocate a request for the caller
  assert(q->requests[q->in].status == EMPTY);
  *req = &q->requests[q->in];
  q->in = (q->in + 1) % QUEUE_LEN;
  q->size++;
  assert(q->size <= QUEUE_LEN);

  pthread_mutex_unlock(&q->queue_lk);
}

// Called after client has filled the request retured by fuse_queue_alloc_req()
void fuse_queue_req_ready(struct fuse_queue *q, struct request *req)
{
  assert(req->status == EMPTY);
  __asm__ __volatile__ ("" ::: "memory");
  req->status = UNHANDLED;
}

// Called by the server to get a new unhandled request
// This is a NON-BLOCKING call. If no new handled request is available, 
// return -1 and set *req to NULL. Otherwise, return 0 and set *req to point
// to the request. 
int fuse_queue_get_req(struct fuse_queue *q, struct request **req)
{
  pthread_mutex_lock(&q->queue_lk);
  if (q->requests[q->out].status == UNHANDLED) {
    *req = &q->requests[q->out];
    q->out = (q->out + 1) % QUEUE_LEN;
    pthread_mutex_unlock(&q->queue_lk);
    return 0;
  }
  else {
    assert(q->requests[q->out].status == EMPTY);
    *req = NULL;
    pthread_mutex_unlock(&q->queue_lk);
    return -1;
  }
}

// Called after server has written in reply to *req
void fuse_queue_reply_ready(struct request *req)
{
  pthread_mutex_lock(&req->req_lk);
  assert(req->status == UNHANDLED);
  req->status = REPLIED;
  pthread_cond_signal(&req->replied_cond);
  pthread_mutex_unlock(&req->req_lk);
}

// Called by client to block until reply has been written in by the server
void fuse_queue_get_reply(struct fuse_queue *q, struct request *req)
{
  pthread_mutex_lock(&req->req_lk);
  while (req->status != REPLIED)
    pthread_cond_wait(&req->replied_cond, &req->req_lk);
  pthread_mutex_unlock(&req->req_lk);
}

// Called when client has finished processing reply and no longer needs it. 
// *req will then bean cleaned up by the queue
void fuse_queue_reply_done(struct fuse_queue *q, struct request *req)
{
  pthread_mutex_lock(&q->queue_lk);
  req->status = DONE;
  while(q->requests[q->gc].status == DONE) {
    q->requests[q->gc].status = EMPTY;
    q->gc = (q->gc + 1) % QUEUE_LEN;
    assert(q->size > q->size - 1);
    q->size--;
  }
  if (q->size < QUEUE_LEN)
    pthread_cond_broadcast(&q->not_full_cond);
  pthread_mutex_unlock(&q->queue_lk);
}
