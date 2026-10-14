#include<stdio.h>
int main()
{
	int i;
	int sum=0;
	
	for(i=1;i<=99;i+=2)
	{
		sum=sum+i;
	}
	printf("100以内的奇数和=%d",sum);
	return 0;
}
