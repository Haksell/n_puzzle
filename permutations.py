# https://stackoverflow.com/a/24689277/10793260


def int_to_perm(n, size):
    permuted = [0] * size
    elems = list(range(size))
    for i in range(size):
        n, ind = divmod(n, size - i)
        permuted[i] = elems[ind]
        elems[ind] = elems[size - i - 1]
    return permuted


def perm_to_int(perm):
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
