#include "head.h"

//
// Created by William Ma on 10/12/21.
//
#include <assert.h>
#include <stdlib.h>

#include "stack.h"

struct stack_t *stack_init(int alloc_len) {
    assert(alloc_len > 0);

    struct stack_t *stack = malloc(sizeof(struct stack_t));
    stack->len = 0;
    stack->alloc_len = alloc_len;
    stack->arr = malloc(stack->alloc_len * sizeof(void *));
    return stack;
}

void stack_deinit(struct stack_t *stack) {
    free(stack->arr);
    free(stack);
}

void stack_push(struct stack_t *stack, void *elem) {
    stack->len++;
    if (stack->len > stack->alloc_len) {
        stack->alloc_len = 2 * stack->len;
        stack->arr = realloc(stack->arr, stack->alloc_len * sizeof(void *));
    }

    stack->arr[stack->len - 1] = elem;
}

void *stack_pop(struct stack_t *stack) {
    assert(stack->len > 0);
    stack->len--;
    return stack->arr[stack->len];
}

int stack_len(struct stack_t *stack) {
    return stack->len;
}
