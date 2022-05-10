#include<iostream>
#include<stdlib.h>
#include<string.h>
#include <sstream> 
#include<ppl.hh>
using namespace std;
namespace PPL = Parma_Polyhedra_Library;


int main()
{
    FILE* fp;
    char  line1[10];
    char  line2[500];
    char  line3[100];
   char  line4[10];
    fp = fopen("poly.txt" , "r");
    fgets(line1, sizeof(line1), fp);
    fgets(line2, sizeof(line2), fp);
    fgets(line3, sizeof(line3), fp);
    fgets(line4, sizeof(line4), fp);
    
    //read line4 
    stringstream geek(line4); 
    int num_cst;
    geek>>num_cst;
    //read line 3
    char *p1 = strtok(line3, ",");	
    //cout<<p1<<endl;
    int E[num_cst]={0};
    int k = 0;
   int l=0;
    while(k< strlen(p1)){
	 if (p1[k]=='E'){
		break;
	}
	else{
		if(p1[k]=='0'){
			E[l] = 0;
			l+=1;
		}
		if(p1[k]=='1'){
			E[l] = 1;
			l+=1;
		}
		k+=1;
	}

    }
    //read line 1
    stringstream geek1(line1); 
    int dim;
    geek1>>dim;
    //read line 2
    char * p = strtok(line2, ",");
   //cout<<dim<<endl;
   PPL::Constraint_System cs;
   int count=0;
   // loop through the string to extract all other tokens
   while( p != NULL ) {
     // printf( " %s\n", p); //printing each token
	//char p[]="-1*x11-2*x12+7";
	int A[dim+1]={0};
	size_t len = strlen(p);
	int i=1;
	int num = 0;
	int NF=1;
	int index=0;
	char S = ' ';
	if (p[0]=='-'){
		S = '-';
	}
	if(p[0]=='x'){
		num=1;
		NF=0;
	}	

	//cout<<num<<endl;
	while (p[i]!='E'){
		//cout<<p[i]<<endl;
		//cout<<index<<endl;
		if (NF==1){
			if (p[i]=='*' || p[i]=='x'){
				NF=0;
				index = 0;
			}
			else{
				num = num*10+ ((int)(p[i])-'0');
			  }	
			
		}
		else{
			if(p[i]=='+' || p[i]=='-'){
				if (S=='-'){
					if (num==0)
						A[index] = -1;
					else
						A[index] = -num;
				}
				else{
					if(num==0)
						A[index] = 1;
					else
						A[index] = num;			
				}
				NF=1;
				S = p[i];
				num = 0;
				index = 0;
			}
			else{
				index = index*10 + ((int)(p[i])-'0');
			}
			
		}
		i+=1;
	}
	//cout<<"complete"<<endl;
	//cout<<index<<endl;
	if (index==0){
		if (S=='-')
			A[dim] = -num;
		else{
			if(num==0)
				A[dim] = 1;
			else
				A[dim] = num;
		}
	}
	else{
		if (S=='-')
			A[index] = -num;
		else{
			if(num==0)
				A[index] = 1;
			else
				A[index] = num;
		}
	}

	PPL::Linear_Expression e;
	for(int j=0; j<dim;j++){
		e+=A[j]*Variable(j);
	}
	e+=A[dim];
	if(E[count]==0)	{
		cs.insert(e>=0);
	}
	else{
		cs.insert(e==0);
	}
	count+=1;
	
	/*
	for(i=0; i<dim+1;i++){
	cout<<A[i]<<" ";
	}
	*/
      p = strtok(NULL, ",");
   }

   NNC_Polyhedron ph(dim);
   ph.add_constraints(cs);
   if(not(ph.is_empty()) && not(ph.affine_dimension()==0)){
	cout<<"True"<<endl;
  }
  else{
	cout<<"False"<<endl;
 }
 fclose(fp); 	

   return 0;
}
