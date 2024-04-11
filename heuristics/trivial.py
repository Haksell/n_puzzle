def hamming(puzzle, goal):
    return sum(pi != gi for pi, gi in zip(puzzle, goal) if pi != 0)


def constant_zero(puzzle, goal):
    return 0
