import itertools
import math
import sys


def panic(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def clamp(x, mini, maxi):
    return mini if x < mini else maxi if x > maxi else x


# TODO: accept rectangles
# TODO: directly in Puzzle class?
def make_goal(s):
    ts = s * s
    puzzle = [-1] * ts
    x = y = 0
    dx = 1
    dy = 0
    for cur in itertools.chain(range(1, ts), [0]):
        puzzle[x + y * s] = cur
        cur += 1
        if (
            x + dx >= s
            or x + dx < 0
            or y + dy >= s
            or y + dy < 0
            or puzzle[x + dx + (y + dy) * s] != -1
        ):
            dx, dy = -dy, dx
        x += dx
        y += dy
    return puzzle


def __safe_isqrt(n):
    assert isinstance(n, int) and n >= 0
    i = math.isqrt(n)
    if i * i == n:
        return i
    return i if i * i == n else None


def print_puzzle(puzzle):
    size = __safe_isqrt(len(puzzle))
    assert size is not None
    w = len(str(size**2))
    for y in range(0, size * size, size):
        print(*[f"{puzzle[x + y]:{w}}" for x in range(size)])


def is_solvable(puzzle):
    def parity_empty(puzzle, size):
        py, px = divmod(puzzle.index(0), size)
        return (size ^ py ^ px ^ 1) & 1

    def parity_permutation(puzzle):
        seen = set()
        transpositions = 0
        for i in range(len(puzzle)):
            if i in seen:
                continue
            seen.add(i)
            j = puzzle[i]
            while j != i:
                seen.add(j)
                j = puzzle[j]
                transpositions ^= 1
        return transpositions

    def parity_compared_to_goal(puzzle, size):
        return parity_permutation(puzzle) ^ parity_permutation(make_goal(size))

    size = math.isqrt(len(puzzle))
    return parity_empty(puzzle, size) == parity_compared_to_goal(puzzle, size)
