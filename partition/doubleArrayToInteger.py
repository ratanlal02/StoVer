from fractions import Fraction, gcd
from functools import reduce


#----------------------------------------------------------------------------------------------#
def lcm(numbers):

	""" Get the least common multiple of a list of numbers
		-------------------------------------------------------------------------------
		input: 	numbers		[1,2,6]		list of integers
		output:				6			integer """

	return reduce(lambda x, y: (x*y)/gcd(x,y), numbers, 1)




#----------------------------------------------------------------------------------------------#
def proportional_integer_vector(v):

	""" Computes a proportional vector with integer values from one with rational
	values.
	-------------------------------------------------------------------------------
	input:	v	[Fraction(1, 3), Fraction(1, 2)]	numpy.array
	output:	pv	[2,3]								list of integer """

	#print v
	# Determine the list for numerators and denominators
	numerator_list = []
	denominator_list = []

	for value in v:
		numerator_list.append(value.numerator)
		denominator_list.append(value.denominator)

	# Least common multiple of the denominators
	least_cm = lcm(denominator_list)

	integer_list = [int(least_cm*a/b) for a,b in zip(numerator_list,denominator_list)]

	# Divide every integer by the greatest common divisor to obtain the smallest possible values
	GCD = reduce(gcd,integer_list)
	for i in range(len(integer_list)):
		integer_list[i] = integer_list[i]/GCD

	return integer_list



#----------------------------------------------------------------------------------------------#
def real2integer(real_array):

	""" Given a list of reals it returns a list of integers. """
	#print "real"
	#print real_array
	rational = []
	for value in real_array:
		rational.append(Fraction(value))
	#print 'rational solution =',rational

	integer = proportional_integer_vector(rational)
	#print 'integer solution =',integer

	return integer

