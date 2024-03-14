import math
import os
import sys

from lib import make_goal, print_puzzle


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
    def parity_empty(puzzle, size):
        py, px = divmod(puzzle.index(0), size)
        return (size ^ py ^ px ^ 1) & 1

    def parity_permutation(puzzle):
        seen = set()
        transpositions = 0
        for i in range(len(puzzle)):
            if i in seen:
                continue
            seen.add(i)
            j = puzzle[i]
            while j != i:
                seen.add(j)
                j = puzzle[j]
                transpositions ^= 1
        return transpositions

    def parity_compared_to_goal(puzzle, size):
        goal = make_goal(size)
        return parity_permutation(puzzle) ^ parity_permutation(goal)

    size = math.isqrt(len(puzzle))
    return parity_empty(puzzle, size) == parity_compared_to_goal(puzzle, size)


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
                __panic(e)
    if size is None:
        __panic("Empty file")
    height = len(puzzle) // size
    if height != size:
        __panic(f"Invalid height (got {height}, expected {size})")
    if not __is_solvable(puzzle):
        __panic("Unsolvable puzzle")
    return puzzle


def parse(argv):
    return __parse_puzzle(__parse_args(argv))


"""
solvable
1 2 3
8   4
7 6 5

1 2 3 8 4 7 6 5
"""
