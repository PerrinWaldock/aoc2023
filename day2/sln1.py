import numpy as np
import re
from collections import deque

datafile = "input.txt"
#datafile = "sample.txt"

validids = deque()

validmaxes = {"red": 12, "green": 13, "blue": 14}

for line in open(datafile, "r"):
	game, data = line.split(":")
	gamenumber = int(re.findall("[0-9]+", game)[0])
	gamedatas = data.split(";")

	gamedata = {}

	for gd in gamedatas:
		colornums = gd.split(",")
		for cn in colornums:
			number, color = cn.strip().split(" ")
			if color not in gamedata.keys():
				gamedata[color] = deque()
			gamedata[color].append(int(number))

	maximums = {c: max(n) for c, n in gamedata.items()}

	validID = True
	for c, m in maximums.items():
		if m > validmaxes[c]:
			validID = False
	
	if validID:
		validids.append(gamenumber)

print(validids)
print(sum(validids))
