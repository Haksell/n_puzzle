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


def __check_solvable(puzzle):
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
            except ValueError:
                __panic(f"Invalid size: {line}")
        else:
            row = list(map(int, line.split()))  # TODO: try
            assert (
                len(row) == size
            ), f"invalid row size (for {len(row)}, expected {size})"
            for x in row:
                assert 0 <= x, f"negative number found: {x}"
                assert x < size, f"number too big for given puzzle size: (got {x})"
            assert all(0 <= x < size * size for x in row)
            assert all(x not in seen for x in row)
            seen |= set(row)
            puzzle.append(row)
    assert len(puzzle) == size
    assert __check_solvable(puzzle)
    return puzzle


def parse(argv):
    return __parse_puzzle(__parse_args(argv))