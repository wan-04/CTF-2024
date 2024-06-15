#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

long int storage[0x20];
long int sizeS[0x20];
int create()
{
    long long size;
    long long idx;
    long long *buf = NULL;
    printf("Size: ");
    scanf("%lld", &size);
    printf("Index: ");
    scanf("%lld", &idx);
    buf = malloc(size);
    if (buf == NULL)
    {
        printf("Error allocating memory\n");
        return 1;
    }
    storage[idx] = (long int)buf;
    sizeS[idx] = size;
    printf("Buffer: ");
    read(0, buf, size + 0x20);

    return 0;
}

int print_func()
{
    int idx;
    printf("idx: ");
    scanf("%d", &idx);
    puts((char *)storage[idx]);
    return 0;
}
int edit()
{
    int idx;
    printf("idx: ");
    scanf("%d", &idx);
    printf("buf: ");
    read(0, (char *)storage[idx], sizeS[idx] + 0x20);
}
int menu()
{
    int choice = 0;
    puts("---Menu---");
    puts("1. Create");
    puts("2. Print ");
    puts("3. Edit ");
    scanf("%d", &choice);
    return choice;
}

int main()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    while (1)
    {
        switch (menu())
        {
        case 1:
            create();
            break;
        case 2:
            print_func();
            break;
        case 3:
            edit();
            break;
        case 4:
            return 0;
        default:
            break;
        }
    }
}