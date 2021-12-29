with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]


count_0 = [0 for i in range(12)]
for a in arr:
    for i, x in enumerate(a):
        if x == "0":
            count_0[i] += 1

gamma = ""
epsilon = ""
for x in count_0:
    if x >= len(arr) // 2:
        gamma += "0"
        epsilon += "1"
    else:
        gamma += "1"
        epsilon += "0"

print(int(gamma, 2) * int(epsilon, 2))
