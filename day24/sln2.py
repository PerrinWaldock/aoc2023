import numpy as np
import re
from collections import deque, OrderedDict, namedtuple
from functools import cache
from copy import copy
from scipy.optimize import fsolve
from random import random, shuffle

VERBOSE = False

datafile = "input.txt"
#datafile = "sample.txt" #154

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

Hailstone = namedtuple("Hailstone", ['x', 'y', 'z', 'vx', 'vy', 'vz'])

if "sample" in datafile:
	minx, maxx = (7, 27)
	miny, maxy = (7, 27)
	minz, maxz = (7, 27)
else:
	minx, maxx = (200000000000000, 400000000000000)
	miny, maxy = (200000000000000, 400000000000000)
	minz, maxz = (200000000000000, 400000000000000)

stones = deque()
for line in lines:
	stones.append(Hailstone(*getintsinline(line)))

stones = list(stones)

"""
maybe use the projection of the intersections of the paths?....
NO -- solve this as a many by many matrix. Set up with few dimensions then expand

TODO reduce number of equations?..
"""

# def geneqns(stones):
# 	s0, s1, s2 = stones
# 	def equations(vars):
# 		x, y, z, vx, vy, vz, t0, t1, t2 = vars
# 		eqns = [
# 			x + vx*t0 - (s0.x + s0.vx*t0),
# 			y + vy*t0 - (s0.y + s0.vy*t0),
# 			z + vz*t0 - (s0.z + s0.vz*t0),
# 			x + vx*t1 - (s1.x + s1.vx*t1),
# 			y + vy*t1 - (s1.y + s1.vy*t1),
# 			z + vz*t1 - (s1.z + s1.vz*t1),
# 			x + vx*t2 - (s2.x + s2.vx*t2),
# 			y + vy*t2 - (s2.y + s2.vy*t2),
# 			z + vz*t2 - (s2.z + s2.vz*t2)
# 		]
# 		return eqns
# 	return equations

def geneqns(stones):
	a,b,c = stones
	def equations(vars):
		x, y, z, vx, vy, vz = vars
		eqns = [
			(a.vx - vx)*y + vy*(x - a.x) - ((a.vx - vx)*a.y + a.vy*(x - a.x)),
			(a.vx - vx)*z + vz*(x - a.x) - ((a.vx - vx)*a.z + a.vz*(x - a.x)),
			(b.vx - vx)*y + vy*(x - b.x) - ((b.vx - vx)*b.y + b.vy*(x - b.x)),
			(b.vx - vx)*z + vz*(x - b.x) - ((b.vx - vx)*b.z + b.vz*(x - b.x)),
			(c.vx - vx)*y + vy*(x - c.x) - ((c.vx - vx)*c.y + c.vy*(x - c.x)),
			(c.vx - vx)*z + vz*(x - c.x) - ((c.vx - vx)*c.z + c.vz*(x - c.x))
		]
		return eqns
	return equations
	
	#np.zeros(9)
#root = fsolve(geneqns(stones[1:4]), (24,13,10,-3,1,2,1,2,3), maxfev=100000)
#(24,13,10,-3,1,2,1,2,3)

def isintish(n, tol=2):
	return round(round(n) - n, tol) == 0 

def findtime(a, b):
	ts = deque()
	try:
		ts.append((a.x - b.x)/(b.vx - a.vx))
	except:
		pass
	try:
		ts.append((a.y - b.y)/(b.vy - a.vy))
	except:
		pass
	try:
		ts.append((a.z - b.z)/(b.vz - a.vz))
	except:
		pass
	#print("proto ts", ts)
	ts = list(set([round(t, 2) for t in ts]))
	if len(ts) > 1:
		return np.nan #raise Exception(f"{a} and {b} do not intersect! {ts}")
	return ts[0]

def isgoodsolution(rock):
	ts = deque()
	for s in stones:
		t = findtime(rock, s)
		if np.isnan(t) or np.isinf(t) or not isintish(t) or t < 0:
			return False
		else:
			ts.append(t)
	#print("ts", ts)
	return True


success = False
iters = 0
while not success: #NOTE: too unlikely to solve -- need to figure out analytically
	iters += 1
	x0 = minx + (maxx - minx)*random()
	y0 = miny + (maxy - miny)*random()
	z0 = minz + (maxz - minz)*random()
	vx0 = 600*(random()-0.5)
	vy0 = 600*(random()-0.5)
	vz0 = 600*(random()-0.5)
	t0 = 0
	t1 = 0
	t2 = 0
	#guess = (x0, y0, z0, vx0, vy0, vz0, t0, t1, t2)
	guess = (x0, y0, z0, vx0, vy0, vz0)
	shuffle(stones)
	root, infodict, success, mesg = fsolve(geneqns(stones[:3]), guess, maxfev=100000, full_output=True, xtol=1e-17) #TODO may need to use different solver that accommodates 16 digits of precision
	success = success == 1
	print("->", success, iters, root)
#	if any([not isintish(n) for n in root]) or round(root[6]) == t0 or round(root[7]) == t1 or round(root[8]) == t2:
	if any([not isintish(n) for n in root]):
		success = False
	if success:
		success = isgoodsolution(Hailstone(*root[0:6]))

print(iters)
print(root)
print(root[0]+root[1]+root[2])