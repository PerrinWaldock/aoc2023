import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

"""
for each map, create a translation function (a2b and b2a)

"""

getintsinline = lambda l: [int(n) for n in re.findall("[0-9]+", l)]

scores = deque()

lines = [line for line in open(datafile, "r")]

seeds = getintsinline(lines[0].split(":")[1])

symbollist = [c for c in string.punctuation if c != "."]

mapnums = []


for ind, line in enumerate(lines[1:]):
	if "map:" in line:
		mapnums.append([])
		continue
	else:
		nums = getintsinline(line)
		if len(nums):
			mapnums[-1].append(nums)

mapnums = [sorted(nums, key=lambda x: x[0]) for nums in mapnums]

def mapfn(x, numslist):
	for nums in numslist:
		if x >= nums[1] and (x - nums[1]) < nums[2]:
			return nums[0] + (x - nums[1])
	return x

seedchain = {seed: deque() for seed in seeds}

for seed in seeds:
	seedchain[seed].append(seed)
	for numslist in mapnums:
		seedchain[seed].append(mapfn(seedchain[seed][-1], numslist))

best = list(seedchain.keys())[0]
for seed, chain in seedchain.items():
	print(seed, chain)
	if chain[-1] < seedchain[best][-1]:
		best = seed

print("")
print(best, seedchain[best])



		


		
		
		