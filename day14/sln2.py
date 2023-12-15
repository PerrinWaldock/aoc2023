import numpy as np
import re
from collections import deque
from functools import cache
from copy import copy

datafile = "input.txt"
#datafile = "sample.txt" #21

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([l for l in line]) for line in lines])

#print(grid)

grids = deque()

def tiltup(grd):
	moved=True
	while moved:
		moved = False
		rocklocations = np.argwhere(grd == "O")
		for rl in rocklocations:
			if rl[0] > 0 and grd[rl[0]-1, rl[1]] == ".":
				grd[rl[0]-1, rl[1]] = "O"
				grd[rl[0], rl[1]] = "."
				moved = True
	return grd

def calcload(grd):
	load = 0
	height = np.shape(grd)[0]
	rocklocations = np.argwhere(grd == "O")
	for rl in rocklocations:
		load += height - rl[0]
	return load

MAXROTATIONS = 1000000000
newg = copy(grid)
grids.append(copy(newg))
foundrepeat = False
for rotations in range(1,MAXROTATIONS):
	lastup = copy(grid)

	#print(np.argwhere(newg == "#"))
	for _ in range(4): #tilts north, west, south, east
		newg = tiltup(newg)
		newg = np.rot90(newg, 3)
	#print(np.argwhere(newg == "#"))
	#print(newg)
	#print(calcload(newg))

	for oldcount, oldgrid in enumerate(grids):
		if np.all(newg == oldgrid):
			foundrepeat = True
			#print(f"repeat between {oldcount} {rotations}: {calcload(newg)}")
			break
	if foundrepeat:
		break

	grids.append(copy(newg)) #grids[n] is the grid after n full rotations

patternperiod = rotations - oldcount
patternoffset = oldcount
gridsind =  ((MAXROTATIONS-patternoffset)%patternperiod) + patternoffset

endgrid = grids[gridsind]
print(endgrid)
#print(newg)
print(calcload(endgrid))