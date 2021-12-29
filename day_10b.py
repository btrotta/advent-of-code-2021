import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [a.strip() for a in data]


def match(a, b):
    return ([a, b] == ["(", ")"]) or ([a, b] == ["[", "]"]) or ([a, b] == ["{", "}"]) or ([a, b] == ["<", ">"])


def complete_row(a):
    stack = []
    for ch in a:
        if ch in ['(', '[', '{', '<']:
            stack.append(ch)
        else:
            ch2 = stack.pop()
            if not(match(ch2, ch)):
                return -1
    score = 0
    for ch in reversed(stack):
        score *= 5
        score += {'(': 1, '[': 2, '{': 3, '<': 4}[ch]
    return score


scores = []
for a in arr:
    curr_score = complete_row(a)
    if curr_score > -1:
        scores.append(curr_score)

print(np.median(scores))
