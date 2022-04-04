#ifndef VECTOR_H
#define VECTOR_H

// A simple vector implementation

struct int_vector {
    int* v;
    int len;
    int capacity;
};

struct int_vector int_vector_init(int);

void int_vector_push(struct int_vector*, int);

int int_vector_get(struct int_vector*, int);

#endif
