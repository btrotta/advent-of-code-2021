with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

ans = 0
for a in arr:
    in_val, out_val = a.split("|")
    for x in out_val.strip().split(" "):
        x = x.replace(" ", "")
        if len(x) in [2, 3, 4, 7]:
            ans += 1

print(ans)



