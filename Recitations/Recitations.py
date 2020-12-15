file = open('input.txt')

seen = dict()
turn = -1
spoken = -1
lastNum = -1
input = [int(val) for val in file.readline().strip().split(',')]

while turn < 30000000:
    seen[lastNum] = turn - 1
    turn += 1
    if turn < len(input):
        lastNum = spoken
        spoken = input[turn]
    else:
        if spoken in seen:
            lastNum = spoken
            spoken = turn - 1 - seen[spoken]
        else:
            lastNum = spoken
            spoken = 0

print(lastNum)