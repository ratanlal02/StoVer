import configparser
import json

def input_reader(filePath):
	"""
	input: filePath - path of input file
	output: 
		A - a matrix for affine relation
		mean - an interval vector of size n
		covar - an interval matrix of size n(n-1)/2 
		initmean - an interval vector of size n
		initcovar - an interval matrix of size n(n-1)/2
		noisemean - a vector of size n
		noisecovar - a covariance matrix of size nxn
	"""
	inifile = configparser.ConfigParser()
	inifile.read(filePath, 'UTF-8')
    
	A = json.loads(inifile.get('settings', 'affine'))
	mean = json.loads(inifile.get('settings', 'mean'))
	covar = json.loads(inifile.get('settings', 'covar'))
	initmean = json.loads(inifile.get('settings', 'initmean'))
	initcovar = json.loads(inifile.get('settings', 'initcovar'))
	noisemean = json.loads(inifile.get('settings', 'noisemean'))
	noisecovar = json.loads(inifile.get('settings', 'noisecovar'))
	dim = json.loads(inifile.get('settings', 'dim'))
	lemean = json.loads(inifile.get('settings', 'lemean'))
	lecovar = json.loads(inifile.get('settings', 'lecovar'))

	return (A, mean, covar, initmean, initcovar, noisemean, noisecovar, dim, lemean, lecovar)
