file = open("input.txt")

correct = 0
for line in file:
    vals = line.split()
    pos1 = int(vals[0].split("-")[0])-1
    pos2 = int(vals[0].split("-")[1])-1
    targetChar = vals[1].strip(":")
    string = vals[2]

    if bool(string[pos1] == targetChar) ^ bool(string[pos2] == targetChar):
        correct += 1

print(correct)