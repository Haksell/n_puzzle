import itertools
import math


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
