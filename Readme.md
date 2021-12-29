# Python solutions for Advent of Code 2021

### Day 1

Iterate over the arrays and maintain a running sum.

### Day 2

Process the instructions in order.

### Day 3

Part 1: Iterate over the numbers, using a dictionary to count of the number of 0s in each position.
Part 2: We need to repeatedly discard part of the list of numbers, according to whether their
`n`th bit is the most common value for position n. To avoid iterating over the list multiple times 
to determine which numbers to discarding, we sort the list first. Then after the discarding step
for each `n`, the remaining list of numbers will be ordered so that all the numbers with 0 in the
`(n + 1)`th bit will be at the start, so we just need to iterate over the current list to find 
the point at which the `(n + 1)`th bit changes from 0 to 1, and then discard either the first or
second half of the list. I did this iteration just by linear search, which is fast enough for the 
given use case, but it could be sped up using binary search.

### Day 4
Maintain 2 arrays to keep track of how many numbers are marked on each row and column of each board.
When incrementing the counters, if the new value is 5, the board has won and we calculate its score.

### Day 5
Maintain a numpy array to represent the grid (this makes it faster and 
easier to update a line segment, compared to a python array). Iterate over the set of lines 
and increment the value of the array covered by the line segment.

### Day 6
Since the number of lanternfish grows exponentially, it's too inefficient to list them in an array.
But we only need to keep track of how many fish are at each cycle point for each step, so 
we can use the `Counter` data structure.

### Day 7
Part 1: The median minimises the sum of absolute distances; see https://math.stackexchange.com/questions/113270/the-median-minimizes-the-sum-of-absolute-deviations-the-ell-1-norm.
Part 2: The optimal position must be between the minimum and maximum of the crabs' positions. 
We can just iterate over all the positions. For each possible position, the fuel spent by
each crab is `1 + 2 + 3 + ... + n` where `n` is the distance it travels. We can calculate this 
using Gauss' formula; see https://nrich.maths.org/2478.

### Day 8
Part 1 is straightforward. For part 2, iterate over all the permutations of the set of segments; each permutation 
represents a bijective mapping from the set of segments to itself, i.e. a possible way of 
connecting the signals to the display segments. E.g. the permutation `gacdefa` represents the 
mapping that transforms `abcdefg` into `gacdefa`, i.e. the signal for `a` is connected to the dispay 
for `g`, etc. There are 7 segments, so `7! = 5040` permutations, which is computationally feasible.
Define a dictionary that maps each number to its set of display segments (for a correctly 
wired display). Then, for each permutation, use this dictionary to check whether each 
pattern of observed display segments translates to a valid number. Stop when we find a valid permutation.

### Day 9
Part 1 is straightforward: iterate over all grid points and check whether they are lower than surrounding values.
For part 2, we can represent the grid as a graph where each pair of adjacent points
(vertically or horizontally) is connected by an edge unless one of the points is a 9. Then the 
basins are the connected components of the graph. To find these connected components, find the
first grid point which is not 9 and assign it a basin number. Use depth-first search 
to find all the points connected to it and assign them the same basin number. When there are no 
more connected points, find the next grid value that is not 9, and not already assigned to a basin, 
and repeat the process.

### Day 10
We use a stack to represent the set of currently-open pairs of brackets. When we encounter an opening bracket
(`(`, `[` or `{`), add it to the stack. When we encounter a closing bracket (`)`, `]`, or `}`), if the 
line is complete the corresponding starting bracket should be on the top of the stack; in this 
case pop it off (since this bracket pair is now closed), and continue. If we reach the end of the line
and the stack is not empty, the line is incomplete, so this solves part 1. For part 2, we complete 
the line by popping open brackets off the stack and adding the corresponding closing brackets 
to the line.

### Day 11
For each step, use a `while`-loop to keep iterating until there are no more flashes. The loop
continues as long as any value in the new grid is greater than 9.

### Day 12
Use depth-first search. Use a stack to represent the set of vertices (caves) to be visited. 
For part 1, each 
member of the stack represents a partial path from the start to the end. Each stack member is a 
length-3 list where the first element is a list of vertices in the path, the second is the _set_ 
of vertices in the path (for faster lookups), and the third is the set of neighbours of the 
current last vertex in the path.
After vising each vertex, add to the stack the set of its neighbours which can be visited. For 
small vertices, only add them if they are not already in the path (which we look up using the
vertex set described above). For part 2, we can have one small vertex which is visited twice, 
so the idea is similar except each stack member also keeps track of how many times each vertex 
has been visited, and whether any small vertices have been visited twice.

### Day 13
This is straightforward to implement using `numpy`, which has built-in operations for horizontal 
and vertical flips.

### Day 14
For part 1, we can just simulate the changes to the polymer, representing it as a string. 
For part 2, the polymer string would be too large for this to be feasible. So instead we use a 
counter to keep track of the count of each possible pair at each step, and another counter 
to keep track of the number of each character.

### Day 15
Use Dijkstra's algorithm to find the shortest path. As described in the Wikipedia entry
(https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) we can implement this efficiently by 
using a priority queue (i.e. a python `heapq` object) to find the node with the shortest current 
distance at each step. We also need a dictionary to reference items in the priority queue so 
that we can update them or mark them as invalid; see 
https://docs.python.org/3.6/library/heapq.html#priority-queue-implementation-notes.

### Day 16
This is like parsing an arithmetic expression, so we use depth-first search. The stack 
represents the nested brackets of the expression. When we pop a sub-packet off the stack, update the position of the 
parser, and either the number of sub-packets parsed, or the length of the parsed sub-packets. For part 2, 
we also need to update the value of its parent, using the parent's operation and current value, and the 
value of the just-popped packet.

### Day 17

For any given number of steps and initial velocity, we can find a closed-form expression 
for the probe's `x` and `y` coords using Gauss' formula. Then, the key is to note that the 
number of steps `s`, and the velocities are all integers, and `s` is a factor of `2 * y`, 
so `s` must be less than `abs(2y)`. Thus we can iterate over all `y` in the target range, 
and for each `y`, iterate over `s <= 2*y`. We calculate the initial `y` velocity in terms of `y`
and `s`, then calculate the allowable ranges for the `x` velocity.


### Day 18

Represent each expression as a binary tree. The sum is represented by adding a new node at the top with the operands
as the left and right values. To process the explode and split operations we need to traverse the tree in order, left 
to right.


### Day 19

Since the problem statement mentions that the relative positions of all the scanners can be reconstructed, there 
must be an ordering of the scanners such that consecutive scanners have at least 12 beacons in common. Starting 
from the first scanner, we use depth-first search to find this path. Each time we visit a node, we transform its 
coordinates to the coordinates of the first scanner (which is possible because we have already transformed the coordinates 
of all the previously-visited scanners). 

For part 1, after finding a path through the scanners, concatenate all the coordinates (which are all now in the same coordinate 
system), and count the unique rows.

For part 2, when visiting each node we record its distance from the first scanner. Then after finding the path, 
iterate over all pairs of nodes and calculate the Manhattan distance between them.

### Day 20

Use numpy arrays to simulate the image at each enhancement step. The size of the output grows with each enhancement 
step, and if the 0th value of the enhancement algorithm is 1, then the (infinite-sized) border of the image will be all 
1's after the first step (in this case the 511th value of the enhancement algorithm must be 0, so that the border 
becomes all 0's after an even number of steps).

### Day 21

For Part 1, just simulate the game. 

Part 2 is a dynamic programming task. Players cannot have more than 21 turns each 
(since their score increases with each turn). There are 27 ways each player can roll the die for their first turn,
and 7 possibilities for their position and score (since the sum of 3 die rolls is between 3 and 9 inclusive). So 
for each player, and each possible position and score for that player, we can calculate the number of ways this player 
could have rolled the die for this outcome to occur (ignoring the other player's die rolls). We then do this 
iteratively for subsequent turns, based on the previous turn's possible outcomes and their associated number of 
universes (provided the previous turn's score is 
< 21). We do this independently for each player. 

Finally, to find the total number of universes where player 1 wins, 
we iterate over player 1's possible ways of achieving a score >= 21, and multiply by the number of ways that player 2
could have achieved a score < 21 in 1 fewer turns (since player 1 goes first, so if player 1 wins, player 1's total 
number of turns is 1 more than player 2's). We do similarly for player 2 (except that if player 2 wins, both players
have had the same number of turns).

### Day 22

For part 1, simulate the grid using a matrix. For part 2, we can divide the grid up into 
3-dimensional regions by splitting along the edges of the x, y, z ranges. Then within
each region, all the lights are either on or off, so then we simulate the operations 
using a matrix as in part 1, except that each entry in the matrix now represents a 
3-d region instead of a single cube.

### Day 23

Use depth-first search to find the least-cost sequence of moves. We can speed up the search as follows: (1) If cost 
of current partial sequence of moves exceeds cost of an already-found viable full solution, stop checking further moves.
(2) Immediately move any amphipods in hallway to destination rooms when this is possible, before checking other 
moves. (3) Immediately move any amphipods from their starting room to their destination when this is possible (i.e.
moving amphipod has nothing above it, destination room contains only amphipods of correct type, and there is a 
clear path in hallway). (4) When adding new moves to a partial sequence, check that this does create a blockage in 
the hallway (if there are 2 amphipods in the hallway, and one must move right to get to its destination room, and the
other must move left to get to its destination room, and they must cross over each other to do this, they will be 
stuck forever).


### Day 24

First process the instructions to move inputs later in list if this does not change the outcome. Also remove 
instructions that multiply or divide a value by 1, or add 0. This will speed up the search.

Then, iterate through the list of instructions and determine the range of possible values of each variable based on
the previous values and the current instruction. Then do the same process backward, and continue until we cannot 
update any more values.

Finally, search for the highest possible inputs. Use a stack to maintain the best possible partial list of inputs (which 
represents the starting part of the model number). Execute the instructions and when one is invalid (e.g.
mod or division with invalid operand, or value outside the allowable ranges we have found), decrement the current input 
if it is > 1, or otherwise pop it off the stack. Then go back to the input instruction of the last item in the stack
and continue processing instructions.

Part 2 is similar to part 1, except we begin with the lowest possible inputs and increment.


### Day 25

Simulate the grid using a numpy array.
