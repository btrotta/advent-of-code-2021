import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()

# members of arr are on/off, then x, y, z, ranges
arr = []
for line in data:
    if line == "\n":
        break
    curr = []
    if line.startswith("on"):
        curr.append(1)
    else:
        curr.append(0)
    coords = line.split(" ")[1].split(",")
    for c in coords:
        a, b = [int(x) for x in c.split("=")[1].split("..")]
        curr += [a, b]
    arr.append(curr)

grid = np.zeros((101, 101, 101), int)
for a in arr:
    val = a[0]
    grid[50 + a[1]: 50 + a[2] + 1,
         50 + a[3]: 50 + a[4] + 1,
         50 + a[5]: 50 + a[6] + 1] = val

print(sum(grid.flatten()))
