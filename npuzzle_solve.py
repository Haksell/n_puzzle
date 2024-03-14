from parsing import parse
from pprint import pprint
import sys


def main(argv):
    puzzle = parse(argv)
    pprint(puzzle)


if __name__ == "__main__":
    main(sys.argv)
