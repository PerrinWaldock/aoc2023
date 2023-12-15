import numpy as np
import re
from collections import deque

datafile = "input.txt"
#datafile = "sample2.txt" #4
#datafile = "sample3.txt" #8
#datafile = "sample4.txt" #10

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

from copy import copy
directions = np.array([copy(grid), copy(grid)])

counter = 0
distances[startloc[0]][startloc[1]] = 0
for ind, ap in enumerate(activepaths):
	endloop = False
	loc, dir = ap
	while not endloop:
		newloc = nextloc(loc, dir)
		newdir = [d for d in "news" if validpath(newloc, d) and d != invertdir(dir)][0]

		if grid[newloc[0]][newloc[1]] == "S":
			endloop = True

		counter += 1
		distances[newloc[0]][newloc[1]] = counter
		directions[ind][newloc[0]][newloc[1]] = newdir
		loc = newloc
		dir = newdir

distances = distances.astype(int)
np.savetxt('distances.txt', np.transpose(distances), fmt='%i', delimiter=' ')
looppipe = (distances > 0).astype(int)
looppipe[startloc[0]][startloc[1]] = 1
np.savetxt('looppipe.txt', np.transpose(looppipe), fmt='%i', delimiter='')

#iterate through to 

enclosedareas = np.zeros(np.shape(grid)).astype(int)


ngrid = np.array([[c == "n" for jnd, c in enumerate(row)] for ind, row in enumerate(directions[0])]).astype(int)
sgrid = np.array([[c == "s" for jnd, c in enumerate(row)] for ind, row in enumerate(directions[0])]).astype(int)
egrid = np.array([[c == "e" for jnd, c in enumerate(row)] for ind, row in enumerate(directions[0])]).astype(int)
wgrid = np.array([[c == "w" for jnd, c in enumerate(row)] for ind, row in enumerate(directions[0])]).astype(int)

def isenclosedhoriwall(dirs1, dirs2):
	#dirs1 encloses one way, dirs2 encloses the other:
	wallcounter = 0
	for d1, d2 in zip(dirs1, dirs2):
		if "e" in d1+d2 and "w" in d1+d2: #horizontal wall
			if "e" in d1: #this logic may be suspect
				wallcounter += 1
			else:
				wallcounter -= 1
		elif d1 == "e" or d2 == "w": #bent wall
			wallcounter += 0.5
		elif d1 == "w" or d2 == "e":
			wallcounter -= 0.5
	return np.abs(wallcounter) % 2

def isenclosedvertwall(dirs1, dirs2):		
	#dirs1 encloses one way, dirs2 encloses the other:
	direction = ""
	wallcounter = 0
	for d1, d2 in zip(dirs1, dirs2):
		if "n" in d1+d2 and "s" in d1+d2: #horizontal wall
			if "n" in d1: #this logic may be suspect
				wallcounter += 1
			else:
				wallcounter -= 1
		elif d1 == "n" or d2 == "s": #bent wall
			wallcounter += 0.5
		elif d1 == "s" or d2 == "n":
			wallcounter -= 0.5
	return np.abs(wallcounter) % 2



for ind, row in enumerate(looppipe):
	for jnd, c in enumerate(row):
		if not c and ind and jnd: #not part of the loop pipe
			if isenclosedvertwall(directions[0,0:ind,jnd], directions[1,0:ind,jnd]) and isenclosedhoriwall(directions[0,ind,0:jnd], directions[1,ind,0:jnd]):
				enclosedareas[ind,jnd] = 1

print(np.sum(np.ravel(enclosedareas)))

"""
try going around the pipe, looking for insides?
"""