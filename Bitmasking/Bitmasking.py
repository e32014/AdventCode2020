import re
import copy
file = open('input.txt')

memory = dict()
mask = None
for line in file:
    if line.startswith('mask'):
        mask = re.match('^mask = ([X01]+)$', line.strip()).group(1)
    elif line.startswith('mem'):
        unmaskedPos, val = re.match('^mem\\[([0-9]+)\\] = ([0-9]+)$', line.strip()).groups()[0:2]
        unmaskedPos = int(unmaskedPos)
        val = int(val)
        oneMask = int(mask.replace('X', '0'), 2)
        oneMaskedPos = unmaskedPos | oneMask
        for i in range(0, 2**mask.count('X')):
            mask.count('X')
            replaceChars = ('{0:0' + str(mask.count('X')) + 'b}').format(i)
            newMask = ('{0:0' + str(len(mask)) + 'b}').format(oneMaskedPos)
            lastPos = 0
            for char in replaceChars:
                lastPos = mask.index('X', lastPos)
                newMask = newMask[:lastPos] + char + newMask[lastPos+1:]
                lastPos += 1
            memory[int(newMask, 2)] = val
total = 0
for entry in memory:
    total += memory[entry]
print(total)
