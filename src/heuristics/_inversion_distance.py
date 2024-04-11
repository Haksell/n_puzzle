import math


def __merge(arr, temp_arr, lo, mi, hi):
    left_idx = lo
    right_idx = mi + 1
    temp_idx = 0
    inv_count = 0
    while left_idx <= mi and right_idx <= hi:
        if arr[left_idx] <= arr[right_idx]:
            temp_arr[temp_idx] = arr[left_idx]
            left_idx += 1
        else:
            temp_arr[temp_idx] = arr[right_idx]
            right_idx += 1
            inv_count += mi - left_idx + 1
        temp_idx += 1
    for i in range(temp_idx):
        arr[lo + i] = temp_arr[i]
    return inv_count


def __merge_sort(arr, temp_arr, lo, hi):
    inv_count = 0
    if lo < hi:
        mi = (lo + hi) >> 1
        inv_count += __merge_sort(arr, temp_arr, lo, mi)
        inv_count += __merge_sort(arr, temp_arr, mi + 1, hi)
        inv_count += __merge(arr, temp_arr, lo, mi, hi)
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
