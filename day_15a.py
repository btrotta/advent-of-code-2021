import numpy as np
import heapq

with open("data.txt", "r") as f:
    data = f.readlines()
arr = [[int(i) for i in list(s.strip())] for s in data]

num_rows = len(arr)
num_cols = len(arr[0])

nodes = [(x, y) for x in range(num_rows) for y in range(num_cols)]

edges = {((x, y), (x + 1, y)): arr[x + 1][y] for x in range(num_rows - 1) for y in range(num_cols)}
edges.update({((x, y), (x, y + 1)): arr[x][y + 1] for x in range(num_rows) for y in range(num_cols - 1)})
edges.update({((x, y), (x - 1, y)): arr[x - 1][y] for x in range(1, num_rows) for y in range(num_cols)})
edges.update({((x, y), (x, y - 1)): arr[x][y - 1] for x in range(num_rows) for y in range(1, num_cols)})

edge_map = {a: {} for a in nodes}
for a, b in edges:
    edge_map[a][b] = edges[a, b]

# Dijkstra's algorithm

# first member of tuple denotes validity, 0 = valid, 1 = invalid, so that we can update
# priorities as described here:
# https://docs.python.org/3.6/library/heapq.html#priority-queue-implementation-notes
unvisited = [[0, np.inf, n] for n in nodes]
unvisited[0] = [0, 0, (0, 0)]
heapq.heapify(unvisited)
unvisited_map = {n: unvisited[i] for i, n in enumerate(nodes)}
dist_map = {n: np.inf for n in nodes}
dist_map[0, 0] = 0

while len(unvisited_map) > 0:
    _, dist, node = heapq.heappop(unvisited)
    for neighbour in edge_map[node]:
        if neighbour in unvisited_map:
            new_dist = dist_map[node] + edge_map[node][neighbour]
            if new_dist < unvisited_map[neighbour][1]:
                old_queue_member = unvisited_map.pop(neighbour)
                old_queue_member[0] = 1  # mark invalid
                new_queue_member = [0, new_dist, neighbour]
                heapq.heappush(unvisited, new_queue_member)
                unvisited_map[neighbour] = new_queue_member
                dist_map[neighbour] = new_dist
    if node == (num_rows, num_cols):
        break
    unvisited_map.pop(node)

print(dist_map[num_rows - 1, num_cols - 1])
