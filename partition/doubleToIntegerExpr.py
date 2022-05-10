import os
import sys
import re
sys.path.insert(0,'./partition')
import doubleArrayToInteger as dai

#This transform the expression into real coefficient without division operator 
def Realexp_wo_denominator (expr):
	"""
	input:  expr - '1.6x+2.5y<=5' (inequality with real coefficients)
	output: expr - '16x+25y <= 50' (inequality with integer coefficients)
	"""
	length = len(expr)
	L1 = expr
	L2 = []
	unit = ''
	flag = True
	preUnit = ''
	for i in range(length):
		if (L1[i].isdigit() or L1[i] == '.'):
			flag = True
			unit += L1[i]
		else:
			if(isOperator(L1[i])):
				Flag = True
				if(unit == ''):
					L2.append(L1[i])
				else:
					L2.append(unit)
					L2.append(L1[i])
					unit = ''
			else:
				if (flag == True):
					if(i == 0):
						L2.append('1')
						L2.append('*')
					else:
						if(not(L1[i-1] == '*') and not(L1[i-1].isdigit())):
							L2.append('1')
							L2.append('*')
						else:
							L2.append(unit)
					unit = L1[i]
					flag = False
				else:
					unit += L1[i]
	L2.append(unit)
	L3 = []
	for i in range(len(L2)):
		if (contains_digits(L2[i])):
			L3.append(L2[i])
	#print L3
	L4 = dai.real2integer(L3)
	exp = ''
	k = 0
	for i in range(len(L2)):
		if (contains_digits(L2[i])):
			if (i != len(L2)-1):
				if(L4[k] == 1 and not(contains_digits(L2[i+1])) and L2[i+1] != '*'):
					k = k+1
					continue
			exp += str(L4[k])
			k = k +1
		else:
			exp += L2[i]
	return exp

# string contains digit	checking
def contains_digits(d):
	try:
		s = d.split('_')
		digit = re.compile('\d')
		return bool(digit.search(s[0]))
	except SyntaxError:
		print("Error in function contains_digits")				
	
# string is operator	
def isOperator(op):
	try:
		if (op == '+' or op == '-' or op =='(' or op ==')' or op =='*' or op=='>' or op == '<' or op == '=' or op == ' ' or op =='*'):
			return True
		else:
			return False
	except SyntaxError:
		print("Error in function isOperator")


			
				
		

