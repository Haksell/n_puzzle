from enum import IntEnum, auto
from heapq import heappop, heappush
import math
import time
from heuristics import manhattan, manhattan_with_conflicts
from math import isqrt
from lib import make_goal
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
    # yield would be cooler but it's somehow slower with pypy
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


def __reconstruct_solution(size, came_from, hash_puzzle):
    # TODO: keep track of 0 pos
    size_sq = size * size
    solution = []
    while (move := came_from[hash_puzzle]) is not None:
        solution.append(move)
        puzzle = int_to_perm(hash_puzzle, size_sq)
        __do_move(puzzle, OPPOSITE_MOVES[move], size, puzzle.index(0))
        hash_puzzle = perm_to_int(puzzle)
    return solution[::-1]


def __a_star(puzzle, heuristic):
    size = isqrt(len(puzzle))
    goal = make_goal(size)
    hash_goal = perm_to_int(goal)
    hash_puzzle = perm_to_int(puzzle)
    came_from = {hash_puzzle: None}
    solution_lengths = {hash_puzzle: 0}
    frontier = [(heuristic(puzzle, goal), hash_puzzle)]
    while frontier:
        (_, hash_current) = heappop(frontier)
        if hash_current == hash_goal:
            return __reconstruct_solution(size, came_from, hash_current)
        current = int_to_perm(hash_current, len(puzzle))
        zero_idx = current.index(0)
        solution_length = solution_lengths[hash_current] + 1
        for move in __available_moves(size, zero_idx, came_from[hash_current]):
            __do_move(current, move, size, zero_idx)
            hash_neighbor = perm_to_int(current)
            if solution_length < solution_lengths.get(hash_neighbor, math.inf):
                came_from[hash_neighbor] = move
                solution_lengths[hash_neighbor] = solution_length
                heappush(
                    frontier,
                    (solution_length + heuristic(current, goal), hash_neighbor),
                )
            __do_move(current, move, size, zero_idx)
    raise RuntimeError("No solution found. This is impossible.")


def __main(argv):
    puzzle = parse(argv)
    for heuristic in [manhattan_with_conflicts, manhattan]:
        t0 = time.time()
        solution = __a_star(puzzle, heuristic)
        print(
            "".join(move.name[0] for move in solution),
            heuristic(puzzle, make_goal(isqrt(len(puzzle)))),
            len(solution),
            f"{time.time() - t0:.3f}s",
            heuristic.__name__,
        )


if __name__ == "__main__":
    __main(sys.argv)
