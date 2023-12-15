import numpy as np
import regex as re #allows overlapping

from collections import deque

infile = "input.txt"
#infile = "sample2.txt"

numbers = deque()

spellednumbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def getnum1(line):
	nums = re.findall(f"[0-9]", line)
	numstring = f"{nums[0]}{nums[-1]}"
	number = int(numstring)
	return number

#NOTE: does not match overlapping
def getnum2(line):
	nums = re.findall(f"[0-9]|{'|'.join(spellednumbers)}", line, overlapped=True)
	numstring = f"{nums[0]}{nums[-1]}"
	for ind, string in enumerate(spellednumbers):
		numstring = numstring.replace(string, str(ind))
	number = int(numstring)
	print(line.strip(), nums, number)
	return number


with open(infile, "r") as f:
	for line in f:
		numbers.append(getnum2(line))

print(sum(numbers))

#54412 is too low?