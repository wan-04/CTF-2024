#include <bits/stdc++.h>
using namespace std;

bool check(int n)
{
    if (n < 2)
        return false;
    for (int i = 2; i <= sqrt(n); i++)
    {
        if (n % i == 0)
            return false;
    }
    return true;
}

int main()
{
    vector<int> prime, nonprime;
    int num;
    string line;

    while (getline(cin, line))
    {
        stringstream ss(line);
        int num;
        vector<int> buf;
        while (ss >> num)
        {
            if (check(num))
            {
                prime.push_back(num);
            }
            else
            {
                nonprime.push_back(num);
            }
        }
    }

    for (int i = prime.size() - 1; i >= 0; --i)
    {
        cout << prime[i] << " ";
    }

    cout << endl;

    reverse(nonprime.begin(), nonprime.end());
    for (int i = 0; i < (int)nonprime.size(); ++i)
    {
        cout << nonprime[i] << " ";
    }
}