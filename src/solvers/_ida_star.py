from copy import deepcopy
from itertools import count


def __ida_star(puzzle, heuristic, max_depth, moves):
    for move in puzzle.available_moves(moves[-1] if moves else None):
        puzzle.do_move(move)
        moves.append(move)
        h = heuristic(puzzle)
        if h == 0 or (
            h + len(moves) <= max_depth
            and __ida_star(puzzle, heuristic, max_depth, moves)
        ):
            return moves
        moves.pop()
        puzzle.do_move(move.opposite())


def ida_star(puzzle, heuristic):
    if heuristic(puzzle) == 0:
        return []
    for max_depth in count(1):
        solution = __ida_star(deepcopy(puzzle), heuristic, max_depth, [])
        if solution is not None:
            return solution
