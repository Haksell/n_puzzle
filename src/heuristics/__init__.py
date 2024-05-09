from ._manhattan_with_conflicts import manhattan_with_conflicts
from ._inversion_distance import inversion_distance
from ._lebesgue import chebyshev, euclidean, manhattan
from ._trivial import constant_zero, hamming

HEURISTICS = [
    manhattan_with_conflicts,
    inversion_distance,
    chebyshev,
    euclidean,
    manhattan,
    constant_zero,
    hamming,
]
