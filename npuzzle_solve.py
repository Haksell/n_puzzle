from parsing import parse_args, parse_puzzle
from pprint import pprint
import sys


def main(argv):
    content = parse_args(argv)
    puzzle = parse_puzzle(content)
    pprint(puzzle)


if __name__ == "__main__":
    main(sys.argv)
