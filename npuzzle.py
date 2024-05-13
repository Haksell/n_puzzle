import argparse
from copy import deepcopy
import re
from src import HEURISTICS, Puzzle, SOLVERS, Visualizer
from src.utils import panic, parse_size
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
            panic("Can't specify both a filename and a random size.")
        else:
            return Puzzle.from_file(args.filename)
    else:
        if args.random:
            return Puzzle.random(*parse_size(args.random))
        else:
            panic("You should specify a filename or a random size.")


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, help="Filename of the puzzle to solve")
    parser.add_argument(
        "--random", type=str, help="Generate a random puzzle of size [height]x[width]"
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Visualize the solution"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print the puzzle states"
    )
    parser.add_argument(
        "--line-by-line", action="store_true", help="Solve the puzzle line by line"
    )
    __add_list_arg(parser, "heuristic", HEURISTICS)
    __add_list_arg(parser, "solver", SOLVERS)
    args = parser.parse_args()
    puzzle = __make_puzzle(args)
    heuristic = next(h for h in HEURISTICS if h.__name__ == args.heuristic)
    solver = next(s for s in SOLVERS if s.__name__ == args.solver)
    return puzzle, heuristic, solver, args.line_by_line, args.visualize, args.verbose


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


def __solve_line_by_line(puzzle, solver, heuristic):
    solution = []
    full_goal = deepcopy(puzzle.goal)
    zeroy, zerox = divmod(full_goal.index(0), puzzle.width)
    pw = puzzle.width
    mask = {0}
    time_complexity = 0
    size_complexity = 0
    while puzzle.minx < puzzle.maxx or puzzle.miny < puzzle.maxy:
        dt = zeroy - puzzle.miny
        dr = puzzle.maxx - zerox
        db = puzzle.maxy - zeroy
        dl = zerox - puzzle.minx
        best = max(dt, dr, db, dl)
        if best == dt:
            line = full_goal[puzzle.miny * pw : (puzzle.miny + 1) * pw][
                puzzle.minx : puzzle.maxx + 1
            ]
            print(f"Solving row {puzzle.miny}...")
            puzzle.miny += 1
        elif best == dr:
            line = full_goal[puzzle.maxx :: pw][puzzle.miny : puzzle.maxy + 1]
            print(f"Solving col {puzzle.maxx}...")
            puzzle.maxx -= 1
        elif best == db:
            line = full_goal[puzzle.maxy * pw : (puzzle.maxy + 1) * pw][
                puzzle.minx : puzzle.maxx + 1
            ]
            print(f"Solving row {puzzle.maxy}...")
            puzzle.maxy -= 1
        else:
            line = full_goal[puzzle.minx :: pw][puzzle.miny : puzzle.maxy + 1]
            print(f"Solving col {puzzle.minx}...")
            puzzle.minx += 1
        mask.update(line)
        puzzle.update_goal([x if x in mask else -1 for x in full_goal])
        line_solution, sub_time_complexity, sub_size_complexity = solver(
            deepcopy(puzzle), heuristic
        )
        time_complexity += sub_time_complexity
        size_complexity = max(size_complexity, sub_size_complexity)
        for move in line_solution:
            puzzle.do_move(move)
        solution.extend(line_solution)
    return solution, time_complexity, size_complexity


def __main():
    puzzle, heuristic, solver, line_by_line, visualize, verbose = __parse_args()
    print(
        f"Using {__solver_name(solver)} with {heuristic.__name__} to solve this puzzle{' line by line' if line_by_line else ''}:"
    )
    print(puzzle)
    t0 = time.time()
    solution, time_complexity, size_complexity = (
        __solve_line_by_line(deepcopy(puzzle), solver, heuristic)
        if line_by_line
        else solver(deepcopy(puzzle), heuristic)
    )
    print(f"Time complexity: {time_complexity:,} states selected")
    print(
        f"Size complexity: at most {size_complexity:,} state{'s' if size_complexity>=2 else ''} stored in memory at the same time"
    )
    print(f"Found {len(solution)}-move solution in {time.time() - t0:.3f}s:")
    print("".join(move.name[0] for move in solution))
    if verbose:
        __print_states(puzzle, solution)
    if visualize:
        Visualizer(puzzle, solution).run()


if __name__ == "__main__":
    __main()
