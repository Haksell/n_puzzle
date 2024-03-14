#!/usr/bin/env python

import sys
import argparse
import random


def make_goal(s):
    ts = s * s
    puzzle = [-1] * ts
    cur = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while True:
        puzzle[x + y * s] = cur
        if cur == 0:
            break
        cur += 1
        if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * s] != -1):
            iy = ix
            ix = 0
        elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y + iy) * s] != -1):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        if cur == s * s:
            cur = 0

    return puzzle


def swap_empty(p, s):
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


def make_unsolvable(p):
    if p[0] == 0 or p[1] == 0:
        p[-1], p[-2] = p[-2], p[-1]
    else:
        p[0], p[1] = p[1], p[0]


def make_puzzle(s, solvable, iterations):
    p = make_goal(s)
    for _ in range(iterations):
        swap_empty(p, s)
    if not solvable:
        make_unsolvable(p)
    return p


def parse_args():
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
    args = parse_args()
    solvable = (
        True
        if args.solvable
        else False
        if args.unsolvable
        else random.choice([True, False])
    )
    puzzle = make_puzzle(args.size, solvable=solvable, iterations=args.iterations)
    w = len(str(args.size**2))
    print(f"# This puzzle is {'solvable' if solvable else 'unsolvable'}")
    print(args.size)
    for y in range(args.size):
        print(
            " ".join(str(puzzle[x + y * args.size]).rjust(w) for x in range(args.size))
        )


if __name__ == "__main__":
    main()
