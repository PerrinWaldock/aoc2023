import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("[0-9]+", l)]

lines = [line for line in open(datafile, "r")]

times = getintsinline(lines[0])
distances = getintsinline(lines[1])
		
def distanceTravelled(holdtime, totaltime):
	return holdtime*(totaltime - holdtime)

winwayscount = deque()

for time, distance in zip(times, distances):
	ways2win = 0
	for holdtime in range(time):
		if distanceTravelled(holdtime, time) > distance:
			ways2win += 1

	winwayscount.append(ways2win)

print(np.product(winwayscount))


		
		
		