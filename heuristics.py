import math


def manhattan(puzzle, goal):
    assert len(puzzle) == len(goal)
    size = math.isqrt(len(puzzle))
    goal_pos = {v: i for i, v in enumerate(goal) if v != 0}
    total_distance = 0
    for i, v in enumerate(puzzle):
        if v == 0:
            continue
        gy, gx = divmod(goal_pos[v], size)
        py, px = divmod(i, size)
        total_distance += abs(gy - py) + abs(gx - px)
    return total_distance
