# On top of being admissible, solvers require that:
# (heuristic(puzzle) == 0) == puzzle.is_solved()

from ._manhattan_with_conflicts import manhattan_with_conflicts
from ._inversion_distance import inversion_distance
from ._lebesgue import chebyshev, euclidean, manhattan

# TODO: heuristic that prefers solved edges to solved centers
# TODO: solver decorator that returns [] on solved puzzle


def hamming(puzzle, goal):
    return sum(0 != pi != gi for pi, gi in zip(puzzle, goal))


HEURISTICS = [
    manhattan_with_conflicts,
    inversion_distance,
    chebyshev,
    euclidean,
    manhattan,
    hamming,
]
