import sys
from ppl import *
sys.path.insert(0,'./partition')
import partition as ptn
import multiprocessing
import networkx as nx
import subprocess

sys.path.insert(0,'./z3py')
import smt as smt


def is_intersectwith_node(vertex, node, inode, mean_dict, variance_dict):
	'''
	input:
		node - a pair of polyhedra
		inode - a pair of hyperrectangles
		mean_dict - dictionary of mean variables
		variance_dict - dictionary of variance variables
	'''
	result = []
	#poly_mean = NNC_Polyhedron(len(mean_dict), 'universe')
	#poly_variance = NNC_Polyhedron(len(variance_dict), 'universe')
	if type(node[0])==NNC_Polyhedron:
		poly_mean = node[0]
	else:
		poly_mean = ptn.construct_poly(node[0], mean_dict)
	
	if type(node[1])==NNC_Polyhedron:
		poly_variance = node[1]
	else:
		Vl = [node[1][0][i][j] for i in range(len(node[1][0])) for j in range(len(node[1][0]))]
		Vu = [node[1][1][i][j] for i in range(len(node[1][1])) for j in range(len(node[1][1]))]
		poly_variance = ptn.construct_poly([Vl, Vu], variance_dict)

	#cehcking whether intersection is empty for initial polyhedral set
	i_mean = inode[0]
	i_variance = inode[1]
	imean_poly = ptn.construct_poly(i_mean, mean_dict)
	ivariance_poly = ptn.construct_poly(i_variance, variance_dict)
	#print imean_poly.constraints()
	#print ivariance_poly.constraints()
	#print poly_mean.constraints()
	#print poly_variance.constraints()
	M_poly = NNC_Polyhedron(len(mean_dict), 'universe')
	M_poly.add_constraints(imean_poly.constraints())
	M_poly.add_constraints(poly_mean.constraints())
	V_poly = NNC_Polyhedron(len(variance_dict), 'universe')
	V_poly.add_constraints(ivariance_poly.constraints())
	V_poly.add_constraints(poly_variance.constraints())
	
	#imean_poly.intersection_assign(poly_mean)
	#ivariance_poly.intersection_assign(poly_variance)
	#using z3py python
	cs1 = M_poly.constraints()
	cs2 = V_poly.constraints()
	#print cs1
	#print cs2
	smt.check_constraints(len(mean_dict), cs1)
	status1 = subprocess.run(["python3", "check.py"], stdout=subprocess.PIPE, text=True)
	status1 = status1.stdout.strip("\n")
	smt.check_constraints(len(variance_dict), cs2)
	status2 = subprocess.run(["python3", "check.py"], stdout=subprocess.PIPE, text=True)
	status2 = status2.stdout.strip("\n")
	#print status1
	#print status2
	if(status1!='no solution' and status2!='no solution'):
		result.append((vertex, True))
		#print "True"
	else:
		result.append((vertex, False))

	
	#use c++ version of ppl 
	'''
	cs = imean_poly.constraints()
	ptn.write_constraints(len(mean_dict), cs)
	status1 = commands.getstatusoutput('./a.out')
	cs1 = ivariance_poly.constraints()
	ptn.write_constraints(len(variance_dict), cs1)
	status2 = commands.getstatusoutput('./a.out')

	if(status1[1]=='True' and status2[1]=='True'):
		result.append((vertex, True))
	else:
		result.append((vertex, False))
	'''
	#using ppl in python		
	'''
	if not(imean_poly.is_empty()) and not(ivariance_poly.is_empty()):
		result.append((vertex, True))
	else:
		result.append((vertex, False))
	'''
	
	#cehcking whether intersection is empty for unsafe polyhedral set
	
	#u_mean = unode[0]
	#u_variance = unode[1]
	#umean_poly = ptn.construct_poly(u_mean, mean_dict)
	#uvariance_poly = ptn.construct_poly(u_variance, variance_dict)
	instr = ''
	for i in range(len(mean_dict)):
		instr = mean_dict[i]+'='+'Variable('+str(i)+')'
		exec(instr)
	M_poly = NNC_Polyhedron(len(mean_dict), 'universe')
	#M_poly.add_constraints(umean_poly.constraints())
	M_poly.add_constraints(poly_mean.constraints())
	V_poly = NNC_Polyhedron(len(variance_dict), 'universe')
	#V_poly.add_constraints(uvariance_poly.constraints())
	V_poly.add_constraints(poly_variance.constraints())
	#umean_poly.intersection_assign(poly_mean)
	#uvariance_poly.intersection_assign(poly_variance)
	# use z3py python
	# add constraints for the unsafe specifications
	numOfVehicle = len(mean_dict)/2
	
	
	print(M_poly.constraints())
	for i in range(int(numOfVehicle)):
		for j in range(int(numOfVehicle)):
			if (i<j):
				M_poly.add_constraint(eval(mean_dict[2*j])-eval(mean_dict[2*i])>=2)
				M_poly.add_constraint(eval(mean_dict[2*j+1])-eval(mean_dict[2*i+1])>=2)
	
	cs1 = M_poly.constraints()
	cs2 = V_poly.constraints()
	
	
	smt.check_constraints(len(mean_dict), cs1)
	status1 = subprocess.run(["python3", "check.py"], stdout=subprocess.PIPE, text=True)
	status1 = status1.stdout.strip("\n")
	smt.check_constraints(len(variance_dict), cs2)
	status2 = subprocess.run(["python3", "check.py"], stdout=subprocess.PIPE, text=True)
	status2 = status2.stdout.strip("\n")
	if(status1!='no solution' and status2!='no solution'):
		result.append((vertex, True))
	else:
		result.append((vertex, False))
	
	#use c++ version of ppl 
	'''
	cs = umean_poly.constraints()
	ptn.write_constraints(len(mean_dict), cs)
	status1 = commands.getstatusoutput('./a.out')
	cs1 = uvariance_poly.constraints()
	ptn.write_constraints(len(variance_dict), cs1)
	status2 = commands.getstatusoutput('./a.out')

	if(status1[1]=='True' and status2[1]=='True'):
		result.append((vertex, True))
	else:
		result.append((vertex, False))
	'''
	#using ppl version of python	
	'''
	if not(umean_poly.is_empty()) and not(umean_poly.affine_dimension()==0):
		if not(uvariance_poly.is_empty()) and not(uvariance_poly.affine_dimension()==0):
			result.append((vertex, True))
		else:
			result.append((vertex, False))
	else:
		result.append((vertex, False))	
	'''

	return result

def is_reach(G, init_lst, unsafe_lst):
	'''
	input:
		G - a networkx graph
		init_lst - a list of initial nodes
		unsafe_lst - a list of unsafe nodes
	'''
	#print G.edges()
	#print G.nodes()
	for inode in init_lst:
		Rs = nx.descendants(G, inode)
		Rs.add(inode)
		if (Rs & set(unsafe_lst)):
			return True	
	return False

	
	
		



def check_specification(G, P_dict, init_node, dim):
	'''
	input: 
		G - abstract graph
		I - a pair of polyhedra 
		F - a pair of polyhedra
	'''
	mean_dict={}
	for i in range(dim):
		mean_dict[i] = 'x'+'_'+str(i)

	variance_dict = {}
	for i in range(dim*dim):
		variance_dict[i] = 'x'+'_'+str(i)
	#identify abstract initial nodes
	init_lst=[]
	unsafe_lst = []
	for node in G.nodes():
		result = is_intersectwith_node(node, P_dict[node], init_node, mean_dict, variance_dict)
		if result[0][1]==True:
			init_lst.append(result[0][0])
		if result[1][1]==True:
			unsafe_lst.append(result[1][0])

	print(init_lst)
	print(unsafe_lst)
	status = is_reach(G, init_lst, unsafe_lst)
	if status==True:
		return "Unknown"
	else:
		return "True"
	
	
	
		
	


	
		
