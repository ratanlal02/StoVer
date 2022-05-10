#include<iostream>
#include<stdlib.h>
#include<string.h>
#include <sstream> 
using namespace std;
int main(){
 
char p[]="-1*x11-2*x12+7";
int A[17]={0};
size_t len = strlen(p);
int i=1;
int num = 0;
int NF=1;
int index=0;
char S = ' ';
if (p[0]=='-'){
	S = '-';
}
else{
	num = (int)p[0] - '0';
}
cout<<num<<endl;
while (i< len){
	if (NF==1){
		if (p[i]=='*'){
			NF=0;
			index = 0;
		}
		else{
			num = num*10+ ((int)(p[i])-'0');
		  }	
		i+=1;
	}
	else{
		if(p[i]=='+' || p[i]=='-'){
			if (S=='-'){
				A[index] = -num;
			}
			else{
				A[index] = num;			
			}
			NF=1;
			S = p[i];
			num = 0;
			index = 0;
		}
		else{
			if (p[i]!='x'){
				index = index*10 + ((int)(p[i])-'0');
			}
		}
		i+=1;
	}
}

if (index==0){
	if (S=='-')
		A[16] = -num;
	else
		A[16] = num;
}
else{
	if (S=='-')
		A[index] = -num;
	else
		A[index] = num;
}
for(i=0; i<17;i++){
	cout<<A[i]<<" ";
}

return 0;
}
