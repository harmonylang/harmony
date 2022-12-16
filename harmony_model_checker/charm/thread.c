#include "head.h"

#include <assert.h>
#include "thread.h"

#ifdef __APPLE__

#include <pthread.h>
#include <errno.h>

int pthread_spin_init(pthread_spinlock_t *lock, int pshared) {
    __asm__ __volatile__ ("" ::: "memory");
    *lock = 0;
    return 0;
}

int pthread_spin_destroy(pthread_spinlock_t *lock) {
    return 0;
}

int pthread_spin_lock(pthread_spinlock_t *lock) {
    while (1) {
        int i;
        for (i=0; i < 10000; i++) {
            if (__sync_bool_compare_and_swap(lock, 0, 1)) {
                return 0;
            }
        }
        sched_yield();
    }
}

int pthread_spin_trylock(pthread_spinlock_t *lock) {
    if (__sync_bool_compare_and_swap(lock, 0, 1)) {
        return 0;
    }
    return EBUSY;
}

int pthread_spin_unlock(pthread_spinlock_t *lock) {
    __asm__ __volatile__ ("" ::: "memory");
    *lock = 0;
    return 0;
}

#endif // __APPLE__

#ifdef CHARM_WINDOWS

void thread_create(void (*f)(void *arg), void *arg){
    (void) CreateThread( 
         NULL,         // default security attributes
         0,            // default stack size
         (LPTHREAD_START_ROUTINE) f, arg,
         0,            // default creation flags
         NULL); 	   // receive thread identifier
}

void mutex_init(mutex_t *mutex){
#ifdef WINMUTEX
    *mutex = CreateMutex(NULL, FALSE, NULL);
#else
    *mutex = CreateSemaphore( 
        NULL,    // default security attributes
        1,       // initial count
        1,       // maximum count
        NULL);    // unnamed
#endif
    assert(*mutex != NULL);
}

void mutex_acquire(mutex_t *mutex){
    DWORD r = WaitForSingleObject(*mutex, INFINITE);
    assert(r == WAIT_OBJECT_0);
}

bool mutex_try_acquire(mutex_t *mutex){
    DWORD r = WaitForSingleObject(*mutex, 0);
    return r == WAIT_OBJECT_0;
}

void mutex_release(mutex_t *mutex){
#ifdef WINMUTEX
    ReleaseMutex(*mutex);
#else
    ReleaseSemaphore( 
        *mutex,  // handle to semaphore
        1,       // increase count by one
        NULL);   // previous count return value
#endif
}

void mutex_destroy(mutex_t *mutex){
    CloseHandle(*mutex);
    *mutex = NULL;
}

void barrier_init(barrier_t *barrier, unsigned int count){
    barrier->threads_required = barrier->threads_left = count;
    barrier->cycle = 0;
    InitializeCriticalSection(&barrier->mutex);
    InitializeConditionVariable(&barrier->cond);
}

void barrier_wait(barrier_t *barrier){
    EnterCriticalSection(&barrier->mutex);

    if (--barrier->threads_left == 0) {
        barrier->cycle++;
        barrier->threads_left = barrier->threads_required;
        WakeAllConditionVariable(&barrier->cond);
    }
    else {
        unsigned int cycle = barrier->cycle;
        while (cycle == barrier->cycle)
            SleepConditionVariableCS(&barrier->cond,
                        &barrier->mutex, INFINITE);
    }

    LeaveCriticalSection(&barrier->mutex);
}

void barrier_destroy(barrier_t *barrier){
    DeleteCriticalSection(&barrier->mutex);
}

#else // pthreads

void thread_create(void (*f)(void *arg), void *arg){
    pthread_t tid;
    pthread_create(&tid, NULL, (void *(*)(void *)) f, arg);
}

void mutex_init(mutex_t *mutex){
    pthread_mutex_init(mutex, NULL);
}

void mutex_acquire(mutex_t *mutex){
    pthread_mutex_lock(mutex);
}

bool mutex_try_acquire(mutex_t *mutex){
    return pthread_mutex_trylock(mutex) == 0;
}

void mutex_release(mutex_t *mutex){
    pthread_mutex_unlock(mutex);
}

void mutex_destroy(mutex_t *mutex){
    pthread_mutex_destroy(mutex);
}

void barrier_init(barrier_t *barrier, unsigned int count){
    barrier->threads_required = barrier->threads_left = count;
    barrier->cycle = 0;
    pthread_mutex_init(&barrier->mutex, NULL);
    pthread_cond_init(&barrier->cond, NULL);
}

void barrier_wait(barrier_t *barrier){
    pthread_mutex_lock(&barrier->mutex);

    if (--barrier->threads_left == 0) {
        barrier->cycle++;
        barrier->threads_left = barrier->threads_required;
        pthread_cond_broadcast(&barrier->cond);
    }
    else {
        unsigned int cycle = barrier->cycle;
        while (cycle == barrier->cycle)
            pthread_cond_wait(&barrier->cond, &barrier->mutex);
    }
    pthread_mutex_unlock(&barrier->mutex);
}

void barrier_destroy(barrier_t *barrier){
    pthread_cond_destroy(&barrier->cond);
    pthread_mutex_destroy(&barrier->mutex);
}

#endif

unsigned int getNumCores(){
#ifdef _WIN32
    SYSTEM_INFO sysinfo;
    GetSystemInfo(&sysinfo);
    return (unsigned int) sysinfo.dwNumberOfProcessors;
#elif defined(_SC_NPROCESSORS_ONLN)
    return (unsigned int) sysconf(_SC_NPROCESSORS_ONLN);
#else
    int nm[2];
    size_t len = 4;
    uint32_t count;

    nm[0] = CTL_HW;
    nm[1] = HW_AVAILCPU;
    sysctl(nm, 2, &count, &len, NULL, 0);
    if (count < 1) {
        nm[1] = HW_NCPU;
        sysctl(nm, 2, &count, &len, NULL, 0);
        if (count < 1) {
            count = 1;
        }
    }
    return count;
#endif
}
