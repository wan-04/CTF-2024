#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
long long win = 0xdeadbeef;
long int storage[0x20];
int create()
{
    long long size;
    long long idx;
    long long *buf = NULL;
    printf("Size: ");
    scanf("%lld", &size);
    if (size > 0x480)
        exit(0);
    printf("Index: ");
    scanf("%lld", &idx);
    buf = malloc(size);
    if (buf == NULL)
    {
        printf("Error allocating memory\n");
        return 1;
    }
    storage[idx] = (long int)buf;
    printf("Buffer: ");
    read(0, buf, size);
    return 0;
}

int del()
{
    int idx;
    printf("Index: ");
    scanf("%d", &idx);
    free((char *)storage[idx]);
}

int print_func()
{
    if(win == 0xcafebabe)
    {
        system("/bin/sh");
    }
}
int sCreate()
{
    long long size;
    long long off;
    long long idx;
    char *buf = NULL;

    printf("Size: ");
    scanf("%lld", &size);
    if (size > 0x480)
        exit(0);

    printf("Index: ");
    scanf("%lld", &idx);

    buf = malloc(size);
    if (buf == NULL)
    {
        printf("Error allocating memory\n");
        return 1;
    }

    printf("Offset: ");
    scanf("%lld", &off);

    printf("Buffer: ");
    read(0, buf + off, size - off);

    storage[idx] = (long int)buf;

    return 0;
}

int menu()
{
    int choice = 0;
    puts("---Menu---");
    puts("1. Create");
    puts("2. Print ");
    puts("3. Delete ");
    scanf("%d", &choice);
    return choice;
}

int main()
{
    char *target = NULL;
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    target = malloc(0x18);
    *(long long*)target = (long long)&win;
    while (1)
    {
        switch (menu())
        {
        case 0:
            sCreate();
            break;
        case 1:
            create();
            break;
        case 2:
            print_func();
            break;
        case 3:
            del();
            break;
        case 4:
            return 0;
        default:
            break;
        }
    }
}