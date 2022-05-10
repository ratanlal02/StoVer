import sys
import time
import cvxpy as cp
import numpy as np
sys.path.insert(0,'./parser')
import reader as parse


def bmc_encoding(A, Ilmean, Iumean, Ilcovar, Iucovar, Dlmean, Dumean, Dlcovar, Ducovar, K, dim):
	'''
	input:
		A - affine relation
		Ilmean - a list of lower initial mean values
		Iumean - a list of upper initial mean values
		Ilmean - a list of lower unsafe mean values
		Iumean - a list of upper unsafe mean values
		K - bound
		dim - dimension of the system
	'''
	estime = time.time()
	AT = A.transpose()
	Smean = []
	Scovar = []
	Dmean = []
	Dcovar = []
	for i in range(K+1):
		Smean.append(cp.Variable(dim))
		Scovar.append(cp.Variable((dim,dim),PSD=True))
	for i in range(K):
		Dmean.append(cp.Variable(dim))
		Dcovar.append(cp.Variable((dim,dim),PSD=True))
	predicates = []
	#symmetric constraints
	for i in range(K+1):
		predicates +=[Scovar[i] == Scovar[i].T]
	for i in range(K):
		predicates+= [Dcovar[i] == Dcovar[i].T]

	#initial constraints
	predicates += [Smean[0]>=Ilmean, Smean[0]<=Iumean]
	predicates += [Scovar[0]>=Ilcovar, Scovar[0]<=Iucovar]
	
	#unsafe constraints
	#predicates += [Smean[K]>=Ulmean, Smean[K]<=Uumean]
	#predicates += [Scovar[K]>=Ulcovar, Scovar[K]<=Uucovar]
	
	#noise constraints
	for i in range(K):
		predicates += [Dmean[i]>=Dlmean, Dmean[i]<=Dumean]
		predicates += [Dcovar[i]>=Dlcovar, Dcovar[i]<=Ducovar]
	
	# linear relation
	for i in range(K):
		predicates += [Smean[i+1] == (A @ Smean[i]) + Dmean[i]]
		predicates += [Scovar[i+1] == A @ Scovar[i] @ AT + Dcovar[i]]
	eetime = time.time()
	print("encoding time", eetime-estime)
	
	sstime = time.time()
	List_status = []
	numOfVehicle = dim/2
	for i in range(K):
		temp_predicates = predicates
		for j in range(int(numOfVehicle)):
			for k in range(int(numOfVehicle)):
				if (j<k):
					temp_predicates += [cp.norm(Smean[i][2*k:2*k+1]-Smean[i][2*j:2*j+1])<=1]
			
		#semi-definite problems
		prob = cp.Problem(cp.Minimize(0), temp_predicates)
		status = prob.solve()
		if (str(status)=='inf'):
			List_status.append(False)
		else:
			List_status.append(True)
	setime = time.time()
	print("satisfiability time", setime-sstime)
	
	if True in List_status:
		return False
	else:
		return True
	
	
	
		
		
	
		

	


def bmc(FilePath):
	'''
	input:
		FilePath - path of input file
		
	'''
	#Conf = (A (0), mean (1), covar (2), initmean (3), initcovar (4), noisemean (5), noisecovar (6), dim (7), lemean (8), lecovar (9))

	pstime = time.time()
	Conf = parse.input_reader(FilePath)
	dim = Conf[7]
	#linear relation
	A = np.array(Conf[0])

	#initial specfication
	Ilmean = Conf[3][0]
	Iumean = Conf[3][1]
	Ilcovar = []
	Iucovar = []
	j=0
	for i in range(dim):
		Ilcovar.append(Conf[4][0][j:j+dim])
		Iucovar.append(Conf[4][1][j:j+dim])
		j +=dim
	Ilcovar = np.array(Ilcovar)
	Ilcovar = np.array(Iucovar)

	#noise mean
	Dlmean = Conf[5]
	Dumean = Conf[5]
	Dlcovar = Conf[6]
	Ducovar = Conf[6]
	
	# bound
	K = 2
	status = bmc_encoding(A, Ilmean, Iumean, Ilcovar, Iucovar, Dlmean, Dumean, Dlcovar, Ducovar, K, dim)
	petime = time.time()
	print(status)
	print("Total time", petime-pstime) 
	

		

	



if __name__ == "__main__":
    bmc(sys.argv[1])
