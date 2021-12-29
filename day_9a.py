import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [[int(ch) for ch in row.strip()] for row in data]
arr = np.array(arr)
ans = 0
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        x_min = max(0, i - 1)
        x_max = min(arr.shape[0], i + 2)
        y_min = max(0, j - 1)
        y_max = min(arr.shape[1], j + 2)
        sub = arr[x_min:x_max, y_min:y_max].copy()
        if (arr[i, j] <= np.min(sub)) and (np.sum(sub == arr[i, j]) == 1):
            ans += arr[i, j] + 1

print(ans)

