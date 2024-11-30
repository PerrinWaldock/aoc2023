import numpy as np
import re
from collections import deque, namedtuple, OrderedDict
from functools import cache
from copy import copy
import string

datafile = "input.txt"
#datafile = "sample.txt" #8000*4000=32000000

"""
parse the input to get all of the bricks
sort the bricks by Z, number accordingly (3rd number should allow sorting by Z)
start filling up a 3D volume with numbers corresponding to each brick
create second and third array of deques for each brick. one will contain bricks below, one will contain bricks above
for each brick, add all above it to the relevant array AND add those immediately below it to a relevant array
bricks where all above have at least two below can be vaporized
"""

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

bricks = deque()

Brick = namedtuple("Brick", ['x0', 'y0', 'z0', 'x1', 'y1', 'z1', "n"])

for ind, line in enumerate(lines):
	bricks.append(Brick(*getintsinline(line), ind))
	#print(string.ascii_uppercase[ind], bricks[-1])

bricks = sorted(bricks, key=lambda x: x.z0)

nummap = {ind: b.n for ind, b in enumerate(bricks)}

minx = min([b.x0 for b in bricks])
maxx = max([b.x1 for b in bricks])
miny = min([b.y0 for b in bricks])
maxy = max([b.y1 for b in bricks])
minz = min([b.z0 for b in bricks]) #TODO this will probably become not space efficient
maxz = max([b.z1 for b in bricks])

brickheights = np.array([[0 for x in range(minx, maxx+1)] for y in range(miny, maxy+1)])
#bricknums = [[deque() for x in range(minx, maxx+1)] for y in range(miny, maxy+1)]
topbricks = np.array([[-1 for x in range(minx, maxx+1)] for y in range(miny, maxy+1)])

bricksbelow = [set() for _ in bricks]

for bricknum, b in enumerate(bricks):
	brickheight = b.z1-b.z0+1
	xs, ys = np.meshgrid(np.arange(b.x0, b.x1+1), np.arange(b.y0, b.y1+1))
	xs = np.ravel(xs)
	ys = np.ravel(ys)

	maxheight = np.max(brickheights[ys, xs])
	maxcoords = np.argwhere(brickheights[ys, xs] == maxheight)
	newheight = maxheight + brickheight

	print(nummap[bricknum], maxheight, brickheight, newheight)

	maxxs = np.ravel(xs[maxcoords])
	maxys = np.ravel(ys[maxcoords])

	for x, y in zip(maxxs, maxys): #TODO likely a more efficient way of doing this
		bricksbelow[bricknum].add(topbricks[y,x])

	for x, y in zip(xs, ys):
		brickheights[y, x] = newheight
		topbricks[y, x] = bricknum

	print(topbricks)
	print(brickheights)

#TODO purge -1 from bricksbelow
		
bricksabove = [set() for _ in bricks]

for ind, belowset in enumerate(bricksbelow):
	belowset.discard(-1)
	for b in list(belowset):
		bricksabove[b].add(ind)

print(bricksbelow)
print(bricksabove)

print(topbricks)

destroyablebricks = deque()

for ind, aboveset in enumerate(bricksabove):
	supported = True
	for b in list(aboveset):
		if len(bricksbelow[b]) == 1:
			supported = False
			break
	if supported:
		destroyablebricks.append(ind)

print(destroyablebricks)
print(len(destroyablebricks))

#oldtopbricks = np.array([[nummap[topbricks[y,x]] for x in range(minx, maxx+1)] for y in range(miny, maxy+1)])
#print(oldtopbricks)