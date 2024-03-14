import os
import sys


def __panic(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def __parse_args(argv):
    MAX_FILE_SIZE = 1 << 15
    try:
        assert len(argv) == 2
        filename = argv[1]
    except AssertionError:
        program_name = argv[0] if len(argv) >= 1 else os.path.basename(__file__)
        __panic(f"Usage: python {program_name} <filename>")
    try:
        content = open(filename).read(MAX_FILE_SIZE)
        assert len(content) != MAX_FILE_SIZE, f"file too big (max={MAX_FILE_SIZE})"
    except Exception as e:
        __panic(f"Failed to read puzzle '{filename}': {e}")
    return content


def __is_solvable(puzzle):
    return True  # TODO


def __parse_puzzle(content):
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
                __panic(f"Invalid size: {line}")
        else:
            try:
                row = line.split()
                assert (
                    len(row) == size
                ), f"Invalid width (got {len(row)}, expected {size})"
                puzzle.append([])
                for x in line.split():
                    assert all(c.isdigit() for c in x), f"Invalid natural number: {x}"
                    x = int(x)
                    assert (
                        x < size * size
                    ), f"Number too big for given puzzle size: (got {x}, max {size*size-1})"
                    assert x not in seen, f"Duplicate number: {x}"
                    seen.add(x)
                    puzzle[-1].append(x)
            except AssertionError as e:
                __panic(e)
    if size is None:
        __panic("Empty file")
    if len(puzzle) != size:
        __panic(f"Invalid height (got {len(puzzle)}, expected {size})")
    if not __is_solvable(puzzle):
        __panic("Unsolvable puzzle")
    return puzzle


def parse(argv):
    return __parse_puzzle(__parse_args(argv))
