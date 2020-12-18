import re
file = open('input.txt')


def evalParen(equation):
    if equation[0] == '(':
        return evalMulti(equation[1:-1])
    else:
        return int(equation[0])


def evalAddi(equation):
    depth = 0
    pos = 0
    lastCheck = 0
    val = 0
    while pos < len(equation):
        if equation[pos] == '(':
            depth += 1
        elif equation[pos] == ')':
            depth -= 1
        elif equation[pos] == '+' and depth == 0:
            leftSide = evalParen(equation[lastCheck:pos])
            val += leftSide
            lastCheck = pos + 1
        pos += 1
    return val + evalParen(equation[lastCheck:pos])


def evalMulti(equation):
    depth = 0
    pos = 0
    lastCheck = 0
    val = 1
    while pos < len(equation):
        if equation[pos] == '(':
            depth += 1
        elif equation[pos] == ')':
            depth -= 1
        elif equation[pos] == '*' and depth == 0:
            leftSide = evalAddi(equation[lastCheck:pos])
            val *= leftSide
            lastCheck = pos + 1
        pos += 1
    return val * evalAddi(equation[lastCheck:pos])

total = 0
for line in file:
    equation = re.findall("\\d+|[+*()]", line)
    print(equation)
    result = evalMulti(equation)
    total += result

print(total)