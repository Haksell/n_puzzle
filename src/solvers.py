from heapq import heappop, heappush
from itertools import count
import sys
from src.Puzzle import Puzzle


def __reconstruct_solution(came_from, puzzle):
    solution = []
    while (move := came_from[puzzle.hash()]) is not None:
        solution.append(move)
        puzzle.do_move(move.opposite())
    return solution[::-1]


def __solver(puzzle, heuristic, optimal, max_depth, push, pop):
    hash_puzzle = puzzle.hash()
    came_from = {hash_puzzle: None}
    solution_lengths = {hash_puzzle: 0}
    frontier = [(heuristic(puzzle, puzzle.goal), hash_puzzle)]
    while frontier:
        (depth, hash_current) = pop(frontier)
        if depth > max_depth:
            continue
        current = Puzzle(puzzle.height, list(hash_current))
        if current.is_solved():
            return __reconstruct_solution(came_from, current)
        solution_length = solution_lengths[hash_current] + 1
        for move in current.available_moves(came_from[hash_current]):
            current.do_move(move)
            hash_neighbor = current.hash()
            if solution_length < solution_lengths.get(hash_neighbor, sys.maxsize):
                came_from[hash_neighbor] = move
                solution_lengths[hash_neighbor] = solution_length
                depth = heuristic(current, puzzle.goal) + solution_length * optimal
                push(frontier, (depth, hash_neighbor))
            current.do_move(move.opposite())
    raise RuntimeError("No solution found. This shouldn't be possible.")


def a_star(puzzle, heuristic):
    return __solver(puzzle, heuristic, True, sys.maxsize, heappush, heappop)


def ida_star(puzzle, heuristic, step=1):
    for max_depth in count(0, step=step):
        solution = __solver(puzzle, heuristic, True, max_depth, list.append, list.pop)
        if solution is not None:
            return solution


def best_first_search(puzzle, heuristic):
    return __solver(puzzle, heuristic, False, sys.maxsize, heappush, heappop)


SOLVERS = [a_star, ida_star, best_first_search]
