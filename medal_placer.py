import random, itertools, copy

from itertools import product

def medal_grid(ice_grid, medal_grid, medal_number):
    foo = copy.deepcopy(medal_grid)

    rows = len(ice_grid)
    cols = len(ice_grid[0])

    medals_existing = 0

    for I, J in product(range(rows - 1), range(cols - 1)):
        check = any(foo[I + i][J + j] == 2 * i + j for i, j in product(range(2), range(2)))
        if check:
            medals_existing += 1
            for i, j in product(range(2), range(2)):
                foo[i][j] = 2 * i + j

    to_check = list(itertools.product(range(rows - 1), range(cols - 1)))

    for I, J in reversed(to_check):
        ice_check = not all(ice_grid[I + i][J + j] == 0 for i, j in product(range(2), range(2)))
        if ice_check:
            to_check.remove((I, J))

    while True:
        added = 0
        bar = copy.deepcopy(foo)
        to_check_copy = (*to_check,)

        while to_check_copy:
            I, J = to_check_copy.pop(random.randrange(len(to_check_copy)))

            ice_check = (ice_grid[I + i][J + j] == 0 for i, j in product(range(2), range(2)))
            medal_check = (bar[I + i][J + j] == -1 for i, j in product(range(2), range(2)))

            if all(ice_check) and all(medal_check):
                added += 1
                for i, j in product(range(2), range(2)):
                    bar[I + i][J + j] = 2 * i + j
                if medals_existing + added == medal_number:
                    return bar

mg = [[-1 for _ in range(9)] for _ in range(9)]
ig = [[-1 for _ in range(9)] for _ in range(9)]

ig[0][1:6] = ig[1][1:6] = (0,) * 5

mg[0][0] = 0
mg[1][0] = 2

print(ig)
print(mg)
print(medal_grid(ig, mg, 3))
