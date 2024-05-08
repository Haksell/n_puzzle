import itertools
import math
from src.lib import do_move, panic


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
        return parity_permutation(tiles) ^ parity_permutation(Puzzle.make_goal(size))

    size = math.isqrt(len(tiles))
    return parity_empty(tiles, size) == parity_compared_to_goal(tiles, size)


class Puzzle:
    # TODO: accept rectangles
    # TODO: remove retarded make_goal argument
    def __init__(self, size, tiles, *, make_goal=True):
        assert sorted(tiles) == list(
            range(size * size)
        ), f"Invalid puzzle of size {size}: {tiles}"
        self.__size = size
        self.__tiles = tiles
        if make_goal:
            self.__goal = Puzzle.make_goal(self.__size)

    def __len__(self):
        return len(self.__tiles)

    @property
    def height(self):
        return self.__size

    @property
    def width(self):
        return self.__size

    # TODO: remove __iter__ (maybe) and __getitem__(definitely)

    def __iter__(self):
        yield from self.__tiles

    def __getitem__(self, idx):
        return self.__tiles[idx]

    def is_correct(self, i):
        return self[i] == self.__goal[i]

    def do_move(self, move):
        do_move(self.__tiles, move, self.__size, self.__tiles.index(0))

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
    def make_goal(cls, s):  # TODO: accept rectangles
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
        return cls(s, tiles, make_goal=False)

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
        if not is_solvable(tiles):  # TODO: in class
            panic("Unsolvable puzzle")
        return cls(size, tiles)

    @classmethod
    def random(cls, width, height):
        pass  # TODO
