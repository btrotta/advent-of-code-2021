with open("data.txt", "r") as f:
    data = f.readlines()
arr = [int(i) for i in data]

ans = 0
for i in range(1, len(arr)):
    if arr[i] > arr[i-1]:
        ans += 1
print(ans)
