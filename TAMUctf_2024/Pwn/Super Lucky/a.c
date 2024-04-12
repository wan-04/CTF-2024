#include <stdio.h>

int main()
{
    srand(0);
    for (int i = 0; i < 16; i ++)
        printf("%d,", rand());
    printf("\n");
    for (int i = 0; i < 7; i ++)
        printf("%d,", rand());
}
// 26285,2997,14680,20976,31891,21655,25906,