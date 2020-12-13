import math
file = open('input.txt')


def check(schedules, val, step, start):
    time = start
    while True:
        currTime = time + schedules.index(str(val))
        if currTime % val == 0:
            print(time)
            return time
        time += step

file.readline() # Discard that first line now
schedules = [val for val in file.readline().strip().split(',')]
valSchedules = [int(val) for val in schedules if val != 'x']

step = valSchedules[0]
start = valSchedules[0]
for val in valSchedules[1:]:
    start = check(schedules, val, step, start)
    step = step * val


#      17 x 13
# 102   6    8
# 323  19   25
# 544  32   42
# 765
# start is the lowest possible value for the first pair
# step is the multiplication of the values
