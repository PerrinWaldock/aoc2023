import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

scores = deque()

lines = [line for line in open(datafile, "r")]

symbollist = [c for c in string.punctuation if c != "."]

partnumbers = deque()

for ind, line in enumerate(lines):

	cardstr, numsstr = line.split(":")
	cardnum = int(re.findall("[0-9]+", cardstr)[0])

	winnums, yournums = numsstr.split("|")

	winnums = [int(n) for n in re.findall("[0-9]+", winnums)]
	yournums = [int(n) for n in re.findall("[0-9]+", yournums)]

	matches = [n for n in yournums if n in winnums]
	score = 0
	if len(matches) > 0:
		score = 2**(len(matches) - 1)

	scores.append(score)

print(scores)
print(sum(scores))
		


		
		
		