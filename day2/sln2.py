import numpy as np
import re
from collections import deque

datafile = "input.txt"
#datafile = "sample.txt"

powers = deque()

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

	power = np.product(np.fromiter(maximums.values(), dtype=int))
	powers.append(power)
	

print(powers)
print(sum(powers))
