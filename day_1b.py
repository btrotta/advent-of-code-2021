with open("data.txt", "r") as f:
    data = f.readlines()
arr = [int(i) for i in data]

ans = 0
for i in range(1, len(arr) - 2):
    if sum(arr[i: i + 3]) > sum(arr[i - 1: i + 2]):
        ans += 1
print(ans)
