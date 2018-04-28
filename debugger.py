import inputcreator
import sys
import os
import networkx as nx
import numpy as np
import random
from networkx.algorithms import approximation, shortest_paths, tree, traversal
kingdom_names = []
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

def shiv_debugger(num):
	global kingdom_names
	errors = []
	input_directory = os.path.normpath("/Users/shivanesabharwal/cs170proj/inputs")
	output_directory = os.path.normpath("/Users/shivanesabharwal/cs170proj/outputs")
	#count = 20
	for subdir, dirs, files in os.walk(input_directory):
		for file in files:
			if file.endswith(".in"):
				if str(num) in file:
					print(file)
					completeName = os.path.join(output_directory, file[:len(file)-3] + '.out')
					G = inputcreator.inputToGraph(read_to_array("/Users/shivanesabharwal/cs170proj/inputs/" + file))
					outputwriter(G, completeName, file)
					kingdom_names = []
def outputwriter(G, string, file_input):
	# if nx.number_of_nodes(G) == 50:
	# 	f = open("50.out", "w")
	# elif nx.number_of_nodes(G) == 100:
	# 	f = open("100.out", "w")
	# elif nx.number_of_nodes(G) == 200:
	# 	f = open("200.out", "w")
	# else:
	# 	f = open("temp.out", "w")
	input_directory = os.path.normpath("/Users/shivanesabharwal/cs170proj/inputs")
	start_string = ''
	count = 0
	for subdir, dirs, files in os.walk(input_directory):
		for file in files:
			# completeName = os.path.join(output_directory, file[:len(file)-3] + '.out')
			if file_input in file:
				temp = "/Users/shivanesabharwal/cs170proj/inputs/" + file_input 
				with open(temp, "r") as f:
					lines = f.readlines()
					for line in lines:
						if count == 2:
							words = [str(x) for x in line.strip().split()]
							start_string = words[0]
						count = count + 1

	start_int = kingdom_names[0].index(start_string)
	f = open(string, "w")
	p, q = inputcreator.minimum_dominating_solver(G, start_int)
	
	for x in q:
		f.write('' + kingdom_names[0][x] + ' ')

	f.write('\n')

	for y in p:
		f.write('' + kingdom_names[0][y] + ' ')
shiv_debugger(336)