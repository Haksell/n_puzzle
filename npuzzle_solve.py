from math import isqrt
from heuristics import manhattan
from lib import make_goal, print_puzzle
from parsing import parse
import sys


def __a_star(puzzle, heuristic):
    size = isqrt(len(puzzle))
    goal = make_goal(size)
    h = heuristic(puzzle, goal)
    print(h)
    print_puzzle(puzzle)


def main(argv):
    puzzle = parse(argv)
    __a_star(puzzle, manhattan)


if __name__ == "__main__":
    main(sys.argv)
