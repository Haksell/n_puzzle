import itertools
import math
import sys
from src.Move import Move


def panic(message):
    print(message, file=sys.stderr)
    sys.exit(1)


# TODO: in Puzzle class
# TODO: accept rectangles
def make_goal(s):
    ts = s * s
    tiles = [-1] * ts
    x = y = 0
    dx = 1
    dy = 0
    for cur in itertools.chain(range(1, ts), [0]):
        tiles[x + y * s] = cur
        cur += 1
        if (
            x + dx >= s
            or x + dx < 0
            or y + dy >= s
            or y + dy < 0
            or tiles[x + dx + (y + dy) * s] != -1
        ):
            dx, dy = -dy, dx
        x += dx
        y += dy
    return tiles


# TODO: in Puzzle class
# TODO: test with rectangles of various sizes
def is_solvable(tiles):
    def parity_empty(tiles, size):
        py, px = divmod(tiles.index(0), size)
        return (size ^ py ^ px ^ 1) & 1

    def parity_permutation(tiles):
        seen = set()
        transpositions = 0
        for i in range(len(tiles)):
            if i in seen:
                continue
            seen.add(i)
            j = tiles[i]
            while j != i:
                seen.add(j)
                j = tiles[j]
                transpositions ^= 1
        return transpositions

    def parity_compared_to_goal(tiles, size):
        return parity_permutation(tiles) ^ parity_permutation(make_goal(size))

    size = math.isqrt(len(tiles))
    return parity_empty(tiles, size) == parity_compared_to_goal(tiles, size)


class Puzzle:
    # TODO: accept rectangles
    def __init__(self, size, tiles):
        assert sorted(tiles) == list(
            range(size * size)
        ), f"Invalid puzzle of size {size}: {tiles}"
        self.__size = size
        self.__tiles = tiles
        self.__zero_idx = tiles.index(0)
        # TODO:be lazy about calling make_goal
        self.__goal = make_goal(self.__size)

    def __len__(self):
        return len(self.__tiles)

    @property
    def height(self):
        return self.__size

    @property
    def width(self):
        return self.__size

    @property
    def goal(self):
        return self.__goal

    def __iter__(self):
        yield from self.__tiles

    def __getitem__(self, idx):
        return self.__tiles[idx]

    def __str__(self):
        padding = len(str(len(self) - 1))
        return "\n".join(
            " ".join(f"{self[y*self.__size+x]:{padding}}" for x in range(self.__size))
            for y in range(self.__size)
        )

    def hash(self):  # TODO: __hash__
        return tuple(self)  # TODO: constantly updated factorial base

    def is_correct(self, i):
        return self[i] == self.__goal[i]

    def is_solved(self):
        return all(map(int.__eq__, self, self.__goal))

    def do_move(self, move):
        swap_idx = self.__zero_idx + [self.__size, -1, -self.__size, 1][move]
        self.__tiles[self.__zero_idx], self.__tiles[swap_idx] = (
            self.__tiles[swap_idx],
            self.__tiles[self.__zero_idx],
        )
        self.__zero_idx = swap_idx

    def available_moves(self, last):
        y, x = divmod(self.__zero_idx, self.__size)
        moves = []
        if y != 0 and last != Move.UP:
            moves.append(Move.DOWN)
        if x != self.__size - 1 and last != Move.RIGHT:
            moves.append(Move.LEFT)
        if y != self.__size - 1 and last != Move.DOWN:
            moves.append(Move.UP)
        if x != 0 and last != Move.LEFT:
            moves.append(Move.RIGHT)
        return moves

    @staticmethod
    def __read_file(filename):
        MAX_FILE_SIZE = 1 << 15
        try:
            content = open(filename).read(MAX_FILE_SIZE)
            assert len(content) != MAX_FILE_SIZE, f"file too big (max={MAX_FILE_SIZE})"
        except Exception as e:
            panic(f"Failed to read puzzle '{filename}': {e}")
        return content

    @classmethod
    def from_file(cls, filename):
        content = cls.__read_file(filename)
        size = None
        seen = set()
        tiles = []
        for line in content.splitlines():
            line = line.split("#")[0].strip()
            if not line:
                continue
            if size is None:
                try:
                    size = int(line)
                    assert size >= 2
                except (AssertionError, ValueError):
                    panic(f"Invalid size: {line}")
            else:
                try:
                    row = line.split()
                    assert (
                        len(row) == size
                    ), f"Invalid width (got {len(row)}, expected {size})"
                    for x in row:
                        assert all(
                            c.isdigit() for c in x
                        ), f"Invalid natural number: {x}"
                        x = int(x)
                        assert (
                            x < size * size
                        ), f"Number too big for given puzzle size: (got {x}, max {size*size-1})"
                        assert x not in seen, f"Duplicate number: {x}"
                        seen.add(x)
                        tiles.append(x)
                except AssertionError as e:
                    panic(e)
        if size is None:
            panic("Empty file")
        height = len(tiles) // size
        if height != size:
            panic(f"Invalid height (got {height}, expected {size})")
        if not is_solvable(tiles):
            panic("Unsolvable puzzle")
        return cls(size, tiles)

    @classmethod
    def random(cls, width, height):
        pass  # TODO
