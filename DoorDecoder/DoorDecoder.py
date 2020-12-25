file = open('input.txt')

def applyTransform(subjectNum, currNum):
    return (subjectNum * currNum) % 20201227


subjectNum = 7
currNum = 1
turns = 0

cardNum = int(file.readline().strip())
doorNum = int(file.readline().strip())

while currNum != cardNum and currNum != doorNum:
    currNum = applyTransform(subjectNum, currNum)
    turns += 1

print(turns)
consider = None
if currNum == cardNum:
    consider = doorNum
else:
    consider = cardNum
currNum = 1
for _ in range(0,turns):
    currNum = applyTransform(consider, currNum)

print(currNum)