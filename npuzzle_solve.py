from enum import IntEnum, auto
from heapq import heappop, heappush
import time
from heuristics import HEURISTICS
from math import isqrt
from lib import make_goal, print_puzzle
from parsing import parse
from permutations import int_to_perm, perm_to_int
import sys


class Move(IntEnum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


OPPOSITE_MOVES = {
    Move.UP: Move.DOWN,
    Move.RIGHT: Move.LEFT,
    Move.DOWN: Move.UP,
    Move.LEFT: Move.RIGHT,
}


# TODO: execute the moves directly on the hashed value
def __do_move(puzzle, move, size, zero_idx):
    swap_idx = (
        zero_idx
        + {
            Move.UP: size,
            Move.RIGHT: -1,
            Move.DOWN: -size,
            Move.LEFT: 1,
        }[move]
    )
    puzzle[zero_idx], puzzle[swap_idx] = puzzle[swap_idx], puzzle[zero_idx]


def __available_moves(size, zero_idx, last):
    y, x = divmod(zero_idx, size)
    moves = []
    if y != 0 and last != Move.UP:
        moves.append(Move.DOWN)
    if x != size - 1 and last != Move.RIGHT:
        moves.append(Move.LEFT)
    if y != size - 1 and last != Move.DOWN:
        moves.append(Move.UP)
    if x != 0 and last != Move.LEFT:
        moves.append(Move.RIGHT)
    return moves


def __reconstruct_solution(puzzle, size, came_from, hash_puzzle):
    solution = []
    while True:
        move = came_from[hash_puzzle]
        if move is None:
            return solution[::-1]
        solution.append(move)
        puzzle = int_to_perm(hash_puzzle, size * size)
        __do_move(puzzle, OPPOSITE_MOVES[move], size, puzzle.index(0))
        hash_puzzle = perm_to_int(puzzle)


def __a_star(puzzle, heuristic):
    # TODO: fix optimality
    size = isqrt(len(puzzle))
    goal = make_goal(size)
    hash_goal = perm_to_int(goal)
    hash_puzzle = perm_to_int(puzzle)
    came_from = {hash_puzzle: None}
    len_solution = {hash_puzzle: 0}
    open_set = [(heuristic(puzzle, goal), hash_puzzle)]
    while open_set:
        _, hash_puzzle = heappop(open_set)
        puzzle = int_to_perm(hash_puzzle, len(puzzle))
        zero_idx = puzzle.index(0)
        for move in __available_moves(size, zero_idx, came_from[hash_puzzle]):
            __do_move(puzzle, move, size, zero_idx)
            hash_moved = perm_to_int(puzzle)
            if hash_moved not in came_from:  # TODO: overwrite if better value
                came_from[hash_moved] = move
                len_solution[hash_moved] = len_solution[hash_puzzle] + 1
                if hash_moved == hash_goal:
                    return __reconstruct_solution(goal, size, came_from, hash_moved)
                heappush(
                    open_set,
                    (len_solution[hash_moved] + heuristic(puzzle, goal), hash_moved),
                )
            __do_move(puzzle, move, size, zero_idx)
    raise RuntimeError("No solution found. This is impossible.")


"""
$ time p npuzzle_solve.py puzzles/valid/solvable4a.txt
 3  9  2 10
11  6 12 15
 1 14  7  8
 0  5 13  4
DLULDLDDRULUURDRDLLURRDDRUUULDDDLLUURDRRUULDDRDLUURDDLLURU 58
python npuzzle_solve.py puzzles/valid/solvable4a.txt  190.86s user 8.20s system 99% cpu 3:21.03 total

$ time p npuzzle_solve.py puzzles/valid/solvable4b.txt
10  8  9  6
 3 11 15  2
 7  1  4  0
 5 13 14 12
RDDRUUURDDDLUURDDLUULDDLUUURRRDLLLURRDLDDLUUURDDLURDRURDLDLUUR 62
python npuzzle_solve.py puzzles/valid/solvable4b.txt  164.78s user 7.43s system 99% cpu 2:52.28 total

$ time p npuzzle_solve.py puzzles/valid/solvable4c.txt
 6  7 13 12
 2  5  3 11
15  4  8 10
 9  1  0 14
DLDRRULDRDRUULDDLLURRDLLURURULDLURRRDLLLDRRRULDDRULLUR 54
python npuzzle_solve.py puzzles/valid/solvable4c.txt  2.48s user 0.15s system 98% cpu 2.672 total

$ time p npuzzle_solve.py puzzles/valid/solvable4d.txt
14  4 11  7
 9  0 15  6
 2  1 13 10
 8 12  3  5
URDLULLDRDRUUURDLLDLDRRRUULLLDRUULDDRUURRDLDDLUULDRRU 53
python npuzzle_solve.py puzzles/valid/solvable4d.txt  32.38s user 1.53s system 99% cpu 33.933 total

$ time p npuzzle_solve.py puzzles/valid/solvable4e.txt
10  6 14  4
11 12  1  5
 2  9  7 13
 8 15  3  0
DRURDRDLLDRUURDDLUURDLUURDDLLDLURUULDRURDLLDDRURU 49
python npuzzle_solve.py puzzles/valid/solvable4e.txt  41.33s user 1.75s system 99% cpu 43.109 total
"""


def __main(argv):
    puzzle = parse(argv)
    print_puzzle(puzzle)
    for heuristic in HEURISTICS:
        t0 = time.time()
        solution = __a_star(puzzle, heuristic)
        print(
            "".join(move.name[0] for move in solution),
            len(solution),
            f"{time.time() - t0:.3f}s",
            heuristic.__name__,
        )


if __name__ == "__main__":
    __main(sys.argv)
