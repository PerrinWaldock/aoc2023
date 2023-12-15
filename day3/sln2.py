import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

lines = [line for line in open(datafile, "r")]

symbollist = [c for c in string.punctuation if c != "."]

ratios = deque()

for ind, line in enumerate(lines):
	#hunt for numbers
	for m in re.finditer("\*", line):
		jnd = m.span()[0]

		#hunt for any number that is adjacent, then ID its first digit

		matches = deque()
		if ind > 0:
			matches.extend(re.finditer("[0-9]+", lines[ind-1]))
		matches.extend(re.finditer("[0-9]+", line))
		if ind < len(lines)-1:
			matches.extend(re.finditer("[0-9]+", lines[ind+1]))

		adjacentnums = deque()
		for nummatch in matches:
			if nummatch.span()[0] <= jnd+1 and nummatch.span()[1] >= jnd: 
				adjacentnums.append(int(nummatch.group()))
		if len(adjacentnums) == 2:
			ratios.append(np.product(adjacentnums))

print(ratios)
print(sum(ratios))
		


		
		
		