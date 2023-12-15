import numpy as np
import re
from collections import deque
import string

datafile = "input.txt"
#datafile = "sample3.txt"

powers = deque()

getintsinline = lambda l: [int(n) for n in re.findall("[0-9]+", l)]

lines = [line for line in open(datafile, "r")]

sequence = lines[0].strip()

inst = {}
		
for line in lines[2:]:
	key, choices = line.split("=")
	key = key.strip()
	choices = re.findall("[0-9A-Z]+", choices)
	inst[key] = choices

activekeys = [x for x in inst.keys() if x[2] == "A"]

print(activekeys)

# steps = 0
# while len([x for x in activekeys if x[2] == "Z"]) != len(activekeys):
# 	dir = sequence[steps%len(sequence)]
# 	steps += 1

# 	newkeys = deque()
# 	for key in activekeys:
# 		if dir == "L":
# 			newkey = inst[key][0]
# 		elif dir == "R":
# 			newkey = inst[key][1]
# 		newkeys.append(newkey)
	
# 	activekeys = list(set(newkeys))
# 	if (steps%10000) == 0:
# 		print(steps, dir, activekeys)

# 	#print(steps, dir, activekeys)

roots = {ak: deque() for ak in activekeys}

for ak in activekeys:
	steporder = {}
	steps = 0
	k = ak
	while True:
		dir = sequence[steps%len(sequence)]
		steporder[k+dir] = steps
		steps += 1
		if dir == "L":
			newkey = inst[k][0]
		elif dir == "R":
			newkey = inst[k][1]
		k = newkey
		if k[2] == "Z":
			roots[ak].append(steps)
			print(ak, k, steps)
			#if len(roots[ak]) > 10:
			#	break
			break
		#if k+dir in steporder.keys():
		#	print(steps)
		#	break

for k, rootlist in roots.items():
	print(k, rootlist)
vals = list(np.ravel(list(roots.values())))

print(vals)

vals = [int(v) for v in vals]

#remove all common factors

def removecommonfactors(nums):
	for ind in range(2,min(nums)):
		if sum([1 for v in nums if v%ind == 0]) == len(nums):
			print(ind)
			return removecommonfactors([v//ind for v in nums])
	return nums

def pythonproduct(nums):
	runningtotal = 1
	for n in nums:
		runningtotal *= n
	return runningtotal


def calculate_prime_factors(N):
    prime_factors = set()
    if N % 2 == 0:
        prime_factors.add(2)
    while N % 2 == 0:
        N = N // 2
        if N == 1:
            return prime_factors
    for factor in range(3, N + 1, 2):
        if N % factor == 0:
            prime_factors.add(factor)
            while N % factor == 0:
                N = N // factor
                if N == 1:
                    return prime_factors
factors = {}
for val in vals:
	factors[val] = calculate_prime_factors(val)




def reducednum(nums):
	maxval = int(max(nums))
	#maxval = 71958382637
	for ind in range(2,maxval):
		runningtotal = pythonproduct(nums)
		if runningtotal%ind: #can't reduce the number of loops by this number
			continue
		newnum = runningtotal/ind
		#print("factor:", ind, newnum)
		if sum([1 for v in nums if newnum%v == 0]) == len(nums):
			print(ind)
			return reducednum([v//ind for v in nums])
	return runningtotal

bignum = pythonproduct(vals)

for ind in range(7):
	print(ind, bignum/(281**ind), [bignum/(281**ind)/v for v in vals])

#pick the 

# print(reducednum(vals))



		
		
		
"""
wrong: 
35425771156910852049204797
71958382637
"""