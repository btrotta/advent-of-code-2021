import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()

arr = np.array([[int(ch) for ch in a.strip()] for a in data])

step = 0
while True:
    arr += 1
    step += 1
    while np.max(arr) > 9:
        changed = arr > 9
        while np.any(changed):
            arr = np.where(changed, 0, arr)
            for i in range(arr.shape[0]):
                for j in range(arr.shape[1]):
                    if (not(changed[i, j])) and (arr[i, j] != 0) and (arr[i, j] <= 9):
                        flashes = [[x, y] for x in range(max(0, i - 1), min(arr.shape[0], i + 2))
                                        for y in range(max(0, j - 1), min(arr.shape[1], j + 2))
                                        if changed[x, y]]
                        arr[i, j] += len(flashes)
            changed = arr > 9
    if np.max(arr) == 0:
        break
print(step)

