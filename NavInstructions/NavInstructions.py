file = open('input.txt')

waypoint = (10, 1)
pos = (0,0)

for line in file:
    command = line[0]
    val = int(line.strip()[1:])
    if command == 'N':
        waypoint = (waypoint[0], waypoint[1] + val)
    elif command == 'E':
        waypoint = (waypoint[0] + val, waypoint[1])
    elif command == 'S':
        waypoint = (waypoint[0], waypoint[1] - val)
    elif command == 'W':
        waypoint = (waypoint[0] - val, waypoint[1])
    elif command == 'L':
        if val == 90:
            waypoint = (-waypoint[1], waypoint[0])
        elif val == 180:
            waypoint = (-waypoint[0], -waypoint[1])
        elif val == 270:
            waypoint = (waypoint[1], -waypoint[0])
    elif command == 'R':
        if val == 90:
            waypoint = (waypoint[1], -waypoint[0])
        elif val == 180:
            waypoint = (-waypoint[0], -waypoint[1])
        elif val == 270:
            waypoint = (-waypoint[1], waypoint[0])
    elif command == 'F':
        pos = (pos[0] + val * waypoint[0], pos[1] + val * waypoint[1])

print(abs(pos[0]) + abs(pos[1]))