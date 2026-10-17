#include<stdio.h>
#include<stdlib.h>
int main()
{
	
	int i=0;
	int sum=0;
	int n=0;
	double average;
	
	printf("请输入你要求平均值的数字个数：\n");//获取个数以便创建动态内存 
	scanf("%d",&n) ;
	int *arr=(int*)malloc(n*sizeof(int));
	if(arr==NULL||n<=0)                       //排除错误的输入并报错 
	{
		printf("请输入正整数\n"); 
		return 1;
	}

	printf("请输入要求平均值的数字（按回车后输入下一个）：\n");     //获取数组 
	for(i=0;i<n;i++)
	{
		scanf("%d",&arr[i]);
		sum=sum+arr[i];                      //通过循环获得sum 
	}
	average=(double)sum/n;                   //double强行转换为浮点数计算平均值 
	printf("平均数为%.2f\n",average);
	free(arr);                              //free清空内存 
	arr=NULL;
	system("pause");
	return 0;

}
