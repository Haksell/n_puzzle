from copy import deepcopy
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
                estimate = heuristic(current, puzzle.goal) + solution_length * optimal
                heappush(frontier, (estimate, hash_neighbor))
            current.do_move(move.opposite())


def a_star(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, True)


def best_first_search(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, False)


def __ida_star(puzzle, heuristic, max_depth, depth, moves, came_from, solution_lengths):
    hash_current = puzzle.hash()
    solution_length = solution_lengths[hash_current] + 1
    for move in puzzle.available_moves(came_from[hash_current]):
        puzzle.do_move(move)
        hash_neighbor = puzzle.hash()
        if solution_length < solution_lengths.get(hash_neighbor, sys.maxsize):
            moves.append(move)
            if puzzle.is_solved():
                return moves
            came_from[hash_neighbor] = move
            solution_lengths[hash_neighbor] = solution_length
            depth = heuristic(puzzle, puzzle.goal) + solution_length
            if depth <= max_depth and __ida_star(
                puzzle, heuristic, max_depth, depth, moves, came_from, solution_lengths
            ):
                return moves
            moves.pop()
        puzzle.do_move(move.opposite())


def ida_star(puzzle, heuristic):
    for max_depth in count(0):
        print(max_depth)
        solution = __ida_star(
            deepcopy(puzzle),
            heuristic,
            max_depth,
            0,
            [],
            {puzzle.hash(): None},
            {puzzle.hash(): 0},
        )
        if solution is not None:
            return solution


SOLVERS = [a_star, best_first_search, ida_star]
