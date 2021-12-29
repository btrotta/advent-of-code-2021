import numpy as np

with open("data.txt", "r") as f:
    data = f.readlines()

words = data[0].split(" ")
for w in words:
    if w.startswith("x="):
        x_min, x_max = [int(a) for a in w[2:-1].split("..")]
    elif w.startswith("y="):
        y_min, y_max = [int(a) for a in w[2:].split("..")]


best_height = 0
pairs = set()
eps = 1e-15
# Let x, y represent the point where the probe first is inside the target and vy_0
# the initial velocity of y. By Gauss' formula, we have y = 0.5 * s * (2 * vy_0 - s + 1),
# i.e. 2y = s * (2 * vy_0 - s + 1)
# If there is some integer s, vy_0 satisfying this equation, then s <= abs(2y)
for y in range(y_min, y_max + 1):
    for s in range(1, abs(2 * y) + 1):
        vy_0 = y/s + 0.5 * (s - 1)
        if abs(vy_0 - np.floor(vy_0)) > eps:
            # vy_0 is not an integer
            continue
        vy_0 = int(vy_0)
        # trajectory peaks when velocity = 0, i.e. at t = vy_0, and the height at this
        # point is 0.5 * t * (2 * vy_0 - t + 1) = 0.5 * vy_0 * (vy_0 + 1)
        if s >= vy_0:
            curr_best = 0.5 * vy_0 * (vy_0 + 1)
        else:
            # probe does not reach potential peak because it hits the target area first
            curr_best = 0.5 * s * (2 * vy_0 - s + 1)
        # check for feasible vx_0
        # If vx_0 <= s, the x position after s steps is 0.5 * vx_0 * (vx_0 + 1).
        # Using the quadratic formula, and the fact that x_min and x_max must be positive
        # (since only positive vx_0) are allowed, we find the following feasible
        # range for x when vx_0 < s:
        vx_0_lower = max(0, np.ceil(0.5 * (-1 + np.sqrt(1 + 8 * x_min))))
        vx_0_upper = min(s, np.floor(0.5 * (-1 + np.sqrt(1 + 8 * x_max))))
        for vx_0 in range(int(vx_0_lower), int(vx_0_upper) + 1):
            if vx_0 <= s:
                pairs.add((vx_0, vy_0))
                best_height = max(best_height, curr_best)

        # If vx_0 >= s, the x position after s steps is 0.5 * s * (2 * vx_0 - s + 1)
        # For this to be in the target range we need
        # x_min / s + (s + 1) / 2 <= vx_0  <= x_max / s + (s + 1) / 2
        for vx_0 in range(int(np.ceil(x_min / s + (s - 1) / 2)), int(np.floor(x_max / s + (s - 1) / 2)) + 1):
            if vx_0 >= s:
                pairs.add((vx_0, vy_0))
                best_height = max(best_height, curr_best)

print(len(pairs))
