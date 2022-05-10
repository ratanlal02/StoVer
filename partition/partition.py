import sys
import subprocess
import os
import cvxpy as cp
import numpy as np
from ppl import *
sys.path.insert(0,'./partition')
import polyhedral as poly
import doubleToIntegerExpr as dtie

sys.path.insert(0,'./z3py')
import smt as smt


def construct_poly(H, var_dict):
	'''
	input: 
		H - hyperrectangle
		var_dict - dictionary of variables
	output:
		poly - a polyhedral set corresponds to H
	'''
	#dimension of the system
	dim = len(var_dict)
	instr=''
	for i in range(dim):
		instr = var_dict[i]+'='+'Variable('+str(i)+')'
		exec(instr)
	#transform hyperrectangle to polyhedral set
	Poly = NNC_Polyhedron(dim, 'universe')	
	for i in range(dim):
		expl = var_dict[i]+'>='+str(H[0][i])
		expu = var_dict[i]+'<='+str(H[1][i])
		exp = dtie.Realexp_wo_denominator(expl)
		Poly.add_constraint(eval(exp))
		exp = dtie.Realexp_wo_denominator(expu)
		Poly.add_constraint(eval(exp))

	return Poly

def write_constraints(dim, cs):
	'''
	input:
		cs -a set of polyhedral constraints
		dim - dimension of the constraint system
	output:
		status - True/False

	'''	
	f = open('poly.txt', 'w')
	f.write(str(dim)+'\n')
	exp = ''
	first = 1
	op =''
	for c in cs:
		if c.is_equality():
			exp = str(c).split('==')[0]
			op += '1 '
		else:
			exp = str(c).split('>=')[0]
			op+= '0 '
		if first==1:
			f.write(exp+'E')
			first=0
		else:
			f.write(','+exp+'E')
	f.write('\n')
	op = op[:-1]+'E'
	f.write(op+'\n')
	f.write(str(len(cs)))
	f.close()
			
def is_spsd(Poly, var_dict, flag):
	'''
	input:
		Poly - a polyhedral set
		var_dict - dictionary of variable
		flag - True (need to check whether matrix is sspd)
	'''
	if flag==False:
		return True
	else:
		dim = len(var_dict)/8
		dim = int(dim)
		print(dim)
		A = cp.Variable((dim,dim), PSD=True)
		predicates = [A ==A.T]
		
		for c in Poly.constraints():
			coeff_list = c.coefficients()
			print(coeff_list)
			inhomo_term = c.inhomogeneous_term()
			if c.is_equality():
				predicates+= [sum([coeff_list[dim*i+j]*A[i][j] for i in range(dim) for j in range(dim)])==-inhomo_term]
			else:
				predicates+= [sum([coeff_list[dim*i+j]*A[i][j] for i in range(dim) for j in range(dim)])>=-inhomo_term]

		#semi-definite problems
		prob = cp.Problem(cp.Minimize(0), predicates)
		status = prob.solve()
		#etime= time.time()
		#print etime-stime
		if str(status) == 'inf':
			return False
		else:
			return True
		
		
		


def partition(I, Pred, var_dict, flag):
	'''
	input:
		I - list of interval 
		Pred - a list of linear expression
		dim - dimension of the system
		flag = True (matrix)

	output:
		P - a list of polyhedra for the partition of I with respect to Pred
	'''
	print(I)
	print(Pred)
	print(var_dict)

	#dimension of the system
	dim = len(var_dict)/2
	instr=''
	for i in range(int(dim)):
		instr = var_dict[i]+'='+'Variable('+str(i)+')'
		exec(instr)

	
	#partition
	P = []
	#convert Pred into a set of polyhedral
	LE = poly.get_linearexps(Pred, var_dict)
	E = poly.create_elements(LE, var_dict)
	#polyhedral for an interval I
	I_poly = construct_poly(I, var_dict)
	#print "E"
	#print I_poly.constraints()
	i=0
	for gen_poly in E:
		#print gen_poly.constraints()
		Poly = NNC_Polyhedron(len(var_dict), 'universe')
		Poly.add_constraints(gen_poly.constraints())
		Poly.intersection_assign(I_poly)
		#P = minimize(gen_poly)
		#gen_poly.minimized_constraints()
		cs = Poly.constraints()
		#print cs
		#checking emptiness using z3py
		smt.check_constraints(len(var_dict), cs)
		status = subprocess.run(['python3', 'check.py'], capture_output=True)
		status = str(status.stdout)
		print(status)
		status = status.split('\n')
		#print(status[1])
		print(i)
		i+=1
		if (len(status)!=2):
			if is_spsd(Poly, var_dict, flag):
				P.append(Poly)
				print("Yes")
			#i+=1
		#checking emptyness using ppl in c++
		'''
		write_constraints(dim, cs)
		status = commands.getstatusoutput('./a.out')
		if(status[1]=='True'):
			P.append(gen_poly)
		'''
		#checking emptiness using ppl in python
		'''
		print gen_poly.is_empty()
		if not(gen_poly.is_empty()) and not(gen_poly.affine_dimension()==0):
			P.append(gen_poly)
		'''
	print("Done")
	return P
		
	
	
	
	
		


