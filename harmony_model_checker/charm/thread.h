#ifndef SRC_THREAD_H
#define SRC_THREAD_H

#include <stdbool.h>

#ifdef _WIN32
#ifndef __MINGW32__
#define CHARM_WINDOWS
#endif
#endif

#ifdef _WIN32
#include <windows.h>
#endif

#ifdef CHARM_WINDOWS
typedef HANDLE *mutex_t;

typedef struct {
    CRITICAL_SECTION mutex;
    CONDITION_VARIABLE cond;
    unsigned int threads_required;
    unsigned int threads_left;
    unsigned int cycle;
} barrier_t;

#else // pthreads

#include <pthread.h>
#include <unistd.h>

#ifdef __APPLE__
#include <sys/param.h>
#include <sys/sysctl.h>

typedef int pthread_spinlock_t;

int pthread_spin_init(pthread_spinlock_t *lock, int pshared);
int pthread_spin_lock(pthread_spinlock_t *lock);
int pthread_spin_trylock(pthread_spinlock_t *lock);
int pthread_spin_unlock(pthread_spinlock_t *lock);
#endif // __APPLE__

typedef pthread_mutex_t mutex_t;

typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    unsigned int threads_required;
    unsigned int threads_left;
    unsigned int cycle;
} barrier_t;

#endif

#include <time.h>

void thread_create(void (*f)(void *arg), void *arg);
void mutex_init(mutex_t *mutex);
void mutex_acquire(mutex_t *mutex);
bool mutex_try_acquire(mutex_t *mutex);
void mutex_release(mutex_t *mutex);
void mutex_destroy(mutex_t *mutex);
void barrier_init(barrier_t *barrier, unsigned int count);
void barrier_wait(barrier_t *barrier);
void barrier_destroy(barrier_t *barrier);
unsigned int getNumCores();

#endif // SRC_THREAD_H
