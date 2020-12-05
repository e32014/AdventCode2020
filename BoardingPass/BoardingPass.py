file = open("input.txt")

min_row = 0
max_row = 127
min_col = 0
max_col = 7

seats = []
for line in file:
    for i in range(0, 7):
        if line[i] == 'F':
            max_row = (min_row + max_row) // 2
        else:
            min_row = (min_row + max_row) // 2 + 1
    for j in range(7, 10):
        if line[j] == 'L':
            max_col = (min_col + max_col) // 2
        else:
            min_col = (min_col + max_col) // 2 + 1
    score = min_row * 8 + min_col
    seats.append((min_row, min_col, score))

    min_row = 0
    max_row = 127
    min_col = 0
    max_col = 7

seats.sort(key=lambda x: x[2])
potential = {seat[2] for seat in seats}
allSeats = set(range(0, 128 * 8))
potentials = allSeats.difference(potential)
print(potentials)