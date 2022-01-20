#ifdef WIN32

#include <windows.h>

typedef HANDLE *mutex_t;

typedef struct {
    CRITICAL_SECTION mutex;
    CONDITION_VARIABLE cond
    unsigned int threads_required;
    unsigned int threads_left;
    unsigned int cycle;
} barrier_t;

#else // pthreads

#include <pthread.h>
#include <unistd.h>

#ifndef _SC_NPROCESSORS_ONLN
#include <sys/sysctl.h>
#endif

typedef pthread_mutex_t mutex_t;

typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    unsigned int threads_required;
    unsigned int threads_left;
    unsigned int cycle;
} barrier_t;

#endif

void thread_create(void (*f)(void *arg), void *arg);
void mutex_init(mutex_t *mutex);
void mutex_acquire(mutex_t *mutex);
void mutex_release(mutex_t *mutex);
void mutex_destroy(mutex_t *mutex);
void barrier_init(barrier_t *barrier, unsigned int count);
void barrier_wait(barrier_t *barrier);
void barrier_destroy(barrier_t *barrier);
int getNumCores();
