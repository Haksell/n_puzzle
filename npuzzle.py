import argparse
from copy import deepcopy
import re
from src import heuristics, solvers
from src.Puzzle import Puzzle
from src.utils import panic
from src.Visualizer import Visualizer
import time


def __add_list_arg(parser, flag, funcs):
    names = [h.__name__ for h in funcs]
    parser.add_argument(
        f"--{flag}",
        type=str,
        choices=names,
        default=names[0],
        help=f"Type of {flag} to use. Defaults to {names[0]}.",
    )


def __make_puzzle(args):
    if args.filename:
        if args.random:
            panic("Can't specify both a filename and a random size")
        else:
            return Puzzle.from_file(args.filename)
    else:
        if args.random:
            if fullmatch := re.fullmatch(r"(\d+)x(\d+)", args.random):
                return Puzzle.random(int(fullmatch.group(1)), int(fullmatch.group(2)))
            else:
                panic(f"Invalid size: {args.random}")
        else:
            panic("Can't specify both a filename and a random size")


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Filename of the puzzle to solve")
    parser.add_argument(
        "--random", type=str, help="Generate a random puzzle of size [h]x[w]"
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Visualize the solution"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print the puzzle states"
    )
    __add_list_arg(parser, "heuristic", heuristics.HEURISTICS)
    __add_list_arg(parser, "solver", solvers.SOLVERS)
    args = parser.parse_args()
    puzzle = __make_puzzle(args)
    heuristic = next(h for h in heuristics.HEURISTICS if h.__name__ == args.heuristic)
    solver = next(s for s in solvers.SOLVERS if s.__name__ == args.solver)
    return puzzle, heuristic, solver, args.visualize, args.verbose


def __solver_name(solver):
    official = solver.__name__
    fullmatch = re.fullmatch(r"(\w+)_star", official)
    return fullmatch.group(1).upper() + "*" if fullmatch else official


def __print_states(puzzle, solution):
    line_width = (puzzle.padding + 1) * puzzle.width - 1
    print()
    print("=== PUZZLE STATES ===")
    print()
    print(puzzle)
    for move in solution:
        puzzle.do_move(move)
        print()
        print(move.char() * line_width)
        print()
        print(puzzle)


def __main():
    puzzle, heuristic, solver, visualize, verbose = __parse_args()
    print(
        f"Using {__solver_name(solver)} with {heuristic.__name__} to solve this puzzle:"
    )
    print(puzzle)
    t0 = time.time()
    solution = solver(deepcopy(puzzle), heuristic)
    print(f"Found {len(solution)}-move solution in {time.time() - t0:.3f}s:")
    print("".join(move.name[0] for move in solution))
    if verbose:
        __print_states(puzzle, solution)
    if visualize:
        Visualizer(puzzle, solution).run()


if __name__ == "__main__":
    __main()
