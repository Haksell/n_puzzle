import itertools
from math import factorial
import os
from src.lib import is_solvable, make_goal

# TODO: fix parsing testing from src.parse_puzzle import parse_puzzle
from src.hash_puzzle import compressed
import pytest

DIR_VALID = "puzzles/valid"
DIR_INVALID = "puzzles/invalid"


def test_parse_valid():
    KNOWN_PUZZLES = {
        os.path.join(DIR_VALID, "subject3.txt"): [3, 2, 6, 1, 4, 0, 8, 7, 5],
        os.path.join(DIR_VALID, "swap3.txt"): [1, 2, 3, 0, 8, 4, 7, 6, 5],
        os.path.join(DIR_VALID, "solvable8.txt"): [
            1,
            45,
            11,
            35,
            17,
            54,
            46,
            51,
            3,
            37,
            29,
            44,
            5,
            26,
            22,
            25,
            27,
            28,
            55,
            60,
            15,
            10,
            12,
            0,
            24,
            41,
            39,
            58,
            47,
            52,
            2,
            40,
            18,
            8,
            49,
            4,
            20,
            7,
            36,
            9,
            43,
            21,
            30,
            23,
            48,
            59,
            63,
            6,
            62,
            53,
            33,
            34,
            56,
            61,
            14,
            38,
            57,
            13,
            42,
            31,
            19,
            50,
            32,
            16,
        ],
        **{
            os.path.join(DIR_VALID, f"solved{i}.txt"): make_goal(i)
            for i in range(3, 10)
        },
    }
    for filename in sorted(os.listdir(DIR_VALID)):
        filename = os.path.join(DIR_VALID, filename)
        print(filename)
        puzzle = parse_puzzle(filename)
        if filename in KNOWN_PUZZLES:
            assert puzzle == KNOWN_PUZZLES[filename]


def test_parse_invalid():
    filenames = sorted(os.listdir(DIR_INVALID))
    filenames.append("/osquery.flags")
    filenames.append("/dev/random")
    filenames.append("/")
    filenames.append("/abcdefgh")
    for filename in filenames:
        filename = os.path.join(DIR_INVALID, filename)
        print(filename)
        with pytest.raises(SystemExit) as exc_info:
            parse_puzzle(filename)
        assert exc_info.value.code == 1


def test_is_solvable():
    for i in range(3, 10):
        goal = make_goal(i)
        assert is_solvable(goal)
        goal[0], goal[1] = goal[1], goal[0]
        assert not is_solvable(goal)
        goal[2], goal[1] = goal[1], goal[2]
        assert is_solvable(goal)
    assert is_solvable([2, 6, 8, 1, 4, 3, 5, 0, 7])
    assert is_solvable([4, 3, 6, 2, 8, 5, 1, 7, 0])
    assert is_solvable([11, 14, 1, 10, 7, 4, 12, 15, 13, 5, 3, 2, 8, 6, 9, 0])
    assert is_solvable([10, 3, 1, 8, 7, 14, 0, 13, 15, 5, 4, 9, 6, 2, 11, 12])
    assert is_solvable(
        [
            12,
            22,
            9,
            10,
            5,
            11,
            4,
            18,
            14,
            1,
            19,
            8,
            20,
            7,
            6,
            3,
            16,
            0,
            2,
            23,
            24,
            17,
            13,
            15,
            21,
        ]
    )
    assert is_solvable(
        [
            3,
            12,
            16,
            8,
            24,
            20,
            10,
            9,
            4,
            21,
            13,
            5,
            7,
            15,
            11,
            2,
            0,
            17,
            18,
            23,
            19,
            6,
            14,
            22,
            1,
        ]
    )
    assert is_solvable(
        [
            5,
            30,
            27,
            25,
            33,
            3,
            2,
            19,
            32,
            0,
            15,
            6,
            29,
            16,
            34,
            1,
            23,
            4,
            31,
            13,
            17,
            26,
            11,
            20,
            18,
            12,
            22,
            21,
            24,
            28,
            14,
            9,
            35,
            8,
            10,
            7,
        ]
    )
    assert is_solvable(
        [
            13,
            12,
            11,
            28,
            30,
            1,
            35,
            9,
            0,
            26,
            31,
            3,
            14,
            32,
            10,
            2,
            4,
            23,
            7,
            19,
            17,
            34,
            25,
            22,
            27,
            20,
            6,
            16,
            33,
            24,
            21,
            5,
            8,
            18,
            15,
            29,
        ]
    )
    assert not is_solvable([5, 4, 7, 2, 1, 0, 6, 8, 3])
    assert not is_solvable([3, 7, 0, 4, 5, 1, 8, 6, 2])
    assert not is_solvable([13, 12, 8, 1, 3, 4, 14, 10, 6, 2, 0, 7, 9, 15, 5, 11])
    assert not is_solvable([14, 4, 7, 5, 6, 1, 15, 12, 8, 2, 9, 10, 0, 11, 13, 3])
    assert not is_solvable(
        [
            17,
            11,
            3,
            0,
            4,
            2,
            21,
            22,
            23,
            9,
            6,
            15,
            14,
            13,
            7,
            1,
            19,
            16,
            18,
            12,
            8,
            20,
            24,
            5,
            10,
        ]
    )
    assert not is_solvable(
        [
            17,
            3,
            19,
            12,
            11,
            5,
            23,
            10,
            21,
            16,
            7,
            15,
            1,
            14,
            4,
            13,
            18,
            8,
            0,
            24,
            9,
            6,
            22,
            20,
            2,
        ]
    )
    assert not is_solvable(
        [
            1,
            4,
            16,
            28,
            18,
            26,
            24,
            33,
            5,
            7,
            22,
            34,
            6,
            35,
            10,
            32,
            0,
            19,
            12,
            30,
            31,
            3,
            27,
            2,
            20,
            23,
            9,
            13,
            25,
            11,
            29,
            15,
            21,
            17,
            8,
            14,
        ]
    )
    assert not is_solvable(
        [
            20,
            6,
            26,
            22,
            27,
            29,
            12,
            5,
            0,
            25,
            13,
            7,
            14,
            15,
            2,
            34,
            8,
            18,
            9,
            23,
            28,
            3,
            30,
            17,
            35,
            24,
            33,
            1,
            31,
            21,
            16,
            4,
            32,
            11,
            10,
            19,
        ]
    )


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


def test_compression():
    for size in range(6):
        results = []
        for n, p in enumerate(itertools.permutations(range(size))):
            p = list(p)
            res = compressed.do_hash(p)
            assert compressed.undo_hash(compressed.do_hash(p), size) == p
            assert compressed.do_hash(compressed.undo_hash(n, size)) == n
            results.append(res)
        assert sorted(results) == list(range(factorial(size)))
