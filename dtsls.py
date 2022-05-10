import sys
import subprocess
import time
sys.path.insert(0,'./parser')
import reader as parse
sys.path.insert(0,'./partition')
import polyhedral as poly
import grid as gp
import partition as ptn

sys.path.insert(0,'./log')
import history as hist

sys.path.insert(0,'./abstraction')
import polyabstraction as pabst 
import hyperabstraction as habst

sys.path.insert(0,'./checker')
import checker as ckr


def variance_partition(I_variance, Pred, dim):
	'''
	input:
		I_variance - list of size 2, where first list of size dim x dim  contains lower bound and second list contains upper bound
		Pred - a list of dim x dim lists
		dim - dimension of the system
	output:
		P_variance = list of polyhedral sets
	'''
	variance_dict = {}
	for i in range(dim*dim):
		variance_dict[i] = 'x'+'_'+str(i)

	L = []
	for pred in Pred:
		exp = ''
		for i in range(dim*dim):
			if pred[i] > 0:
				exp+= str(pred[i])+'*'+variance_dict[i]+'+'
			elif pred[i]< 0:
				exp = exp[:-1]
				exp+= str(pred[i])+'*'+variance_dict[i]+'+'
		if pred[dim*dim]!=0:
			exp = exp+ str(pred[dim*dim])
		else:
			exp = exp[:-1]
		L.append(exp)
	#print "Le for variance", L
	P_variance = ptn.partition(I_variance, L, variance_dict, True)
	return P_variance

	

	


def mean_partition(I_mean, Pred, dim):
	'''
	input: I_mean - list of size 2, where first list of size dim contains lower bound and second list contains upper bound
		Pred - list of linear expression, e.g. ['x_0', 'x_1']
		dim - dimension of the system
	output: 
		P_mean - list of polyhedral sets
	'''
	mean_dict={}
	for i in range(dim):
		mean_dict[i] = 'x'+'_'+str(i)
	L = []
	for pred in Pred:
		exp = ''
		for i in range(dim):
			if pred[i] > 0:
				exp+= str(pred[i])+'*'+mean_dict[i]+'+'
			elif pred[i]< 0:
				exp = exp[:-1]
				exp+= str(pred[i])+'*'+mean_dict[i]+'+'
		if pred[dim]!=0:
			exp = exp+str(pred[dim])
		else:
			exp = exp[:-1]
		L.append(exp)
	P_mean = ptn.partition(I_mean, L, mean_dict, False)
	return P_mean



def dtsls(FilePath):
	'''
	input:
		FilePath - path of input file
		
	'''
	#Conf = (A (0), mean (1), covar (2), initmean (3), initcovar (4), unsafemean (5), unsafecovar (6), noisemean (7), noisecovar (9), dim (9), lemean (10), lecovar (11))

	sTtime = time.time()
	Conf = parse.input_reader(FilePath)
	#dimension of the system
	dim = Conf[7]
	#starting partition time
	sptime = time.time()
	#partitioning
	is_poly = True
	P_mean = []
	P_variance = []
	if is_poly:	
		#Partitioning of mean with respect to a given set of linear expression
		print("Mean partitioning is in process")
		P_mean = mean_partition(Conf[1], Conf[8], dim)
		print("1")
		#Partition of covariance with respect to a given set of linear expression
		print("Variance partitiong is in process")
		P_variance = variance_partition(Conf[2], Conf[9], dim)
		print("2")
	else:
		uniform_size = 2
		manual = True
		P_mean = gp.vector_partition(Conf[1], uniform_size, manual)
		Vl = []
		Vu = []
		j=0
		for i in range(dim):
			Vl.append(Conf[2][0][j:j+dim])
			Vu.append(Conf[2][1][j:j+dim])
			j +=dim
		I_variance = [Vl, Vu]
		manual = True
		P_variance = gp.matrix_partition(I_variance, uniform_size, manual)
	#end partition time
	eptime = time.time()
	#abstraction of discrete time stochastic systems
	noise_node = (Conf[5], Conf[6])
	#starting abstraction time
	satime = time.time()
	print("abstraction is processing")
	if is_poly:
		G, P_dict = pabst.poly_abstraction(P_mean, P_variance, Conf[0], noise_node, dim)
	else:
		G, P_dict = habst.hyper_abstraction(P_mean, P_variance, Conf[0], noise_node, dim)
	eatime = time.time()
	print("3")
	#hist.write_graph(G)
	#safety checking time
	sctime = time.time()
	#initial nodes
	init_node = (Conf[3], Conf[4])
	#unsafe nodes
	#unsafe_node = (Conf[5], Conf[6])
	#check the specification
	print("safety checking is in process")
	result = ckr.check_specification(G, P_dict, init_node, dim)
	ectime = time.time()
	print("4")
	eTtime = time.time()
	print("result is =", result)
	print("abstract node is = ", len(G.nodes()))
	print("abstract edge is = ", len(G.edges()))
	print("partition time is =", eptime-sptime)
	print("abstraction time is =", eatime-satime)
	print("safety checking time is =", ectime-sctime)
	print("Total time is =", eTtime-sTtime)

	

	

if __name__ == "__main__":
    dtsls(sys.argv[1])









	
