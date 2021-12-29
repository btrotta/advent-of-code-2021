with open("data.txt", "r") as f:
    data = f.readlines()
arr = [int(i) for i in data[0].split(",")]

best_dist = sum(abs(x - 0) * (abs(x - 0) + 1) / 2 for x in arr)
for i in range(0, max(arr)):
    curr_dist = sum(abs(x - i) * (abs(x - i) + 1) / 2 for x in arr)
    best_dist = min(curr_dist, best_dist)

print(best_dist)
