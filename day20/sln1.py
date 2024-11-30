import numpy as np
import re
from collections import deque, namedtuple, OrderedDict
from functools import cache
from copy import copy

datafile = "input.txt"
#datafile = "sample1.txt" #8000*4000=32000000
#datafile = "sample2.txt" #4250*2750=11687500


getintsinline = lambda l: [int(n) for n in re.findall("\-*[0-9]+", l)]

lines = [line.strip() for line in open(datafile, "r")]

"""
TODO need some smart way of tracking WHERE the input comes from to make sure that the Conjunction understands
	maybe input comes as a tuple -- name + value?
	note: conjunctions need to be initialized with ALL of their inputs to False -- 

TODO need to change how system works -- outputs need to be handled SIMULTANEOUSLY, not sequentially as the logic currently requires
	probably append instructions to a list instead of treating as classes?...
"""

#this doesn't work because everything is processed immediately after pulse is sent

pulsecount = [0,0]

"""
class FlipFlop:
	def __init__(self, name, outputs):
		self.state = 0
		self.name = name
		self.outputs = outputs

	def out(self, inputname, inputstate):
		print(f"{inputname} sends {self.name} pulse {inputstate}")
		if not inputstate:
			self.state = 1 - self.state
			for op in self.outputs:
				pulsecount[self.state] += 1
				objects[op].out(self.name, self.state)

	def __repr__(self) -> str:
		return f"%{self.name} -> {','.join(self.outputs)} : {self.state}"

class Conjunction:
	def __init__(self, name, inputs, outputs):
		self.name = name
		self.inputs = {nm: 0 for nm in inputs}
		self.outputs = outputs

	def out(self, inputname, inputstate):
		print(f"{inputname} sends {self.name} pulse {inputstate}")
		self.inputs[inputname] = inputstate
		if np.product(list(self.inputs.values())) == 1:
			outval = 0
		else:
			outval = 1
		for op in self.outputs:
			pulsecount[outval] += 1
			objects[op].out(self.name, outval)

	def __repr__(self) -> str:
		return f"&{self.name} -> {','.join(self.outputs)} : {self.inputs}"

class Broadcaster:
	def __init__(self, name, outputs):
		self.name = name
		self.outputs = outputs

	def out(self, num):
		for _ in range(num):
			outval = 0
			pulsecount[outval] += 1 #one low pulse for pressing the button
			print(f"Button send broadcaster pulse 0")
			for op in self.outputs:
				pulsecount[outval] += 1
				objects[op].out(self.name, outval)

	def __repr__(self) -> str:
		return f"{self.name} -> {','.join(self.outputs)}"
	
class Output:
	def __init__(self, name):
		self.name = name	

	def out(self, inputname, inputstate):
		print(f"{inputname} sends {self.name} pulse {inputstate}")

	def __repr__(self) -> str:
		return f"{self.name} -> N/A"

objects = {}

if datafile == "sample2.txt":
	objects["output"] = Output("output")


for line in lines:
	name, outputs = line.split(" -> ")
	outputs = [o.strip() for o in outputs.split(",")]

	if name[0] == "%": #flipflow
		name = name[1:]
		objects[name] = FlipFlop(name, outputs)

	elif name[0] == "&": #conjunction
		name = name[1:]
		inputs = []
		for l in lines:
			n, ops = l.split(" -> ")
			n = n[1:]
			ops = [o.strip() for o in ops.split(",")]
			if name in ops:
				inputs.append(n)
		objects[name] = Conjunction(name, inputs, outputs)

	elif name == "broadcaster": #broadcaster
		objects[name] = Broadcaster(name, outputs)

for n, o in objects.items():
	print(o)
print("")
objects["broadcaster"].out(1)
for n, o in objects.items():
	print(o)
print("")
# objects["broadcaster"].out(1)
# for n, o in objects.items():
# 	print(o)

print(pulsecount)
print(pulsecount[0]*pulsecount[1])
"""


"""
architecture
process lines. Create a dict of classes that take an input value and input name and return a value and a series of outputs. 
a queue should have a single button press instruction loaded. outputs are paired with 
pulsecounts are updated in the main loop, not in the class
"""

class FlipFlop:
	def __init__(self, name, outputs):
		self.state = 0
		self.name = name
		self.outputs = outputs

	def out(self, inputname, inputstate):
		#print(f"{inputname} sends {self.name} pulse {inputstate}")
		if not inputstate:
			self.state = 1 - self.state
			outval = self.state
			return self.outputs, outval
		else:
			return None, None

	def __repr__(self) -> str:
		return f"%{self.name} -> {','.join(self.outputs)} : {self.state}"

class Conjunction:
	def __init__(self, name, inputs, outputs):
		self.name = name
		self.inputs = {nm: 0 for nm in inputs}
		self.outputs = outputs

	def out(self, inputname, inputstate):
		#print(f"{inputname} sends {self.name} pulse {inputstate}")
		self.inputs[inputname] = inputstate
		if np.product(list(self.inputs.values())) == 1:
			outval = 0
		else:
			outval = 1
		return self.outputs, outval

	def __repr__(self) -> str:
		return f"&{self.name} -> {','.join(self.outputs)} : {self.inputs}"
	
class Button:
	def __init__(self, name="Button", outputs=["broadcaster"]):
		self.name = name
		self.outputs = outputs

	def out(self, inputname, inputstate):
		outval = 0
		#print(f"Button send broadcaster pulse 0")
		return self.outputs, outval

	def __repr__(self) -> str:
		return f"{self.name} -> {','.join(self.outputs)}"

class Broadcaster:
	def __init__(self, name, outputs):
		self.name = name
		self.outputs = outputs

	def out(self, inputname, inputstate):
		outval = 0
		#print(f"{inputname} send broadcaster pulse {inputstate}")
		return self.outputs, outval

	def __repr__(self) -> str:
		return f"{self.name} -> {','.join(self.outputs)}"
		
class Output:
	def __init__(self, name):
		self.name = name	

	def out(self, inputname, inputstate):
		#print(f"{inputname} sends {self.name} pulse {inputstate}")
		return None, None

	def __repr__(self) -> str:
		return f"{self.name} -> N/A"

Pulse = namedtuple("Instruction", "source output value")

objects = {}

if datafile == "sample2.txt":
	objects["output"] = Output("output")


for line in lines:
	name, outputs = line.split(" -> ")
	outputs = [o.strip() for o in outputs.split(",")]

	if name[0] == "%": #flipflop
		name = name[1:]
		objects[name] = FlipFlop(name, outputs)

	elif name[0] == "&": #conjunction
		name = name[1:]
		inputs = []
		for l in lines:
			n, ops = l.split(" -> ")
			n = n[1:]
			ops = [o.strip() for o in ops.split(",")]
			if name in ops:
				inputs.append(n)
		objects[name] = Conjunction(name, inputs, outputs)

	elif name == "broadcaster": #broadcaster
		objects[name] = Broadcaster(name, outputs)

for n, o in objects.items():
	print(o)
print("")

instructions = deque()


for iter in range(1000):
	rxcount = 0
	instructions.appendleft(Pulse("button", "broadcaster", 0))
	while len(instructions):
		instr = instructions.pop()
		pulsecount[instr.value] += 1
		if instr.output == "rx":
			continue
		outputs, value = objects[instr.output].out(instr.source, instr.value)
		if outputs is not None and value is not None:
			for output in outputs:
				instructions.appendleft(Pulse(instr.output, output, value))
	if rxcount == 0:
		break


for n, o in objects.items():
	print(o)
print("")
# objects["broadcaster"].out(1)
# for n, o in objects.items():
# 	print(o)

print(pulsecount)
print(pulsecount[0]*pulsecount[1])