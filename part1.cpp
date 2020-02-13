#include<bits/stdc++.h>
using namespace std;

int A[4];


int main()
{
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	int n;cin>>n;

	int flag = 0;
	float disc = 0.25;

	float A[4]={0.0,0.0,0.0,10.0};
	float B[4]={0.0,0.0,0.0,10.0};
	for (int i=0;i<n;i++)
	{
		for(int j=2;j>0;j--)
		{
			float l = disc*(0.2*B[j+1]+0.8*B[j-1]) -1;
			float r = disc*(0.8*B[j+1]+0.2*B[j-1]) -1;
			// cout<<l<<" "<<r<<"\n";
			A[j]=max(l,r);
		}
		A[0]=max(disc*(0.2*B[1]+0.8*B[0]) - 1,disc*(0.8*B[1]+0.2*B[0]) - 1);
		for(int k=0;k<4;k++)
			{
				cout<<B[k]<<" ";
				B[k]=A[k];
			}
			cout<<"\n";
		flag = 1;
	}



	// while(flag)
	// {
	// 	flag = 0;
	// 	for(int i=0;i<3;++i)	B[i] = A[i];
	// 	for(int j=2;j>-1;--j)
	// 	{
	// 		A[j] = -1 + max()
	// 	}
	// }
	
	return 0;
}