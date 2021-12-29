import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [[int(ch) for ch in row.strip()] for row in data]
arr = np.array(arr)
basin_num = np.zeros(arr.shape)
basin_num[:] = -2
basin_num = np.where(arr == 9, -1, basin_num)
visited = np.zeros(arr.shape)

curr_basin = 0
while np.min(basin_num) == -2:
    # find an unassigned value
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if basin_num[i, j] == -2:
                break
        if basin_num[i, j] == -2:
            break
    basin_num[i, j] = curr_basin
    # find all the adjoining points
    to_visit = [[x, y] for x in range(max(0, i - 1), min(arr.shape[0], i + 2))
                for y in range(max(0, j - 1), min(arr.shape[1], j + 2))
                if (basin_num[x, y] == -2) and (abs(x - i) + abs(y - j) == 1)]
    while len(to_visit) > 0:
        i, j = to_visit.pop()
        basin_num[i, j] = curr_basin
        to_visit += [[x, y] for x in range(max(0, i - 1), min(arr.shape[0], i + 2))
                     for y in range(max(0, j - 1), min(arr.shape[1], j + 2))
                     if (basin_num[x, y] == -2) and (abs(x - i) + abs(y - j) == 1)]
    curr_basin += 1

basin_count = [np.sum(basin_num == i) for i in range(curr_basin + 1)]
print(np.prod(np.sort(basin_count)[-3:]))
