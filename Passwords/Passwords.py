import re
file = open("input.txt")

correct = 0
for line in file:
    match = re.search("(\\d+)-(\\d+) (\\w): (\\w+)", line)
    vals = line.split()
    pos1 = int(match.group(1)) - 1
    pos2 = int(match.group(2)) - 1
    targetChar = match.group(3)
    string = match.group(4)

    if bool(string[pos1] == targetChar) ^ bool(string[pos2] == targetChar):
        correct += 1

print(correct)