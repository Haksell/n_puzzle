import os
from lib import make_goal
from parsing import parse
import pytest

DIR_VALID = "puzzles/valid"
DIR_INVALID = "puzzles/invalid"


def test_valid():
    for filename in sorted(os.listdir(DIR_VALID)):
        filename = os.path.join(DIR_VALID, filename)
        print(filename)
        print(parse(["npuzzle_solve.py", filename]))


def test_invalid():
    for filename in sorted(os.listdir(DIR_INVALID)):
        filename = os.path.join(DIR_INVALID, filename)
        print(filename)
        with pytest.raises(SystemExit) as exc_info:
            parse(["npuzzle_solve.py", filename])
        assert exc_info.value.code == 1


def test_is_solvable():
    assert False


def test_make_goal():
    assert make_goal(3) == [1, 2, 3, 8, 0, 4, 7, 6, 5]
    assert make_goal(4) == [1, 2, 3, 4, 12, 13, 14, 5, 11, 0, 15, 6, 10, 9, 8, 7]
    assert make_goal(5) == [
        1,
        2,
        3,
        4,
        5,
        16,
        17,
        18,
        19,
        6,
        15,
        24,
        0,
        20,
        7,
        14,
        23,
        22,
        21,
        8,
        13,
        12,
        11,
        10,
        9,
    ]
    assert make_goal(6) == [
        1,
        2,
        3,
        4,
        5,
        6,
        20,
        21,
        22,
        23,
        24,
        7,
        19,
        32,
        33,
        34,
        25,
        8,
        18,
        31,
        0,
        35,
        26,
        9,
        17,
        30,
        29,
        28,
        27,
        10,
        16,
        15,
        14,
        13,
        12,
        11,
    ]
