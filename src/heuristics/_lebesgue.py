import math


def __lebesgue(puzzle, dist_func):
    total_distance = 0
    goal_pos = puzzle.goal_pos
    width = puzzle.width
    for i, v in enumerate(puzzle):
        if v == 0:
            continue
        # TODO: cache divmod
        gy, gx = divmod(goal_pos[v], width)
        py, px = divmod(i, width)
        total_distance += dist_func(gx - px, gy - py)
    return total_distance


def manhattan(puzzle):
    return __lebesgue(puzzle, lambda dx, dy: abs(dx) + abs(dy))


def euclidean(puzzle):
    return __lebesgue(puzzle, math.hypot)


def chebyshev(puzzle):
    return __lebesgue(puzzle, lambda dx, dy: max(abs(dx), abs(dy)))
