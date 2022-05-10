import numpy as np
import itertools

def interval_partition(Lower, Upper, m):
	"""
	input:	
		interval - an array of min and max value [min, max]
		n - number of uniform subinterval
	output - a list of intervals
	"""
	Intval_lst = []
	delta = float(Upper-Lower)/m
	temp = Lower
	while temp <= Upper:
		if temp+delta >= Upper:
			Intval_lst.append([temp, Upper])
			break
		else:
			Intval_lst.append([temp, temp+delta])
			temp += delta
	#print(Intval_lst)
	return Intval_lst

def vector_partition(V, m, manual):
	"""
	input:
		V - a list of two arrays (one for lower vector, another for upper vector)
	output:
		IntVec_list - lists of list of two arrays (one for lower vector, another for upper vector)
	"""
	# list of interval vectors in the form of list of lower and upper vectors	
	IntVec_lst = []

	S_list=[]
	n=0
	if manual==True:
		n=2
		V = [[0,2], [2,5]]
		for i in range(2):
			S_list.append(V)
		
	else:
		#lower vector 
		Lower_vec = V[0]
		# upper vector
		Upper_vec = V[1]
		n = len(Lower_vec)
		# list of list of intervals for each dimension
		#S_list = []
		for i in range(n):
			S_list.append(interval_partition(Lower_vec[i], Upper_vec[i], m))

	#cartesian product of all intervals
	for t in itertools.product(*S_list):
		Lower = []
		Upper = []
		for i in range(n):
			Lower.append(t[i][0])
			Upper.append(t[i][1])
		IntVec_lst.append([Lower, Upper])
	return IntVec_lst

def matrix_partition(M, m, manual):
	"""
	input:
		M - list of lower and upper matrix
		m - division at each entries
	"""
	# list of interval matrices via a list of lower and upper matrix
	IntMat_lst = []

	S_list=[]
	n=0
	if manual==True:
		n=2
		V = [[0,2], [2,5]]
		for i in range(2):
			j=i
			while(j<2):
				S_list.append(V)
				j+=1
	else:
		# lower matrix
		Lower_mat = M[0]
		# upper matrix
		Upper_mat = M[1]
		# size of matrix
		n = len(Lower_mat[0])	
		# list of list intervals for each symmetric entries
		#S_list = []
		for i in range(n):
			j = i
			while(j < n):
				S_list.append(interval_partition(Lower_mat[i][j], Upper_mat[i][j], m))
				j+=1

	#cartesian product of all intervals
	for t in itertools.product(*S_list):
		Lower = []
		Upper = []
		s = 0;
		for i in range(n):
			low_vec = []
			up_vec = []	
			for j in range(n):
				if i > j:
					low_vec.append(Lower[j][i])
					up_vec.append(Upper[j][i])
					
				else:
					
					low_vec.append(t[s][0])
					up_vec.append(t[s][1])
					s+=1
				
			Lower.append(low_vec)
			Upper.append(up_vec)
			
		
		IntMat_lst.append([Lower, Upper])

	return IntMat_lst
			
			



'''

L = [[[0,0],[0,0]], [[5,5],[5,5]]]

#result = vector_partition(L, 2)
result = matrix_partition(L, 2)
print(result)
'''
				
	
		


			
			

	
