import numpy as np

from itertools import product
from random import randrange as r


def generate(n):
    a = [[[[r(6), r(4), *((-1, r(4)) if r(2) else (0, -1))] for _ in range(9)] for _ in range(9)] for _ in range(n)]
    return np.array(a)


def permute(orig_data):
    l = orig_data.shape[0]

    permuted_data = np.tile(orig_data, (720, 1, 1, 1))

    permutations = (permutation for permutation in product(*(range(6),) * 6) if all(i in permutation for i in range(6)))

    bool_arrays = [orig_data[:, :, :, 0] == i for i in range(6)]

    for i, permutation in enumerate(permutations):
        for new_colour, bool_array in zip(permutation, bool_arrays):
            permuted_data[i * l: (i + 1) * l, :, :, 0][bool_array] = new_colour

    return permuted_data


def test(p):
    permutations = (permutation for permutation in product(*(range(6),) * 6) if all(i in permutation for i in range(6)))

    for perm, state in zip(permutations, p):
        print('*' * 9)
        print(perm)
        print('\n'.join(''.join(str(el[0]) for el in row) for row in state))
        print('*' * 9)

p = permute(generate(1))
test(p)
