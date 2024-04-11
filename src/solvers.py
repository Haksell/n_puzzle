from enum import IntEnum
from heapq import heappop, heappush
from itertools import count
import math
from src.lib import make_goal


class Move(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(self):
        return Move(self.value ^ 2)


def __do_move(puzzle, move, size, zero_idx):
    # TODO: execute the moves directly on the hashed value
    swap_idx = zero_idx + [size, -1, -size, 1][move]
    puzzle[zero_idx], puzzle[swap_idx] = puzzle[swap_idx], puzzle[zero_idx]


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


def __reconstruct_solution(size, came_from, hash_puzzle, hash_pair):
    # TODO: keep track of 0 pos
    size_sq = size * size
    solution = []
    while (move := came_from[hash_puzzle]) is not None:
        solution.append(move)
        puzzle = hash_pair.undo_hash(hash_puzzle, size_sq)
        __do_move(puzzle, move.opposite(), size, puzzle.index(0))
        hash_puzzle = hash_pair.do_hash(puzzle)
    return solution[::-1]


def __setup_search(puzzle, hash_pair):
    size = math.isqrt(len(puzzle))
    goal = make_goal(size)
    hash_goal = hash_pair.do_hash(goal)
    hash_puzzle = hash_pair.do_hash(puzzle)
    came_from = {hash_puzzle: None}
    solution_lengths = {hash_puzzle: 0}
    return (size, goal, hash_goal, hash_puzzle, came_from, solution_lengths)


def __heap_solver(puzzle, heuristic, hash_pair, optimal):
    size, goal, hash_goal, hash_puzzle, came_from, solution_lengths = __setup_search(
        puzzle, hash_pair
    )
    frontier = [(heuristic(puzzle, goal), hash_puzzle)]
    while frontier:
        (_, hash_current) = heappop(frontier)
        if hash_current == hash_goal:
            return __reconstruct_solution(size, came_from, hash_current, hash_pair)
        current = hash_pair.undo_hash(hash_current, len(puzzle))
        zero_idx = current.index(0)
        solution_length = solution_lengths[hash_current] + 1
        for move in __available_moves(size, zero_idx, came_from[hash_current]):
            __do_move(current, move, size, zero_idx)
            hash_neighbor = hash_pair.do_hash(current)
            if solution_length < solution_lengths.get(hash_neighbor, math.inf):
                came_from[hash_neighbor] = move
                solution_lengths[hash_neighbor] = solution_length
                h = heuristic(current, goal)
                heap_priority = solution_length + h if optimal else h
                heappush(frontier, (heap_priority, hash_neighbor))
            __do_move(current, move, size, zero_idx)
    raise RuntimeError("No solution found. This is impossible.")


def __ida_star(puzzle, heuristic, hash_pair, max_depth):
    def dfs(hash_current, depth):
        if depth > max_depth:
            return None
        if hash_current == hash_goal:
            return __reconstruct_solution(size, came_from, hash_current, hash_pair)
        current = hash_pair.undo_hash(hash_current, len(puzzle))
        zero_idx = current.index(0)
        solution_length = solution_lengths[hash_current] + 1
        for move in __available_moves(size, zero_idx, came_from[hash_current]):
            __do_move(current, move, size, zero_idx)
            hash_neighbor = hash_pair.do_hash(current)
            if solution_length < solution_lengths.get(hash_neighbor, math.inf):
                came_from[hash_neighbor] = move
                solution_lengths[hash_neighbor] = solution_length
                h = heuristic(current, goal)
                heap_priority = solution_length + h if optimal else solution_length + h
                if (solution := dfs(hash_neighbor, heap_priority)) is not None:
                    return solution
            __do_move(current, move, size, zero_idx)
        return None

    size, goal, hash_goal, hash_puzzle, came_from, solution_lengths = __setup_search(
        puzzle, hash_pair
    )
    optimal = True
    return dfs(hash_puzzle, heuristic(puzzle, goal))


def a_star(puzzle, heuristic, hash_pair):
    return __heap_solver(puzzle, heuristic, hash_pair, True)


def best_first_search(puzzle, heuristic, hash_pair):
    return __heap_solver(puzzle, heuristic, hash_pair, False)


def ida_star(puzzle, heuristic, hash_pair, step=1):
    return next(
        solution
        for max_depth in count(0, step=step)
        if (solution := __ida_star(puzzle, heuristic, hash_pair, max_depth)) is not None
    )
