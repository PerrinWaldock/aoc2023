import numpy as np
import re
from collections import deque, OrderedDict
from functools import cache
from copy import copy

VERBOSE = True

datafile = "input.txt"
#datafile = "sample.txt" #21

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

grid = np.array([np.array([l for l in line]) for line in lines])

steps = lines[0].split(",")

def hashgorithm(s):
	sum = 0
	for c in s:
		sum += ord(c)
		sum *= 17
		sum %= 256
	return sum

boxes = [OrderedDict() for _ in range(256)]

for step in steps:
	if "-" in step:
		label = step.split("-")[0]
		remove = True
	if "=" in step:
		label, focallen = step.split("=")
		remove = False
	boxno = hashgorithm(label)

	if VERBOSE:
		print(boxes[boxno])
	
	if remove:
		if label in boxes[boxno].keys():
			boxes[boxno].pop(label)
	else:
		boxes[boxno][label] = int(focallen)

	if VERBOSE:
		print(step)
		print(boxes[boxno])
		print("")

focalpower = 0
for ind, box in enumerate(boxes):
	if VERBOSE and len(box) > 0:
		print(ind, box)
	for jnd, (lens, fl) in enumerate(box.items()):
		focalpower += (ind+1)*(jnd+1)*fl
print(focalpower)


"""
answers:
391786 is too high
"""