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
#datafile = "sample.txt"

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([l for l in line]) for line in lines]) 

minx = 0
miny = 0
maxy, maxx = tuple(np.shape(grid))#tuple(np.shape(grid) + np.array((1,1)))


class Path:
	def __init__(self, start, past=set()):
		if start not in past:
			past.add(start)
		self.past = past
		self.loc = start

	def isvalid(self, loc):
		if (loc[0] >= miny and loc[1] >= minx
	  		and loc[0] < maxy and loc[1] < maxx #within bounds
			and	(np.abs(self.loc[0] - loc[0]) == 0 and np.abs(self.loc[1] - loc[1]) == 1
				or np.abs(self.loc[0] - loc[0]) == 1 and np.abs(self.loc[1] - loc[1]) == 0) #adjacent
			and loc not in self.past): #not already covered
			char = grid[loc[0],loc[1]]
			if char == ".":
				return True
			elif char == "#":
				return False
			elif char == ">" and loc[1] - self.loc[1] == 1:
				return True
			elif char == "<" and loc[1] - self.loc[1] == -1:
				return True
			elif char == "^" and loc[0] - self.loc[0] == -1:
				return True
			elif char == "v" and loc[0] - self.loc[0] == 1:
				return True
		return False
	
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
		
	def copy(self):
		return Path(start=self.loc, past=copy(self.past))
	
	def isfinished(self):
		if self.loc[0] == maxy-1:
			return True
		else:
			return False
		
	def pathlen(self):
		return len(self.past)-1
	
	def __repr__(self) -> str:
		return f"{self.loc} {self.past}"
	

activepaths = [Path((0,1))]
finishedpaths = deque()

while len(activepaths):
	path = activepaths.pop()

	if path.isfinished():
		finishedpaths.append(path)
		continue

	nextsteps = path.validnext()
	if len(nextsteps) == 1:
		path.step(nextsteps[0])
		activepaths.append(path)
	else:
		for loc in nextsteps: #branch here
			newpath = path.copy()
			newpath.step(loc)
			activepaths.append(newpath)

pathlens = [fp.pathlen() for fp in finishedpaths]
for pl in pathlens:
	print(pl)
print(max(pathlens))
