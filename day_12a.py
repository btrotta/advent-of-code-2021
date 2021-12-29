import itertools
from copy import deepcopy

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

edges = [a.split("-") for a in arr]
edges = edges + [[y, x] for [x, y] in edges]
nodes = list(set(itertools.chain.from_iterable([[a[0], a[1]] for a in edges])))
is_small = lambda ch: ch.lower() == ch

edge_dict = {n: [] for n in nodes}
for n1, n2 in edges:
    edge_dict[n1].append(n2)

# each path consists of a list of nodes visited in order, a set of all vertices,
# and a list of possible next vertices
paths = [[["start"], {"start"}, deepcopy(edge_dict["start"])]]
ans = 0
while len(paths) > 0:
    curr_path = paths.pop()
    for n in curr_path[-1]:
        if n == "end":
            ans += 1
            continue
        new_path = deepcopy(curr_path)
        new_path[0].append(n)
        new_path[1].add(n)
        new_path[2] = []
        for m in edge_dict[n]:
            if is_small(m):
                if m not in new_path[1]:
                    new_path[2].append(m)
            else:
                new_path[2].append(m)
        if new_path[-1] != []:
            paths.append(new_path)

print(ans)
