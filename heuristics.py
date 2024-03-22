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


def euclidean(puzzle, goal):
    return __lebesgue(puzzle, goal, math.hypot)


def manhattan(puzzle, goal):
    return __lebesgue(puzzle, goal, lambda dx, dy: abs(dx) + abs(dy))


def chebyshev(puzzle, goal):
    return __lebesgue(puzzle, goal, lambda dx, dy: max(abs(dx), abs(dy)))


def hamming(puzzle, goal):
    return sum(pi != gi for pi, gi in zip(puzzle, goal) if pi != 0)


def __corner_conflicts(puzzle, goal):
    size = math.isqrt(len(puzzle))
    top_left = 0
    top_right = size - 1
    bottom_left = (size - 1) * size
    bottom_right = size * size - 1
    return sum(
        puzzle[corner] != goal[corner]
        and (
            puzzle[horizontal_neighbor] == goal[horizontal_neighbor]
            or puzzle[vertical_neighbor] == goal[vertical_neighbor]
        )
        for corner, horizontal_neighbor, vertical_neighbor in [
            (top_left + 0, top_left + 1, top_left + size),
            (top_right, top_right - 1, top_right + size),
            (bottom_left, bottom_left + 1, bottom_left - size),
            (bottom_right, bottom_right - 1, bottom_right - size),
        ]
    )


def __line_conflicts(line_puzzle, line_goal):
    # TODO: handle multiple conflicts
    line_puzzle_pos = {n: i for i, n in enumerate(line_puzzle)}
    for i in range(len(line_goal)):
        if line_goal[i] not in line_puzzle_pos:
            continue
        for j in range(i + 1, len(line_goal)):
            if line_goal[j] not in line_puzzle_pos:
                continue
            if line_puzzle_pos[line_goal[j]] < line_puzzle_pos[line_goal[i]]:
                return 1
    return 0


def __linear_conflicts(puzzle, goal):
    return 0
    size = math.isqrt(len(puzzle))
    conflicts = 0
    for i in range(size):
        slice_row = slice(size * i, size * (i + 1), None)
        slice_col = slice(i, None, size)
        conflicts += __line_conflicts(puzzle[slice_row], goal[slice_row])
        conflicts += __line_conflicts(puzzle[slice_col], goal[slice_col])
    return conflicts


def manhattan_with_conflicts(puzzle, goal):
    return (
        manhattan(puzzle, goal)
        + 2 * __corner_conflicts(puzzle, goal)
        + 2 * __linear_conflicts(puzzle, goal)
    )


HEURISTICS = [manhattan_with_conflicts, manhattan, euclidean, chebyshev, hamming]
