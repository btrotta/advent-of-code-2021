import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()

coords = []
for line in data:
    if line.startswith("---"):
        curr_coords = []
    elif line == "\n":
        coords.append(np.array(curr_coords, dtype=np.int32))
    else:
        curr_coords.append([int(i) for i in line.strip().split(",")])
coords.append(np.array(curr_coords, dtype=np.int32))


def transforms(coords):
    # generate list of transformations of axes
    transformation_list = []
    # permutations of the axes
    axes_perms = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    for perm in axes_perms:
        new_coords = np.zeros(coords.shape).astype(int)
        new_coords[:, 0] = coords[:, perm[0]]
        new_coords[:, 1] = coords[:, perm[1]]
        new_coords[:, 2] = coords[:, perm[2]]
        # for permutations that interchange 2 axes, need to reverse the third axis
        if perm == [0, 2, 1]:
            new_coords[:, 0] *= -1
        elif perm == [1, 0, 2]:
            new_coords[:, 2] *= -1
        elif perm == [2, 1, 0]:
            new_coords[:, 1] *= -1
        # can reverse any 2 axes, or none
        for flip in [[], [0, 1], [0, 2], [1, 2]]:
            if flip == []:
                yield new_coords
            else:
                new_coords2 = np.copy(new_coords)
                for a in flip:
                    new_coords2[:, a] *= -1
                yield new_coords2


# transform scanner coords that have beacons in common to have same coord system
to_visit = [0]
visited = set()
dist = {0: [0, 0, 0]}  # distance from first scanner
while len(to_visit) > 0:
    i = to_visit.pop()
    visited.add(i)
    for j in range(len(coords)):
        if (i == j) or (j in visited):
            continue
        c1 = coords[i]
        c2 = coords[j]
        match_found = False
        # try aligning on pairs of coords
        # only need to check len(c) - 11 rows since size of overlap must be >= 12
        for row1 in range(min(11, len(c1) - 1), len(c1)):
            if match_found:
                break
            c1_new = c1 - c1[row1, :]
            for row2 in range(min(11, len(c2) - 1), len(c2)):
                if match_found:
                    break
                c2_new = c2 - c2[row2, :]
                c2_origin_new = - c2[[row2], :]
                c2_new_ext = np.concatenate([c2_new, c2_origin_new], axis=0)
                for c2_t_ext in transforms(c2_new_ext):
                    c2_t = c2_t_ext[:-1, :]
                    c2_origin_new_t = c2_t_ext[-1, :]
                    if match_found:
                        break
                    concat = np.concatenate([c1_new, c2_t], axis=0)
                    unique = np.unique(concat, axis=0)
                    len_match = len(concat) - len(unique)
                    if len_match >= 12:
                        print(f"Scanners {i} and {j} have {len_match} matches")
                        match_found = True
                        to_visit.append(j)
                        # transform coords[j] to be in same system as coords[i]
                        coords[j] = c2_t + c1[row1, :]
                        dist[j] = c2_origin_new_t + c1[row1, :]

max_dist = 0
for i in range(len(coords)):
    for j in range(i + 1, len(coords)):
        curr_dist = np.sum(np.abs(dist[i] - dist[j]))
        max_dist = max(curr_dist, max_dist)

print(max_dist)
