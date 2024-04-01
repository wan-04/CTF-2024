#include <stdio.h>
#include <math.h>
int check(int n)
{
    for (int i = 2; i <= sqrt(n); i++)
    {
        if (n % i == 0)
            return 0;
    }
    return 1;
}

int main()
{
    int n;
    scanf("%d", &n);
    int a[n];
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &a[i]);
    }
    int cnt = 0;
    for (int i = 0; i < n; i++)
    {

        for (int j = i + 1; j < n; j++)
        {
            int res = 0;
            for (int k = i; k < j; k++)
            {
                res += a[k];
            }
            if (check(res) == 1)
                cnt++;
        }
    }
    printf("%d", cnt);
}