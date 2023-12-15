import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("[0-9]+", l)]

lines = [line for line in open(datafile, "r")]

sequence = lines[0].strip()

inst = {}
		
for line in lines[2:]:
	key, choices = line.split("=")
	key = key.strip()
	choices = re.findall("[A-Z]+", choices)
	inst[key] = choices

steps = 0
key = "AAA"
while key != "ZZZ":
	dir = sequence[steps%len(sequence)]
	steps += 1

	print(key, dir)

	if dir == "L":
		key = inst[key][0]
	elif dir == "R":
		key = inst[key][1]


print(steps)


		
		
		