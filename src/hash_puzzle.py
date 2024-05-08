from dataclasses import dataclass
from typing import Any, Callable, List


@dataclass
class HashPair:
    name: str
    do_hash: Callable[[List[int]], Any]
    undo_hash: Callable[[Any, int], List[int]]


# TODO: more basic __perm_to_int with 4/5 bits for each number

# https://stackoverflow.com/a/24689277/10793260


def __perm_to_int(perm):
    k = 0
    m = 1
    n = len(perm)
    pos = list(range(n))
    elems = list(range(n))
    for i in range(n - 1):
        k += m * pos[perm[i]]
        m *= n - i
        pos[elems[n - i - 1]] = pos[perm[i]]
        elems[pos[perm[i]]] = elems[n - i - 1]
    return k


def __int_to_perm(n, size):
    permuted = [0] * size
    elems = list(range(size))
    for i in range(size):
        n, ind = divmod(n, size - i)
        permuted[i] = elems[ind]
        elems[ind] = elems[size - i - 1]
    return permuted


compressed = HashPair("compressed", __perm_to_int, __int_to_perm)
uncompressed = HashPair(
    "uncompressed", tuple, lambda a, _: list(a)
)  # TODO: just identity function
