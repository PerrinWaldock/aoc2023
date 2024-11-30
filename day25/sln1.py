# https://en.wikipedia.org/wiki/Connectivity_%28graph_theory%29

"""
dumb solution: brute force, pick three wires to remove and see if it affects connectity. 1000^3 possibilities, not efficient

smarter: 
	traverse graph, look for nodes with the fewest numbers of paths between them, try removing along common paths?
		paths[a,b] = deque(set(intermediate nodes),)

links to consider: 
	P-time min cuts to increase length of shortest path: https://stackoverflow.com/questions/14496220/algorithm-for-removing-fewest-edges-to-force-increase-in-length-of-shortest-path

	maps to maximum flow problem: https://en.wikipedia.org/wiki/Maximum_flow_problem ?
		push relabel to solve? https://en.wikipedia.org/wiki/Push%E2%80%93relabel_maximum_flow_algorithm

look for graph algorithm library?
	https://networkx.org/documentation/stable/tutorial.html
		cut_size ?

should consider changing to a proper class to describe the graph
"""

import numpy as np
import re
from collections import deque, OrderedDict
from functools import cache
from copy import copy

VERBOSE = False

datafile = "input.txt"
datafile = "sample.txt"

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

graph = {}

for line in lines:
	key, vals = line.split(":")
	vals = set([v.strip() for v in vals.strip().split(" ")])
	if key not in graph:
		graph[key] = vals
	else:
		graph[key].update(vals)
	for val in vals:
		if val not in graph:
			graph[val] = set([key])
		else:
			graph[val].add(key)

print(graph)

def removenode(node, graph):
	connectednodes = graph[node]
	for n in list(connectednodes):
		graph[n].remove(node)
	graph.pop(node)

def removewire(node1, node2, graph):
	graph[node1].remove(node2)
	graph[node2].remove(node1)

def findconnected(start, graph):
	nodes = set()
	searching = deque()
	searching.append(start)
	nodes.add(start)

	while len(searching):
		node = searching.pop()
		for cnode in graph[node]:
			if cnode not in nodes:
				nodes.add(cnode)
				searching.append(cnode)
	return nodes

def subgraphs(graph):
	nodes2consider = set(graph)
	subs = deque()
	while len(nodes2consider):
		node = list(nodes2consider)[0]
		connodes = findconnected(node, graph)
		subs.append(connodes)
		nodes2consider.difference_update(connodes)
	return subs

subs = subgraphs(graph)
print(subs)
print(len(subs))