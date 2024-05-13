import math


def lebesgue(puzzle, dist_func):
    total_distance = 0
    goal_pos = puzzle.goal_pos
    width = puzzle.width
    for i, v in enumerate(puzzle):
        if v <= 0:
            continue
        # TODO: cache divmod
        gpv = goal_pos[v]
        if gpv == -1:
            continue
        gy, gx = divmod(goal_pos[v], width)
        py, px = divmod(i, width)
        total_distance += dist_func(gx - px, gy - py)
    return total_distance


def manhattan(puzzle):
    return puzzle.manhattan_distance


def euclidean(puzzle):
    return lebesgue(puzzle, math.hypot)


def chebyshev(puzzle):
    return lebesgue(puzzle, lambda dx, dy: max(abs(dx), abs(dy)))
