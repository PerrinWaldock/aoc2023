import numpy as np
import re
from collections import deque
from functools import cache

datafile = "input.txt"
#datafile = "sample.txt" #21

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]
#add second column/row any time there is one with no galaxies?

def countgroups(springs):
	groups = deque()
	lastworked = False
	for ind, c in enumerate(springs):
		if c == "#":
			if lastworked == False:
				groups.append(1)
				lastworked = True
			else:
				groups[-1] += 1
		else:
			lastworked = False
	return list(groups)

def comparegroups(springs, refgroups):
	groups = deque()
	lastworked = False
	for ind, c in enumerate(springs):
		if c == "#":
			if lastworked == False:
				groups.append(1)
				lastworked = True
			else:
				groups[-1] += 1
		else:
			lastworked = False
			if len(groups) > len(refgroups) or (len(groups) > 0 and groups[-1] != refgroups[len(groups)-1]):
				return False
	if list(groups) != list(refgroups):
		return False
	else:
		return True

def genpermutations(working,broken):
	if working == 0 and broken == 0:
		return []
	elif working == 0:
		return ["."*broken]
	elif broken == 0:
		return ["#"*working]
	else:
		set1 = genpermutations(working-1, broken)
		set2 = genpermutations(working, broken-1)
		return ["#"+s for s in set1]+["."+s for s in set2]
	

def removeFromGroup(num, group):
	 #NOTE: negative numbers mean a problem
	if len(group) == 0:
		return (-1,)
	elif group[0] >= num:
		newgroup = (group[0]-num,) + group[1:]
		return newgroup
	else:
		return removeFromGroup(num - group[0], group[1:])
	
@cache
def validconfigs(springstr, groups, priorworking=False):
	"""
	use groups[0] == 0 to mean next MUST be a broken

	need to track:
		remainingstring
		remaining groups
		
	at each call
		check to make sure not in invalid configuration
		then, either
			insert a broken gear and try
			check to make sure it is possible to insert the next run of working gears
	"""

	#	nextunknown = springstr.find("?")


	numunknown = springstr.count("?")
	numknownworking = springstr.count("#")
	sumcombos = sum(groups)
	if numunknown + numknownworking < sumcombos or numknownworking > sumcombos:
		return 0
	elif numunknown == 0 and comparegroups(springstr, groups):
		return 1
	elif len(springstr) == 0 and (len(groups) == 0 or groups[0] == 0):
		return 1
	
	if priorworking:
		if groups[0] > 0:
			if (springstr[0] == "#" or springstr[0] == "?"):
				return validconfigs(springstr[1:], removeFromGroup(1, groups), priorworking=True)
			else: # cannot add broken gear to this group
				return 0
		elif groups[0] == 0:
			if (springstr[0] == "." or springstr[0] == "?"):
				return validconfigs(springstr[1:], groups[1:], priorworking=False) #clear slate to start
			else: # cannot add working gear to this group
				return 0
		else:
			print("PROBLEM!", springstr, groups, priorworking)
	else:
		if springstr[0] == ".":
			return validconfigs(springstr[1:], groups, priorworking=False)
		elif springstr[0] == "#":
			return validconfigs(springstr[1:], removeFromGroup(1, groups), priorworking=True)
		else: #=="?"
			return validconfigs(springstr[1:], groups, priorworking=False) + validconfigs(springstr[1:], removeFromGroup(1, groups), priorworking=True)

totalvalidconfigs = deque()

for line in lines:
	springs, conditions = line.split(" ")
	expandsprings = "?".join([springs]*5)
	conditions = conditions.strip()
	expandconditions = ",".join([conditions]*5)
	springs = expandsprings
	conditions = expandconditions

	#springs = np.array([s for s in springs])
	conditions = tuple([int(n) for n in conditions.split(",")])

	vcs = validconfigs(springs, conditions)

	totalvalidconfigs.append(vcs)

print(totalvalidconfigs)
print(sum(totalvalidconfigs))


"""
possibilities:
	disperse working gears more intelligently -- we know how many total are allowed
		DONE -- still not fast enough
	find each group. examine possibilities for each group independently
		troubles in dealing with ??????.??????
	combinatorics -- track each valid possibility for each group of unknowns, especially the beginning and end groups
	some sort of recursive divide-and-conquer using the known brokens and known workings?
	-> recursive algorithm that 
		(A) takes input as a list of numbers and list of positions
		(B) once known base case reached, easily calculate all possibilities
		pass tuple for groups, spring as string so hashable -> use @cache
"""
		
	
