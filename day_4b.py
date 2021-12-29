with open("data.txt", "r") as f:
    data = f.readlines()
arr = [s.replace("\n", "") for s in data]

numbers = [int(a) for a in arr[0].split(",")]
boards = []
curr_board = []
for i in range(2, len(arr)):
    if arr[i] == "":
        boards.append(curr_board)
        curr_board = []
    else:
        curr_board.append([int(j) for j in arr[i].split()])
boards.append(curr_board)

row_found = [[0, 0, 0, 0, 0] for i in range(len(boards))]
col_found = [[0, 0, 0, 0, 0] for i in range(len(boards))]
won = [0 for i in range(len(boards))]


def bingo():
    for n in numbers:
        for k, b in enumerate(boards):
            for j, row in enumerate(b):
                for i, x in enumerate(row):
                    if x == n:
                        row[i] = -1
                        row_found[k][j] += 1
                        col_found[k][i] += 1
                        if (row_found[k][j] == 5) or (col_found[k][i] == 5):
                            if won[k] == 0:
                                won[k] = 1
                                ans = n * sum(b[x][y] for x in range(5) for y in range(5) if
                                          b[x][y] != -1)
                                if sum(won) == len(boards):
                                    return(ans)

bingo()
