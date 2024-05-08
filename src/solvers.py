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


def __heap_solver(puzzle, heuristic, optimal):
    hash_puzzle = puzzle.hash()
    came_from = {hash_puzzle: None}
    solution_lengths = {hash_puzzle: 0}
    frontier = [(heuristic(puzzle, puzzle.goal), hash_puzzle)]
    while frontier:
        (_, hash_current) = heappop(frontier)
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
                heappush(frontier, (depth, hash_neighbor))
            current.do_move(move.opposite())


def a_star(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, True)


def best_first_search(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, False)


def __ida_star(puzzle, heuristic, optimal, max_depth):
    hash_puzzle = puzzle.hash()
    came_from = {hash_puzzle: None}
    solution_lengths = {hash_puzzle: 0}
    frontier = [(heuristic(puzzle, puzzle.goal), hash_puzzle)]
    while frontier:
        (depth, hash_current) = frontier.pop()
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
                frontier.append((depth, hash_neighbor))
            current.do_move(move.opposite())


def ida_star(puzzle, heuristic):
    for max_depth in count(0):
        solution = __ida_star(puzzle, heuristic, True, max_depth)
        if solution is not None:
            return solution


SOLVERS = [a_star, best_first_search, ida_star]
