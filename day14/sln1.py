import numpy as np
import re
from collections import deque
from functools import cache

datafile = "input.txt"
#datafile = "sample.txt" #21

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([l for l in line]) for line in lines])

print(grid)



moved=True
while moved:
	moved = False
	rocklocations = np.argwhere(grid == "O")
	for rl in rocklocations:
		if rl[0] > 0 and grid[rl[0]-1, rl[1]] == ".":
			grid[rl[0]-1, rl[1]] = "O"
			grid[rl[0], rl[1]] = "."
			moved = True

load = 0
height = np.shape(grid)[0]
for rl in rocklocations:
	load += height - rl[0]

print(load)