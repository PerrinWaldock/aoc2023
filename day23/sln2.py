"""
TODO
	maintain array of active paths, split into two every time there is a fork
		each path is a 
			set of tuples with places it has been
			current coordinate
			can calculate the length of path based on number of items in set
"""

import numpy as np
import re
from collections import deque, OrderedDict
from functools import cache
from copy import copy

VERBOSE = False

datafile = "input.txt"
#datafile = "sample.txt" #154

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([l for l in line]) for line in lines]) 
oldgrid = copy(grid)
pathgrid = copy(grid)

minx = 0
miny = 0
maxy, maxx = tuple(np.shape(grid))#tuple(np.shape(grid) + np.array((1,1)))

#shortcut key should be the first square after an intersection, value should be the intersection it leads to and a set of the squares it took to reach that point
#TODO should only store intersections in the set + increment a step counter to improve space efficiency
shortcuts = {}

"""
TODO something is wrong around 109,111 -- appears to be a self-intersection
"""

#START should be the FIRST square after the intersection
class Path:
	def __init__(self, start, past=set()):
		if start in shortcuts:
			self.start = start
			self.past = past
			self.loc, self.pastsincestart = shortcuts[start]
			if self.loc in self.past:
				raise Exception("Invalid Starting Location -- start in past") 
			self.past.update(self.pastsincestart)
			self.past.add(self.start)
			self.past.add(self.loc)
		else:
			self.pastsincestart = set([start])
			if start in past:
				raise Exception("Invalid Starting Location -- start in past")
			past.add(start)
			self.start = start
			self.past = past
			self.loc = start

	def istraversable(self, loc):
		return (loc[0] >= miny and loc[1] >= minx
	  		and loc[0] < maxy and loc[1] < maxx #within bounds
			and	(np.abs(self.loc[0] - loc[0]) == 0 and np.abs(self.loc[1] - loc[1]) == 1
				or np.abs(self.loc[0] - loc[0]) == 1 and np.abs(self.loc[1] - loc[1]) == 0) #adjacent
			and grid[loc[0],loc[1]] in ".><^v")

	def isvalid(self, loc):
		return self.istraversable(loc) and loc not in self.past

	def traversablenext(self):
		proposed = [(self.loc[0],self.loc[1]-1),
			  		(self.loc[0],self.loc[1]+1),
					(self.loc[0]-1,self.loc[1]),
					(self.loc[0]+1,self.loc[1]) ]
		return [loc for loc in proposed if self.istraversable(loc)]

	def validnext(self):
		proposed = [(self.loc[0],self.loc[1]-1),
			  		(self.loc[0],self.loc[1]+1),
					(self.loc[0]-1,self.loc[1]),
					(self.loc[0]+1,self.loc[1]) ]
		return [loc for loc in proposed if self.isvalid(loc)]
	
	def step(self, loc):
		if self.isvalid(loc):
			self.loc = loc
			self.past.add(loc)
			self.pastsincestart.add(loc)
		
	def copyto(self, loc):
		if self.isvalid(loc):
			return Path(start=loc, past=copy(self.past))
		else:
			raise Exception("Invalid Starting Location")
	
	def isfinished(self):
		if self.loc[0] == maxy-1:
			return True
		else:
			return False
		
	def pathlen(self):
		return len(self.past)-1
	
	def __repr__(self) -> str:
		return f"{self.loc} {self.past}"
	

activepaths = deque([Path((0,1))])
finishedpaths = deque()


currentbest = 0
while len(activepaths):
	path = activepaths.pop()

	if path.isfinished():
		finishedpaths.append(path)
		pl = path.pathlen()
		if pl > currentbest:
			currentbest = pl
		continue

	nextsteps = path.validnext()

	if len(nextsteps) == 0:
		if len(path.traversablenext()) == 0:
			grid[path.start[0]][path.start[1]] = "#" #kill the invalid path
		continue
	elif len(nextsteps) == 1:
		path.step(nextsteps[0])
		activepaths.append(path)
	else:
		shortcuts[path.start] = (path.loc, path.pastsincestart)
		for loc in nextsteps: #branch here
			try:
				newpath = path.copyto(loc)
				activepaths.append(newpath)
			except:
				continue #shortcut to invalid branch
	print(len(activepaths), len(finishedpaths), currentbest)

finishedpaths = list(finishedpaths)
finishedpaths.sort(key=lambda fp: fp.pathlen())
pathlens = [fp.pathlen() for fp in finishedpaths] 
#TODO could make more efficient by skipping unneccesary checks, etc
#TODO should look up travelling salesman problem to see if it can reduce some branches
"""
ways to make more efficient
	DONE go depth, not breadth first
		DONE if dead end encountered due to #, stick a # at the start of the path
	track which direction travelling to reduce number of checks (track "last" as well as curret), only check in set if at a fork ?
	modifications
		DONE: modify the map to cut out all dead ends
		create lookup table of jumptos
			if step is on table, 
"""

for pl in pathlens:
	print(pl)
print(max(pathlens), currentbest)
# for start, shortset in shortcuts.items():
# 	print(f"{start}: {shortset}\n")

lp = finishedpaths[-1]
for pt in lp.past:
	pathgrid[pt[0]][pt[1]] = "O"

np.savetxt("pathgrid.txt", pathgrid, fmt="%s", delimiter="")
np.savetxt("pathgrid.txt", pathgrid, fmt="%s", delimiter="")


"""
4634 is too low
7337 is too high
6402 is wrong
"""