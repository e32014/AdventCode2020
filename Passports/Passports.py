import re

file = open("input.txt")

required = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
validEyes = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

onPort = []
valid = 0
for line in file:
    if line == "\n":
        if len(set(onPort).intersection(required)) == len(required):
            valid += 1
        onPort = []
    else:
        for seg in line.split():
            key, val = seg.split(":")[0:2]
            if key == "byr" and len(val) == 4 and 1920 <= int(val) <= 2002:
                onPort.append(key)
            elif key == "iyr" and len(val) == 4 and 2010 <= int(val) <= 2020:
                onPort.append(key)
            elif key == "eyr" and len(val) == 4 and 2020 <= int(val) <= 2030:
                onPort.append(key)
            elif key == "hgt":
                if val.endswith("cm") and 150 <= int(val[0:-2]) <= 193:
                    onPort.append(key)
                elif val.endswith("in") and 59 <= int(val[0:-2]) <= 76:
                    onPort.append(key)
            elif key == "hcl" and re.match("^#[0-9a-f]{6}$", val):
                onPort.append(key)
            elif key == "ecl" and val in validEyes:
                onPort.append(key)
            elif key == "pid" and re.match("^[0-9]{9}$", val):
                onPort.append(key)
            elif key == "cid":
                onPort.append(key)

if len(set(onPort).intersection(required)) == len(required):
    valid += 1
print(valid)