file = open("input.txt")

vals = [int(line) for line in file]
vals = sorted(vals)

lowest = 0
mid = 1
highest = len(vals) - 1

sum = 0
while sum != 2020:
    sum = vals[lowest] + vals[mid] + vals[highest]
    if sum > 2020:
        highest -= 1
    elif sum < 2020 and lowest + 1 == mid:
        mid += 1
        lowest = 0
    elif sum < 2020 and lowest + 1 != mid:
        lowest += 1
    else:
        print(vals[lowest], vals[mid], vals[highest], vals[lowest] * vals[highest] * vals[mid])
