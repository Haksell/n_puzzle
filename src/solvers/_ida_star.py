from copy import deepcopy
from itertools import count


def __ida_star(puzzle, heuristic, max_depth, moves):
    if puzzle.is_solved():
        return moves
    for move in puzzle.available_moves(moves[-1] if moves else None):
        puzzle.do_move(move)
        moves.append(move)
        estimate = heuristic(puzzle, puzzle.goal) + len(moves)
        if estimate <= max_depth and __ida_star(puzzle, heuristic, max_depth, moves):
            return moves
        moves.pop()
        puzzle.do_move(move.opposite())


def ida_star(puzzle, heuristic):
    for max_depth in count(0):
        solution = __ida_star(deepcopy(puzzle), heuristic, max_depth, [])
        if solution is not None:
            return solution
