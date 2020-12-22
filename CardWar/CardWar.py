file = open('input.txt')


def recursiveDecking(deck1, deck2):
    previousStates = set()
    while True:
        pDeck1 = [str(val) for val in deck1]
        pDeck2 = [str(val) for val in deck2]
        if (",".join(pDeck1), ",".join(pDeck2)) in previousStates:
            return True
        draw1 = deck1.pop(0)
        draw2 = deck2.pop(0)
        # Winner True means player 1 wins, otherwise its player 2
        winner = False
        if len(deck1) >= draw1 and len(deck2) >= draw2:
            winner = recursiveDecking(deck1[:draw1], deck2[:draw2])
        elif draw1 < draw2:
            winner = False
        elif draw1 > draw2:
            winner = True
        if winner:
            deck1 += [draw1, draw2]
        else:
            deck2 += [draw2, draw1]
        if len(deck1) == len(deck1) + len(deck2):
            return True
        elif len(deck2) == len(deck1) + len(deck2):
            return False
        previousStates.add((",".join(pDeck1), ",".join(pDeck2)))


deck1 = []
deck2 = []

line = file.readline()
currPlayer = 1
while line != "":
    if line == "\n":
        currPlayer = 2
    elif not line.startswith("Player"):
        if currPlayer == 1:
            deck1.append(int(line.strip()))
        else:
            deck2.append(int(line.strip()))
    line = file.readline()
print(deck1, deck2)

recursiveDecking(deck1, deck2)

print(deck1, deck2)

score = 0
winnerDeck = deck1 if len(deck1) > len(deck2) else deck2
for i in range(0, len(winnerDeck)):
    score += (len(winnerDeck) - i) * winnerDeck[i]
print(score)