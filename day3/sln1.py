import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

lines = [line for line in open(datafile, "r")]

symbollist = [c for c in string.punctuation if c != "."]

partnumbers = deque()

for ind, line in enumerate(lines):
	#hunt for numbers
	for match in re.finditer("[0-9]+", line):
		surroundingchars = ""

		leftind = match.span()[0] - 1
		if leftind < 0:
			leftind = 0
		else:
			surroundingchars += line[leftind]

		rightind = match.span()[1]
		if rightind >= len(line):
			pass
		else:
			surroundingchars += line[rightind]

		if ind > 0: #get chars above
			surroundingchars += lines[ind-1][leftind:rightind+1]
		if ind < len(lines)-1: #get chars below
			surroundingchars += lines[ind+1][leftind:rightind+1]

		if sum([c in surroundingchars for c in symbollist]):
			partnumbers.append(int(match.group()))

		print(match.group(), surroundingchars)

print(partnumbers)
print(sum(partnumbers))
		


		
		
		