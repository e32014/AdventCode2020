import copy


def lookDir(state, dir, pos, max):
    x, y = pos
    maxx, maxy = max
    while 0 <= x < maxx and 0 <= y < maxy:
        if (x, y) != pos:
            if state[y][x] == '#':
                return True
            if state[y][x] == 'L':
                return False

        if 'L' in dir:
            x -= 1
        elif 'R' in dir:
            x += 1
        if 'U' in dir:
            y -= 1
        elif 'D' in dir:
            y += 1
    return False


def updateState(state):
    updatedState = copy.deepcopy(state)
    for j in range(0, len(state)):
        for i in range(0, len(state[j])):
            if state[j][i] == '.':
                continue
            adj = 0

            adj += 1 if lookDir(state, 'L', (i, j), (len(state[j]), len(state))) else 0
            adj += 1 if lookDir(state, 'LU', (i, j), (len(state[j]), len(state))) else 0
            adj += 1 if lookDir(state, 'U', (i, j), (len(state[j]), len(state))) else 0
            adj += 1 if lookDir(state, 'UR', (i, j), (len(state[j]), len(state))) else 0
            adj += 1 if lookDir(state, 'R', (i, j), (len(state[j]), len(state))) else 0
            adj += 1 if lookDir(state, 'RD', (i, j), (len(state[j]), len(state))) else 0
            adj += 1 if lookDir(state, 'D', (i, j), (len(state[j]), len(state))) else 0
            adj += 1 if lookDir(state, 'DL', (i, j), (len(state[j]), len(state))) else 0

            if state[j][i] == 'L' and adj == 0:
                updatedState[j][i] = '#'
            elif state[j][i] == '#' and adj >= 5:
                updatedState[j][i] = 'L'
    return updatedState


def printMatrix (matrix):
    for line in matrix:
        print(line)


file = open('input.txt')

state = [list(line.strip()) for line in file]
lastState = []
reps = 0

while state != lastState:
    lastState = state
    reps += 1
    state = updateState(lastState)

print(reps)

total = 0
for line in state:
    total += sum([1 for val in line if val == '#'])
print(total)