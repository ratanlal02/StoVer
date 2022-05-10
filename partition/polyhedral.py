from ppl import *
import time
import sys
import os
import copy
sys.path.insert(0,'./partition')
import doubleToIntegerExpr as dtie
sys.path.insert(0,'./z3py')
import smt as smt

def get_linearexps(strLE,inv_var_dict):

	""" Generates a list of PPL linear expressions from a list of string linear expressions. """

#	Define variables
	for i in inv_var_dict:
		instr = str(inv_var_dict[i]) + ' = Variable(' + str(i) + ')'
		exec(instr)

#	Create each linear_expression
#	general linear expression (to set the space dimension)
	gen_le = ''
	for i in inv_var_dict:
			gen_le = gen_le + '0*' + str(inv_var_dict[i]) + '+'
	gen_le = gen_le[:-1]


	LE=[]
	#print gen_le
	for sle in strLE:
		exp = dtie.Realexp_wo_denominator(sle)
		le = eval(gen_le + '+' + exp)
		LE.append(le)

	return LE


def create_elements(LE, var_dict):
	"""
	input: 
		LE - a list of linear expression
		dim - dimension of the systems

	output:
		E - create a list of partitions 
	"""
	#dimension of the system

	dim = len(var_dict)
	instr=''
	
	for i in range(dim):
		instr = var_dict[i]+'='+'Variable('+str(i)+')'
		exec(instr)


	E =[]
	aux_E = []
	
	is_first = True
	for e in LE:
		if is_first==True:
			pbg = NNC_Polyhedron(dim, 'universe')
			ple = NNC_Polyhedron(dim, 'universe')
			pbg.add_constraint(e>=0)
			ple.add_constraint(e<0)
			E.append(pbg)
			E.append(ple)
			is_first= False
		else:
			aux_E =[]
			for poly in E:
				for i in range(2):
					temp_poly = copy.copy(poly)
					if i==0:
						temp_poly.add_constraint(e>=0)
					else:
						temp_poly.add_constraint(e<0)
					
					if (not(temp_poly.is_empty()) and not(temp_poly.affine_dimension==0)):
						aux_E.append(temp_poly)
			E = copy.copy(aux_E)
	return E	


				

'''
def create_elements(LE):
	"""
	Generate elements of a partition from a list of linear expressions.
	input:	LE	Linear Expressions      list of ppl.Linear_Expressions	
											
	output:	E	Elements                list of ppl.NNC_Polyhedron
	"""
	# Element list
	E = []
	

	# We will check the first linear expression in the input list
	first_le = True
	for le in LE:
		
		# Constraints definition
		#ceq = le == _sage_const_0 					# Equality ppl.constraint
		#cbg = le > _sage_const_0 					# Bigger than zero ppl.constraint
		#csm = le < _sage_const_0 					# Smaller than zero ppl.constraint
		#ceq = le >= 0 					# Equality ppl.constraint
		cbg = le >= 0 					# Bigger than zero ppl.constraint
		csm = le <= 0 					# Smaller than zero ppl.constraint

		
		#print 'ceq=',ceq
		#print 'cbg=',cbg
		#print 'csm=',csm


		# Construct polyhedra with the constraints
		#peq = NNC_Polyhedron(ceq)
		pbg = NNC_Polyhedron(cbg)
		psm = NNC_Polyhedron(csm)
		
		##print 'peq=',peq
		#print 'peq.constraints()=',peq.constraints()
		#print 'pbg=',pbg
		#print 'pbg.constraints()=',pbg.constraints()
		#print 'psm=',psm
		#print 'psm.constraints()=',psm.constraints()

		if first_le == True:

			# Add polyhedra to the element list
			#E.append(peq)
			E.append(pbg)
			E.append(psm)
			#print 'New elements:'
			#print '   peq=',peq.constraints()
			#print '   pbg=',pbg.constraints()
			#print '   psm=',psm.constraints()

			# We will not check the first linear expression anymore
			first_le = False

		else:
			# Duplicate de element list
			aux_E = []
			# SPLIT ELEMENTS
			# Check if the elements are divided by the new linear expression
			for e in E:
				# the element is divided in case intersections with cbg and csm are different from emptiness
				# element intersected with pbg
				new_ebg = NNC_Polyhedron(e)
				#print new_ebg
				#print 'new_ebg=',new_ebg.constraints()
				new_ebg.intersection_assign(pbg)
				#print 'new_ebg after intersection with ',pbg.constraints(),' =',new_ebg.constraints()
                    
				if (new_ebg.is_empty() == False) and (new_ebg != e):
					# element intersected with psm
					new_esm = NNC_Polyhedron(e)
					new_esm.intersection_assign(psm)
                    
					if new_esm.is_empty() == False:
						# in the case the element is divided, this one disappears and three new elements are defined
						#print 'Element ',e.constraints(),' divided.'
						new_eeq = NNC_Polyhedron(e)
						#new_eeq.intersection_assign(peq)
						addebg = True
						for exp in aux_E:
							if new_ebg <= exp:
								addebg= False
								break
						if addebg == True:
							aux_E.append(new_ebg)
						addesm = True
						for exp in aux_E:
							if new_esm <= exp:
								addesm= False
								break
						if addesm == True:
							aux_E.append(new_esm)
						
						#aux_E.append(new_eeq)
						#print 'New elements:'
						#print '   new_ebg=',new_ebg.constraints()
						#print '   new_esm=',new_esm.constraints()
						#print '   new_eeq=',new_eeq.constraints()

				else:
					# the element is not divided
					#print ' Element',e.constraints(), 'not divided.'
					adde = True
					for exp in aux_E:
						if e <= exp:
							adde= False
							break
					if adde==True:
						aux_E.append(e)
			E = aux_E[:]

	return E
'''

def correct_exp(exp):
	#print exp
	preexp=''
	for i in range(len(exp)):
		if i>0 and (exp[i]=='+' or exp[i]=='-' or exp[i]=='>=' or exp[i]=='<=' or exp[i]=='>' or exp[i]=='<' or exp[i]=='=='):
			break
		else:
			preexp+=exp[i]
	exp = '(0 '+preexp+') '+exp[i:]
	#print exp
	return exp



def get_linearexp(filename):
	f = open(filename, 'r')
	contents = f.readlines()
	f.close()
	# M - it is a list of (polyhedra) which is a parition of state space
	M = []
	for i in range(len(contents)):
		line = contents[i].rstrip('\n')
		if (line != ''):
			M.append(line)
	return M
							
	


					

#def create_partition(LE, var_dict):
	
'''
var_dict = {}
var_dict[0] = 'x'
var_dict[1]='y'
L = ['x', 'y', 'x-y']
LE = get_linearexps(L, var_dict)
E = create_elements(LE)
for p in E:
	print(p.constraints())
print E
'''

"""
for e in E:
	print e.constraints()[0]
"""


'''
def create_elements(LE, var_dict):
	"""
	input: 
		LE - a list of linear expression
		dim - dimension of the systems

	output:
		E - create a list of partitions 
	"""
	#dimension of the system

	dim = len(var_dict)
	instr=''
	
	for i in range(dim):
		instr = var_dict[i]+'='+'Variable('+str(i)+')'
		exec(instr)


	E =[]
	
	is_first = True
	for e in LE:
		if is_first==True:
			csbg = Constraint_System()
			csbg.insert(e>=0)		
			csle = Constraint_System()
			csle.insert(e<0)
			E.append(csbg)
			E.append(csle)
			is_first= False
		else:
			aux_E =[]
			for cs in E:
				for i in range(2):
					cs1 = copy.copy(cs)
					if i==0:
						cs1.insert(e>=0)
					else:
						cs1.insert(e<0)	
					smt.check_constraints(dim, cs1)
					status = commands.getstatusoutput('python2 check.py')
					if not(status[1]=='no solution'):
						aux_E.append(cs1)
			E = copy.copy(aux_E)
	M = []
	for cs in E:
		Poly = NNC_Polyhedron(dim, 'universe')
		Poly.add_constraints(cs)
		M.append(Poly)	
	print len(M)
	return M	


'''	

