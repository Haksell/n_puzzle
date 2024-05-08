from copy import deepcopy
from heapq import heappop, heappush
from itertools import count
import sys
from src.Puzzle import Puzzle


def __reconstruct_solution(came_from, puzzle):
    solution = []
    while (move := came_from[tuple(puzzle)]) is not None:
        solution.append(move)
        puzzle.do_move(move.opposite())
    return solution[::-1]


def __heap_solver(puzzle, heuristic, optimal):
    tup_puzzle = tuple(puzzle)
    came_from = {tup_puzzle: None}
    solution_lengths = {tup_puzzle: 0}
    frontier = [(heuristic(puzzle, puzzle.goal), tup_puzzle)]
    while frontier:
        (_, tup_current) = heappop(frontier)
        current = Puzzle(puzzle.height, list(tup_current))
        if current.is_solved():
            return __reconstruct_solution(came_from, current)
        solution_length = solution_lengths[tup_current] + 1
        for move in current.available_moves(came_from[tup_current]):
            current.do_move(move)
            tup_neighbor = tuple(current)
            if solution_length < solution_lengths.get(tup_neighbor, sys.maxsize):
                came_from[tup_neighbor] = move
                solution_lengths[tup_neighbor] = solution_length
                estimate = heuristic(current, puzzle.goal) + solution_length * optimal
                heappush(frontier, (estimate, tup_neighbor))
            current.do_move(move.opposite())


def a_star(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, True)


def best_first_search(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, False)


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


SOLVERS = [a_star, best_first_search, ida_star]
