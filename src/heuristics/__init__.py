# On top of being admissible, solvers require that heuristic(0) <=> puzzle is solved

from ._manhattan_with_conflicts import manhattan_with_conflicts
from ._inversion_distance import inversion_distance
from ._lebesgue import chebyshev, euclidean, manhattan


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
