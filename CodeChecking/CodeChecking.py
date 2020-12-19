file = open('input.txt')


def validateRule(ruleList, rules, input, pos):
    isValid = False
    startPos = pos
    for rule in rules:
        validRule = True
        pos = startPos
        for part in rule:
            if isinstance(part, int):
                checkedRule, pos = validateRule(ruleList, ruleList[part], input, pos)
                validRule = validRule and checkedRule
                if not validRule:
                    break
            else:
                validRule = input[pos] == part
                pos += 1
        isValid = isValid or validRule
        if isValid:
            break
    return isValid, pos

line = file.readline().strip()
rules = dict()
while line != "":
    key = int(line.split(":")[0])
    vals = line.split(":")[1].strip().split(" ")
    rule = []
    ruleList = []
    for val in vals:
        if val == '|':
            ruleList.append(rule)
            rule = []
        else:
            if val.startswith("\""):
                rule.append(val[1:-1])
            else:
                rule.append(int(val))
    ruleList.append(rule)
    rules[key] = ruleList
    line = file.readline().strip()
print(rules)
count = 0
for line in file:
    count42 = 0
    count31 = 0
    pos = 0
    isValid = True
    lastPos = 0
    while isValid and pos < len(line.strip()):
        lastPos = pos
        isValid, pos = validateRule(rules, rules[42], line.strip(), pos)
        print(pos, isValid)
        if isValid:
            count42 += 1
    print("===================")
    isValid = True
    pos = lastPos
    while isValid and pos < len(line.strip()):
        lastPos = pos
        isValid, pos = validateRule(rules, rules[31], line.strip(), pos)
        print(pos, isValid)
        if isValid:
            count31 += 1
    if pos == len(line.strip()) and count42 > count31 and isValid:
        count += 1
    print(line.strip())
    print(count42)
    print(count31)
print(count)