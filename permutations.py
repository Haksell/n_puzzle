from functools import cache


@cache
def __factorial(n):
    return 1 if n <= 1 else n * __factorial(n - 1)


# TODO efficiently: https://stackoverflow.com/questions/9860588/maximum-value-for-long-integer


def perm_to_int(perm):
    assert sorted(perm) == list(range(len(perm)))
    return (
        perm[0] * __factorial(len(perm) - 1)
        + perm_to_int([x - (x > perm[0]) for x in perm[1:]])
        if perm
        else 0
    )


def int_to_perm(n, size):
    assert isinstance(n, int) and 0 <= n < __factorial(size)
    if size == 0:
        return []
    first, n = divmod(n, __factorial(size - 1))
    return [first] + [x + (x >= first) for x in int_to_perm(n, size - 1)]
