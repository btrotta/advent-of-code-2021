import itertools

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

true_patterns = {0: {'a', 'b', 'c', 'e', 'f', 'g'},
                 1: {'c', 'f'},
                 2: {'a', 'c', 'd', 'e', 'g'},
                 3: {'a', 'c', 'd', 'f', 'g'},
                 4: {'b', 'c', 'd', 'f'},
                 5: {'a', 'b', 'd', 'f', 'g'},
                 6: {'a', 'b', 'd', 'e', 'f', 'g'},
                 7: {'a', 'c', 'f'},
                 8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
                 9: {'a', 'b', 'c', 'd', 'f', 'g'}}

true_patterns_reverse = {"".join(sorted(list(true_patterns[key]))): key for key in true_patterns}

ans = 0
for a in arr:
    in_val, out_val = a.split("|")
    all_codes = set("".join(sorted(x)) for x in in_val.strip().split(" ") + out_val.strip().split(" "))
    for p in itertools.permutations(list('abcdefg')):
        obs_to_true = {x: 'abcdefg'[i] for i, x in enumerate(p)}
        valid = True
        # check all codes translate into numbers
        nums = set()
        for code in all_codes:
            true_code = "".join(sorted(obs_to_true[ch] for ch in code))
            if true_code in true_patterns_reverse:
                nums.add(true_patterns_reverse[true_code])
            else:
                valid = False
                break
        if valid:
            break
    output_codes = [sorted(x) for x in out_val.strip().split(" ")]
    curr_output = 0
    for i, code in enumerate(reversed(output_codes)):
        true_code = "".join(sorted(obs_to_true[ch] for ch in code))
        curr_output += true_patterns_reverse[true_code] * (10 ** i)
    ans += curr_output

print(ans)
