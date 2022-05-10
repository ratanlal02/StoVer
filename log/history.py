def write_graph(G):
	'''
	input:
		G - networkx graph
	output:
		graph.txt - write node and edge of the graph in graph.txt
	'''
	f = open('./log/graph.txt', 'w')
	f.write("Nodes are :"+str(G.nodes())+'\n')
	f.write("Edges are ")
	for edge in G.edges():
		f.write(str(edge)+'\n')
	f.close()

def write_polydict(P_dict):
	'''
	input: 
		P_dict - a dictionary of polyhedra
	output:
		dict.txt - write dictionary 
	'''
	
	f = open('./log/graph.txt', 'w')
	for t in P_dict.iteritems():
		f.write(str(t)+'\n')
	f.close()

	
		
