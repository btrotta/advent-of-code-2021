import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()

# parse into list of brackets and numbers
parsed_arr = []
for a in data:
    a = a.strip()
    new_a = []
    i = 0
    while i < len(a):
        ch = a[i]
        if ch in ["[", "]", ","]:
            new_a.append(ch)
            i += 1
        else:
            prev_i = i
            while (i < len(a)) and a[i] not in ["[", "]", ","]:
                i += 1
            new_a.append(int(a[prev_i: i]))
    parsed_arr.append(new_a)


def make_tree(a, first_ind):
    # parse into a tree
    max_ind = first_ind
    start = [-1, None, None, first_ind]  # value, ptr to left child, ptr to right child, index, depth
    stack = [start]
    node_dict = {first_ind: stack[-1]}
    curr = stack[-1]
    for x in a:
        if x == "[":
            max_ind += 1
            curr[1] = [-1, None, None, max_ind]
            stack.append(curr[1])
            node_dict[max_ind] = curr[1]
            curr = stack[-1]
        elif x == "]":
            stack.pop()
            if len(stack) > 0:
                curr = stack[-1]
        elif x == ",":
            stack.pop()
            curr = stack[-1]
            max_ind += 1
            curr[2] = [-1, None, None, max_ind]
            stack.append(curr[2])
            node_dict[max_ind] = curr[2]
            curr = stack[-1]
        else:
            curr[0] = x
    return node_dict, start


def reduce(node_dict, start):
    changed = True
    max_ind = max(node_dict.keys()) + 1
    while changed:
        changed = False
        for action in ["explode", "split"]:
            # traverse tree in order
            # set of nodes visited - a node is visited after its left subtree has been visited
            visited = set()
            # set of nodes with both subtrees visited
            subtrees_visited = set()
            stack = [start]
            right_val = None
            depth = 0
            depth_of_visited_node = None
            number_nodes_visited = []
            while len(stack) > 0:
                node_visited = None
                curr = stack[-1]
                # check that node still exists (could have been removed by exploding)
                if curr[3] not in node_dict:
                    stack.pop()
                    continue
                if curr[0] != -1:
                    # curr is a number
                    visited.add(curr[3])
                    node_visited = curr
                    depth_of_visited_node = depth
                    subtrees_visited.add(curr[3])
                    number_nodes_visited.append(curr[3])
                    if (right_val is not None) and (number_node_to_add_right_val == len(number_nodes_visited)):
                        curr[0] += right_val
                        break
                    stack.pop()
                    depth -= 1
                    if len(stack) > 0:
                        curr = stack[-1]
                elif (curr[1][3] in subtrees_visited) and (curr[2][3] in subtrees_visited):
                    # left and right subtrees visited
                    subtrees_visited.add(curr[3])
                    stack.pop()
                    depth -= 1
                    if len(stack) > 0:
                        curr = stack[-1]
                elif curr[1][3] in subtrees_visited:
                    # only left subtree visited
                    visited.add(curr[3])
                    node_visited = curr
                    depth_of_visited_node = depth
                    stack.append(curr[2])
                    curr = stack[-1]
                    depth += 1
                else:
                    # no subtrees visited
                    stack.append(curr[1])
                    curr = stack[-1]
                    depth += 1
                if node_visited is not None:
                    if (action == "explode") and (depth_of_visited_node >= 4) and (node_visited[0] == -1) and (right_val is None):
                        left_val = node_visited[1][0]
                        right_val = node_visited[2][0]
                        if len(number_nodes_visited) > 1:
                            node_dict[number_nodes_visited[-2]][0] += left_val
                        number_node_to_add_right_val = len(number_nodes_visited) + 2
                        node_visited[0] = 0
                        node_dict.pop(node_visited[1][3])
                        node_dict.pop(node_visited[2][3])
                        node_visited[1] = None
                        node_visited[2] = None
                        visited.add(node_visited[3])
                        subtrees_visited.add(node_visited[3])
                        changed = True
                    elif (action == "split") and (node_visited[0] >= 10):
                        val = node_visited[0]
                        max_ind += 1
                        node_visited[1] = [int(np.floor(val / 2)), None, None, max_ind]
                        node_dict[max_ind] = node_visited[1]
                        max_ind += 1
                        node_visited[2] = [int(np.ceil(val / 2)), None, None, max_ind]
                        node_dict[max_ind] = node_visited[2]
                        node_visited[0] = -1
                        changed = True
                        break
            if changed:
                # we have already done an explode action, so don't do any more actions
                break

def find_magnitude(start):
    # find the magnitude
    visited = set()
    # set of nodes with both subtrees visited
    subtrees_visited = set()
    magnitude_dict = {}
    stack = [start]
    while len(stack) > 0:
        curr = stack[-1]
        if curr[0] != -1:
            # curr is a number
            visited.add(curr[3])
            subtrees_visited.add(curr[3])
            magnitude_dict[curr[3]] = curr[0]
            stack.pop()
            if len(stack) > 0:
                curr = stack[-1]
        elif (curr[1][3] in subtrees_visited) and (curr[2][3] in subtrees_visited):
            # left and right subtrees visited
            subtrees_visited.add(curr[3])
            magnitude_dict[curr[3]] = 3 * magnitude_dict[curr[1][3]] + 2 * magnitude_dict[curr[2][3]]
            stack.pop()
            if len(stack) > 0:
                curr = stack[-1]
        elif curr[1][3] in subtrees_visited:
            # only left subtree visited
            visited.add(curr[3])
            stack.append(curr[2])
            curr = stack[-1]
        else:
            # no subtrees visited
            stack.append(curr[1])
            curr = stack[-1]
    return magnitude_dict[start[3]]

# add the numbers
left_node_dict, left_start = make_tree(parsed_arr[0], 0)
for i in range(1, len(parsed_arr)):
    right_node_dict, right_start = make_tree(parsed_arr[i], max(left_node_dict.keys()) + 1)
    left_node_dict.update(right_node_dict)
    left_start = [-1, left_start, right_start,  max(left_node_dict.keys()) + 1]
    left_node_dict[max(left_node_dict.keys()) + 1] = left_start
    reduce(left_node_dict, left_start)

find_magnitude(left_start)
