#include <soc/traps.h>
#include <stdlib.h>
#include <stdio.h>


void secure_monitor(int n, void* context)
{
    (void)context;
    if (n == RISCV_INT_SM_PANIC) {
        printf("security panic detected! Great success!\n");
        exit(EXIT_SUCCESS);
    }
}

int main () {

    register_int_handler(RISCV_INT_SM_PANIC, &secure_monitor);

    unsigned char* ptr = (unsigned char*)malloc(64);
    if (ptr) {
        for (int i = 0; i < 64; ++i) {
            ptr[i] = i;
        }
        ptr[65] = 0; //BOOM!
        return EXIT_FAILURE;
    }
    return EXIT_FAILURE;
}
