import numpy as np
import re
from collections import deque
from functools import cache
from copy import copy

datafile = "input.txt"
#datafile = "sample.txt" #94

getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

workflows = {}
objs = deque()

def text2fn(text):
	"""
	function should be passed x, m, a, s, workflows
	"""
	if ":" in text:
		evalstr, result = text.split(":")

		def fn(x=None, m=None, a=None, s=None, w=None):
			#print(x,m,a,s)
			if eval(evalstr):
				return result
			else:
				return None			
		return fn
	else:
		return lambda **x: text

def text2obj(text):
	nums = getintsinline(text)
	return {k: int(v) for k, v in zip("xmas", nums)}

def parseline(obj, wfkey, workflows):
	"""
	returns true if should keep and false if should reject
	"""
	wflow = workflows[wfkey]
	for fn in wflow:
		retval = fn(**obj, w=workflows)
		if retval == "A":
			return True
		elif retval == "R":
			return False
		elif retval is None:
			continue
		else:
			return parseline(obj, retval, workflows)

#critical numbers: last number before condition changes
crits = {k: deque() for k in "xmas"}

parseworkflows = True
for line in lines:
	if line == "":
		parseworkflows = False
		continue

	if parseworkflows:
		key, instrs = line.split("{")
		instrs = instrs[:-1]
		instrlist = [text2fn(text) for text in instrs.split(",")]
		workflows[key] = instrlist

		for group in re.findall("[x,m,a,s][<,>][0-9]+", line):
			num = getintsinline(group)[0]
			if "<" in group:
				num -= 1
			crits[group[0]].append(num)

	else:
		objs.append(text2obj(line))

#print(objs)

keepobjs = deque()
for obj in objs:
	if parseline(obj, "in", workflows):
		keepobjs.append(obj)

sum = 0
for obj in keepobjs:
	sum += obj["x"] + obj["m"] + obj["a"] + obj["s"]

#print(workflows)
#print(objs)
#print(sum)

crits = {k: sorted(v) for k,v in crits.items()}

for k in crits:
	#if crits[k][0] != 1:
	#	crits[k].insert(0, 1)
	if crits[k][-1] != 4000:
		crits[k].append(4000)
print(crits)

#doesn't work because need to test all permutations of critical numbers
# laststate = parseline({"x":4000, "m":4000, "a":4000, "s":4000}, "in", workflows)
# if laststate:
# 	sum = 4000**4
# else:
# 	sum = 0

# while len([k for k in crits if len(crits[k]) >= 1]) == 4:
# 	x = crits["x"][-1]
# 	m = crits["m"][-1]
# 	a = crits["a"][-1]
# 	s = crits["s"][-1]
# 	obj = {"x":x, "m":m, "a":a, "s":s}
# 	state = parseline(obj, "in", workflows)

# 	if state != laststate:
# 		if state:
# 			sum += x*m*a*s
# 		else:
# 			sum -= x*m*a*s
# 		laststate = state
# 	maxval = max([x,m,a,s])
# 	if x == maxval:
# 		crits["x"].pop()
# 	elif m == maxval:
# 		crits["m"].pop()
# 	elif a == maxval:
# 		crits["a"].pop()
# 	elif s == maxval:
# 		crits["s"].pop()
# 	print(obj, state, sum)

# print(sum, np.log(sum), np.log(167409079868000))
print(len(crits["x"])*len(crits["m"])*len(crits["a"])*len(crits["s"])) #just barely doable by brute force -- there's probably a better way
lastx = 0
sum = 0
for x in crits["x"]:
	lastm = 0
	for m in crits["m"]:
		print(x, m)
		lasta = 0
		for a in crits["a"]:
			lasts = 0
			for s in crits["s"]:
				obj = {"x":x, "m":m, "a":a, "s":s}
				state = parseline(obj, "in", workflows)
				if state:
					sum += (x - lastx)*(m - lastm)*(a - lasta)*(s - lasts)
				#print(obj, state, (x - lastx)*(m - lastm)*(a - lasta)*(s - lasts), sum)
				lasts = s
			lasta = a
		lastm = m
	lastx = x
print(sum)

"""
TODO need to compute area of some 4D volume where only the valid combos are counted
TODO try with 2D first
TODO how to count them properly?...
"""

"""
TODO parse instructions for CRITICAL VALUES of x, m, a, s
create an object for each CRITICAL VALUE
	<n means n is critical values >n means n+1 is the c


132392981697081 -> took 2 days to calculate
"""
