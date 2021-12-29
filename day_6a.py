from collections import Counter

with open("data.txt", "r") as f:
    data = f.readlines()
arr = data[0].split(",")

arr = [int(a) for a in arr]

count_by_timer = Counter(arr)

for d in range(80):
    new_counts = Counter()
    new_counts[8] = count_by_timer[0]
    for t in range(0, 8):
        new_counts[t] = count_by_timer[t + 1]
    new_counts[6] += count_by_timer[0]
    count_by_timer = new_counts

print(sum(count_by_timer.values()))
