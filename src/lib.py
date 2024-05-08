import math
import sys


def panic(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def clamp(x, mini, maxi):
    return mini if x < mini else maxi if x > maxi else x


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
