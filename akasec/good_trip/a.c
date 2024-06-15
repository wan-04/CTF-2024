#include <stdio.h>
#include <sys/mman.h>

int main() {
    int flags = PROT_READ | PROT_WRITE | PROT_EXEC;
    printf("%d", flags);
    return 0;
}