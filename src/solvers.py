from heapq import heappop, heappush
from itertools import count
import math
from src.Puzzle import Puzzle
from src.lib import Move, do_move


def __available_moves(size, zero_idx, last):
    # TODO: yield would be cooler but it's somehow slower with pypy
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
    solution = []
    while (move := came_from[hash_puzzle]) is not None:
        solution.append(move)
        puzzle = list(hash_puzzle)
        do_move(puzzle, move.opposite(), size, puzzle.index(0))
        hash_puzzle = tuple(puzzle)
    return solution[::-1]


def __solver(puzzle, heuristic, optimal, max_depth, push, pop):
    size = math.isqrt(len(puzzle))
    goal = Puzzle.make_goal(puzzle.height)
    hash_goal = tuple(goal)
    hash_puzzle = tuple(puzzle)
    came_from = {hash_puzzle: None}
    solution_lengths = {hash_puzzle: 0}
    frontier = [(heuristic(puzzle, goal), hash_puzzle)]
    while frontier:
        (depth, hash_current) = pop(frontier)
        if depth > max_depth:
            continue
        if hash_current == hash_goal:
            return __reconstruct_solution(size, came_from, hash_current)
        current = list(hash_current)
        zero_idx = current.index(0)  # TODO keep value somewhere
        solution_length = solution_lengths[hash_current] + 1
        for move in __available_moves(size, zero_idx, came_from[hash_current]):
            do_move(current, move, size, zero_idx)
            hash_neighbor = tuple(current)
            if solution_length < solution_lengths.get(hash_neighbor, math.inf):
                came_from[hash_neighbor] = move
                solution_lengths[hash_neighbor] = solution_length
                depth = heuristic(current, goal) + solution_length * optimal
                push(frontier, (depth, hash_neighbor))
            do_move(current, move, size, zero_idx)


def a_star(puzzle, heuristic):
    return __solver(puzzle, heuristic, True, math.inf, heappush, heappop)


def ida_star(puzzle, heuristic, step=1):
    for max_depth in count(0, step=step):
        solution = __solver(puzzle, heuristic, True, max_depth, list.append, list.pop)
        if solution is not None:
            return solution


def best_first_search(puzzle, heuristic):
    return __solver(puzzle, heuristic, False, math.inf, heappush, heappop)


SOLVERS = [a_star, ida_star, best_first_search]
