import random
import functools


def rand(rows, columns):
    return [[random.randrange(6) for _ in range(rows)] for _ in range(columns)]


def find_row_matches(array):
    return [(i, j) for i in range(len(array)) for j in range(len(array[i]) - 2) if array[i][j] is array[i][j + 1] is array[i][j + 2]]


def find_column_matches(array):
    return [(i, j) for i in range(len(array) - 2) for j in range(len(array[i])) if array[i + 1][j] is array[i + 1][j] is array[i + 2][j]]


def row_op(identity, element):
    if len(identity) is not 0 and identity[-1][0] is element[0] and identity[-1][1] + 1 is element[1]:
        last = identity.pop()
        identity.append((*last[:-1], last[-1] + 1))
        # return [*identity[:-1], (*identity[-1][:-1], identity[-1][-1] + 1)]
    else:
        identity.append((*element, 3))
        # return [*identity, (*element, 3)]
    return identity


def column_op(identity, element):
    if len(identity) is not 0 and identity[-1][0] is element[0] and identity[-1][0] + 1 is element[0]:
        last = identity.pop()
        identity.append((*last[:-1], last[-1] + 1))
        # return [*identity[:-1], (*identity[-1][:-1], identity[-1][-1] + 1)]
    else:
        identity.append((*element, 3))
        # return [*identity, (*element, 3)]
    return identity


def remove_duplicates(op, l):
    return functools.reduce(op, l, [])


def gen():
    while True:
        r = rand(10, 10)
        mr = find_row_matches(r)
        mc = find_column_matches(r)
        dr = remove_duplicates(row_op, mr)
        dc = remove_duplicates(column_op, mc)
        if len(mr) is not len(dr) or len(mc) is not len(dc):
            return r, mr, mc, dr, dc

r, mr, mc, dr, dc = gen()
