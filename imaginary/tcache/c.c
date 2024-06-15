#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main()
{
    unsigned long *ptr[0x10];
    for (int i = 0; i < 14; i++)
    {
        ptr[i] = malloc(0x90);
    }
    malloc(0x10);
    for (int i = 0; i < 14; i++)
    {
        if (i % 2 == 0)
            free(ptr[i]);
    }

    for (int i = 0; i < 14; i++)
    {
        if (i % 2 != 0)
            free(ptr[i]);
    }
    (ptr[13][-1]) = 0xb0;
    free(ptr[13]);

}