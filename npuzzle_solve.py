from enum import IntEnum, auto
from heapq import heappop, heappush
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
    frontier = [(heuristic(puzzle, goal), hash_puzzle)]
    while frontier:
        _, hash_puzzle = heappop(frontier)
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
                    frontier,
                    (len_solution[hash_moved] + heuristic(puzzle, goal), hash_moved),
                )
            __do_move(puzzle, move, size, zero_idx)
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
