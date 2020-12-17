file = open('input.txt')

def countDirs(grid, pos):
    count = 0
    x, y, z, w = pos
    for wdiff in range(-1, 2):
        for zdiff in range(-1, 2):
            for xdiff in range(-1, 2):
                for ydiff in range(-1, 2):
                    if (x + xdiff, y + ydiff, z + zdiff, w + wdiff) in grid and (xdiff, ydiff, zdiff, wdiff) != (0, 0, 0, 0):
                        count += 1
    return count


def determineCorners(grid):
    xs = [x for x, _, _, _ in grid]
    ys = [y for _, y, _, _ in grid]
    zs = [z for _, _, z, _ in grid]
    ws = [w for _, _, _, w in grid]
    return (min(xs), min(ys), min(zs), min(ws)), (max(xs)+1, max(ys)+1, max(zs)+1, max(ws)+1)


def simulateStep(grid, upLeftCorner, downRightCorner):
    nextStep = set()
    for w in range(upLeftCorner[3] - 1, downRightCorner[3] + 1):
        for z in range(upLeftCorner[2] - 1, downRightCorner[2] + 1):
            for x in range(upLeftCorner[0] - 1, downRightCorner[0] + 1):
                for y in range(upLeftCorner[1] - 1, downRightCorner[1] + 1):
                    count = countDirs(grid, (x,y,z,w))
                    if (x,y,z,w) in grid and (count == 2 or count == 3):
                        nextStep.add((x,y,z,w))
                    if (x,y,z,w) not in grid and count == 3:
                        nextStep.add((x,y,z,w))
    newUpLeft, newDownRight = determineCorners(nextStep)
    return nextStep, newUpLeft, newDownRight



grid = set()
i = 0
max_y = 0
for line in file:
    j = 0
    max_y = len(line)
    for char in list(line):
        if char == '#':
            grid.add((i,j,0,0))
        j += 1
    i += 1
upLeft = (0, 0, 0, 0)
downRight = (i, max_y, 1, 1)
for _ in range(0, 6):
    grid, upLeft, downRight = simulateStep(grid, upLeft, downRight)
print(len(grid))