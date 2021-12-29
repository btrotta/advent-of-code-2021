from copy import deepcopy

with open("data.txt", "r") as f:
    data = f.readlines()

instructions = []
for line in data:
    words = line.strip().split(" ")
    for i, w in enumerate(words):
        if words[i].replace("-","").isdigit():
            words[i] = int(words[i])
    instructions.append(words)

# reorder instructions to move inputs later in list if this does not change the outcome
old_instructions = instructions
changed = True
while changed:
    changed = False
    for i, ins in enumerate(old_instructions):
        if ins[0] == "inp":
            a = ins[1]
            for j in range(i + 1, len(instructions)):
                ins2 = instructions[j]
                if (ins2[0] != "inp") and (a in [ins2[1], ins2[2]]):
                    break
            else:
                continue
            if j > i + 1:
                instructions = old_instructions[:i] + old_instructions[i + 1:j] + [instructions[i]] + instructions[j:]
                changed = True
    old_instructions = instructions

# remove instructions that multiply or divide a number by 1, or add 0
old_instructions = instructions
changed = True
while changed:
    changed = False
    for i, ins in enumerate(old_instructions):
        if ((ins[0] in ["div", "mul"]) and (ins[2] == 1)) or ((ins[0] == "add") and (ins[2] == 0)):
            instructions = old_instructions[:i] + instructions[(i + 1):]
            changed = True
            break
    old_instructions = instructions


max_set_size = 5000000

def update_with_intersection(s, t):
    # update s by intersecting with t
    # return s and a boolean indicating whether s has changed
    if (s is None) and (t is None):
        return s, False
    elif (s is None) and (t is not None):
        return deepcopy(t), True
    elif t is None:
        return s, False
    old_s = deepcopy(s)
    s = s.intersection(t)
    changed = len(s) != len(old_s)
    return s, changed


def forward_step(i, ranges):
    # calculate the allowable ranges after executing step i, based on the allowable
    # ranges for step i
    # if size of range is > max_set_size, store as None
    ins = instructions[i]
    curr = ranges[i]
    if i == 0:
        prev = {a: {0} for a in ["w", "x", "y", "z"]}
    else:
        prev = ranges[i - 1]
    if ins[0] == "inp":
        a = ins[1]
        curr[a], changed = update_with_intersection(curr[a], set(list(range(1, 10))))
    else:
        op, a, b = ins
        literal_b = b not in ["w", "x", "y", "z"]
        new_a = None
        if op == "add":
            if literal_b and prev[a] is not None:
                new_a = {x + b for x in prev[a]}
            elif (prev[a] is not None) and (prev[b] is not None):
                if len(prev[a]) * len(prev[b]) <= max_set_size:
                    new_a = {x + y for x in prev[a] for y in prev[b]}
        elif op == "mul":
            if literal_b and (b == 0):
                new_a = {0}
            if literal_b and (prev[a] is not None):
                new_a = {x * b for x in prev[a]}
            elif (prev[a] is not None) and (prev[b] is not None):
                if len(prev[a]) * len(prev[b]) <= max_set_size:
                    new_a = {x * y for x in prev[a] for y in prev[b]}
        elif op == "div":
            if literal_b and (prev[a] is not None):
                new_a = {x // b for x in prev[a]}
            elif (prev[a] is not None) and (prev[b] is not None):
                div = {x // y for x in prev[a] for y in prev[b] if y != 0}
                if len(div) <= max_set_size:
                    new_a = div
        elif op == "mod":
            if literal_b and (prev[a] is not None):
                new_a = {x % b for x in prev[a] if x >= 0}
            elif (prev[a] is not None) and (prev[b] is not None):
                new_a = {x % y for x in prev[a] for y in prev[b] if x >= 0 and y > 0}
            else:
                if literal_b:
                    if b <= max_set_size:
                        new_a = set(list(range(0, b)))
        elif op == "eql":
            new_a = {0, 1}
            if (prev[a] is not None) and (literal_b or prev[b] is not None):
                if literal_b:
                    intersection = {b}.intersection(prev[a])
                    union = {b}.union(prev[a])
                else:
                    intersection = prev[b].intersection(prev[a])
                    union = {b}.union(prev[a])
                if len(intersection) == 0:
                    new_a = {0}
                if len(union) == 1:
                    new_a = {1}
        curr[a], changed = update_with_intersection(curr[a], new_a)
    for var in ["w", "x", "y", "z"]:
        if var != a:
            curr[var], curr_changed = update_with_intersection(curr[var], prev[var])
            changed = max(changed, curr_changed)
    return changed


def backward_step(ranges, i):
    # propagate constraints backwards one step
    if i == 0:
        return False
    curr = ranges[i]
    prev = ranges[i - 1]
    ins = instructions[i]
    changed = False
    if ins[0] == "inp":
        a = ins[1]
    else:
        op, a, b = ins
        literal_b = b not in ["w", "x", "y", "z"]
        new_a = None
        new_b = None
        if op == "add":
            if literal_b and (curr[a] is not None):
                new_a = {x - b for x in curr[a]}
            elif (curr[a] is not None) and (curr[b] is not None):
                if len(curr[a]) * len(curr[b]) < max_set_size:
                    new_a = {x - y for x in curr[a] for y in curr[b]}
        elif op == "mul":
            if curr[a] == {0}:
                if literal_b and (b != 0):
                    prev[a] = {0}
                elif not literal_b:
                    if (prev[b] is not None) and (0 not in prev[b]):
                        prev[a] = {0}
                    if (prev[a] is not None) and (0 not in prev[a]):
                        prev[b] = {0}
            elif curr[a] == {1}:
                prev[a] = {1, -1}
                if not literal_b:
                    prev[b] = {1, -1}
            elif curr[a] is not None:
                if literal_b:
                    if b != 0:
                        new_a = {x // b for x in curr[a]}
                elif (curr[a] is not None) and (curr[b] is not None) and (0 not in curr[b]):
                    div = {x // y for x in curr[a] for y in curr[b]}
                    if len(div) < max_set_size:
                        new_a = div
                        if 0 in curr[a]:
                            new_a = new_a.union({0})
        elif op == "div":
            if literal_b and (prev[a] is not None) and (curr[a] is not None):
                new_a = {x for x in prev[a] if x // b in curr[a]}
            elif (prev[a] is not None) and (prev[b] is not None) and (curr[a] is not None):
                new_pairs = {(x, y) for x in prev[a] for y in prev[b] if y != 0 and x // y in curr[a]}
                if len(new_pairs) < max_set_size:
                    new_a = {p[0] for p in new_pairs}
                    new_b = {p[1] for p in new_pairs}
            elif literal_b and (curr[a] is not None):
                if abs(b) * len(curr[a]) < max_set_size:
                    new_a = {x * b + c for x in curr[a] for c in range(-abs(b) - 1, abs(b) + 1)
                             if (x * b + c) // b in curr[a]}
        elif op == "mod":
            # must have a >= 0 and b > 0 after previous step
            if literal_b and (prev[a] is not None) and (curr[a] is not None):
                new_a = {x for x in prev[a] if (x >= 0) and (x % b in curr[a])}
            elif prev[a] is not None:
                new_a = {x for x in prev[a] if x >= 0}
        elif op == "eql":
            if curr[a] == {1}:
                if literal_b:
                    new_a = {b}
                elif (prev[a] is not None) and (prev[b] is not None):
                    intersect = prev[a].intersection(prev[b])
                    new_a = intersect
                    new_b = intersect
            elif curr[a] == {0}:
                if literal_b and (prev[a] is not None):
                    new_a = prev[a].difference({b})
                elif (prev[a] is not None) and (prev[b] is not None) and (len(prev[b]) == 1):
                    new_a = prev[a].difference(prev[b])
                elif (prev[b] is not None) and (prev[a] is not None) and (len(prev[a]) == 1):
                    new_b = prev[b].difference(prev[a])
        prev[a], changed = update_with_intersection(prev[a], new_a)
        if not literal_b:
            prev[b], curr_changed = update_with_intersection(prev[b], new_b)
            changed = max(changed, curr_changed)
    for var in ["w", "x", "y", "z"]:
        if var != a:
            prev[var], curr_changed = update_with_intersection(prev[var], curr[var])
            changed = max(changed, curr_changed)
    return changed


# for each instruction, specify allowable ranges of variables just after executing the
# instruction
default_ranges = {a: None for a in ["w", "x", "y", "z"]}
ranges = [deepcopy(default_ranges) for i in range(len(instructions))]
# must have z = 0 after final step
ranges[-1]["z"] = {0}
changed = True
while changed:
    changed = False
    # apply constraints forward
    for i in range(len(instructions)):
        changed = forward_step(i, ranges)
    # apply constraints backward
    for j in range(len(instructions) - 1, -1, -1):
        changed = max(changed, backward_step(ranges, j))

print(sum(ranges[i][a] is None for i in range(len(ranges)) for a in list("wxyz")))
print(sum(len(ranges[i][a]) for i in range(len(ranges)) for a in list("wxyz")
          if ranges[i][a] is not None))
assert(all(len(ranges[i][a]) > 0 for i in range(len(ranges)) for a in list("wxyz")
           if ranges[i][a] is not None))


# current inputs being tried
# each element is a list of length 3 containing input value, instruction number of the
# input instruction, and dictionary of variable values just before input
# instruction is executed
first_input = [i for i in range(len(instructions)) if instructions[i][0] == "inp"][0]
curr_inputs = []
found = False
while not found:
    if len(curr_inputs) == 0:
        last_vars = {"x": 0, "y": 0, "z": 0, "w": 0}
        next_instruction = 0
        val = 9
    else:
        val, next_instruction, last_vars = curr_inputs[-1]
    vars = deepcopy(last_vars)
    if len(curr_inputs) < 10:
        print("".join(str(x[0]) for x in curr_inputs))
    for instruction_num in range(next_instruction, len(instructions)):
        invalid = False
        # do operation
        if instructions[instruction_num][0] == "inp":
            a = instructions[instruction_num][1]
            if instruction_num != next_instruction:
                curr_inputs.append([9, instruction_num, deepcopy(vars)])
                if len(curr_inputs) < 10:
                    print("".join(str(x[0]) for x in curr_inputs))
                val, next_instruction, last_vars = curr_inputs[-1]
                vars = deepcopy(last_vars)
            vars[a] = val
        else:
            op, a, b = instructions[instruction_num]
            a_val = vars[a]
            if b in vars:
                b_val = vars[b]
            else:
                b_val = b
            if op == "add":
                vars[a] += b_val
            elif op == "mul":
                vars[a] *= b_val
            elif op == "div":
                if b_val == 0:
                    invalid = True
                else:
                    vars[a] = a_val // b_val
            elif op == "mod":
                if (a_val < 0) or (b_val <= 0):
                    invalid = True
                else:
                    vars[a] = a_val % b_val
            elif op == "eql":
                vars[a] = int(a_val == b_val)
        for var in ["w", "x", "y", "z"]:
            if (ranges[instruction_num][var] is not None) and (vars[var] not in ranges[instruction_num][var]):
                invalid = True
        if invalid:
            while curr_inputs[-1][0] <= 1:
                curr_inputs.pop()
            curr_inputs[-1][0] -= 1
            break
    else:
        # end of instructions reached without executing any invalid ones
        if vars["z"] == 0:
            # optimal solution found
            found = True
            break
        else:
            while curr_inputs[-1][0] <= 1:
                curr_inputs.pop()
            curr_inputs[-1][0] -= 1


def test_num(num):
    digits = list(reversed(list(int(i) for i in list(str(num)))))
    vars = {x: 0 for x in list("wxyz")}
    for instruction_num in range(len(instructions)):
        invalid = False
        # do operation
        if instructions[instruction_num][0] == "inp":
            a = instructions[instruction_num][1]
            vars[a] = digits.pop()
        else:
            op, a, b = instructions[instruction_num]
            a_val = vars[a]
            if b in vars:
                b_val = vars[b]
            else:
                b_val = b
            if op == "add":
                vars[a] += b_val
            elif op == "mul":
                vars[a] *= b_val
            elif op == "div":
                if b_val == 0:
                    invalid = True
                else:
                    vars[a] = a_val // b_val
            elif op == "mod":
                if (a_val < 0) or (b_val <= 0):
                    invalid = True
                else:
                    vars[a] = a_val % b_val
            elif op == "eql":
                vars[a] = int(a_val == b_val)
            if invalid:
                return False
    if vars["z"] == 0:
        assert len(digits) == 0
        return True
    return False

num = int("".join(str(x[0]) for x in curr_inputs))
assert(len(str(num)) == 14)
assert(test_num(num))
print(num)
