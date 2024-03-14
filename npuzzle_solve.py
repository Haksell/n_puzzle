from lib import print_puzzle
from parsing import parse
import sys


def main(argv):
    puzzle = parse(argv)
    print_puzzle(puzzle)


if __name__ == "__main__":
    main(sys.argv)
