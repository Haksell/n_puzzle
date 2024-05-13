from copy import deepcopy
from itertools import count


def __ida_star(puzzle, heuristic, max_depth, moves):
    time_complexity = 1
    for move in puzzle.available_moves(moves[-1] if moves else None):
        puzzle.do_move(move)
        moves.append(move)
        h = heuristic(puzzle)
        if h == 0:
            return moves, time_complexity
        if h + len(moves) <= max_depth:
            solution, sub_time_complexity = __ida_star(
                puzzle, heuristic, max_depth, moves
            )
            time_complexity += sub_time_complexity
            if solution is not None:
                return moves, time_complexity
        moves.pop()
        puzzle.do_move(move.opposite())
    return None, time_complexity


def ida_star(puzzle, heuristic):
    if heuristic(puzzle) == 0:
        return [], 0, 0
    total_time_complexity = 0
    for max_depth in count(1):
        solution, time_complexity = __ida_star(
            deepcopy(puzzle), heuristic, max_depth, []
        )
        total_time_complexity += time_complexity
        if solution is not None:
            return solution, time_complexity, 1
