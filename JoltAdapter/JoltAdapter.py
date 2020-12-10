import math

file = open('input.txt')

adapters = sorted([int(line) for line in file])
adapters = [0] + adapters + [max(adapters) + 3]
curr = 0
subGroups = []
previousStart = 0
for i in range(0, len(adapters) - 1):
    if adapters[i+1] - adapters[i] >= 3:
        subGroups.append(adapters[previousStart:i+1])
        previousStart = i + 1
subGroups.append(adapters[previousStart:])
total = 1
for group in subGroups:
    print(group, len(group))
    if len(group) == 3:
        total *= 2
    elif len(group) == 4:
        total *= 4
    elif len(group) == 5:
        total *= 7

print(total)


# 0, 1, 2, 3, 4
# 0, 2, 3, 4
# 0, 1, 3, 4
# 0, 1, 2, 4
# 0, 2, 4
# 0, 3, 4
# 0, 1, 4