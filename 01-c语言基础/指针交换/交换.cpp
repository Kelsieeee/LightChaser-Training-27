#include<stdio.h>
int main()
{
	 int a=114;
	 int b=514;
	 int *p=&a;
	 int *q=&b;
	 int t=*p;
	 
	 printf("原本a的值为%d,b的值为%d.\n",a,b);
	 
	 a=*q;
	 b=t;
	 
	 printf("交换后a的值为%d，b的值为%d.\n",a,b);
	 
	 return 0;
}
