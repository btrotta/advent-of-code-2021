from collections import Counter
from copy import deepcopy

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

polymer = arr[0]

insertions = arr[2:]
rules = {}
for a in insertions:
    left, right = a.split(" -> ")
    rules[left] = right

polymer_pairs = Counter([polymer[i: i + 2] for i in range(len(polymer) - 1)])
letter_counter = Counter(list(polymer))
for step in range(40):
    new_letter_counter = deepcopy(letter_counter)
    new_polymer_pairs = deepcopy(polymer_pairs)
    for pair in polymer_pairs:
        if pair in rules:
            new_pairs = [pair[0] + rules[pair], rules[pair] + pair[1]]
            add_counter = {new_pairs[0]: polymer_pairs[pair], new_pairs[1]: polymer_pairs[pair]}
            subtract_counter = {pair: polymer_pairs[pair]}
            new_polymer_pairs.update(add_counter)
            new_polymer_pairs.subtract(subtract_counter)
            new_letter_counter.update({rules[pair]: polymer_pairs[pair]})
    letter_counter = new_letter_counter
    polymer_pairs = new_polymer_pairs

sorted_vals = list(reversed(sorted(letter_counter.values())))
print(sorted_vals[0] - sorted_vals[-1])
