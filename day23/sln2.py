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
shortcuts = {}

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

testpath = Path((-1,-1))	
intersections = 0
for x in range(minx, maxx):
	for y in range(miny, maxy):
		testpath.loc = (y,x)
		if grid[x,y] != "#" and len(testpath.validnext()) > 2:
			print(x,y)
			intersections += len(testpath.validnext()) - 2
print(intersections)

import time
time.sleep(10)

activepaths = deque([Path((0,1))])
numfinished = 0
bestpath = None
currentbest = 0

while len(activepaths):
	path = activepaths.pop()

	if path.isfinished():
		numfinished += 1
		pl = path.pathlen()
		if pl > currentbest:
			bestpath = path
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
	print(f"{len(activepaths)} {numfinished} {currentbest} {len(shortcuts)}/{intersections}")

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

# for start, shortset in shortcuts.items():
# 	print(f"{start}: {shortset}\n")

lp = bestpath
for pt in lp.past:
	pathgrid[pt[0]][pt[1]] = "O"

np.savetxt("pathgrid.txt", pathgrid, fmt="%s", delimiter="")
np.savetxt("pathgrid.txt", pathgrid, fmt="%s", delimiter="")

print(currentbest)


"""
4634 is too low
7337 is too high
6402 is wrong
4635 is wrong
6406 is correct
"""