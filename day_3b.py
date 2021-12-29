with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

arr_new = sorted(arr)
for i in range(12):
    for j, x in enumerate(arr_new):
        if x[i] == "1":
            break
    if j > len(arr_new) / 2:
        arr_new = arr_new[:j]
    else:
        arr_new = arr_new[j:]
    if len(arr_new) == 1:
        break
oxygen = arr_new[0]

arr_new = sorted(arr)
for i in range(12):
    for j, x in enumerate(arr_new):
        if x[i] == "1":
            break
    if j <= len(arr_new) / 2:
        arr_new = arr_new[:j]
    else:
        arr_new = arr_new[j:]
    if len(arr_new) == 1:
        break
c02 = arr_new[0]

print(int(oxygen, 2) * int(c02, 2))
