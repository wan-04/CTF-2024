#include <stdio.h>

int main()
{
    char *a = malloc(0x10);
    memset(a, 0x20, 0);
}