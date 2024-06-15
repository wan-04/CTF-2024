#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
long int storage[0x20];
long int sizeS[0x20];
long int count = 0;
long int win = 0xdeadbeef;
int create()
{
    long long size;
    long long idx;
    long long *buf = NULL;
    printf("Size: ");
    scanf("%lld", &size);
    buf = malloc(size);
    if (buf == NULL)
    {
        printf("Error allocating memory\n");
        return 1;
    }
    storage[count] = (long int)buf;
    sizeS[count++] = size;
    printf("Buffer: ");
    read(0, buf, size);
    return 0;
}

int createPlus()
{
    long long size;
    long long *buf = NULL;
    long long *detail = NULL;
    printf("Size: ");
    scanf("%lld", &size);
    buf = malloc(size);
    if (buf == NULL)
    {
        printf("Error allocating memory\n");
        return 1;
    }
    storage[count] = (long int)buf;
    sizeS[count++] = size;
    printf("Buffer: ");
    read(0, buf, size - 8 + 2);
    printf("Detail: ");
    detail = malloc(size * 2);
    storage[count] = (long int)detail;
    sizeS[count++] = size * 2;
    *((long long *)(buf + (size - 8) / 8)) = (long long)detail;
    read(0, detail, size - 8 + 2);
    count++;

    return 0;
}

int del()
{
    int idx;
    printf("idx: ");
    scanf("%d", &idx);
    free((long int *)storage[idx]);
}
int edit()
{
    int idx;
    printf("idx: ");
    scanf("%d", &idx);
    printf("Buffer: ");
    read(0, (long int *)storage[idx], sizeS[idx]);
}
int editP()
{
    int idx;
    printf("idx: ");
    scanf("%d", &idx);
    char *buf = ((char *)storage[idx] + sizeS[idx] - 8);
    long int a;
    a = *(long int *)buf;
    printf("%llx", a);
    printf("buffer: ");
    read(0, (long int *)a, sizeS[idx]);
}
int menu()
{
    int choice = 0;
    puts("---Menu---");
    puts("1. Create");
    puts("2. Create+ ");
    puts("3. Delete ");
    scanf("%d", &choice);
    return choice;
}
void getShell()
{
    if (win != 0xdeadbeef)
        system("cat flag.txt");
    exit(0);
}

int main()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    printf("win 0x%llx\n", &win);
    while (1)
    {
        switch (menu())
        {
        case 0:
            del();
            break;
        case 1:
            create();
            break;
        case 2:
            createPlus();
            break;
        case 3:
            edit();
            break;
        case 4:
            editP();
            break;
        case 5:
            getShell();
            break;
        default:
            break;
        }
    }
}