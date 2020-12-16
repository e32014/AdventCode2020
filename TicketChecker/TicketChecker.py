import re
import copy

file = open('input.txt')

line = file.readline().strip()
fields = []
while line != "":
    match = re.match('^([a-zA-Z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$', line)
    fields.append((match.group(1), (int(match.group(2)), int(match.group(3))), (int(match.group(4)), int(match.group(5)))))
    line = file.readline().strip()

file.readline()
myTicket = file.readline().strip()
file.readline()
file.readline()
oTicket = file.readline().strip()
errorRate = 0
validTickets = []
while oTicket != "":
    ticket = [ int(val) for val in oTicket.split(',') ]
    valid = True
    for pos in range(0, len(ticket)):
        value = ticket[pos]
        matches = set()
        for field, range1, range2 in fields:
            if range1[0] <= value <= range1[1] or range2[0] <= value <= range2[1]:
                matches.add(field)
                break
        if len(matches) == 0:
            valid = False
            break
    if valid:
        validTickets.append(ticket)
    oTicket = file.readline().strip()

myTicket = [int(val) for val in myTicket.split(',')]
ticketNames = [copy.deepcopy(set([name for name, _, _ in fields])) for _ in range(0, len(myTicket))]
for ticket in validTickets:
    for pos in range(0, len(ticket)):
        value = ticket[pos]
        matches = set()
        for field, range1, range2 in fields:
            if range1[0] <= value <= range1[1] or range2[0] <= value <= range2[1]:
                matches.add(field)
        ticketNames[pos] = ticketNames[pos].intersection(matches)
removeFromOthers = set()
while len(removeFromOthers) < len(ticketNames):
    for pos in range(0, len(ticketNames)):
        if len(ticketNames[pos]) == 1:
            val = ticketNames[pos].pop()
            removeFromOthers.add(val)
            ticketNames[pos] = {val}
        elif len(ticketNames[pos]) > 1:
            ticketNames[pos] = ticketNames[pos].difference(removeFromOthers)

multSum = 1
for pos in range(0, len(ticketNames)):
    if ticketNames[pos].pop().startswith('departure'):
        multSum = myTicket[pos] * multSum
print(ticketNames)
print(myTicket)
print(multSum)