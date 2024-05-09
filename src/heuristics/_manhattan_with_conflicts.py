from ._lebesgue import manhattan


def __get_ceil_index(arr, tail_indices, lo, hi, key):
    while hi - lo > 1:
        mi = lo + hi >> 1
        if arr[tail_indices[mi]] <= key:
            hi = mi
        else:
            lo = mi
    return hi


def __longest_increasing_subsequence(a):
    if len(a) <= 1:
        return len(a)
    a = list(reversed(a))
    tail_indices = [0]
    prev_indices = [-1] * (len(a) + 1)
    for i in range(1, len(a)):
        if a[i] > a[tail_indices[0]]:
            tail_indices[0] = i
        elif a[i] < a[tail_indices[-1]]:
            prev_indices[i] = tail_indices[-1]
            tail_indices.append(i)
        else:
            pos = __get_ceil_index(a, tail_indices, -1, len(tail_indices) - 1, a[i])
            prev_indices[i] = tail_indices[pos - 1]
            tail_indices[pos] = i
    res = 0
    i = tail_indices[-1]
    while i >= 0:
        i = prev_indices[i]
        res += 1
    return res


def __line_conflicts(line_puzzle, line_goal):
    common = set(line_puzzle) & set(line_goal)
    common.discard(0)
    line_puzzle = [n for n in line_puzzle if n in common]
    line_goal = [n for n in line_goal if n in common]
    goal_pos = {n: i for i, n in enumerate(line_goal)}
    perm = [goal_pos[n] for n in line_puzzle]
    return len(perm) - __longest_increasing_subsequence(perm)


# TODO: alternative simpler linear conflicts that misses multiple conflicts
# but is faster to compute without lis
def __linear_conflicts(puzzle):
    conflicts = 0
    for i in range(puzzle.height):
        slice_row = slice(puzzle.height * i, puzzle.height * (i + 1), None)
        slice_col = slice(i, None, puzzle.height)
        conflicts += __line_conflicts(puzzle[slice_row], puzzle.goal[slice_row])
        conflicts += __line_conflicts(puzzle[slice_col], puzzle.goal[slice_col])
    return conflicts


# TODO: bring back corner conflicts
# TODO: cache conflicts in Puzzle class
def manhattan_with_conflicts(puzzle):
    return manhattan(puzzle) + 2 * __linear_conflicts(puzzle)
