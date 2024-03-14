import os
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
