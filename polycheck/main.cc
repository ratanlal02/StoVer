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
    char  line1[300];
    char  line2[500];
    fp = fopen("poly.txt" , "r");
    fgets(line1, sizeof(line1), fp);
    fgets(line2, sizeof(line2), fp);
    //cout<<(int)line1<<endl;
    cout<<line2<<endl;
    stringstream geek(line1); 
    int dim;
    geek>>dim;
  cout<<dim<<endl;
    char * token = strtok(line2, " ");
   // loop through the string to extract all other tokens
   while( token != NULL ) {
      printf( " %s\n", token ); //printing each token
      char ch = token[0];
      cout<<ch<<endl;
      token = strtok(NULL, " ");
   }

   PPL::Constraint_System cs;
	
/*
    while (fgets(line, sizeof(line), fp) != NULL)
    {   
        char val1[255];
        char val2[255];
	cout<<line<<endl;
        strcpy(val1, strtok(line, ", "));
	cout<<val1<<endl;
	line = "";
        //strcpy(val2, strtok(NULL, ","));

        //printf("%s|%s\n", val1, val2);          
    }
*/
}
