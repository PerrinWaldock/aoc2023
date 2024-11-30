import numpy as np
import re
from collections import deque
from functools import cache
from copy import copy

datafile = "input.txt"
#datafile = "sample.txt" #94
#datafile = "sample2.txt" #71

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

activepaths = [((0,0), "e", 0, -grid[0,0]), 
			   ((0,0), "s", 0, -grid[0,0])] #TODO may need to start at 1 each


#TODO need to vet out paths before taking them: 
#TODO need to change the order that things are evaluated in to fix off-by-one errors

while len(activepaths):
	newpaths = deque()
	for path in activepaths:
		loc, dir, consteps, oldheatloss = path

		distatloc = distances[loc[0]][loc[1]]

		heatloss = oldheatloss + grid[loc[0]][loc[1]] #calculates the heatloss from entering THIS square

		scorekey = f"{dir}{consteps}"
		newscores = {}
		#TODO not strictly convinced this is optimal
		keystocheck = [f"{dir}{n}" for n in range(consteps, consteps+1)] #TODO may need to replace in with a range
		newbestkeys = []
		for key in keystocheck:
			if key not in distatloc.keys() or (heatloss < distatloc[key]):
				newbestkeys.append(key)
		if len(newbestkeys):
			for key in newbestkeys:
				distatloc[key] = heatloss
		else:
			continue #no point in continuing path if the path doesn't set a high score

		if loc == (max0-1, max1-1) and 4 <= consteps <= 10: #reached finish
			continue

		if consteps < 4:
			newdirs = [dir]
		else:
			newdirs = [d for d in VALIDDIRS if d != OPPOSITEDIR[dir]]

		#TODO add new paths
		for ndir in newdirs:
			if ndir == dir:
				nconsteps = consteps + 1
			else:
				nconsteps = 1
			
			if nconsteps > 10:
				continue


			newloc = nextloc(loc, ndir)
			if newloc is None:
				continue

			newpaths.append((newloc, ndir, nconsteps, heatloss))

	activepaths = newpaths

	#break

def getminofdict(d):
	validd = {k: v for k, v in d.items() if int(k[1:]) >= 4}
	if len(validd):
		return min(validd.values())
	else:
		return np.inf

mindists = np.array([np.array([getminofdict(d) for d in row]) for row in distances])

print(mindists)
print(distances[max0-1][max1-1])
print(mindists[max0-1][max1-1])
		

"""
NOTE: NEED TO END ON A RUN OF AT LEAST 4 OR IT IS INVALID

1040 is too high... (processing mistake on getmin)
"""