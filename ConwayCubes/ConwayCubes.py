import collections
file = open('input.txt')

def countDirs(grid, pos):
    poses = []
    x, y, z, w = pos
    for wdiff in range(-1, 2):
        for zdiff in range(-1, 2):
            for xdiff in range(-1, 2):
                for ydiff in range(-1, 2):
                    if (xdiff, ydiff, zdiff, wdiff) != (0, 0, 0, 0):
                        poses.append((x + xdiff, y + ydiff, z + zdiff, w + wdiff))
    return poses


def simulateStep(grid):
    nextStep = set()
    totalPoses = []
    for pos in grid:
        totalPoses = totalPoses + countDirs(grid, pos)

    posCounts = collections.Counter(totalPoses)
    for key in posCounts:
        if key in grid and (posCounts[key] == 2 or posCounts[key] == 3):
            nextStep.add(key)
        if key not in grid and posCounts[key] == 3:
            nextStep.add(key)
    return nextStep


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
for _ in range(0, 6):
    grid = simulateStep(grid)
print(len(grid))