import copy

file = open("input.txt")

acc = 0
visited = set()
pc = 0

program = file.readlines()

for i in range(0, len(program)):
    progDupe = copy.deepcopy(program)
    repKey, repVal = program[i].strip().split(" ")[0:2]
    if repKey == 'nop':
        progDupe[i] = 'jmp '+repVal
    elif repKey == 'jmp':
        progDupe[i] = 'nop '+repVal
    else:
        continue
    while pc not in visited and pc < len(program):
        line = progDupe[pc]
        visited.add(pc)
        key, val = line.strip().split(" ")[0:2]
        if key == 'nop':
            pc += 1
        elif key == 'acc':
            acc += int(val)
            pc += 1
        elif key == 'jmp':
            pc += int(val)
    if pc >= len(program):
        print(acc, i)
        break
    pc = 0
    acc = 0
    visited = set()