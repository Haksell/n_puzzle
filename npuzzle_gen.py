#!/usr/bin/env python

import argparse
from lib import make_goal, print_puzzle
import random
import sys

# TODO: generate using shuffle + solvable check


def __swap_empty(p, s):
    idx = p.index(0)
    moves = []
    if idx % s > 0:
        moves.append(idx - 1)
    if idx % s < s - 1:
        moves.append(idx + 1)
    if idx >= s:
        moves.append(idx - s)
    if idx < s * (s - 1):
        moves.append(idx + s)
    move = random.choice(moves)
    p[idx] = p[move]
    p[move] = 0


def __make_unsolvable(p):
    if p[0] == 0 or p[1] == 0:
        p[-1], p[-2] = p[-2], p[-1]
    else:
        p[0], p[1] = p[1], p[0]


def __make_puzzle(s, solvable, iterations):
    p = make_goal(s)
    for _ in range(iterations):
        __swap_empty(p, s)
    if not solvable:
        __make_unsolvable(p)
    return p


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
    args = parser.__parse_args()
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
    for size in range(3, 7):
        goal = make_goal(size)
        print_puzzle(goal)
        print()
    return
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
