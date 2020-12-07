import re


def dfs_1(graph, key, visited, holdsGold):
    visited.add(key)
    hasGold = False
    for size, color in graph[key]:
        if color not in visited:
            visited, holdsGold = dfs_1(graph, color, visited, holdsGold)
        hasGold = hasGold or holdsGold[color]
    holdsGold[key] = hasGold
    return visited, holdsGold

def dfs_2(graph, key, visited, sizes):
    count = 1
    for size, color in graph[key]:
        if color not in visited:
            visited, sizes = dfs_2(graph, color, visited, sizes)
        count += int(size) * sizes[color]
    sizes[key] = count
    return visited, sizes


file = open('input.txt')

graph = dict()
reverse = dict()

for line in file:
    matchKey = re.match("^([\\w ]+) bags? contain",line.strip())
    matchValue = re.findall("([\\d]+) ([\\w ]+) bags?", line.strip())
    graph[matchKey.group(1)] = matchValue

print(graph)
visited = {"shiny gold"}
holdsGold = {"shiny gold": True}
for key, val in graph.items():
    if key not in visited:
        visited, holdsGold = dfs_1(graph, key, visited, holdsGold)

print(sum(val == True for _, val in holdsGold.items()) -1)

visited = {}
sizes = dict()
visited, sizes = dfs_2(graph, "shiny gold", visited, sizes)
print(sizes["shiny gold"] - 1)


