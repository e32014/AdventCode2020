import re
file = open('input.txt')

tiles = set()


def simulateLife(tiles):
    adjacents = dict()
    newTiles = set()
    for tile in tiles:
        x, y = tile
        if (x - 1, y) in tiles:
            adjacents.setdefault(tile, set()).add((x - 1, y))
        adjacents.setdefault((x - 1, y), set()).add(tile)
        if (x + 1, y) in tiles:
            adjacents.setdefault(tile, set()).add((x + 1, y))
        adjacents.setdefault((x + 1, y), set()).add(tile)
        if y % 2 == 0:
            if (x - 1, y - 1) in tiles:
                adjacents.setdefault(tile, set()).add((x - 1, y - 1))
            adjacents.setdefault((x - 1, y - 1), set()).add(tile)
            if (x, y - 1) in tiles:
                adjacents.setdefault(tile, set()).add((x, y - 1))
            adjacents.setdefault((x, y - 1), set()).add(tile)
            if (x, y + 1) in tiles:
                adjacents.setdefault(tile, set()).add((x, y + 1))
            adjacents.setdefault((x, y + 1), set()).add(tile)
            if (x - 1, y + 1) in tiles:
                adjacents.setdefault(tile, set()).add((x - 1, y + 1))
            adjacents.setdefault((x - 1, y + 1), set()).add(tile)
        else:
            if (x + 1, y - 1) in tiles:
                adjacents.setdefault(tile, set()).add((x + 1, y - 1))
            adjacents.setdefault((x + 1, y - 1), set()).add(tile)
            if (x, y - 1) in tiles:
                adjacents.setdefault(tile, set()).add((x, y - 1))
            adjacents.setdefault((x, y - 1), set()).add(tile)
            if (x, y + 1) in tiles:
                adjacents.setdefault(tile, set()).add((x, y + 1))
            adjacents.setdefault((x, y + 1), set()).add(tile)
            if (x + 1, y + 1) in tiles:
                adjacents.setdefault(tile, set()).add((x + 1, y + 1))
            adjacents.setdefault((x + 1, y + 1), set()).add(tile)

    for tile in adjacents:
        if tile in tiles and 0 < len(adjacents[tile]) <= 2:
            newTiles.add(tile)
        elif tile not in tiles and len(adjacents[tile]) == 2:
            newTiles.add(tile)
    return newTiles



#
# Grid Layout
# W is x - 1
# E is x + 1
# if y % 2 == 0
# NW is y - 1, x - 1
# NE is y - 1
# SE is y + 1
# SW is x - 1, y + 1
# if y % 2 == 1
# NW is y - 1
# NE is y - 1, x + 1
# SE is y + 1, x + 1
# SW is y + 1
for line in file:
    currPos = (0, 0)
    commands = re.findall("(e|w|se|sw|ne|nw)", line.strip())
    for command in commands:
        x, y = currPos
        if command == 'w':
            currPos = (x - 1, y)
        elif command == 'e':
            currPos = (x + 1, y)
        elif command == 'nw':
            if y % 2 == 0:
                currPos = (x - 1, y - 1)
            else:
                currPos = (x, y - 1)
        elif command == 'ne':
            if y % 2 == 0:
                currPos = (x, y - 1)
            else:
                currPos = (x + 1, y - 1)
        elif command == 'se':
            if y % 2 == 0:
                currPos = (x, y + 1)
            else:
                currPos = (x + 1, y + 1)
        elif command == 'sw':
            if y % 2 == 0:
                currPos = (x - 1, y + 1)
            else:
                currPos = (x, y + 1)
    if currPos not in tiles:
        tiles.add(currPos)
    else:
        tiles.remove(currPos)

for i in range(0, 100):
    tiles = simulateLife(tiles)
    print(len(tiles))