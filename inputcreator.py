import sys
import os
import networkx as nx
import numpy as np
import random
from networkx.algorithms import approximation, shortest_paths, tree, traversal

kingdom_names = []


#takes in a graph and edge between u and v with weight x
def edgeAdder(G, u, v, x):
	G.add_edge(u, v, weight= x)

#adding a node called,u , with conquesting cost, v
def nodeAdder(G, u, v):
	G.add_node(u, conquesting_cost = v)


def adjaceny_matrix_creator(G):
	return (nx.to_numpy_matrix(G)).tolist()

# def addxtoAL(AL, list_of_edges):
# 	for x in list_of_edges:
# 		start, end = x
# 		print(AL[start][end])
# 		AL[start][end] =  AL[start][end] - 10000
# 		AL[end][start] =  AL[end][start] - 10000

# 	for y in AL:
# 		for p in y:
# 			if AL[y][p] == 0:
# 				AL[y][p] = 'x'

# 	for x in list_of_edges:
# 		start, end = x
# 		AL[start][end] += 10000
# 		AL[end][start] += 10000

#adding x's
def ALcreator(G):
	AL = (nx.to_numpy_matrix(G)).tolist()
	print(AL)

	list_of_data = G.nodes.data("conquesting_cost")

	for n in G:
		AL[n][n] = list_of_data[n]

	for x in range(len(AL)):
		for y in range(len(AL)):
			if AL[x][y] == 0:
				AL[x][y] = 'x'

	return AL

#takes in a graph and writes it to a file
def write_to_file(G):
	f = ''
	if nx.number_of_nodes(G) == 50:
		f = open("50.in", "w")
	elif nx.number_of_nodes(G) == 100:
		f = open("100.in", "w")
	elif nx.number_of_nodes(G) == 200:
		f = open("200.in", "w")
	else:
		f = open("temp.in", "w")

	adjacency_list_formatted =  []
	temp = ALcreator(G)
	print(temp)
	f.write('' + str(nx.number_of_nodes(G)) + '' + '\n')
	for x in G.nodes:
		f.write('' + str(x) + ' ')

	f.write('\n')
	f.write('0' + '\n')
	for x in range(len(temp)):
		for y in range(len(temp)):
			f.write('' + str(temp[x][y]) + ' ')
		f.write('\n')
	# for item in f:

	return temp

def read_to_array(file_input):
	global kingdom_names
	checkpoints_from_file = [] 
	with open(file_input, "r") as f:
		lines = f.readlines()
		count = 0
		for line in lines:
			new_line = line.replace("Â", '')
			if count == 1: 
				kingdom_names.append([str(x) for x in new_line.strip().split()])
			if count >= 3:
				temp = [str(x) for x in new_line.strip().split()]
				checkpoints_from_file.append(temp)
			count += 1
	return checkpoints_from_file


#takes in numbers n,k and creates a random graph with n vertices and k edges. Returns graph G
def graphGenerator(n, k):
	G = nx.Graph()
	for i in np.arange(n):
		r = random.randint(10, 100) #conquesting cost
		nodeAdder(G, i, r)

	for j in np.arange(k):
		v = random.randint(0, n - 1)
		u = random.randint(0, n - 1)
		r = random.randint(10, 100) #edge cost
		if u != v:
			edgeAdder(G, u, v, r)

	AL = nx.to_numpy_matrix(G)
	return G

#takes in a graph G and numbers n,k and creates a random graph around G with n vertices and k edges. Returns new graph H
def existingGraphGenerator(G, n, k):
	H = G
	remaining_nodes = n - nx.number_of_nodes(G)
	remaining_edges = k - nx.number_of_edges(G)
	
	if remaining_nodes <= 0 or remaining_edges <= 0:
		return H

	for i in np.arange(remaining_nodes):
		p = i + nx.number_of_nodes(G)
		r = random.randint(10, 100) #conquesting cost
		nodeAdder(H, p, r)

	for j in np.arange(remaining_edges):
		v = random.randint(0, n - 1)
		u = random.randint(0, n - 1)
		r = random.randint(10, 100) #edge cost
		if u != v:
			edgeAdder(H, u, v, r)

	AL = nx.to_numpy_matrix(G)
	return H

def graphWithAPathGenerator(n, k):
	G = nx.Graph()
	for i in np.arange(n):
		if nx.number_of_nodes(G) == 0:
			r = random.randint(10, 20) #conquesting cost
			nodeAdder(G, i, r)
		else:
			r = random.randint(10, 20) #conquesting cost
			nodeAdder(G, i, r)
			q = random.randint(50, 75) #edge cost
			edgeAdder(G, i-1, i, q)
	random_weight = random.randint(50, 75)
	edgeAdder(G, 0, n - 1, q)
	
	remaining_edges = k - nx.number_of_edges(G)

	for i in np.arange(remaining_edges):
		r = random.randint(76, 100) #random edge cost that is strictly greater than the edge costs in the path
		u = random.randint(0, n - 1) #random vertex in G
		v = random.randint(0, n - 1) #random vertex in G
		if u != v:
			edgeAdder(G, u, v, r)

	return G

def generateComplicatedPathGraph(n, k):
	G = nx.Graph()
	nodeAdder(G, 0, 20)
	nodeAdder(G, 1, 5)
	nodeAdder(G, 2, 30)
	nodeAdder(G, 3, 30)
	nodeAdder(G, 4, 30)
	edgeAdder(G, 0, 1, 65)
	edgeAdder(G, 0, 3, 50)
	edgeAdder(G, 1, 3, 55)
	edgeAdder(G, 1, 2, 55)
	edgeAdder(G, 1, 4, 55)
	edgeAdder(G, 2, 3, 55)
	edgeAdder(G, 3, 4, 55)

	nodeAdder(G, 5, random.randint(10, 20))
	edgeAdder(G, 1, 5, random.randint(50, 75))
	
	current_nodes = nx.number_of_nodes(G)
	remaining_nodes = n - nx.number_of_nodes(G)

	for i in np.arange(remaining_nodes):
		j = i + current_nodes
		r = random.randint(10, 20) #conquesting cost
		nodeAdder(G, j, r)
		q = random.randint(50, 75) #edge cost
		edgeAdder(G, j-1, j, q)
	
	random_weight = random.randint(50, 75)
	edgeAdder(G, 0, n - 1, q)
	
	remaining_edges = k - nx.number_of_edges(G)

	for i in np.arange(remaining_edges):
		r = random.randint(76, 100) #random edge cost that is strictly greater than the edge costs in the path
		u = random.randint(0, n - 1) #random vertex in G
		v = random.randint(0, n - 1) #random vertex in G
		if u != v:
			if G.has_edge(u, v) == False:
				edgeAdder(G, u, v, r)


	return G

def test(G):
	for edge in G.edges():
		print(edge)

def minimum_dominating_solver(G, start):
	dom_set = approximation.dominating_set.min_weighted_dominating_set(G, 'conquesting_cost') # finds minimum weighted dominating set
	if len(dom_set) == 1 and start in dom_set:
		return dom_set, [start]
	floyd_warshall = dict(shortest_paths.weighted.all_pairs_dijkstra_path(G))
	floyd_warshall_lengths = dict(shortest_paths.weighted.all_pairs_dijkstra_path_length(G))
	G_prime = nx.Graph()
	nodeAdder(G_prime, start, G.node[start]['conquesting_cost'])
	for node in dom_set:
		nodeAdder(G_prime, node, G.node[node]['conquesting_cost'])
		start_to_node_path_weight = floyd_warshall_lengths[start][node]
		edgeAdder(G_prime, start, node, start_to_node_path_weight)
		for each in dom_set:
			if each != node:
				if not G.has_edge(node, each):
					edge_weight = floyd_warshall_lengths[node][each]
					edgeAdder(G_prime, node, each, edge_weight)
	mst_G_prime = tree.mst.minimum_spanning_tree(G_prime, weight='weight')
	dfs_on_graph = traversal.depth_first_search.dfs_edges(mst_G_prime, source=start)
	bad_tour = []
	for each in dfs_on_graph:
		bad_tour.append(floyd_warshall[each[0]][each[1]])
	prev = None
	tour = []
	for path in bad_tour:
		if prev != None:
			if path[0] != prev[len(prev) - 1]:
				tour.append(floyd_warshall[prev[len(prev) - 1]][path[0]])
		tour.append(path)
		prev = path
	tour.append(floyd_warshall[prev[len(prev) - 1]][start])
	FINAL_TOUR = []
	counter = 0
	for path in tour:
		for node in path:
			if counter != 0:
				if node != FINAL_TOUR[counter - 1]:
					FINAL_TOUR.append(node)
					counter += 1
			else:
				FINAL_TOUR.append(node)
				counter += 1
	# last = None	
	# for num in range(len(FINAL_TOUR)):

	# 	if num == 0:
	# 		pass
	# 	if not G.has_edge(FINAL_TOUR[num], FINAL_TOUR[num-1]):
	# 		print(FINAL_TOUR[num-1], FINAL_TOUR[num], "are not connected")

		# if last == None:
		# 	last = check
		# else:
		# 	if not G.has_edge(last, check):
		# 		print(last, check, "are not connected")
		# 		last = check

	return dom_set, FINAL_TOUR


def find_weight(G, path): # Takes in a graph and path. Returns the weight of the path.
	path_weight = 0
	prev = None
	for node in path: 
		if prev != None: # first node in path
			path_weight += G[prev][node]['weight']
		prev = node
	return path_weight

def outputwriter(G, string, file_input):
	# if nx.number_of_nodes(G) == 50:
	# 	f = open("50.out", "w")
	# elif nx.number_of_nodes(G) == 100:
	# 	f = open("100.out", "w")
	# elif nx.number_of_nodes(G) == 200:
	# 	f = open("200.out", "w")
	# else:
	# 	f = open("temp.out", "w")
	print(kingdom_names)
	input_directory = os.path.normpath("C:/Users/nicol/cs170/Project/new-project-starter-code/inputs")
	start_string = ''
	count = 0
	for subdir, dirs, files in os.walk(input_directory):
		for file in files:
			# completeName = os.path.join(output_directory, file[:len(file)-3] + '.out')
			if file_input in file:
				temp = "C:/Users/nicol/cs170/Project/new-project-starter-code/inputs/" + file_input 
				with open(temp, "r") as f:
					lines = f.readlines()
					for line in lines:
						if count == 2:
							words = [str(x) for x in line.strip().split()]
							print(words, "here")
							start_string = words[0]
						count = count + 1

	start_int = kingdom_names[0].index(start_string)
	f = open(string, "w")
	p, q = minimum_dominating_solver(G, start_int)


	for x in q:
		f.write('' + kingdom_names[0][x] + ' ')

	f.write('\n')

	for y in p:
		f.write('' + kingdom_names[0][y] + ' ')

def inputToGraph(array):
	G = nx.Graph()
	for i in np.arange(len(array)):
		nodeAdder(G, i, 0)

	for i in np.arange(len(array)):
		for j in np.arange(len(array[i])):
			if i == j:
				G.node[i]['conquesting_cost'] = float(array[i][j])
			else:
				if array[i][j] != 'x' and array[i][j] != 'x\n':
					edgeAdder(G, i, j, float(array[i][j]))

	return G

def runOutputs():
	global kingdom_names
	errors = []
	input_directory = os.path.normpath("C:/Users/nicol/cs170/Project/new-project-starter-code/inputs")
	output_directory = os.path.normpath("C:/Users/nicol/cs170/Project/new-project-starter-code/outputs")
	#count = 20
	for subdir, dirs, files in os.walk(input_directory):
		for file in files:
			if file.endswith(".in"):
				#if count >= 0:
				print(file)
				completeName = os.path.join(output_directory, file[:len(file)-3] + '.out')
				G = inputToGraph(read_to_array("C:/Users/nicol/cs170/Project/new-project-starter-code/inputs/" + file))
				
				outputwriter(G, completeName, file)
				kingdom_names = []

	print(errors)

def runOutput(num):
	global kingdom_names
	errors = []
	input_directory = os.path.normpath("C:/Users/nicol/cs170/Project/new-project-starter-code/inputs")
	output_directory = os.path.normpath("C:/Users/nicol/cs170/Project/new-project-starter-code/outputs")
	#count = 20
	for subdir, dirs, files in os.walk(input_directory):
		for file in files:
			if file.endswith(".in"):
				if str(num) in file:
					print(file)
					completeName = os.path.join(output_directory, file[:len(file)-3] + '.out')
					G = inputToGraph(read_to_array("C:/Users/nicol/cs170/Project/new-project-starter-code/inputs/" + file))
					outputwriter(G, completeName, file)
					kingdom_names = []

	#print(errors)


# G = nx.Graph()
# nodeAdder(G, 0, 20)
# nodeAdder(G, 1, 5)
# nodeAdder(G, 2, 30)
# nodeAdder(G, 3, 30)
# nodeAdder(G, 4, 30)
# edgeAdder(G, 0, 1, 13)
# edgeAdder(G, 0, 3, 5)
# edgeAdder(G, 1, 3, 10)
# edgeAdder(G, 1, 2, 10)
# edgeAdder(G, 1, 4, 10)
# edgeAdder(G, 2, 3, 10)
# edgeAdder(G, 3, 4, 10)


# G=generateComplicatedPathGraph(200, 1500)
# write_to_file(G)
# minimum_dominating_solver(G, 0)
# outputwriter(G)
# print("read to array")
# G = inputToGraph(read_to_array("50.in"))

# outputwriter(G, 'C:\Users\nicol\cs170\Project\new-project-starter-code\outputs' + '\tempout.out')
errors = ['175.in', '336.in', '337.in', '338.in', '505.in', '506.in', '528.in', '529.in']
runOutput(336)
				#count -= 1
# nx.write_graphml(G, "testinputs.xml")