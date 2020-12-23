file = open('input.txt')

cups = [int(val) for val in list(file.readline().strip())]
for i in range(len(cups)+1, 1000001):
    cups.append(i)
indices = [0] * 1000001
for i in range(0, len(cups)):
    if i == len(cups) -1:
        indices[cups[i]] = cups[0]
    else:
        indices[cups[i]] = cups[i+1]
turn = 0
start = cups[0]
while turn < 10000000:
    if turn % 100000 == 0:
        print(turn)
    cup1 = indices[start]
    cup2 = indices[cup1]
    cup3 = indices[cup2]
    indices[start] = indices[cup3]
    put = start - 1
    while put in [cup1, cup2, cup3] or put < 1:
        if put < 1:
            put = 1000000
        else:
            put = put - 1
    indices[cup3] = indices[put]
    indices[put] = cup1
    start = indices[start]
    turn += 1
print(indices[1] * indices[indices[1]])