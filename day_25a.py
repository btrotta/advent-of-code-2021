import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()

# represent blank space by 0, > by 1, and v by 2
arr = []
for line in data:
    row = []
    for ch in line.strip():
        if ch == ".":
            row.append(0)
        elif ch == ">":
            row.append(1)
        elif ch == "v":
            row.append(2)
    arr.append(row)

arr = np.array(arr, int)
step = 0
changed = True
while changed:
    changed = False
    # move east
    new_arr = arr.copy()
    for row in range(arr.shape[0]):
        for col in range(arr.shape[1]):
            next_col = (col + 1) % arr.shape[1]
            if (arr[row, col] == 1) and (arr[row, next_col] == 0):
                new_arr[row, next_col] = 1
                new_arr[row, col] = 0
                changed = True
    arr = new_arr
    # move south
    new_arr = arr.copy()
    for row in range(arr.shape[0]):
        next_row = (row + 1) % arr.shape[0]
        for col in range(arr.shape[1]):
            if (arr[row, col] == 2) and (arr[next_row, col] == 0):
                new_arr[next_row, col] = 2
                new_arr[row, col] = 0
                changed = True
    arr = new_arr
    step += 1

print(step)