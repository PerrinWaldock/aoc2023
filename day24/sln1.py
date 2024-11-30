import numpy as np
import re
from collections import deque, OrderedDict, namedtuple
from functools import cache
from copy import copy

VERBOSE = False

datafile = "input.txt"
#datafile = "sample.txt" #154

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

Hailstone = namedtuple("Hailstone", ['x', 'y', 'z', 'vx', 'vy', 'vz'])

if "sample" in datafile:
	minx, maxx = (7, 27)
	miny, maxy = (7, 27)
else:
	minx, maxx = (200000000000000, 400000000000000)
	miny, maxy = (200000000000000, 400000000000000)


#start 2D
# def intersection(a, b):
# 	if a.vx == b.vx and a.vy == b.vy:
# 		return np.inf, np.inf
# 	else:
# 		tx = (a.x - b.x)/(b.vx - a.vx)
# 		ty = (a.y - b.y)/(b.vy - a.vy)
# 		return (a.x + tx*a.vx, a.y + ty*a.vy)

def normalize(a):
	v = np.sqrt(a.vx**2 + a.vy**2) #+x
	return Hailstone(a.x, a.y, a.z, a.vx/v, a.vy/v, a.vz/v)

# def intersection(a, b):
# 	a = normalize(a)
# 	b = normalize(b)
# 	if a.vx == b.vx and a.vy == b.vy:
# 		return np.inf, np.inf
# 	else:
# 		if a.vx == 0:
# 			y = a.y
# 			x = (y - b.y)/(b.vy/b.vx) + b.x
# 		elif b.vx == 0:
# 			y = b.y
# 			x = (y - a.y)/(a.vy/a.vx) + a.x
# 		# elif a.vy == 0:
# 		# 	x = a.x
# 		# 	y = (x - b.x)/(b.vx/b.vy) + b.y
# 		# elif b.vy == 0:
# 		# 	x = b.x
# 		# 	y = (x - a.x)/(a.vx/a.vy) + a.y
# 		else:
# 			ma = (a.vy/a.vx)
# 			mb = (b.vy/b.vx)
# 			x = (ma*a.x - mb*b.x + b.y - a.y)/(ma - mb)
# 			y = ma*(x - a.x)
# 	return x, y

def intersection(a, b):
	denominator = (b.vx*a.vy - a.vx*b.vy)
	if denominator == 0: #TODO is this true?...
		return np.inf, np.inf, np.inf, np.inf
	tb = (a.vy*(a.x-b.x) + a.vx*(b.y-a.y))/denominator
	ta = (b.vy*(a.x-b.x) + b.vx*(b.y-a.y))/denominator
	x = a.x + ta*a.vx
	y = a.y + ta*a.vy
	return x, y, ta, tb

stones = deque()

for line in lines:
	stones.append(Hailstone(*getintsinline(line)))

stones = list(stones)

intersections = 0
for ind, a in enumerate(stones):
	for jnd, b in enumerate(stones[ind+1:]):
		if a != b:
			x, y, ta, tb = intersection(a, b)
			print(a, b, x, y)
			if minx <= x <= maxx and miny <= y <= maxy and ta >= 0 and tb >= 0:
				intersections += 1
				print("CROSS!")
print(intersections)



"""
6406 is too low
"""