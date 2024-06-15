#include <stdio.h>

int main()
{
    char buf[0x30];
    read(0, buf, 0x7ff);
    printf("%s", buf);
}