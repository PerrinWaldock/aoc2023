import numpy as np
import re
from collections import deque

datafile = "input.txt"
#datafile = "sample.txt" #21

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line for line in open(datafile, "r")]
#add second column/row any time there is one with no galaxies?

def countgroups(springs):
	groups = deque()
	lastworked = False
	for ind, c in enumerate(springs):
		if c == "#":
			if lastworked == False:
				groups.append(1)
				lastworked = True
			else:
				groups[-1] += 1
		else:
			lastworked = False
	return list(groups)
		

totalvalidconfigs = deque()
for line in lines:
	springs, conditions = line.split(" ")
	springs = np.array([s for s in springs])
	conditions = [int(n) for n in conditions.split(",")]

	unknownlocations = np.ravel(np.argwhere(springs == "?"))

	numunknown = len(unknownlocations)

	springstr = springs
	validconfigs = 0
	for ind in range(int(2**numunknown)):
		binary = np.binary_repr(ind, width=numunknown)
		for jnd, c in enumerate(binary):
			if c == "1":
				s = "#"
			else:
				s = "."
			springstr[unknownlocations[jnd]] = s
		groupcount = countgroups(springstr)
		if groupcount == conditions:
			validconfigs += 1
	totalvalidconfigs.append(validconfigs)

print(sum(totalvalidconfigs))
		
	
