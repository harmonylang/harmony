#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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
