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


def __count_inversions(tiles, goal):
    index_map = {value: idx for idx, value in enumerate(goal)}
    tiles_mapped = [
        index_map[value] for value in tiles if value > 0 and value in index_map
    ]
    temp_arr = [0] * len(tiles_mapped)
    return __merge_sort(tiles_mapped, temp_arr, 0, len(tiles_mapped) - 1)


def __transpose(tiles, height, width):
    return [tiles[y + x * height] for y in range(height) for x in range(width)]


def inversion_distance(puzzle):
    horizontal_inversions = __count_inversions(puzzle, puzzle.goal)
    transpose_inversions = __count_inversions(
        __transpose(puzzle, puzzle.height, puzzle.width),
        __transpose(puzzle.goal, puzzle.height, puzzle.width),
    )
    # TODO: verify when puzzles are not 4x4
    return sum(divmod(horizontal_inversions, 3)) + sum(divmod(transpose_inversions, 3))
