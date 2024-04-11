import math


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
