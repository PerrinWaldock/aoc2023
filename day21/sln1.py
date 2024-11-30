"""
TODO
for 64 iterations
	for each validposition, add new valid positions to a list and remove the old
"""

import numpy as np
import re
from collections import deque, OrderedDict
from functools import cache
from copy import copy

VERBOSE = False

datafile = "input.txt"
#datafile = "sample.txt" #6 steps -> 16

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([l for l in line]) for line in lines]) #first index is y, second is x

validpositions = [np.argwhere(grid == "S")[0]]
grid[validpositions[0][0],validpositions[0][1]] = "."

(maxy, maxx) = np.shape(grid)

for iter in range(64):
	newpositions = deque()
	for pos in validpositions:
		y,x = pos
		if x > 0 and grid[y,x-1] == ".":
			newpositions.append((y,x-1))
		if x < maxx-1 and grid[y,x+1] == ".":
			newpositions.append((y,x+1))
		if y > 0 and grid[y-1,x] == ".":
				newpositions.append((y-1,x))
		if y < maxy-1 and grid[y+1,x] == ".":
			newpositions.append((y+1,x))

	validpositions = list(set(newpositions))

for pos in validpositions:
	y,x = pos
	grid[y,x] = "O"

print(grid)

print(len(validpositions))