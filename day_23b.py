import numpy as np
from copy import deepcopy

from time import time

t = time()

with open("data.txt", "r") as f:
    data = f.readlines()

new_part = ["  #D#C#B#A#", "  #D#B#A#C#"]
data = data[:3] + new_part + data[3:]

# represent an arrangement of the amphipods by length-11 list representing hallway,
# list of 4 length-2 lists representing rooms left-to-right bottom-to-top, and
# integer representing cost
# represent A, B, C, D by 0, 1, 2, 3, and empty space by -1
initial_arrangement = [[], [], 0]
i = 0
for ch in data[1][1:12]:
    if ch in list("ABCD"):
        initial_arrangement[0].append(list("ABCD").index(ch))
        i += 1
    elif ch == ".":
        initial_arrangement[0].append(-1)
        i += 1
# bottom row of rooms
i = 0
for ch in data[5]:
    if ch in list("ABCD"):
        initial_arrangement[1].append([list("ABCD").index(ch)])
        i += 1
    elif ch == ".":
        initial_arrangement[1].append([-1])
        i += 1
# other rows of rooms, from bottom to top
for row in [4, 3, 2]:
    i = 0
    for ch in data[row]:
        if ch in list("ABCD"):
            initial_arrangement[1][i].append(list("ABCD").index(ch))
            i += 1
        elif ch == ".":
            initial_arrangement[1][i].append(-1)
            i += 1

# locations of room entrances relative to hallway
entrances = [2, 4, 6, 8]
costs = {0: 1, 1: 10, 2: 100, 3: 1000}
room_depth = 4

target_state = [[-1 for i in range(11)], [[j for i in range(room_depth)] for j in range(4)]]


def fill_from_hallway(curr):
    # move amphipods from hallway to destination rooms where possible
    changed = False  # has curr changed during call of this function
    changed_this_iter = True  # has curr changed in last iteration of while-loop
    hallway = curr[0]
    while changed_this_iter:
        changed_this_iter = False
        for amp in [0, 1, 2, 3]:
            room = curr[1][amp]
            if room[room_depth - 1] != -1:
                # room is full
                continue
            lowest_empty = room.index(-1)
            if lowest_empty == 0:
                available_pos = list(range(room_depth))
            else:
                if any(room[i] != amp for i in range(lowest_empty)):
                    # can't move anything on top of wrong amphipod type
                    continue
                else:
                    available_pos = list(range(lowest_empty, room_depth))
            for move_to in available_pos:
                i = entrances[amp]
                while (i > 0) and (hallway[i] == -1):
                    i -= 1
                if hallway[i] == amp:
                    hallway[i] = -1
                    room[move_to] = amp
                    changed_this_iter = True
                    changed = True
                    curr[2] += (abs(entrances[amp] - i) + room_depth - move_to) * costs[amp]
                    continue
                i = entrances[amp]
                while (i < len(hallway) - 1) and (hallway[i] == -1):
                    i += 1
                if hallway[i] == amp:
                    hallway[i] = -1
                    room[move_to] = amp
                    changed_this_iter = True
                    changed = True
                    curr[2] += (abs(entrances[amp] - i) + room_depth - move_to) * costs[amp]
                    continue
    return changed


def fill_from_top_of_rooms(curr):
    # move amphipods from tops of rooms to destination rooms where possible
    changed = False  # has curr changed during call of this function
    changed_this_iter = True  # has curr changed in last iteration of while-loop
    while changed_this_iter:
        changed_this_iter = False
        for amp in [0, 1, 2, 3]:
            room = curr[1][amp]
            if room[room_depth - 1] != -1:
                # room is full
                continue
            lowest_empty = room.index(-1)
            if (lowest_empty > 0) and any(room[i] != amp for i in range(lowest_empty)):
                # can't move anything on top of wrong amphipod type
                continue
            for other_amp in [0, 1, 2, 3]:
                if other_amp == amp:
                    continue
                other_room = curr[1][other_amp]
                min_entrance = min(entrances[amp], entrances[other_amp])
                max_entrance = max(entrances[amp], entrances[other_amp])
                if any(curr[0][i] != -1 for i in range(min_entrance, max_entrance + 1)):
                    # hallway is blocked
                    continue
                if other_room[room_depth - 1] != -1:
                    other_lowest_empty = room_depth
                else:
                    other_lowest_empty = other_room.index(-1)
                if other_lowest_empty == 0:
                    continue
                while (other_lowest_empty > 0) and (other_room[other_lowest_empty - 1] == amp):
                    room[lowest_empty] = amp
                    other_room[other_lowest_empty - 1] = -1
                    dist_moved = room_depth - (other_lowest_empty - 1) + abs(entrances[other_amp] - entrances[amp]) + room_depth - lowest_empty
                    curr[2] += dist_moved * costs[amp]
                    other_lowest_empty -= 1
                    lowest_empty += 1
                    changed = True
                    changed_this_iter = True
    return changed


# enumerate the possible solutions using depth-first search
min_energy = np.inf
to_visit = [initial_arrangement]
while len(to_visit) > 0:
    print(len(to_visit))
    curr = to_visit.pop()
    if curr[2] >= min_energy:
        continue
    changed = True
    while changed:
        changed = fill_from_hallway(curr)
        changed = max(changed, fill_from_top_of_rooms(curr))
    # check if this is a solution
    if curr[0:2] == target_state:
        min_energy = min(min_energy, curr[2])
        continue
    # iterate over amphipods in rooms other than their destination and possible
    # moves into hallway
    any_added = False
    for move_from_room in [0, 1, 2, 3]:
        room = curr[1][move_from_room]
        if room[0] == -1:
            # room is empty
            continue
        # move from highest filled position
        if room[room_depth - 1] != -1:
            move_from = room_depth - 1
        else:
            move_from = room.index(-1) - 1
        if all(room[i] == move_from_room for i in range(move_from + 1)):
            # all filled positions are of the correct amphipod type; can't move anything out
            continue
        moving_amp = room[move_from]
        i = entrances[move_from_room]
        hallway = curr[0]
        while (i >= 0) and (hallway[i] == -1):
            i -= 1
        if i == -1:
            min_pos = 0
        else:
            min_pos = i + 1
        i = entrances[move_from_room]
        while (i < len(hallway)) and (hallway[i] == -1):
            i += 1
        if i == len(hallway):
            max_pos = len(hallway) - 1
        else:
            max_pos = i - 1
        for new_pos in range(min_pos, max_pos + 1):
            if new_pos in entrances:
                continue
            # check feasibility - we cannot have two ampiphons that must cross over
            # each other to get to their destinations
            feasible = True
            if entrances[moving_amp] > new_pos:
                for j in range(new_pos + 1, entrances[moving_amp]):
                    if hallway[j] != -1:
                        right_amp = hallway[j]
                        if entrances[right_amp] < new_pos:
                            feasible = False
                            break
            elif entrances[moving_amp] < new_pos:
                for j in range(entrances[moving_amp], new_pos):
                    if hallway[j] != -1:
                        left_amp = hallway[j]
                        if entrances[left_amp] > new_pos:
                            feasible = False
                            break
            if feasible:
                new = deepcopy(curr)
                new[0][new_pos] = room[move_from]
                new[1][move_from_room][move_from] = -1
                new[2] += (abs(new_pos - entrances[
                    move_from_room]) + room_depth - move_from) * costs[new[0][new_pos]]
                to_visit.append(new)
                any_added = True

print(min_energy)
print(time() - t)
