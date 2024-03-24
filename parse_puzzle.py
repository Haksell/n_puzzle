from lib import is_solvable, panic


def __read_file(filename):
    MAX_FILE_SIZE = 1 << 15
    try:
        content = open(filename).read(MAX_FILE_SIZE)
        assert len(content) != MAX_FILE_SIZE, f"file too big (max={MAX_FILE_SIZE})"
    except Exception as e:
        panic(f"Failed to read puzzle '{filename}': {e}")
    return content


def parse_puzzle(filename):
    content = __read_file(filename)
    size = None
    seen = set()
    puzzle = []
    for line in content.splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        if size is None:
            try:
                size = int(line)
                assert size >= 3
            except (AssertionError, ValueError):
                panic(f"Invalid size: {line}")
        else:
            try:
                row = line.split()
                assert (
                    len(row) == size
                ), f"Invalid width (got {len(row)}, expected {size})"
                for x in row:
                    assert all(c.isdigit() for c in x), f"Invalid natural number: {x}"
                    x = int(x)
                    assert (
                        x < size * size
                    ), f"Number too big for given puzzle size: (got {x}, max {size*size-1})"
                    assert x not in seen, f"Duplicate number: {x}"
                    seen.add(x)
                    puzzle.append(x)
            except AssertionError as e:
                panic(e)
    if size is None:
        panic("Empty file")
    height = len(puzzle) // size
    if height != size:
        panic(f"Invalid height (got {height}, expected {size})")
    if not is_solvable(puzzle):
        panic("Unsolvable puzzle")
    return puzzle
