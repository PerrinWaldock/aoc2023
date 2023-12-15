f = open("input.txt").read().splitlines()
data = []
for x in f: 
  x = x.split()
  data.append([int(var) for var in x])

part1Vals = []
part2Vals = []
for x in data:
  enumerateList = []
  enumerateList.append(x)
  listToAppend = []
  while True:
    for i in range(len(x) -1):
      subtrack = x[i+1] - x[i]
      listToAppend.append(subtrack)
    x = listToAppend
    enumerateList.append(listToAppend)
    if all(v == 0 for v in listToAppend):
      p1v = 0
      p2v = 0
      for idx in range(len(enumerateList) -1, 0, -1):
        p1v +=  enumerateList[idx-1][-1]
        p2v =  enumerateList[idx-1][0] - p2v
      part1Vals.append(p1v)
      part2Vals.append(p2v)
      break
    listToAppend = []
  for line in enumerateList:
    print(line)
  print("\n")

# My time and rank in comments:
print(part1Vals)
print("Part 1: ", sum(part1Vals)) # 00:33:07   6265
print("Part 2: ", sum(part2Vals)) # 00:40:11   5982