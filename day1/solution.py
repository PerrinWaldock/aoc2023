import numpy as np
import re

from collections import deque

infile = "input.txt"

numbers = deque()

with open(infile, "r") as f:
	for line in f:
		nums = re.findall("[0-9]", line)
		print(nums)
		numbers.append(int(f"{nums[0]}{nums[-1]}"))

print(numbers)
print(sum(numbers))