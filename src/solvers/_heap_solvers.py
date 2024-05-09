from heapq import heappop, heappush
from src.Puzzle import Puzzle
import sys


def __reconstruct_solution(came_from, puzzle):
    solution = []
    while (move := came_from[tuple(puzzle)]) is not None:
        solution.append(move)
        puzzle.do_move(move.opposite())
    return solution[::-1]


def __heap_solver(puzzle, heuristic, *, use_g, use_h):
    tup_puzzle = tuple(puzzle)
    came_from = {tup_puzzle: None}
    g_costs = {tup_puzzle: 0}
    if (h := heuristic(puzzle, puzzle.goal)) == 0:
        return []
    frontier = [(h, tup_puzzle)]
    while frontier:
        (_, tup_current) = heappop(frontier)
        current = Puzzle(puzzle.height, list(tup_current))
        g_cost = g_costs[tup_current] + 1
        for move in current.available_moves(came_from[tup_current]):
            current.do_move(move)
            tup_neighbor = tuple(current)
            if g_cost < g_costs.get(tup_neighbor, sys.maxsize):
                came_from[tup_neighbor] = move
                g_costs[tup_neighbor] = g_cost
                if (h := heuristic(current, puzzle.goal)) == 0:
                    return __reconstruct_solution(came_from, current)
                heappush(frontier, (use_g * g_cost + use_h * h, tup_neighbor))
            current.do_move(move.opposite())


def a_star(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=True, use_h=True)


def greedy(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=False, use_h=True)


def uniform_cost(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=True, use_h=False)
