with open("data.txt", "r") as f:
    data = f.readlines()

pos1 = int(data[0].split(": ")[1])
pos2 = int(data[1].split(": ")[1])

num_rolls = 0
score1 = 0
score2 = 0
die_num = 1
while (score1 < 1000) and (score2 < 1000):
    move = 0
    for dieroll in range(3):
        move += die_num
        die_num = (die_num % 100) + 1
    num_rolls += 3
    pos1 = ((pos1 + move - 1) % 10) + 1
    score1 += pos1
    if score1 >= 1000:
        break
    move = 0
    for dieroll in range(3):
        move += die_num
        die_num = (die_num % 100) + 1
    num_rolls += 3
    pos2 = ((pos2 + move - 1) % 10) + 1
    score2 += pos2

print(num_rolls * min(score1, score2))
