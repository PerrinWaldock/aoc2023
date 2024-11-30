import numpy as np
import re
from collections import deque
from functools import cache
from copy import copy

datafile = "input.txt"
#datafile = "sample.txt" #94
#datafile = "sample2.txt" #71

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

def invertdir(d):
	if d == "U":
		return "D"
	elif d == "D":
		return "U"
	elif d == "L":
		return "R"
	elif d == "R":
		return "L"

minx = 0
maxx = 0
miny = 0
maxy = 0
x = 0
y = 0

coordinates = deque()
directions = deque()
distances = deque()
colors = deque()

coordinates.append((x, y))
for line in lines:
	direction, distance, color = line.split()
	distance = int(distance)
	if direction == "U":
		y += distance
	elif direction == "D":
		y -= distance
	elif direction == "L":
		x -= distance
	elif direction == "R":
		x += distance
	if x > maxx:
		maxx = x
	elif x < minx:
		minx = x
	if y > maxy:
		maxy = y
	elif y < miny:
		miny = y

	directions.append(direction)
	distances.append(distance)
	colors.append(color)
	coordinates.append((x, y))

print(minx, miny)
print(maxx, maxy)

grid = np.array([["."]*(maxx-minx+1)]*(maxy-miny+1))
grid2 = copy(grid)

def transform(x, y):
	return x-minx,maxy-y

oldx, oldy = coordinates.popleft()
for (x, y), distance, direction, color in zip(coordinates, distances, directions, colors):
	toldx, toldy = transform(oldx, oldy)
	tx, ty = transform(x, y)

	#print(f"({oldx},{oldy})->({toldx},{toldy}) {distance} {direction}")

	if y != oldy:
		for yn in np.arange(toldy, ty, np.sign(ty-toldy)):
			grid[yn,toldx] = direction
		for yn in np.arange(ty, toldy, -np.sign(ty-toldy)):
			grid2[yn,toldx] = invertdir(direction)
	elif x != oldx:
		for xn in np.arange(toldx, tx, np.sign(tx-toldx)):
			grid[toldy,xn] = direction
		for xn in np.arange(tx, toldx, -np.sign(tx-toldx)):
			grid2[toldy,xn] = invertdir(direction)
	else:
		print("???")
	#print(grid)

	oldx, oldy = x, y

print(grid)
np.savetxt('path.txt', grid, fmt='%s', delimiter='')

def isenclosedhoriwall(dirs1, dirs2):
	#dirs1 encloses one way, dirs2 encloses the other:
	wallcounter = 0
	for d1, d2 in zip(dirs1, dirs2):
		if "L" in d1+d2 and "R" in d1+d2: #horizontal wall
			if "R" in d1: #this logic may be suspect
				wallcounter += 1
			else:
				wallcounter -= 1
		elif d1 == "R" or d2 == "L": #bent wall
			wallcounter += 0.5
		elif d1 == "L" or d2 == "R":
			wallcounter -= 0.5
	return np.abs(wallcounter) % 2

def isenclosedvertwall(dirs1, dirs2):		
	#dirs1 encloses one way, dirs2 encloses the other:
	direction = ""
	wallcounter = 0
	for d1, d2 in zip(dirs1, dirs2):
		if "U" in d1+d2 and "D" in d1+d2: #horizontal wall
			if "U" in d1: #this logic may be suspect
				wallcounter += 1
			else:
				wallcounter -= 1
		elif d1 == "U" or d2 == "D": #bent wall
			wallcounter += 0.5
		elif d1 == "D" or d2 == "U":
			wallcounter -= 0.5
	return np.abs(wallcounter) % 2
	
for x in range(0, maxx-minx):
	for y in range(0, maxy-miny):
		if grid[y,x] != ".":
			continue
		if x == 0 or y == 0 or (y == maxy-miny+1) or (x == maxx - minx + 1): #outside
			continue
		if isenclosedhoriwall(grid[0:y,x], grid2[0:y,x]) and isenclosedvertwall(grid[y,0:x], grid2[y,0:x]):
			grid[y,x] = "I"

print(np.sum(np.ravel(grid!=".")))
np.savetxt('area.txt', grid, fmt='%s', delimiter='')


#TODO first create grid of the correct size


"""
TODO
	use the previous edge-finding and wall-finding code to find interior area
	create some sort of expanding grid class with get, set for elements and getgrid to get a numpy grid

NOTE
	RGB codes are going to need to enter into it somehow...


57377 is too high
47527?
"""