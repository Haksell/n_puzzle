from heapq import heappop, heappush
from src import Puzzle
import sys


def __reconstruct_solution(came_from, puzzle):
    solution = []
    while (move := came_from[tuple(puzzle)]) is not None:
        solution.append(move)
        puzzle.do_move(move.opposite())
    return solution[::-1]


def mask(puzzle):
    return tuple(x if x in puzzle.goal else -1 for x in puzzle)


def __heap_solver(puzzle, heuristic, *, use_g, use_h):
    if (h_cost := heuristic(puzzle)) == 0:
        return [], 0, 0
    tup = mask(puzzle)
    came_from = {tup: None}
    g_costs = {tup: 0}
    open_set = [(h_cost, h_cost, tup)]
    time_complexity = 0
    size_complexity = 1
    while open_set:
        (_, _, tup) = heappop(open_set)
        time_complexity += 1
        puzzle = Puzzle(list(tup), puzzle.height, puzzle.width, goal=puzzle.goal)
        g_cost = g_costs[tup] + 1
        for move in puzzle.available_moves(came_from[tup]):
            puzzle.do_move(move)
            tup = mask(puzzle)
            if g_cost < g_costs.get(tup, sys.maxsize):
                came_from[tup] = move
                g_costs[tup] = g_cost
                if (h_cost := heuristic(puzzle)) == 0:
                    return (
                        __reconstruct_solution(came_from, puzzle),
                        time_complexity,
                        size_complexity,
                    )
                heappush(
                    open_set,
                    (use_g * g_cost + use_h * h_cost, h_cost, tup),
                )
                size_complexity = max(size_complexity, len(open_set) + len(g_costs))
            puzzle.do_move(move.opposite())


def a_star(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=True, use_h=True)


def greedy(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=False, use_h=True)


def uniform_cost(puzzle, heuristic):
    return __heap_solver(puzzle, heuristic, use_g=True, use_h=False)
