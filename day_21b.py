from collections import Counter
from itertools import product

# read data
with open("data.txt", "r") as f:
    data = f.readlines()

pos1 = int(data[0].split(": ")[1])
pos2 = int(data[1].split(": ")[1])

# After each player takes a turn of 3 die rolls, the sum of the die rolls must be
# between 3 and 9. There are 3**3 = 27 combinations in total; we calculate the number of
# combinations that result in each possible sum.
counts = Counter()
for comb in product([1, 2, 3], repeat=3):
    counts.update([sum(comb)])

# ways1[i, j, k] is number of ways player 1 can be on space j and have score k after
# player 1 has had i turns (each turn consisting of 3 die rolls)
ways1 = Counter()
for x in counts:
    space = ((pos1 + x - 1) % 10) + 1
    ways1.update({(1, space, space): counts[x]})
# possibilities[i] is set of possible spaces and scores after player 1 has had i turns
possibilities1 = [set([]), set(tuple(x[1:]) for x in ways1.keys())]
# ways2 is similar but for player 2
ways2 = Counter()
for x in counts:
    space = ((pos2 + x - 1) % 10) + 1
    ways2.update({(1, space, space): counts[x]})
possibilities2 = [set([]), set(tuple(x[1:]) for x in ways2.keys())]

# Each player adds at least 1 to their score after each turn, so each player has at
# most 21 turns before someone wins
for turn in range(2, 22):
    possibilities1.append(set())
    possibilities2.append(set())
    for space, score in possibilities1[turn - 1]:
        if score >= 21:
            continue
        for x in counts:
            new_space = ((space + x - 1) % 10) + 1
            new_score = score + new_space
            ways1.update({(turn, new_space, new_score): ways1[turn - 1, space, score] * counts[x]})
            possibilities1[turn].add((new_space, new_score))
    for space, score in possibilities2[turn - 1]:
        if score >= 21:
            continue
        for x in counts:
            new_space = ((space + x - 1) % 10) + 1
            new_score = score + new_space
            ways2.update({(turn, new_space, new_score): ways2[turn - 1, space, score] * counts[x]})
            possibilities2[turn].add((new_space, new_score))

num_wins_p1 = 0
for turn, space, score in ways1:
    if score >= 21:
        num_wins_p1 += ways1[turn, space, score] \
                       * sum(ways2[turn - 1, space2, score2] for space2, score2
                             in possibilities2[turn - 1] if score2 < 21)

num_wins_p2 = 0
for turn, space, score in ways2:
    if score >= 21:
        num_wins_p2 += ways2[turn, space, score] \
                       * sum(ways1[turn, space1, score1] for space1, score1
                             in possibilities1[turn] if score1 < 21)

print(max(num_wins_p1, num_wins_p2))
