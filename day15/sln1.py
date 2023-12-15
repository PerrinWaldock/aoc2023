import numpy as np
import re
from collections import deque
from functools import cache
from copy import copy

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

sumtotal = 0

for step in steps:
	sumtotal += hashgorithm(step)

print(sumtotal)