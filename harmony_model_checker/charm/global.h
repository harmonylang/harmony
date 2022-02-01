#ifndef SRC_GLOBAL_H
#define SRC_GLOBAL_H

#include <stdint.h>
#include <stdbool.h>

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

#define CALLTYPE_PROCESS       1
#define CALLTYPE_NORMAL        2
#define CALLTYPE_INTERRUPT     3

//void *mcopy(void *p, unsigned int size);
//char *scopy(char *s);
//void mfree(void *p);

#define PRI_HVAL            PRIx64
typedef uint64_t            hvalue_t;

void panic(char *s);
unsigned long to_ulong(const char *p, int len);
double gettime();

#define CHUNKSIZE   (1 << 12)

#endif // SRC_GLOBAL_H
