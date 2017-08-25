from itertools import permutations

import numpy as np


def permute(orig_data):
    l = orig_data.shape[0]

    permuted_data = np.tile(orig_data, (720, 1, 1, 1))

    bool_arrays = [orig_data[:, 0] == i for i in range(6)]

    start, end = 0, l

    for permutation in permutations(range(6)):
        section = permuted_data[start: end, 0]
        for new_colour, bool_array in zip(permutation, bool_arrays):
            section[bool_array] = new_colour
        start, end = end, end + l

    return permuted_data


def permute_generator(orig_data):
    permuted_data = np.copy(orig_data)

    bool_arrays = [orig_data[:, 0] == i for i in range(6)]

    for permutation in permutations(range(6)):
        for new_colour, bool_array in zip(permutation, bool_arrays):
            permuted_data[:, 0][bool_array] = new_colour
        for state in permuted_data:
            yield state
