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
			print(x,m,a,s)
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
	else:
		objs.append(text2obj(line))

print(objs)

keepobjs = deque()
for obj in objs:
	if parseline(obj, "in", workflows):
		keepobjs.append(obj)

sum = 0
for obj in keepobjs:
	sum += obj["x"] + obj["m"] + obj["a"] + obj["s"]

print(workflows)
print(objs)
print(sum)
	



