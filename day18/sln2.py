import numpy as np
import re
from collections import deque
from functools import cache
from copy import copy

datafile = "input.txt"
#datafile = "sample.txt" #62
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

	distance = int(color[2:-2], 16)
	direction = "RDLU"[int(color[-2])]

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

#print(minx, miny)
#print(maxx, maxy)

oldx, oldy = coordinates.popleft()
sum = 0
for (x, y), distance, direction, color in zip(coordinates, distances, directions, colors):
	addamount = 0

	if x == oldx:
		if y < oldy:
			addamount = 0.5*np.abs(y - oldy)# + 1
		elif y > oldy:
			addamount = 0.5*np.abs(y - oldy)
	elif x > oldx:
		addamount = (x - oldx)*(y - miny + 1)
	elif x < oldx:
		addamount = (x - oldx)*(y - miny)
	#print(oldx, x, oldy, y, addamount)

	sum += addamount
	oldx, oldy = x, y

sum += 1

print(int(sum))