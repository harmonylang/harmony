#include <stdio.h>
#include <signal.h>
#include <string.h>

int done = 0;

void handler(int signum){
	done = 1;
}

int main(){
    struct sigaction sa;

    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = handler;
    sa.sa_flags = SA_RESTART; /* Restart syscalls if interrupted */
    sigaction(SIGINT, &sa, NULL);

    while (!done)
        ;
    printf("DONE\n");
    return 0;
}
