from random import randint
import math
import sys


def matrix(n):
	'''
	input:
		n - number of vehicle
		
		A - a square matrix of size 2nx2n
	'''
	A = []
	for i in range(2*n):
		temp = [0.0 for j in range(2*n)];
		print(i)
		if i%2!=0:
			temp[i-1] = 1;
			temp[i] = 1;
		else:
			temp[i] = 1;
			temp[i+1] = 1;
		A.append(temp);
	print(A)			
	return A

def noise_vector(n):
	'''
	input:
		n - number of vehicle
		V - noise mean vector
	'''
	V = [0 for i in range(2*n)]
	return V

def noise_matrix(n):
	'''
	input:
		n - number of vehicle
		
		A - a square matrix of size 2nx2n
	'''
	A = []
	for i in range(2*n):
		temp = [0 for j in range(2*n)]
		temp[i] =1
		A.append(temp)
	return A	


def vector_space(n, L, U, initflag):
	'''
	input:
		n - number of vehicle
		L - lower limit for the space
		U - Upper limit for the space
		
	output:
		List - an interval list of size 2n
	'''
	List = []
	if initflag==True:
		for i in range(n):
			if (i==0):
				List.append([L, L])
				List.append([U, U])
			else:
				List[0].append(L+4*i)
				List[0].append(L+4*i)
				List[1].append(U+4*i)
				List[1].append(U+4*i)
				
	else:
		List.append([L for i in range(2*n)])
		List.append([U for i in range(2*n)])
	return List


def matrix_space(n, L, U):
	'''
	input:
		n - number of vehicles
		L - lower limit for each entry
		U - upper limit for each entry
		
	output:
		L - an interval list of size 2nx2n
	'''
	M = []
	for i in range(2*n):
		temp = [[0, 0] for j in range(2*n)];
		if i%2!=0:
			temp[i-1][0] = L;
			temp[i-1][1] = U;
			temp[i][0] = L;
			temp[i][1] = U;
		else:
			temp[i][0] = L;
			temp[i][1] = U;
			temp[i+1][0] = L;
			temp[i+1][1] = U;
		M.append(temp);		
		
	List = []
	low = []
	high = []
	for i in range(2*n):
		for j in range(2*n):
			low.append(M[i][j][0])
			high.append(M[i][j][1])
	List.append(low)
	List.append(high)
		
	return List
	

def predicate(n, p, C):
	'''
	input:
		n - number of vehicles
		p - number of predicate
	'''
	Le = []
	i=0
	while (i<p):
		P = []
		j = 0
		while(j<n):
			x = randint(-1,1)
			if x==0:
				y = randint(0,1)
				if y==0:
					P.append(1)
				else:
					P.append(-1)
			else:
				P.append(x)
			j+=1
		if P in Le:
			continue
		P.append(randint(0,C))
		i+=1
		Le.append(P)
	return Le

def configure(n, Lmean, Umean, Lcovar, Ucovar, Limean, Uimean, Licovar, Uicovar, Pmean, Pcovar, C):
	'''
	input:
		n - number of vehicles
		Lmean - lower limit for mean space
		Umean - upper limit for mean space
		Lcovar - lower limit for covar space
		Ucovar - upper limit for covar space
		Limean - lower limit for init mean space
		Uimean - upper limit for init mean space
		Licovar - lower limit for init covar space
		Uicovar - upper limit for init covar space
		Pmean - number of predicate for mean		
		Pcovar - number of predicate for covar
		C - range for constant of predicate
	output:
		config.ini - a configuration file

	'''
	#Conf = (A (0), mean space (1), covar space (2), initmean (3), initcovar (4), noisemean (5), noisecovar (6), dim (7), lemean (8), lecovar (9))
	f = open(str(n)+'_'+str(Pmean)+'.ini', 'w')
	f.write('[settings]'+'\n')
	#construct affine matrix
	A = matrix(n)
	f.write('affine = '+str(A)+'\n')

	#mean space
	mean = vector_space(n, Lmean, Umean, False)
	f.write('mean = '+ str(mean)+'\n')
	
	#covar space
	covar = matrix_space(n, Lcovar, Ucovar)
	f.write('covar = '+str(covar)+'\n')

	#init mean space
	initmean = vector_space(n, Limean, Uimean, True)
	f.write('initmean = '+str(initmean)+'\n')

	#init covar space
	initcovar = matrix_space(n, Licovar, Uicovar)
	f.write('initcovar = '+str(initcovar)+'\n')
	
	# noise mean
	noisemean = noise_vector(n)
	f.write('noisemean = '+str(noisemean)+'\n')

	#noise covar
	noisecovar = noise_matrix(n)
	f.write('noisecovar = '+str(noisecovar)+'\n')
	
	#dimension
	f.write('dim = '+str(2*n)+'\n')	

	#predicate for mean
	Lemean = predicate(2*n, Pmean, C)
	f.write('lemean = '+str(Lemean)+'\n')
	#predicate for covar
	Lecovar = predicate((2*n)*(2*n), Pcovar, C)
	f.write('lecovar = '+str(Lecovar)+'\n')
	f.close()
	

	
def create_input(num_Of_Vehicles, num_Of_Pred_Mean, num_Of_Pred_Covar):
	'''

	'''
	##############
	## Space
	##############
	# lower limit for mean space
	Lmean = 0
	# upper limit for mean space
	Umean = 1000
	#lower limit for covar space
	Lcovar = 0
	#upper limit for covar space
	Ucovar = 1000

	##################
	## initial space
	##################
	# lower limit for init mean space
	Limean = 0
	# upper limit for init mean space
	Uimean = 1
	#lower limit for init covar space
	Licovar = 0
	#upper limit for init covar space
	Uicovar = 1
	
	##################
	## parition 
	##################
	#number of predicate for mean
	Pmean = num_Of_Pred_Mean
	#number of predicate for covar
	Pcovar = num_Of_Pred_Covar
	# constants for the predicate
	C = 100
	configure(num_Of_Vehicles, Lmean, Umean, Lcovar, Ucovar, Limean, Uimean, Licovar, Uicovar, Pmean, Pcovar, C)

num_Of_Pred_Mean = 5
num_Of_Pred_Covar = 1
num_Of_Vehicles = 5
create_input(num_Of_Vehicles, num_Of_Pred_Mean, num_Of_Pred_Covar)
 
	


