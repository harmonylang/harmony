#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
    Step 1: read the entire "program" into an array.
        At the end, each element in the array will have
        an "Op" object in it, subclassed into PushOp,
        StoreOp, ReturnOp, etc.

    Step 2: execute the program, starting at program counter 0
        You'll need:
            - a program counter (an integer)
            - a stack (of Value objects, subclassed into IntValue, etc.)
            - a stack pointer, initially pointing to the top of the stack
            - a map of StringValue to Value to hold the variables.
                For example, this maps "x" to 3, say.
                Store operations put something in the map.  Load operations
                take something out of the map.
*/

int main(){
    int stack[100];
    int *sp = &stack[100];

    for (;;) {
        char code[100];
        char arg[100];
        int n = scanf("%s %s", code, arg);
        if (n <= 0)
            break;
        if (strcmp(code, "Push") == 0) {
            *--sp = atoi(arg);
        }
        else if (strcmp(code, "Store") == 0) {
            printf("storing %d into %s\n", *sp++, arg);
        }
        else if (strcmp(code, "Return") == 0) {
            // ignore
        }
    }
    return 0;
}
