import networkx as nx
from networkx.algorithms import approximation, shortest_paths, tree, traversal
import numpy as np
import inputcreator
def test(G):
	for edge in G.edges():
		print(edge)

def minimum_dominating_solver(G, start):
	dom_set = approximation.dominating_set.min_weighted_dominating_set(G, 'conquesting_cost') # finds minimum weighted dominating set
	print(dom_set)
	floyd_warshall = dict(shortest_paths.weighted.all_pairs_dijkstra_path(G))
	floyd_warshall_lengths = dict(shortest_paths.weighted.all_pairs_dijkstra_path_length(G))
	G_prime = nx.Graph()
	inputcreator.nodeAdder(G_prime, start, G.node[start]['conquesting_cost'])
	for node in dom_set:
		inputcreator.nodeAdder(G_prime, node, G.node[node]['conquesting_cost'])
		start_to_node_path_weight = floyd_warshall_lengths[start][node]
		inputcreator.edgeAdder(G_prime, start, node, start_to_node_path_weight)
		for each in dom_set:
			if each != node:
				if not G.has_edge(node, each):
					edge_weight = floyd_warshall_lengths[node][each]
					inputcreator.edgeAdder(G_prime, node, each, edge_weight)
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
				print("Need to add path back for", prev)
				tour.append(floyd_warshall[prev[len(prev) - 1]][start])
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
	print(FINAL_TOUR)

def find_weight(G, path): # Takes in a graph and path. Returns the weight of the path.
	path_weight = 0
	prev = None
	for node in path: 
		if prev != None: # first node in path
			path_weight += G[prev][node]['weight']
		prev = node
	return path_weight

G = nx.Graph()
inputcreator.nodeAdder(G, 0, 20)
inputcreator.nodeAdder(G, 1, 5)
inputcreator.nodeAdder(G, 2, 30)
inputcreator.nodeAdder(G, 3, 30)
inputcreator.nodeAdder(G, 4, 30)
inputcreator.edgeAdder(G, 0, 1, 20)
inputcreator.edgeAdder(G, 0, 3, 5)
inputcreator.edgeAdder(G, 1, 3, 10)
inputcreator.edgeAdder(G, 1, 2, 10)
inputcreator.edgeAdder(G, 1, 4, 10)
inputcreator.edgeAdder(G, 2, 3, 10)
inputcreator.edgeAdder(G, 3, 4, 10)
minimum_dominating_solver(G, 0)

# def closest_special_node(G, special_set, current) :

# # Input: Graph, set of special vertices and current vertex
# # Output: Closest special node to current vertex
# 	closest = None
# 	minimum_path = float('inf')
# 	actual_path = None
# 	for each in special_set:
# 		if each != current:
# 			candidate = shortest_path(G, source=current, target=each, 'weight')
# 			for node in path_to_each: # for loop to compute weight of path
# 				if prev != None: # first node in path
# 					path_weight += G[prev][node]['weight']
# 				prev = node
# 			if path_weight < minimum_path:
# 					minimum_path = path_weight
# 					closest = each
# 					actual_path = candidate
# 	return closest, actual_path, path_weight
# def closest_node(current, dom_set, shortest_path_dict): # helper function that returns sol where sol[0] is the closest node in dom_set and sol[1] is the weight of the path to the closest node in dom_set
# 	first = None # will hold node to visit first at the end of following for loop
# 	min_weight_start = float('inf')
# 	for each in dom_set:
# 		if each not in visited:
# 			prev = None
# 			path_weight = 0 
# 			path_to_each = paths_from_source[current][each]
# 			for node in path_to_each: # for loop to compute weight of path
# 				if prev != None: # first node in path
# 					path_weight += G[prev][node]['weight']
# 				prev = node
			# if path_weight < min_weight_start:
			# 	min_weight_start = path_weight
			# 	first = each
# 	dom_set.discard(first)




	







