import math


def __lebesgue(puzzle, goal, dist_func):
    assert len(puzzle) == len(goal)
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


def manhattan(puzzle, goal):
    return __lebesgue(puzzle, goal, lambda dx, dy: abs(dx) + abs(dy))


def euclidean(puzzle, goal):
    return __lebesgue(puzzle, goal, math.hypot)


def chebyshev(puzzle, goal):
    return __lebesgue(puzzle, goal, lambda dx, dy: max(abs(dx), abs(dy)))
