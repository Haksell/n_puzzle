import argparse
import time
from src import heuristics, solvers
from src.hash_puzzle import compressed, uncompressed
from src.parse_puzzle import parse_puzzle


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename of the puzzle.")
    parser.add_argument(
        "--compress", action="store_true", help="Compress the puzzle representation."
    )
    return parser.parse_args()


def __main():
    args = __parse_args()
    puzzle = parse_puzzle(args.filename)
    for solver in [
        solvers.best_first_search,
        solvers.ida_star,
        solvers.a_star,
    ]:
        for heuristic in [heuristics.manhattan_with_conflicts]:
            for hash_pair in [compressed, uncompressed]:
                t0 = time.time()
                solution = solver(puzzle, heuristic, hash_pair)
                print(
                    # "".join(move.name[0] for move in solution),
                    # heuristic(puzzle, make_goal(math.isqrt(len(puzzle)))),
                    len(solution),
                    f"{time.time() - t0:.3f}s",
                    solver.__name__,
                    heuristic.__name__,
                    "compressed" if hash_pair == compressed else "uncompressed",
                )


if __name__ == "__main__":
    __main()
