import itertools
import time
import networkx as nx
import cvxpy as cp
import numpy as np
#from multiprocessing import Pool
#import multiprocessing 
def poly_cartesian_product(P_mean, P_variance):
	'''
	input:		
		P_mean - a list mean vectors
		P_variance - a list of variances
	output:
		P - P_mean x P_variance
	'''
	P = []
	P_dict = {}
	i = 0
	for pmean in P_mean:
		for pvariance in P_variance:
			P.append((pmean, pvariance))
			P_dict[i] = (pmean, pvariance)
			i+=1


	return P, P_dict


#replace matrix of variables in a set of constraints for a polyhedral set poly
def poly_add_constraints_for_matrix(predicates, poly, mat_vars, dim):
	'''
	input: constraints - a list of constraints
		P - a list of constraints for a polyhedral set
	output:
		constraints - updated list of constraints
	'''
	for c in poly.constraints():
		coeff_list = c.coefficients()
		inhomo_term = c.inhomogeneous_term()
		if c.is_equality():
			predicates+= [sum([coeff_list[dim*i+j]*mat_vars[i][j] for i in range(dim) for j in range(dim)])==-inhomo_term]
		else:
			predicates+= [sum([coeff_list[dim*i+j]*mat_vars[i][j] for i in range(dim) for j in range(dim)])>=-inhomo_term]
	return predicates

#replace vector of variables in a set of constraints for a polyhedral set poly
def poly_add_constraints_for_vector(predicates, poly, vec_vars, dim):
	'''
	input: constraints - a list of constraints
		P - a list of constraints for a polyhedral set
	output:
		constraints - updated list of constraints
	'''
	
	for c in poly.constraints():
		coeff_list = c.coefficients()
		inhomo_term = c.inhomogeneous_term()
		if c.is_equality():
			predicates+= [sum(coeff_list[i]*vec_vars[i] for i in range(dim))==-inhomo_term]
		else:
			predicates+= [sum(coeff_list[i]*vec_vars[i] for i in range(dim))>=-inhomo_term]
	return predicates


#this is for constraints representation of a polyhedral set
#P_dict, source_node, target_node, A, noise_node, dim
def poly_is_edge(t):
	'''
	input:
		source_node - a pair of polyhedra (pmean, pvariance)
		target_node - a pair of polyhedra	
		A - a matrix of size dim x dim
		noise_node - a pair of mean and variance
		dim - dimension of the system

	output:
		status - True/False
	'''
	#stime = time.time()
	P_dict = t[0]
	source_node = P_dict[t[1]]
	target_node = P_dict[t[2]]
	A = t[3]
	noise_node = t[4]
	dim = t[5]
	print(dim)
	#affine matrix to numpy
	A = np.array(A)
	AT = A.transpose()
	#values of mean vectors and variances
	noise_mean = noise_node[0]
	noise_variance = noise_node[1]
	s_mean = source_node[0]
	s_variance = source_node[1]
	t_mean = source_node[0]
	t_variance = target_node[1]	
	#create variable for mean
	smean_var = cp.Variable(dim)
	tmean_var = cp.Variable(dim)
	svariance_var = cp.Variable((dim,dim), PSD=True)
	tvariance_var = cp.Variable((dim,dim), PSD= True)
	
	#Symmetric constraints for variance
	predicates = [svariance_var==svariance_var.T]
	predicates += [tvariance_var==tvariance_var.T]
	
	#express polyhedral set in terms of mean and variance variables
	predicates = poly_add_constraints_for_vector(predicates, s_mean, smean_var, dim)
	predicates = poly_add_constraints_for_vector(predicates, t_mean, tmean_var, dim)
	predicates = poly_add_constraints_for_matrix(predicates, s_variance, svariance_var, dim)
	predicates = poly_add_constraints_for_matrix(predicates, t_variance, tvariance_var, dim)

	#relation between source and target mean and variances
	predicates += [tmean_var == (A @ smean_var) + noise_mean]
	print(tvariance_var)
	print(svariance_var)
	print(A)
	print(noise_variance)
	predicates += [tvariance_var == A @ svariance_var @ AT + noise_variance]

	#semi-definite problems
	prob = cp.Problem(cp.Minimize(0), predicates)
	status = prob.solve()
	#etime= time.time()
	#print etime-stime
	if str(status) == 'inf':
		return (t[1], t[2], False)
	else:
		return (t[1], t[2], True)




	
def poly_abstraction(P_mean, P_variance, A, noise_node, dim):
	'''
	input: 
		P_mean - partition of mean
		P_variance - partition of variance
		A - a matrix of size dim x dim for affine relation
		noise_node - a pair of mean and variance
		dim - a dimension of the system
		
	output:
		G = (V,E)
		V - a pair of mean and variance partition element
		E - a subset of V x V
	'''
	
	#cartesian product of P_mean and P_variance
	P, P_dict = poly_cartesian_product(P_mean, P_variance)
	 
	#construct the abstract graph
	G = nx.DiGraph()
	G.add_nodes_from([i for i in range(len(P_dict))])
	#print len(G.nodes())
	#i = 0
	Tuple = []
	Total = len(G.nodes())
	i=0
	#print Total
	for source_node in G.nodes():
		for target_node in G.nodes():
			#check the existence of an edge
			print(i,"of",Total*Total)
			i+=1
			Tuple.append((P_dict, source_node, target_node, A, noise_node, dim))
			
			t = (P_dict, source_node, target_node, A, noise_node, dim)
			result = poly_is_edge(t)
			if (result[2]==True):
				#print "True"
				G.add_edge(source_node, target_node)
			
	'''
	#pool = Pool(processes = 4)
	print "length =",len(Tuple)
	pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
	stime = time.time()
	results = pool.map(poly_is_edge, Tuple)
	pool.close()
    	pool.join()
	etime = time.time()
	print "Time is ", etime-stime
	for output in results:
		if output[2]==True:
			G.add_edge(output[0], output[1])
	'''
	
	return G, P_dict
				




