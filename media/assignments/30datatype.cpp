#include<bits/stdc++.h>
using namespace std;
int main(){ 
int a;
double v;
string s;
cin>>a;
cin>>v;
cin.ignore();
getline(cin, s);
cout<<a+4<<endl;
cout.precision(2);
cout<<fixed<<setprecision(1)<<v+4.0<<endl;
cout<<"HackerRank "<<s<<endl;


return 0;
}