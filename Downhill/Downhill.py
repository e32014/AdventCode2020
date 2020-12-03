file = open("input.txt")

map = [list(line.strip()) for line in file]

def downhill(map, right, down):
    x = 0
    y = 0
    count = 0
    while y < len(map) - down:
        y += down
        x = (x + right) % len(map[y])
        if map[y][x] == "#":
            count += 1
    return count

hill1 = downhill(map, 1, 1)
hill2 = downhill(map, 3, 1)
hill3 = downhill(map, 5, 1)
hill4 = downhill(map, 7, 1)
hill5 = downhill(map, 1, 2)
print(hill1 * hill2 * hill3 * hill4 * hill5)