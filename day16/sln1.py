import numpy as np
import re
from collections import deque, OrderedDict
from functools import cache
from copy import copy

VERBOSE = False

datafile = "input.txt"
#datafile = "sample.txt" #21

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([l for l in line]) for line in lines]) #first index is y, second is x

startlocs = deque()
#todo generate a bunch of starting locations
max0, max1 = np.shape(grid)
for ind in range(0, max0):
	startlocs.append(((ind,0), "e"))
	startlocs.append(((ind,max1-1), "w"))
for ind in range(0, max1):
	startlocs.append(((0,ind), "s"))
	startlocs.append(((max0-1,ind), "n"))

activatetiles = deque()

for startloc in startlocs:
	energized = copy(grid)

	beams = [((0,0), "e")]

	active = [True]

	startpoints = copy(beams)

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
			newloc[0] >= np.shape(grid)[0] or
			newloc[1] < 0 or
			newloc[1] >= np.shape(grid)[1]):
			return None
		else:
			return newloc


	#tile types: . | - / \

	count = 0
	while True:

		newbeams = deque()

		if len(beams) == 0:
			break

		for beam in beams:
			if beam == None:
				continue
			loc, dir = beam
			if loc is None:
				continue

			if beam in startpoints and count > 0: #ignore
				continue
			
			energized[loc[0]][loc[1]] = "#"
			tile = grid[loc[0]][loc[1]]


			if tile == ".":
				newbeams.append((nextloc(loc, dir), dir))
			elif tile == "|":
				if (dir == "n" or dir == "s"):
					newbeams.append((nextloc(loc, dir), dir))
				else:
					newbeams.append((nextloc(loc, "n"), "n"))
					newbeams.append((nextloc(loc, "s"), "s"))
					startpoints.append((loc, "e"))
					startpoints.append((loc, "w"))
			elif tile == "-":
				if (dir == "e" or dir == "w"):
					newbeams.append((nextloc(loc, dir), dir))
				else:
					newbeams.append((nextloc(loc, "w"), "w"))
					newbeams.append((nextloc(loc, "e"), "e"))
					startpoints.append((loc, "n"))
					startpoints.append((loc, "s"))
			elif tile == "\\":
				if dir == "w":
					newbeams.append((nextloc(loc, "n"), "n"))
				elif dir == "n":
					newbeams.append((nextloc(loc, "w"), "w"))
				elif dir == "e":
					newbeams.append((nextloc(loc, "s"), "s"))
				elif dir == "s":
					newbeams.append((nextloc(loc, "e"), "e"))
			elif tile == "/":
				if dir == "e":
					newbeams.append((nextloc(loc, "n"), "n"))
				elif dir == "n":
					newbeams.append((nextloc(loc, "e"), "e"))
				elif dir == "w":
					newbeams.append((nextloc(loc, "s"), "s"))
				elif dir == "s":
					newbeams.append((nextloc(loc, "w"), "w"))
		
		# if count > 10:
		# 	break

		beams = newbeams
		count += 1

	#print(energized)
	activatetiles.append(np.sum(energized == "#"))


print(max(activatetiles))