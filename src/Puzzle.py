from .lib import is_solvable, panic


class Puzzle:
    # TODO: accept rectangles
    def __init__(self, size, tiles):
        assert sorted(tiles) == list(
            range(size * size)
        ), f"Invalid puzzle of size {size}: {tiles}"
        self.__size = size
        self.__tiles = tiles

    def __len__(self):
        return len(self.__tiles)

    # TODO: remove __iter__ (maybe) and __getitem__(definitely)

    def __iter__(self):
        yield from self.__tiles

    def __getitem__(self, idx):
        return self.__tiles[idx]

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
        if not is_solvable(tiles):  # TODO: in class
            panic("Unsolvable puzzle")
        return cls(size, tiles)
