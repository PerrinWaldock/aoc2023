import numpy as np
import re
from collections import deque
from functools import cache
from copy import copy

datafile = "input.txt"
#datafile = "sample.txt" #21

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([int(l) for l in line]) for line in lines])
max0, max1 = np.shape(grid)


"""
comments:
can't use base djikstra's b/c can't go three in a row

algorithm:
keep a list of active paths
	active paths: location, direction, consecutive steps, total heatloss
	add list of active paths
add valid directions to active paths. 

for each path, track

at each location, track best heatloss given a certain direction + steps
	only terminate if worse heatloss and steps at a given direction
	
"""

# class Path():
# 	def __init__(self, pos, )

def nextloc(loc, dir):
	if dir == "n":
		newloc = (loc[0]-1, loc[1])
	if dir == "s":
		newloc = (loc[0]+1, loc[1])
	if dir == "e":
		newloc = (loc[0], loc[1]+1)
	if dir == "w":
		newloc = (loc[0], loc[1]-1)
	
	if (newloc[0] < 0 or 
		newloc[0] >= max0 or
		newloc[1] < 0 or
		newloc[1] >= max1):
		return None
	else:
		return newloc



VALIDDIRS = ["n", "e", "w", "s"]
OPPOSITEDIR = {"n": "s", "s": "n", "e": "w", "w": "e"}

#key format: dirsteps: "e1"
distances = [[{} for _ in range(np.shape(grid)[1])] for _ in range(np.shape(grid)[0])]

activepaths = [((0,0), "e", 1, 0), ((0,0), "s", 1, 0)]


#TODO need to change the order of operations -- the heatloss is being set by adding the PREVIOUS location

while len(activepaths):
	newpaths = deque()
	for path in activepaths:
		loc, dir, consteps, heatloss = path

		distatloc = distances[loc[0]][loc[1]]

		scorekey = f"{dir}{consteps}"
		newscores = {}

		keystocheck = [f"{dir}{n}" for n in range(consteps, 4)]
		newbestkeys = []
		for key in keystocheck:
			if key not in distatloc.keys() or (heatloss < distatloc[key]):
				newbestkeys.append(key)
		if len(newbestkeys):
			for key in newbestkeys:
				distatloc[key] = heatloss
		else:
			continue #no point in continuing path if the path doesn't set a high score

		if loc == (max0-1, max1-1):
			continue

		newloc = nextloc(loc, dir)
		if newloc is None:
			continue
		
		newdirs = [d for d in VALIDDIRS if d != OPPOSITEDIR[dir]]

		newheatloss = heatloss + grid[newloc[0]][newloc[1]]

		#TODO add new paths
		for ndir in newdirs:
			if ndir == dir:
				nconsteps = consteps + 1
			else:
				nconsteps = 1
			if nconsteps > 3:
				continue
			newpaths.append((newloc, ndir, nconsteps, newheatloss))


	activepaths = newpaths

	#break

distances = np.array([np.array([min(d.values()) for d in row]) for row in distances])

print(distances)
print(distances[max0-1][max1-1])
		
