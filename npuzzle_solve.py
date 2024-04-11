import argparse
import time
from src.hash_puzzle import compressed, uncompressed
from src.heuristics import inversion_distance, manhattan, manhattan_with_conflicts
from src.parse_puzzle import parse_puzzle
from src.solvers import a_star, best_first_search


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename of the puzzle.")
    parser.add_argument(
        "--compress", action="store_true", help="Compress the puzzle representation."
    )
    return parser.parse_args()


def __main():
    args = __parse_args()
    hash_pair = compressed if args.compress else uncompressed
    puzzle = parse_puzzle(args.filename)
    for solver in [a_star]:
        for heuristic in [manhattan_with_conflicts, manhattan, inversion_distance]:
            t0 = time.time()
            solution = solver(puzzle, heuristic, hash_pair)
            print(
                # "".join(move.name[0] for move in solution),
                # heuristic(puzzle, make_goal(math.isqrt(len(puzzle)))),
                len(solution),
                f"{time.time() - t0:.3f}s",
                solver.__name__,
                heuristic.__name__,
            )


if __name__ == "__main__":
    __main()
