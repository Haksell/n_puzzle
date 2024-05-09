import itertools
import random
from src.Move import Move
from src.utils import panic


def _read_file(filename):
    MAX_FILE_SIZE = 1 << 15
    try:
        content = open(filename).read(MAX_FILE_SIZE)
        assert len(content) != MAX_FILE_SIZE, f"file too big (max={MAX_FILE_SIZE})"
    except Exception as e:
        panic(f"Failed to read puzzle '{filename}': {e}")
    return content


def _make_goal(height, width):
    length = width * height
    tiles = [-1] * length
    x = y = 0
    dx = 1
    dy = 0
    for cur in itertools.chain(range(1, length), [0]):
        tiles[x + y * width] = cur
        cur += 1
        if (
            x + dx >= width
            or x + dx < 0
            or y + dy >= height
            or y + dy < 0
            or tiles[x + dx + (y + dy) * width] != -1
        ):
            dx, dy = -dy, dx
        x += dx
        y += dy
    return tiles


def __parity_permutation(tiles):
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


def _is_solvable(tiles, height, width):
    py, px = divmod(tiles.index(0), width)
    parity_empty = (len(tiles) ^ py ^ px ^ 1) & 1
    parity_tiles = __parity_permutation(tiles)
    parity_goal = __parity_permutation(_make_goal(height, width))
    return parity_empty == (parity_tiles ^ parity_goal)


# TODO: running manhattan
# TODO: rows iterator, cols iterator
class Puzzle:
    def __init__(self, tiles, height, width):
        assert sorted(tiles) == list(
            range(height * width)
        ), f"Invalid puzzle of size {height}x{width}: {tiles}"
        self.__height = height
        self.__width = width
        self.__tiles = tiles
        self.__zero_idx = tiles.index(0)
        # TODO: be lazy about calling _make_goal
        self.__goal = _make_goal(height, width)
        # TODO: only if manhattan or similar
        self.__goal_pos = [0] * len(tiles)
        for i, n in enumerate(self.__goal):
            self.__goal_pos[n] = i

    def __len__(self):
        return len(self.__tiles)

    def __iter__(self):
        yield from self.__tiles

    def __getitem__(self, idx):
        return self.__tiles[idx]

    def __str__(self):
        return "\n".join(
            " ".join(
                f"{self[y*self.__width+x]:{self.padding}}" for x in range(self.__width)
            )
            for y in range(self.__height)
        )

    @property
    def padding(self):
        return len(str(len(self) - 1))

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def goal(self):
        return self.__goal

    @property
    def goal_pos(self):
        return self.__goal_pos

    def is_correct(self, i):
        return self[i] == self.__goal[i]

    def do_move(self, move):
        swap_idx = self.__zero_idx + [self.__width, -1, -self.__width, 1][move]
        self.__tiles[self.__zero_idx], self.__tiles[swap_idx] = (
            self.__tiles[swap_idx],
            self.__tiles[self.__zero_idx],
        )
        self.__zero_idx = swap_idx

    def available_moves(self, last):
        y, x = divmod(self.__zero_idx, self.__width)
        moves = []
        if y != 0 and last != Move.UP:
            moves.append(Move.DOWN)
        if x != self.__width - 1 and last != Move.RIGHT:
            moves.append(Move.LEFT)
        if y != self.__height - 1 and last != Move.DOWN:
            moves.append(Move.UP)
        if x != 0 and last != Move.LEFT:
            moves.append(Move.RIGHT)
        return moves

    @staticmethod
    def from_file(filename):
        # TODO: accept rectangles
        content = _read_file(filename)
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
        if not _is_solvable(tiles, size, size):
            panic("Unsolvable puzzle")
        return Puzzle(tiles, size, size)

    @staticmethod
    def random(height, width):
        if width < 2 or height < 2:
            panic(f"Invalid size: {height}x{width}")
        tiles = list(range(height * width))
        random.shuffle(tiles)
        if not _is_solvable(tiles, height, width):
            if tiles[0] == 0 or tiles[1] == 0:
                tiles[-1], tiles[-2] = tiles[-2], tiles[-1]
            else:
                tiles[0], tiles[1] = tiles[1], tiles[0]
        return Puzzle(tiles, height, width)
