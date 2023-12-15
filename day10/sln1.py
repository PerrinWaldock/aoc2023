import numpy as np
import re
from collections import deque

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

grid = np.array([np.array([c for c in line if c != "\n"]) for line in open(datafile, "r")])

grid = np.transpose(grid) #first index is horizontal

distances = np.zeros(np.shape(grid))

startloc = np.argwhere(grid == "S")[0]

paths = {"|": "ns",
		 "-": "ew",
		 "L": "ne",
		 "J": "nw",
		 "7": "sw",
		 "F": "es",
		 ".": "",
		 "S": "news"}

def invertdir(d):
	if d == "n":
		return 's'
	elif d == "s":
		return 'n'
	elif d == "e":
		return "w"
	elif d == "w":
		return "e"

pathsto = {k: [invertdir(d) for d in v] for k, v in paths.items()}

def moveloc(lastloc, direction):
	if direction == "n":
		return lastloc + np.array([0,-1])
	elif direction == "s":
		return lastloc + np.array([0,1])
	elif direction == "w":
		return lastloc + np.array([-1,0])
	elif direction == "e":
		return lastloc + np.array([1,0])


def nextloc(lastloc, direction):
	c = grid[lastloc[0]][lastloc[1]]
	#nd = [d for d in paths[c] if d != direction][0]
	return moveloc(lastloc, direction)


activepaths = [startloc + np.array([0,1]),
			   startloc + np.array([0,-1]),
			   startloc + np.array([1,0]),
			   startloc + np.array([-1,0])]

def validpath(location, direction):
	startpipe = grid[location[0]][location[1]]
	end = nextloc(location, direction)
	if -1 in end or end[0] == len(grid) or end[1] == len(grid[0]):
		return False
	endpipe = grid[end[0]][end[1]]
	return direction in paths[startpipe] and direction in pathsto[endpipe]

activepaths = [(startloc, d) for d in paths[grid[startloc[0]][startloc[1]]] if validpath(startloc, d)]

print(activepaths)

#TODO find the two valid routes to go from the start

counters = [0, 0]
distances[startloc[0]][startloc[1]] = 0
endloop = False


while not endloop:
	newpaths = []
	for ind, (loc, dir) in enumerate(activepaths):
		newloc = nextloc(loc, dir)
		newdir = [d for d in "news" if validpath(newloc, d) and d != invertdir(dir)][0]

		#print(activepaths+newpaths)
		for l, _ in activepaths+newpaths:
			if np.all(newloc == l):
				endloop = True
				break

		newpaths.append((newloc, newdir))
		counters[ind] += 1
		distances[newloc[0]][newloc[1]] = counters[ind]

		#print(f"{ind}: {newloc}, {newdir}, {[np.all(newloc == l) for l, _ in activepaths+newpaths]}")
		#print(distances)
		#print("")
	activepaths = newpaths

import sys
np.set_printoptions(threshold=sys.maxsize)

np.savetxt('distances.txt', np.transpose(distances), fmt='%i', delimiter=' ')

print(np.transpose(distances))
print(int(max(np.ravel(distances))))