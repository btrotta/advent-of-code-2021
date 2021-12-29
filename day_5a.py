import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

grid = np.zeros((1000, 1000))

for a in arr:
    p, q = a.split(" -> ")
    x1, y1 = [int(i) for i in p.split(",")]
    x2, y2 = [int(i) for i in q.split(",")]
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        grid[x1, y1:y2 + 1] += 1
    elif y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1
        grid[x1:x2+1, y1] += 1

print(np.sum(grid >= 2))
