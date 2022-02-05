//
// Created by William Ma on 10/12/21.
//

#ifndef SRC_STACK_H
#define SRC_STACK_H

#include <assert.h>
#include <stdlib.h>

struct stack_t {
    void **arr;
    int len;
    int alloc_len;
};

struct stack_t *stack_init(int alloc_len);

void stack_deinit(struct stack_t *stack);

void stack_push(struct stack_t *stack, void *elem);

void *stack_pop(struct stack_t *stack);

int stack_len(struct stack_t *stack);

#endif //SRC_STACK_H
