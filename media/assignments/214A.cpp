#include<bits/stdc++.h>
using namespace std;
void pairs(int x, int y) 
{
int count1 = 0,a,b;

for(a=0;a<=1000;a++)
{
    for(b=0;b<=1000;b++)
    {
        if(a*a+b==x && a+b*b==y)  
        {
            count1++;
        };
     }
}
cout<<count1<<endl;
};
int main(){ 
    int n,m;
    cin>>n>>m;
    pairs(n,m);
return 0;
}