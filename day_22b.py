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

arr = np.array(arr, np.int64)
# add one to the right edges to make numpy indexing easier
arr[:, 2] += 1
arr[:, 4] += 1
arr[:, 6] += 1

# bin each x, y, z dimension into ranges with edges at the left and right
# bounds of each reboot instruction
x_edges = np.sort(np.unique(np.concatenate([arr[:, 1], arr[:, 2]])))
y_edges = np.sort(np.unique(np.concatenate([arr[:, 3], arr[:, 4]])))
z_edges = np.sort(np.unique(np.concatenate([arr[:, 5], arr[:, 6]])))

# find bin numbers
arr_for_bins = np.zeros(arr.shape, np.int64)
arr_for_bins[:, 0] = arr[:, 0]
arr_for_bins[:, 1] = np.searchsorted(x_edges, arr[:, 1])
arr_for_bins[:, 2] = np.searchsorted(x_edges, arr[:, 2])
arr_for_bins[:, 3] = np.searchsorted(y_edges, arr[:, 3])
arr_for_bins[:, 4] = np.searchsorted(y_edges, arr[:, 4])
arr_for_bins[:, 5] = np.searchsorted(z_edges, arr[:, 5])
arr_for_bins[:, 6] = np.searchsorted(z_edges, arr[:, 6])

grid = np.zeros((len(x_edges), len(y_edges), len(z_edges)), np.int64)
# size of each box in the grid
grid_size = np.matmul(np.matmul(np.diff(x_edges)[:, np.newaxis],
                                np.diff(y_edges)[np.newaxis, :])[:, :, np.newaxis],
                      np.diff(z_edges)[np.newaxis, np.newaxis, :])
for a in arr_for_bins:
    val = a[0]
    grid[a[1]:a[2], a[3]:a[4], a[5]:a[6]] = val

print(np.sum((grid[:-1, :-1, :-1] * grid_size).flatten()))
