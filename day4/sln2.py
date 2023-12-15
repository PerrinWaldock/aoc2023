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
	score = len(matches)

	scores.append(score)


copies = [1]*len(lines)

for ind, score in enumerate(scores):
	if score > 0:
		for jnd in range(score):
			if ind+jnd+1 < len(copies):
				copies[ind+jnd+1] += 1*copies[ind] #add a copy of card for each copy of this card

print(scores)
print(copies)
print(sum(copies))
		


		
		
		