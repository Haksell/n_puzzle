import math


def __lebesgue(puzzle, dist_func):
    total_distance = 0
    goal_pos = puzzle.goal_pos
    # print(puzzle.width, goal_pos)
    width = puzzle.width
    for i, v in enumerate(puzzle):
        if v == 0:
            continue
        gpv = goal_pos.get(v)
        if gpv is None:
            continue
        # TODO: cache divmod
        gy, gx = divmod(gpv, width)
        py, px = divmod(i, width)
        # print(v, gy, gx, py, px)
        total_distance += dist_func(gx - px, gy - py)
    # print(total_distance)
    return total_distance


def manhattan(puzzle):
    return __lebesgue(puzzle, lambda dx, dy: abs(dx) + abs(dy))


def euclidean(puzzle):
    return __lebesgue(puzzle, math.hypot)


def chebyshev(puzzle):
    return __lebesgue(puzzle, lambda dx, dy: max(abs(dx), abs(dy)))
