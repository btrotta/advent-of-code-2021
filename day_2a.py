with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

vert = 0
horz = 0
for s in arr:
    a, b = s.split(" ")
    if a == "forward":
        horz += int(b)
    elif a == "down":
        vert += int(b)
    else:
        vert -= int(b)
print(horz * vert)

