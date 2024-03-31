#include <stdio.h>

int main()
{
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j <= i; j++)
            if (j == i || j==0 || i == n-1)
                printf("*");
            else
                printf("%d", i+1);
        printf("\n");
    }
}