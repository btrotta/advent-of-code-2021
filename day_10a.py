with open("data.txt", "r") as f:
    data = f.readlines()
arr = [a.strip() for a in data]


def match(a, b):
    return ([a, b] == ["(", ")"]) or ([a, b] == ["[", "]"]) or ([a, b] == ["{", "}"]) or ([a, b] == ["<", ">"])


def check_row(a):
    stack = []
    for ch in a:
        if ch in ['(', '[', '{', '<']:
            stack.append(ch)
        else:
            ch2 = stack.pop()
            if not(match(ch2, ch)):
                return {')': 3, ']': 57, '}': 1197, '>': 25137}[ch]
    return 0


ans = 0
for a in arr:
    ans += check_row(a)

print(ans)
