import collections

file = open("input.txt")

group = []
total = 0
members = 0
for line in file:
    if line == "\n":
        counter = collections.Counter(group)
        for key, value in counter.items():
            if value == members:
                total += 1
        group = []
        members = 0
    else:
        group = group + list(line.strip())
        members += 1

counter = collections.Counter(group)
for key, value in counter.items():
    if value == members:
        total += 1
print(total)