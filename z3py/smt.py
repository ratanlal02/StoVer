#from z3 import *

def check_constraints(dim, cs):
	'''
	input:
		cs - a list of concstraints
	output:
		result - True/False
	'''	
	f = open("check.py", 'w')
	f.write('from z3 import *\n')
	Var = []
	for i in range(dim):
		f.write('x'+str(i)+'=Real(\'x'+str(i)+'\')\n')
	exp='solve('
	first = 1
	for c in cs:
		if first==1:
			exp+= str(c)
			first = 0
		else:	
			exp+=', '+str(c)
	exp+=')'

	f.write(exp)
	f.close()

'''
dim=2
cs = ['x0 >= 0', '-x0+1>=0', 'x0-2>=0', '-x0+5>=0', 'x1>=0', '-x1+2>=0']

check_constraints(dim,cs)
'''




