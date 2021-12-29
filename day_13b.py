import numpy as np
import matplotlib.pyplot as plt

with open("data.txt", "r") as f:
    data = f.readlines()

coords = []
folds = []
for line in data:
    if line == "\n":
        continue
    elif line.startswith("fold along"):
        axis, num = line[len("fold along "):].strip().split("=")
        folds.append([axis, int(num)])
    else:
        coords.append([int(x) for x in line.strip().split(",")])

x_max = max(x for x, y in coords)
y_max = max(y for x, y in coords)
grid = np.zeros((y_max + 1, x_max + 1))
for x, y in coords:
    grid[y, x] = 1
for axis, p in folds:
    if axis == "x":
        # horizontal flip
        reversed_part = np.flip(grid[:, p + 1:], axis=1)
        if reversed_part.shape[1] < p:
            reversed_part = np.concatenate(np.zeros((reversed_part.shape[0], p - reversed_part.shape[1])))
        grid = np.maximum(reversed_part, grid[:, :p])
    else:
        # vertical flip
        reversed_part = np.flip(grid[p + 1:, :], axis=0)
        if reversed_part.shape[0] < p:
            reversed_part = np.concatenate(np.zeros((p - reversed_part.shape[0], reversed_part.shape[1])))
        grid = np.maximum(reversed_part, grid[:p, :])

plt.imshow(grid)

