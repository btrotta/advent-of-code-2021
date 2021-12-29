import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [int(i) for i in data[0].split(",")]

med = np.median(arr)

print(sum(abs(x - med) for x in arr))
