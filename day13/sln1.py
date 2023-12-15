import numpy as np
import re
from collections import deque
from functools import cache

datafile = "input.txt"
#datafile = "sample.txt" #405

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]


groups = [deque()]

for line in open(datafile, "r"):
	if line == "\n":
		groups.append(deque())
	else:
		groups[-1].append([l for l in line.strip()])

groups = [np.array(g) for g in groups]
#add second column/row any time there is one with no galaxies?

"""
iterate through columns and rows, check to make sure each matches

numpy method may not be the most efficient
"""

summedtotal = 0
for grid in groups:
	hmirrors = deque()

	#print(grid)
	print(np.shape(grid))

	maxwidth = np.shape(grid)[0]
	for ind in range(1, maxwidth): #ind is the first index of the second array
		width = min(ind, maxwidth-ind)
		arr1 = grid[ind-width:ind]
		arr2 = grid[ind+width-1:ind-1:-1]
		#print(np.shape(arr1), np.shape(arr2))
		if (arr1==arr2).all():
			print("h", ind)
			print(arr1)
			print(arr2)
			hmirrors.append(ind)
			summedtotal += ind*100

	vmirrors = deque()

	grid = np.transpose(grid)
	maxwidth = np.shape(grid)[0]
	for ind in range(1, maxwidth):
		width = min(ind, maxwidth-ind)
		arr1 = grid[ind-width:ind]
		arr2 = grid[ind+width-1:ind-1:-1]
		if (arr1==arr2).all():
			print("v", ind)
			print(arr1)
			print(arr2)
			vmirrors.append(ind)
			summedtotal += ind
	print(hmirrors, vmirrors, summedtotal)


print(summedtotal)		
	

"""
pt1 answers:
15931 is too low
"""