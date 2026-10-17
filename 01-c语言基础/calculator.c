#include<stdio.h>
int main(){
double n1,n2; char c;  //两个浮定义点数和一个字符变量
printf("请输入你的算式\n"); //获取运算方式
scanf("%lf %c %lf",&n1,&c,&n2);//输入
    if(c=='+'){
	 printf("%f+%f=%f\n",n1,n2,n1+n2);	}//加法 
   
    if (c=='-'){
	printf("%f-%f=%f\n",n1,n2,n1-n2);     }//减法 
    
    if (c=='*'){
    printf("%f*%f=%f\n",n1,n2,n1*n2);      }//乘法 
   
    if (c=='/')                          //除法 
	{
	  if(n2==0){
	  
      printf("分母不能是0！\n");         }
     else if(n1/n2==(int)(n1/n2)){
	  
       printf("结果可以整除！%f/%f=%f\n",n1,n2,n1/n2);   }
       else{
	   
       printf("结果是小数，%f/%f=%.3f\n",n1,n2,(double)n1/n2);   }
	}
      
return 0;
}
