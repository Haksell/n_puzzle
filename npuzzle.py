import argparse
from src import heuristics, solvers
from src.Puzzle import Puzzle
from src.gui import GUI
import time


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename of the puzzle")
    parser.add_argument(
        "--compress", action="store_true", help="Compress the puzzle representation"
    )
    parser.add_argument("--gui", action="store_true", help="Open a window")
    # TODO: refactor heurstic and solver code
    heuristic_names = [h.__name__ for h in heuristics.HEURISTICS]
    parser.add_argument(
        "--heuristic",
        type=str,
        choices=heuristic_names,
        default=heuristic_names[0],
        help=f"Type of heuristic to use. Defaults to {heuristic_names[0]}.",
    )
    solver_names = [h.__name__ for h in solvers.SOLVERS]
    parser.add_argument(
        "--solver",
        type=str,
        choices=solver_names,
        default=solver_names[0],
        help=f"Type of solver to use. Defaults to {solver_names[0]}.",
    )
    args = parser.parse_args()
    puzzle = Puzzle.from_file(args.filename)
    heuristic = next(h for h in heuristics.HEURISTICS if h.__name__ == args.heuristic)
    solver = next(s for s in solvers.SOLVERS if s.__name__ == args.solver)
    return puzzle, heuristic, solver, args.gui


def __main():
    puzzle, heuristic, solver, gui = __parse_args()
    print(list(puzzle))
    t0 = time.time()
    solution = solver(puzzle, heuristic)
    print(
        "".join(move.name[0] for move in solution),
        len(solution),
        f"{time.time() - t0:.3f}s",
        solver.__name__,
        heuristic.__name__,
    )
    if gui:
        GUI(puzzle, solution).run()


if __name__ == "__main__":
    __main()
