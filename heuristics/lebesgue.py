import math


def __lebesgue(puzzle, goal, dist_func):
    assert len(puzzle) == len(goal)
    size = math.isqrt(len(puzzle))
    goal_pos = {v: i for i, v in enumerate(goal) if v != 0}
    total_distance = 0
    for i, v in enumerate(puzzle):
        if v == 0:
            continue
        gy, gx = divmod(goal_pos[v], size)
        py, px = divmod(i, size)
        total_distance += dist_func(gx - px, gy - py)
    return total_distance


def manhattan(puzzle, goal):
    return __lebesgue(puzzle, goal, lambda dx, dy: abs(dx) + abs(dy))


def euclidean(puzzle, goal):
    return __lebesgue(puzzle, goal, math.hypot)


def chebyshev(puzzle, goal):
    return __lebesgue(puzzle, goal, lambda dx, dy: max(abs(dx), abs(dy)))
