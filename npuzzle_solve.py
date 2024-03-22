from enum import IntEnum, auto
from heapq import heappop, heappush
from heuristics import manhattan
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


# Can we execute the moves directly on the hashed value?
def do_move(puzzle, move, size, zero_idx):
    swap_idx = (
        zero_idx
        + {
            Move.UP: -size,
            Move.RIGHT: 1,
            Move.DOWN: size,
            Move.LEFT: -1,
        }[move]  # TODO: reverse the moves
    )
    try:
        puzzle[zero_idx], puzzle[swap_idx] = puzzle[swap_idx], puzzle[zero_idx]
    except:
        print(puzzle, size, zero_idx, swap_idx)
        raise


def available_moves(size, zero_idx, last):
    y, x = divmod(zero_idx, size)
    moves = []
    if y != 0 and last != Move.DOWN:
        moves.append(Move.UP)
    if x != size - 1 and last != Move.LEFT:
        moves.append(Move.RIGHT)
    if y != size - 1 and last != Move.UP:
        moves.append(Move.DOWN)
    if x != 0 and last != Move.RIGHT:
        moves.append(Move.LEFT)
    return moves


def __a_star(puzzle, heuristic):
    # TODO: came_from idea
    # TODO: check this is A* and not Dijkstra
    size = isqrt(len(puzzle))
    goal = make_goal(size)
    hash_goal = perm_to_int(goal)
    hash_puzzle = perm_to_int(puzzle)
    closed_set = {hash_puzzle}
    print_puzzle(puzzle)
    open_set = [(heuristic(puzzle, goal), hash_puzzle, [])]
    while open_set:
        _, hash_puzzle, moves = heappop(open_set)
        puzzle = int_to_perm(hash_puzzle, len(puzzle))
        zero_idx = puzzle.index(0)
        for move in available_moves(size, zero_idx, moves[-1] if moves else None):
            do_move(puzzle, move, size, zero_idx)
            hash_puzzle = perm_to_int(puzzle)
            if hash_puzzle not in closed_set:
                moves.append(move)
                if hash_puzzle == hash_goal:
                    print("".join(OPPOSITE_MOVES[m].name[0] for m in moves), len(moves))
                    print_puzzle(puzzle)
                    return
                closed_set.add(hash_puzzle)
                heappush(
                    open_set,
                    (len(moves) + heuristic(puzzle, goal), hash_puzzle, moves.copy()),
                )
                moves.pop()
            do_move(puzzle, move, size, zero_idx)
    print("No solution found. This shouldn't happen.")


def main(argv):
    puzzle = parse(argv)
    __a_star(puzzle, manhattan)


if __name__ == "__main__":
    main(sys.argv)
