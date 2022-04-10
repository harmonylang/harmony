#import "head.h"

#include <assert.h>
#include "thread.h"

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
    *mutex = CreateMutex(NULL, FALSE, NULL);
    assert(*mutex != NULL);
}

void mutex_acquire(mutex_t *mutex){
    DWORD r = WaitForSingleObject(*mutex, INFINITE);
    assert(r == WAIT_OBJECT_0);
}

void mutex_release(mutex_t *mutex){
    ReleaseMutex(*mutex);
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

int getNumCores(){
#ifdef _WIN32
    SYSTEM_INFO sysinfo;
    GetSystemInfo(&sysinfo);
    return sysinfo.dwNumberOfProcessors;
#elif defined(_SC_NPROCESSORS_ONLN)
    return sysconf(_SC_NPROCESSORS_ONLN);
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
