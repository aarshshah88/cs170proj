import networkx as nx
from networkx.algorithms import approximation, shortest_paths, tree, traversal
import numpy as np
import inputcreator
def test(G):
	for edge in G.edges():
		print(edge)

def minimum_dominating_solver(G, start):
	dom_set = approximation.dominating_set.min_weighted_dominating_set(G, 'conquesting_cost') # finds minimum weighted dominating set
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

def outputwriter(G):
	if nx.number_of_nodes(G) == 50:
		f = open("50.out", "w")
	elif nx.number_of_nodes(G) == 100:
		f = open("100.out", "w")
	elif nx.number_of_nodes(G) == 200:
		f = open("200.out", "w")
	else:
		f = open("temp.out", "w")
	p, q = minimum_dominating_solver(G, 0)

	for x in q:
		f.write('' + str(x) + ' ')

	f.write('\n')

	for y in p:
		f.write('' + str(y) + ' ')


G = inputcreator.generateComplicatedPathGraph(200, 1500)
inputcreator.write_to_file(G)
minimum_dominating_solver(G, 0)
outputwriter(G)

# G = nx.Graph()
# inputcreator.nodeAdder(G, 0, 20)
# inputcreator.nodeAdder(G, 1, 5)
# inputcreator.nodeAdder(G, 2, 30)
# inputcreator.nodeAdder(G, 3, 30)
# inputcreator.nodeAdder(G, 4, 30)
# inputcreator.edgeAdder(G, 0, 1, 20)
# inputcreator.edgeAdder(G, 0, 3, 5)
# inputcreator.edgeAdder(G, 1, 3, 10)
# inputcreator.edgeAdder(G, 1, 2, 10)
# inputcreator.edgeAdder(G, 1, 4, 10)
# inputcreator.edgeAdder(G, 2, 3, 10)
# inputcreator.edgeAdder(G, 3, 4, 10)
# minimum_dominating_solver(G, 0)






	







