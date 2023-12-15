import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

"""
function (starting range, rangelist)
	for range in rangelist:
		if 

"""

getintsinline = lambda l: [int(n) for n in re.findall("[0-9]+", l)]

lines = [line for line in open(datafile, "r")]

seednums = getintsinline(lines[0].split(":")[1])
seedranges = np.reshape(seednums, (-1,2))
seedranges[:,1] += seedranges[:,0]
seedranges = list(seedranges)

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


def translate(x, numslist):
	for nums in numslist:
		if x >= nums[1] and (x - nums[1]) < nums[2]:
			return nums[0] + (x - nums[1])
	return x

#TODO create a merge ranges function
def mergeranges(ranges):
	outranges = []


	sortranges = sorted(ranges, key=lambda x: x[0])

	#purge zeros:
	sortranges = [r for r in sortranges if r[0] < r[1]]

	current_start = -1
	current_stop = -1

	for start, stop in sortranges:
		if start > current_stop:
			outranges.append((start, stop))
			current_start, current_stop = start, stop
		else:
			outranges[-1] = (current_start, stop)
			current_stop = max(current_stop, stop)

	
	return outranges

def mapfn(inranges, ruleslist):
	#inranges is a deque of ranges to consider
	#outranges is a deque of ranges that get spit out
	outranges = deque()

	print(f"{ind}: in ", inranges, "\trules ", ruleslist)

	for inrange in inranges:
		if inrange[0] == inrange[1]:
			continue

		filledrange = deque()
		for rnums in ruleslist:
			low, high = rnums[1], rnums[1] + rnums[2]

			if inrange[1] <= low or inrange[0] > high: # out of range
				continue
			#elif low <= inrange[0] and inrange[1] < high: #all in range
			#	outranges.append((translate(inrange[0], [rnums]), translate(inrange[1], [rnums])))
				#don't need to worry about untranslated numbers
			#	filledrange.append((inrange[0], inrange[1]))

				#break
			#elif inrange[0] <= low and inrange[1] <= high:#straddles low
			#	outranges.append((translate(low, [rnums]), translate(inrange[1], [rnums])))
			#	filledrange.append((low, inrange[1]))
			#elif low <= inrange[0] and high <= inrange[1]:	#straddles high
			#	outranges.append((translate(inrange[0], [rnums]), translate(high, [rnums])))
			#	filledrange.append((inrange[0], high))			
			else:
				outranges.append((translate(max(inrange[0], low), [rnums]), translate(min(inrange[1], high)-1, [rnums])+1))
				filledrange.append((max(inrange[0], low), min(inrange[1], high)))
		
		if len(filledrange) == 0:
			outranges.append(inrange)
		else:
			filledrange = mergeranges(filledrange)
			print(inrange, np.ravel(list(filledrange)))
			unfilled = [inrange[0], *list(np.ravel(list(filledrange))), inrange[1]]
			for pair in np.reshape(unfilled, (-1,2)):
				if pair[0] < pair[1]:
					outranges.append(list(pair))
		#print(inrange, filledrange, end=" ")
	#print("")

	mergedranges = mergeranges(outranges)
	print(f"{ind}: gen ", outranges, "\t merg ", mergedranges)

	return mergedranges

ranges = deque()
ranges.append(seedranges)

for ind, rulelists in enumerate(mapnums):
	#print(f"{ind}: ", end="")
	#print(ranges[-1], rulelists)
	newranges = mapfn(ranges[-1], rulelists)
	ranges.append(newranges)

print("")
print(ranges[-1])

print(min(np.ravel(list(ranges[-1]))))



		


		
		
		