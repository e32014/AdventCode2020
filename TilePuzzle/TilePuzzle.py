import re
import numpy as np
import copy

file = open('input.txt')


def printMap(img):
    for j in range(0, img.shape[0]):
        print("".join(img[j,:].tolist()))


def checkMonsters(img, monster):
    validPos = set()
    valid = 0
    isValid = True
    for y in range(img.shape[0] - 3):
        for x in range(0, img.shape[0] - 20):
            for offY in range(0, len(monster)):
                if y + offY >= img.shape[0]:
                    isValid = False
                    break
                for offX in range(0, len(monster[offY])):
                    if x + offX >= img.shape[1]:
                        isValid = False
                        break
                    if monster[offY][offX] == "1" and img[y + offY, x + offX] == "1":
                        validPos.add((y+offY, x+offX))
                    elif monster[offY][offX] == "1" and img[y + offY, x + offX] != "1":
                        isValid = False
                        break
                if not isValid:
                    break
            if isValid:
                print(x, y)
                valid += 1
                for posy, posx in validPos:
                    img[posy, posx] = 'M'
            validPos = set()
            isValid = True
    return valid, img

def flipHorizontal(tile):
    return tile[2], tile[1][::-1], tile[0], tile[3][::-1]


def flipVertical(tile):
    return tile[0][::-1], tile[3], tile[2][::-1], tile[1]


def rotateCounterclockwise(tile):
    return tile[1], tile[2][::-1], tile[3], tile[0][::-1]


def rotateClockwise(tile):
    return tile[3][::-1], tile[0], tile[1][::-1], tile[2]

tiles = dict()
tileImage = dict()
tile = []
line = file.readline()
solvedPuzzle = dict()
key = None
while True:
    if line == "\n" or line == "":
        # calculate edges
        bitString = "".join(tile[0])
        top = (int(bitString, 2), int(bitString[::-1], 2))

        bitString = "".join([val[0] for val in tile])
        left = (int(bitString, 2), int(bitString[::-1], 2))

        bitString = "".join([val[-1] for val in tile])
        right = (int(bitString, 2), int(bitString[::-1], 2))

        bitString = "".join(tile[-1])
        bottom = (int(bitString, 2), int(bitString[::-1], 2))
        tiles[key] = (top, right, bottom, left)
        tileImage[key] = np.array(tile)
        tile = []
        key = None
        if line == "":
            break
    elif re.match('^Tile (\\d+):$', line.strip()) is not None:
        key = int(re.match('^Tile (\\d+):$', line.strip()).group(1))
    else:
        tile.append(list(line.strip().replace(".", "0").replace("#", "1")))
    line = file.readline()

graphEdges = dict()
for tile in tiles:
    edges = tiles[tile]
    for otile in tiles:
        if otile != tile:
            oedges = tiles[otile]
            for edge in oedges:
                if edge in edges:
                    solvedPuzzle.setdefault(tile, set()).add((otile, edges.index(edge)))
                    if edges.index(edge) == 0:
                        graphEdges[(tile, otile)] = ('t', False)
                    elif edges.index(edge) == 1:
                        graphEdges[(tile, otile)] = ('r', False)
                    elif edges.index(edge) == 2:
                        graphEdges[(tile, otile)] = ('b', False)
                    else:
                        graphEdges[(tile, otile)] = ('l', False)
                    break
                elif edge[::-1] in edges:
                    solvedPuzzle.setdefault(tile, set()).add((otile, edges.index(edge[::-1])))
                    if edges.index(edge[::-1]) == 0:
                        graphEdges[(tile, otile)] = ('t', True)
                    elif edges.index(edge[::-1]) == 1:
                        graphEdges[(tile, otile)] = ('l', True)
                    elif edges.index(edge[::-1]) == 2:
                        graphEdges[(tile, otile)] = ('r', True)
                    else:
                        graphEdges[(tile, otile)] = ('b', True)
                    break

print(tiles)
print(solvedPuzzle)
queue = []
positions = dict()

considered = set()
for tile in tiles:
    if len(solvedPuzzle[tile]) == 2:
        considered.add(tile)
        dirs = [dir for _, dir in solvedPuzzle[tile]]
        queue = queue + [tile for tile, _ in solvedPuzzle[tile]]
        if 0 in dirs and 1 in dirs:
            print("flip horizontal")
            tiles[tile] = flipHorizontal(tiles[tile])
            positions[tile] = (0, 0, True, False, 0)
        elif 1 in dirs and 2 in dirs:
            print("It's fine")
            positions[tile] = (0, 0, False, False, 0)
        elif 2 in dirs and 3 in dirs:
            print("flip vertical")
            tiles[tile] = flipVertical(tiles[tile])
            positions[tile] = (0, 0, False, True, 0)
        elif 3 in dirs and 0 in dirs:
            print("rotate 180")
            tiles[tile] = flipVertical(flipHorizontal(tiles[tile]))
            positions[tile] = (0, 0, True, True, 0)
        break

print(queue)
print(positions)
while queue:
    consider = queue.pop(0)
    if consider in considered:
        continue
    previous = [tile for tile, _ in solvedPuzzle[consider] if tile in considered]
    dirs = [dir for _, dir in solvedPuzzle[consider]]
    if len(previous) == 1:
        previousTile = previous[0]
        previousInfo = positions[previousTile]
        dirFromPrevious = None
        dirToPrevious = None
        for edge in tiles[consider]:
            if edge in tiles[previousTile]:
                dirFromPrevious = (tiles[previousTile].index(edge), False)
                dirToPrevious = (tiles[consider].index(edge), False)
            elif edge[::-1] in tiles[previousTile]:
                dirFromPrevious = (tiles[previousTile].index(edge[::-1]), True)
                dirToPrevious = (tiles[consider].index(edge), True)
        missingEdges = [dir for dir in range(0, 4) if dir not in dirs]
        if len(missingEdges) == 1:
            if dirFromPrevious[0] == 1:
                if missingEdges[0] == 0:
                    if dirToPrevious[0] == 3:
                        print("no change")
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, False, 0)
                    elif dirToPrevious[0] == 1:
                        print("flip vertical")
                        tiles[consider] = flipVertical(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, True, 0)
                elif missingEdges[0] == 2:
                    if dirToPrevious[0] == 3:
                        print("flip horizontal")
                        tiles[consider] = flipHorizontal(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], True, False, 0)
                    elif dirToPrevious[0] == 1:
                        print("rotate 180")
                        tiles[consider] = flipHorizontal(flipVertical(tiles[consider]))
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], True, True, 0)
                elif missingEdges[0] == 1:
                    if dirToPrevious[0] == 0:
                        print("rotate -90")
                        tiles[consider] = rotateCounterclockwise(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, False, -90)
                    elif dirToPrevious[0] == 2:
                        print("rotate -90 and flip vertical")
                        tiles[consider] = flipVertical(rotateCounterclockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, True, -90)
                elif missingEdges[0] == 3:
                    if dirToPrevious[0] == 0:
                        print("rotate -90 and flip horizontal")
                        tiles[consider] = flipHorizontal(rotateCounterclockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], True, False, -90)
                    elif dirToPrevious[0] == 2:
                        print("rotate 90")
                        tiles[consider] = rotateClockwise(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, False, 90)
            elif dirFromPrevious[0] == 2:
                if missingEdges[0] == 3:
                    if dirToPrevious[0] == 0:
                        print("no change")
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, False, 0)
                    elif dirToPrevious[0] == 2:
                        print("flip horizontal")
                        tiles[consider] = flipHorizontal(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, True, False, 0)
                if missingEdges[0] == 1:
                    if dirToPrevious[0] == 0:
                        print("flip vertical")
                        tiles[consider] = flipVertical(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, True, 0)
                    elif dirToPrevious[0] == 2:
                        print("rotate 180")
                        tiles[consider] = flipVertical(flipHorizontal(tiles[consider]))
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, True, True, 0)
                elif missingEdges[0] == 0:
                    if dirToPrevious[0] == 1:
                        print("rotate -90")
                        tiles[consider] = rotateCounterclockwise(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, False, 0)
                    elif dirToPrevious[0] == 3:
                        print("rotate -90 and flip horizontal")
                        tiles[consider] = flipHorizontal(rotateCounterclockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, True, False, -90)
                elif missingEdges[0] == 2:
                    if dirToPrevious[0] == 1:
                        print("rotate -90 and flip vertical")
                        tiles[consider] = flipVertical(rotateCounterclockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, True, -90)
                    elif dirToPrevious[0] == 3:
                        print("rotate 90")
                        tiles[consider] = rotateClockwise(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, False, 90)
        elif len(missingEdges) == 2:
            if dirFromPrevious[0] == 1:
                if 0 in missingEdges and 1 in missingEdges:
                    if dirToPrevious[0] == 3:
                        print("no change")
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, False, 0)
                    elif dirToPrevious[0] == 2:
                        print("rotate 90 and flip horizontal")
                        tiles[consider] = flipHorizontal(rotateClockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], True, False, 90)
                elif 1 in missingEdges and 2 in missingEdges:
                    if dirToPrevious[0] == 3:
                        print("flip horizontal")
                        tiles[consider] = flipHorizontal(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], True, False, 0)
                    elif dirToPrevious[0] == 0:
                        print("rotate -90")
                        tiles[consider] = rotateCounterclockwise(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, False, -90)
                elif 2 in missingEdges and 3 in missingEdges:
                    if dirToPrevious[0] == 0:
                        print("rotate -90 and flip horizontal")
                        tiles[consider] = flipHorizontal(rotateCounterclockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], True, False, -90)
                    elif dirToPrevious[0] == 1:
                        print("rotate 180")
                        tiles[consider] = flipHorizontal(flipVertical(tiles[consider]))
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], True, True, 0)
                elif 3 in missingEdges and 0 in missingEdges:
                    if dirToPrevious[0] == 1:
                        print("flip vertical")
                        tiles[consider] = flipVertical(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, True, 0)
                    elif dirToPrevious[0] == 2:
                        print("rotate 90")
                        tiles[consider] = rotateClockwise(tiles[consider])
                        positions[consider] = (previousInfo[0] + 1, previousInfo[1], False, False, 90)
            if dirFromPrevious[0] == 2:
                if 0 in missingEdges and 1 in missingEdges:
                    if dirToPrevious[0] == 2:
                        print("rotate 180")
                        tiles[consider] = flipVertical(flipHorizontal(tiles[consider]))
                        positions[consider] = (previousInfo[0], previousInfo[1] +1, True, True, 0)
                    elif dirToPrevious[0] == 3:
                        print("rotate 90 and flip vertical")
                        tiles[consider] = flipVertical(rotateClockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0], previousInfo[1] +1, False, True, 90)
                elif 1 in missingEdges and 2 in missingEdges:
                    if dirToPrevious[0] == 3:
                        print("rotate 90")
                        tiles[consider] = rotateClockwise(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, False, 90)
                    elif dirToPrevious[0] == 0:
                        print("flip vertical")
                        tiles[consider] = flipVertical(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, True, 0)
                elif 2 in missingEdges and 3 in missingEdges:
                    if dirToPrevious[0] == 0:
                        print("no change")
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, False, 0)
                    elif dirToPrevious[0] == 1:
                        print("rotate -90 then flip vertical")
                        tiles[consider] = flipVertical(rotateCounterclockwise(tiles[consider]))
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, True, 0)
                elif 3 in missingEdges and 0 in missingEdges:
                    if dirToPrevious[0] == 1:
                        print("rotate -90")
                        tiles[consider] = rotateCounterclockwise(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, False, False, -90)
                    elif dirToPrevious[0] == 2:
                        print("flip horizontal")
                        tiles[consider] = flipHorizontal(tiles[consider])
                        positions[consider] = (previousInfo[0], previousInfo[1] + 1, True, False, 0)
    elif len(previous) == 2:
        side1 = previous[0]
        side2 = previous[1]
        side1Info = positions[side1]
        side2Info = positions[side2]
        side1FromPrevious = None
        side1ToPrevious = None
        side2FromPrevious = None
        side2ToPrevious = None
        for edge in tiles[consider]:
            if edge in tiles[side1]:
                side1FromPrevious = (tiles[side1].index(edge), False)
                side1ToPrevious = (tiles[consider].index(edge), False)
            elif edge[::-1] in tiles[side1]:
                side1FromPrevious = (tiles[side1].index(edge[::-1]), True)
                side1ToPrevious = (tiles[consider].index(edge), True)
            if edge in tiles[side2]:
                side2FromPrevious = (tiles[side2].index(edge), False)
                side2ToPrevious = (tiles[consider].index(edge), False)
            elif edge[::-1] in tiles[side2]:
                side2FromPrevious = (tiles[side2].index(edge[::-1]), True)
                side2ToPrevious = (tiles[consider].index(edge), True)
        if side1FromPrevious[0] == 1 and side2FromPrevious[0] == 2:
            if side1ToPrevious[0] == 3:
                if side2ToPrevious[0] == 0:
                    print("no change")
                    positions[consider] = (side2Info[0], side1Info[1], False, False, 0)
                elif side2ToPrevious[0] == 2:
                    print("flip horizontal")
                    tiles[consider] = flipHorizontal(tiles[consider])
                    positions[consider] = (side2Info[0], side1Info[1], True, False, 0)
            elif side1ToPrevious[0] == 0:
                if side2ToPrevious[0] == 1:
                    print("rotate -90")
                    tiles[consider] = rotateCounterclockwise(tiles[consider])
                    positions[consider] = (side2Info[0], side1Info[1], False, False, -90)
                elif side2ToPrevious[0] == 3:
                    print("rotate 90 and flip vertical")
                    tiles[consider] = flipVertical(rotateClockwise(tiles[consider]))
                    positions[consider] = (side2Info[0], side1Info[1], False, True, 90)
            elif side1ToPrevious[0] == 1:
                if side2ToPrevious[0] == 0:
                    print("flip vertical")
                    tiles[consider] = flipVertical(tiles[consider])
                    positions[consider] = (side2Info[0], side1Info[1], False, True, 0)
                elif side2ToPrevious[0] == 2:
                    print("rotate 180")
                    tiles[consider] = flipVertical(flipHorizontal(tiles[consider]))
                    positions[consider] = (side2Info[0], side1Info[1], True, True, 0)
            elif side1ToPrevious[0] == 2:
                if side2ToPrevious[0] == 1:
                    print("rotate -90 and flip vertical")
                    tiles[consider] = flipVertical(rotateCounterclockwise(tiles[consider]))
                    positions[consider] = (side2Info[0], side1Info[1], False, True, -90)
                elif side2ToPrevious[0] == 3:
                    print("rotate 90")
                    tiles[consider] = rotateClockwise(tiles[consider])
                    positions[consider] = (side2Info[0], side1Info[1], False, False, 90)
        elif side1FromPrevious[0] == 2 and side2FromPrevious[0] == 1:
            if side2ToPrevious[0] == 3:
                if side1ToPrevious[0] == 0:
                    print("no change")
                    positions[consider] = (side1Info[0], side2Info[1], False, False, 0)
                elif side1ToPrevious[0] == 2:
                    print("flip horizontal")
                    tiles[consider] = flipHorizontal(tiles[consider])
                    positions[consider] = (side1Info[0], side2Info[1], True, False, 0)
            elif side2ToPrevious[0] == 0:
                if side1ToPrevious[0] == 1:
                    print("rotate -90")
                    tiles[consider] = rotateCounterclockwise(tiles[consider])
                    positions[consider] = (side1Info[0], side2Info[1], False, False, -90)
                elif side1ToPrevious[0] == 3:
                    print("rotate 90 and flip vertical")
                    tiles[consider] = flipVertical(rotateClockwise(tiles[consider]))
                    positions[consider] = (side1Info[0], side2Info[1], False, True, 90)
            elif side2ToPrevious[0] == 1:
                if side1ToPrevious[0] == 0:
                    print("flip vertical")
                    tiles[consider] = flipVertical(tiles[consider])
                    positions[consider] = (side1Info[0], side2Info[1], False, True, 0)
                elif side1ToPrevious[0] == 2:
                    print("rotate 180")
                    tiles[consider] = flipVertical(flipHorizontal(tiles[consider]))
                    positions[consider] = (side1Info[0], side2Info[1], True, True, 0)
            elif side2ToPrevious[0] == 2:
                if side1ToPrevious[0] == 1:
                    print("rotate -90 and flip vertical")
                    tiles[consider] = flipVertical(rotateCounterclockwise(tiles[consider]))
                    positions[consider] = (side1Info[0], side2Info[1], False, True, -90)
                elif side1ToPrevious[0] == 3:
                    print("rotate 90")
                    tiles[consider] = rotateClockwise(tiles[consider])
                    positions[consider] = (side1Info[0], side2Info[1], False, False, 90)
    considered.add(consider)
    queue = queue + [tile for tile, _ in solvedPuzzle[consider] if tile not in considered]
imageArr = [[0 for _ in range(0, int(len(tiles) ** .5))] for _ in range(0, int(len(tiles) ** .5))]

for tile in positions:
    x, y, flipHoriz, flipVert, rotate = positions[tile]
    img = tileImage[tile]
    if rotate == -90:
        img = np.rot90(img)
    elif rotate == 90:
        img = np.rot90(img, -1)
    if flipHoriz:
        img = np.flipud(img)
    if flipVert:
        img = np.fliplr(img)
    imageArr[y][x] = img

ogImage = []
for j in range(0, len(imageArr)):
    for subj in range(1, 9):
        line = []
        for i in range(0, len(imageArr)):
            line = line + imageArr[j][i][subj, 1:9].tolist()
        ogImage.append(line)

ogImage = np.array(ogImage)

seaMonster = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "1", " "],
              ["1", " ", " ", " ", " ", "1", "1", " ", " ", " ", " ", "1", "1", " ", " ", " ", " ", "1", "1", "1"],
              [" ", "1", " ", " ", "1", " ", " ", "1", " ", " ", "1", " ", " ", "1", " ", " ", "1", " ", " ", " "]]

mutations = ["None", "90V", "90H", "-90H", "-90HV", "H", "V", "HV"]
for mutation in mutations:
    img = copy.deepcopy(ogImage)
    if mutation.startswith("90"):
        img = np.rot90(img, -1)
    elif mutation.startswith("-90"):
        img = np.rot90(img)
    if 'H' in mutation:
        img = np.flipud(img)
    if 'V' in mutation:
        img = np.fliplr(img)
    count, markedMonsters = checkMonsters(img, seaMonster)
    if count > 0:
        print(count)
        printMap(markedMonsters)
        print(mutation)
        onesRemaining = 0
        for row in img:
            for col in row:
                if col == '1':
                    onesRemaining += 1
        print(onesRemaining)
