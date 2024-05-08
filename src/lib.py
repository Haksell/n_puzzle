from enum import IntEnum
import math
import sys


class Move(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(self):
        return Move(self.value ^ 2)


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


def do_move(tiles, move, size, zero_idx):
    # TODO: execute the moves directly on the hashed value
    swap_idx = zero_idx + [size, -1, -size, 1][move]
    tiles[zero_idx], tiles[swap_idx] = tiles[swap_idx], tiles[zero_idx]
