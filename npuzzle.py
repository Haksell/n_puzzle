import argparse
from src import heuristics, solvers
from src.Puzzle import Puzzle
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


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename of the puzzle")
    parser.add_argument(
        "--visualizer", action="store_true", help="Visualize the solution"
    )
    __add_list_arg(parser, "heuristic", heuristics.HEURISTICS)
    __add_list_arg(parser, "solver", solvers.SOLVERS)
    args = parser.parse_args()
    puzzle = Puzzle.from_file(args.filename)
    heuristic = next(h for h in heuristics.HEURISTICS if h.__name__ == args.heuristic)
    solver = next(s for s in solvers.SOLVERS if s.__name__ == args.solver)
    return puzzle, heuristic, solver, args.visualizer


def __main():
    puzzle, heuristic, solver, visualizer = __parse_args()
    print(puzzle)
    print(f"Using {solver.__name__} with {heuristic.__name__}...")
    t0 = time.time()
    solution = solver(puzzle, heuristic)
    print(f"Found {len(solution)}-move solution in {time.time() - t0:.3f}s:")
    print("".join(move.name[0] for move in solution))
    if visualizer:
        Visualizer(puzzle, solution).run()


if __name__ == "__main__":
    __main()
