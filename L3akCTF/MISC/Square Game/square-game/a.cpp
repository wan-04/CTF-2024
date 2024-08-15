#include <iostream>
#include <vector>

std::vector<std::vector<int>> map(1000000, std::vector<int>(1000000, 0));

bool check(int gx, int gy, int r)
{
    for (int i = gx - r; i < gx + r; i++)
    {
        for (int j = gy - r; j < gy + r; j++)
        {
            if (map[i][j] == 1)
            {
                return true;
            }
            else
                map[i][j] = -1;
        }
    }
    return false;
}

int main()
{
    int hx, hy;
    scanf("%d%d", &hx, &hy);
    map[hx][hy] = 1;

    int gx, gy, r;
    scanf("%d%d%d", &gx, &gy, &r);

    if (check(gx, gy, r) == true)
        printf("YES");
    else
        printf("NO");

    return 0;
}