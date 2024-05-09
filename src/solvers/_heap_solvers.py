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
    if (h_cost := heuristic(puzzle, puzzle.goal)) == 0:
        return []
    tup = tuple(puzzle)
    came_from = {tup: None}
    g_costs = {tup: 0}
    frontier = [(h_cost, tup)]
    while frontier:
        (_, tup) = heappop(frontier)
        puzzle = Puzzle(list(tup), puzzle.height, puzzle.width)
        g_cost = g_costs[tup] + 1
        for move in puzzle.available_moves(came_from[tup]):
            puzzle.do_move(move)
            tup = tuple(puzzle)
            if g_cost < g_costs.get(tup, sys.maxsize):
                came_from[tup] = move
                g_costs[tup] = g_cost
                if (h_cost := heuristic(puzzle, puzzle.goal)) == 0:
                    return __reconstruct_solution(came_from, puzzle)
                heappush(frontier, (use_g * g_cost + use_h * h_cost, tup))
            puzzle.do_move(move.opposite())


def a_star(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=True, use_h=True)


def greedy(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=False, use_h=True)


def uniform_cost(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=True, use_h=False)
