#!/usr/bin/env python

import argparse
from lib import make_goal, print_puzzle
import random
import sys

# TODO: generate using shuffle + solvable check


def __swap_empty(puzzle, size):
    idx = puzzle.index(0)
    moves = []
    if idx % size > 0:
        moves.append(idx - 1)
    if idx % size < size - 1:
        moves.append(idx + 1)
    if idx >= size:
        moves.append(idx - size)
    if idx < size * (size - 1):
        moves.append(idx + size)
    move = random.choice(moves)
    puzzle[idx] = puzzle[move]
    puzzle[move] = 0


def __make_unsolvable(puzzle):
    if puzzle[0] == 0 or puzzle[1] == 0:
        puzzle[-1], puzzle[-2] = puzzle[-2], puzzle[-1]
    else:
        puzzle[0], puzzle[1] = puzzle[1], puzzle[0]


def __make_puzzle(size, solvable, iterations):
    puzzle = make_goal(size)
    for _ in range(iterations):
        __swap_empty(puzzle, size)
    if not solvable:
        __make_unsolvable(puzzle)
    return puzzle


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "size", type=int, help="Size of the puzzle's side. Must be ≥ 3."
    )
    parser.add_argument(
        "-s",
        "--solvable",
        action="store_true",
        default=False,
        help="Forces generation of a solvable puzzle.",
    )
    parser.add_argument(
        "-u",
        "--unsolvable",
        action="store_true",
        default=False,
        help="Forces generation of an unsolvable puzzle.",
    )
    parser.add_argument(
        "-i", "--iterations", type=int, default=10000, help="Number of passes"
    )
    args = parser.parse_args()
    if args.solvable and args.unsolvable:
        print("Can't be both solvable AND unsolvable, dummy !")
        sys.exit(1)
    if args.size < 3:
        print(
            "Can't generate a puzzle with size lower than 2. It says so in the help. Dummy."
        )
        sys.exit(1)
    return args


def main():
    args = __parse_args()
    solvable = (
        True
        if args.solvable
        else False
        if args.unsolvable
        else random.choice([True, False])
    )
    puzzle = __make_puzzle(args.size, solvable=solvable, iterations=args.iterations)
    print(f"# This puzzle is {'solvable' if solvable else 'unsolvable'}")
    print(args.size)
    print_puzzle(puzzle)


if __name__ == "__main__":
    main()
