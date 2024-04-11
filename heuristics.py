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


def __linear_conflicts(puzzle, goal):
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


def constant_zero(puzzle, goal):
    return 0


def __merge(arr, temp_arr, left, mid, right):
    i = left
    j = mid + 1
    k = left
    inv_count = 0

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            k += 1
            i += 1
        else:
            temp_arr[k] = arr[j]
            inv_count += mid - i + 1
            k += 1
            j += 1

    while i <= mid:
        temp_arr[k] = arr[i]
        k += 1
        i += 1

    while j <= right:
        temp_arr[k] = arr[j]
        k += 1
        j += 1

    for loop_var in range(left, right + 1):
        arr[loop_var] = temp_arr[loop_var]

    return inv_count


def __merge_sort(arr, temp_arr, left, right):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2
        inv_count += __merge_sort(arr, temp_arr, left, mid)
        inv_count += __merge_sort(arr, temp_arr, mid + 1, right)
        inv_count += __merge(arr, temp_arr, left, mid, right)
    return inv_count


def __count_inversions(arr1, arr2):
    index_map = {value: idx for idx, value in enumerate(arr2)}
    arr1_mapped = [index_map[value] for value in arr1]
    temp_arr = [0] * len(arr1)
    return __merge_sort(arr1_mapped, temp_arr, 0, len(arr1_mapped) - 1)


def inversion_distance(puzzle, goal):
    size = math.isqrt(len(puzzle))
    vertical_puzzle = [puzzle[i + j * size] for i in range(size) for j in range(size)]
    vertical_goal = [goal[i + j * size] for i in range(size) for j in range(size)]
    horizontal_inversions = __count_inversions(puzzle, goal)
    vertical_inversions = __count_inversions(vertical_puzzle, vertical_goal)
    return sum(divmod(horizontal_inversions, 3)) + sum(divmod(vertical_inversions, 3))
