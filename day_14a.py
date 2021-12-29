from collections import Counter

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

polymer = arr[0]

insertions = arr[2:]
rules = {}
for a in insertions:
    left, right = a.split(" -> ")
    rules[left] = right

ans = ""
for step in range(10):
    ans = ""
    for i in range(len(polymer) - 1):
        if polymer[i: i + 2] in rules:
            if i == 0:
                ans += polymer[i] + rules[polymer[i: i + 2]] + polymer[i + 1]
            else:
                ans += rules[polymer[i: i + 2]] + polymer[i + 1]
        else:
            if i == 0:
                ans += polymer[i: i + 2]
            else:
                ans += polymer[i + 1]
    polymer = ans

sorted_vals = list(reversed(sorted(Counter(list(ans)).values())))
print(sorted_vals[0] - sorted_vals[-1])
