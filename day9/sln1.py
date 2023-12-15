import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line for line in open(datafile, "r")]

lineseqs = [getintsinline(line) for line in lines]

extvals = deque()
for ls in lineseqs:
	arrs = deque()
	arrs.append(np.ravel(ls))
	while any(arrs[-1] != 0):
		arrs.append(np.diff(arrs[-1]))

	arrs = list(arrs)
	#arrs = [arr for arr in arrs if len(arr) >= 1]
	#if arrs[-1][0] != 0:
	#	continue

	arrs[-1] = np.append(arrs[-1], 0)
	for ind in range(len(arrs)-1, 0, -1):
		arr = arrs[ind]
		arrs[ind-1] = np.append(arrs[ind-1], arrs[ind-1][-1] + arrs[ind][-1])
	extvals.append(arrs[0][-1])


	for arr in arrs:
		print(arr)
	print("")

print(extvals)
print(sum(list(extvals)))

"""
wrong answers:
1054536675
-255820491
679992033
1671633462
919

correct answer: 1972648895
"""