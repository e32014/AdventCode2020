import re, copy
file = open('input.txt')

foods = []
allergens = dict()
for line in file:
    match = re.match("((?:\\w+ )+)\\(contains((?: \\w+,?)+)\\)", line.strip())
    ingredients = set(match.group(1).strip().split(" "))
    allergies = set(match.group(2).strip().split(", "))
    foods.append(ingredients)
    for allergy in allergies:
        if allergy in allergens:
            allergens[allergy] = allergens[allergy].intersection(ingredients)
        else:
            allergens[allergy] = copy.deepcopy(ingredients)

print(allergens)
knownAllergy = dict()
while len(knownAllergy) < len(allergens):
    for allergy in allergens:
        if len(allergens[allergy]) == 1 and allergy not in knownAllergy:
            knownAllergy[allergy] = list(allergens[allergy])[0]
        else:
            allergens[allergy] = allergens[allergy].difference(knownAllergy.values())
outgoing = ""
for allergy in sorted(knownAllergy.keys()):
    outgoing += "," + knownAllergy[allergy]
print(outgoing[1:])