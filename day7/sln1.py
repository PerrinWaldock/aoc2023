import numpy as np
import re
from collections import deque
import string

from functools import cmp_to_key

datafile = "input.txt"
#datafile = "sample.txt"

def value(x):
	try:
		return int(x)
	except ValueError:
		if x == "T":
			return 10
		elif x == "J":
			return 11
		elif x == "Q":
			return 12
		elif x == "K":
			return 13
		elif x == "A":
			return 14

def handtype(h):
	unique = list(set(h))
	numbers = {c: len([x for x in h if x == c]) for c in unique}
	if set(numbers.values()) == {5}:
		return 7
	elif set(numbers.values()) == {4,1}:
		return 6
	elif set(numbers.values()) == {2, 3}:
		return 5
	elif sorted(numbers.values()) == [1, 1, 3]:
		return 4
	elif sorted(numbers.values()) == [1,2,2]:
		return 3
	elif sorted(numbers.values()) == [1, 1, 1, 2]:
		return 2
	else:
		return 1

def compare(a, b):
	a = [value(x) for x in a]
	b = [value(x) for x in b]

	if handtype(a) < handtype(b):
		return -1
	elif handtype(a) > handtype(b):
		return 1
	else:
		for x, y in zip(a, b):
			if x < y:
				return -1
			elif x > y:
				return 1
	#return 0


lines = [line for line in open(datafile, "r")]

handbids = {line.split(" ")[0]: int(line.split(" ")[1]) for line in lines}

sortedhands = sorted(list(handbids.keys()), key=cmp_to_key(compare))

winnings = 0
wins = deque()
for ind, hand in enumerate(sortedhands):
	win = (ind + 1)*handbids[hand]
	print(hand, handtype(hand), handbids[hand], win)
	wins.append(win)
	winnings += win


#print(len(list(set(sortedhands))))
print(winnings, np.sum(wins))