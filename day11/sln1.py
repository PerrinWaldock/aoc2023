import numpy as np
import re
from collections import deque

datafile = "input.txt"
#datafile = "sample.txt" #374 9pt 1) 1030 (pt 2)

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

grid = np.array([np.array([c for c in line if c != "\n"]) for line in open(datafile, "r")])
#add second column/row any time there is one with no galaxies?

addrows = np.array([ind for ind, row in enumerate(grid) if "#" not in row])
addcolumns = np.array([ind for ind, row in enumerate(np.transpose(grid)) if "#" not in row])

locations = np.argwhere("#"==grid)

multiplier = 2

distances = deque()

for ind in range(len(locations)):
	for jnd in range(ind+1, len((locations))):
		a, b = locations[ind], locations[jnd]
		steps = np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])

		minx = min(a[0], b[0])
		maxx = max(a[0], b[0])
		miny = min(a[1], b[1])
		maxy = max(a[1], b[1])

		emptycrossings = np.sum((minx < addrows)*(maxx > addrows)) + np.sum((miny < addcolumns)*(maxy > addcolumns))
		steps += emptycrossings*(multiplier-1)

		distances.append(steps)
print(sum(distances))