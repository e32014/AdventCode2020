file = open("input.txt")

values = [int(line.strip()) for line in file]
target = 32321523
for i in range(0, len(values)):
    total = 0
    j = i
    while total < target:
        total += values[j]
        j += 1
    if total == target:
        print(total, min(values[i:j]), max(values[i:j]))
        break