import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("[0-9]+", l)]

lines = [line for line in open(datafile, "r")]

time = int("".join(re.findall("[0-9]+", lines[0])))
distance = int("".join(re.findall("[0-9]+", lines[1])))
		
def distanceTravelled(holdtime, totaltime):
	return holdtime*(totaltime - holdtime)

winwayscount = deque()

print(time, distance)

ways2win = 0
for holdtime in range(time):
	if distanceTravelled(holdtime, time) > distance:
		ways2win += 1

print(ways2win)


		
		
		