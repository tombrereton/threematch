import random, itertools, copy

from itertools import product

def medal_grid(ice_grid: list, medal_grid: list, medal_number: int):
    """
    Fills in a medal grid
    :param ice_grid: Grid of ice
    :param medal_grid: Partial medal grid, only uncovered medals will show
    :param medal_number: Number of medals that need to be in the grid
    :return: Filled medal grid
    """
    # Make a copy of medal_grid
    foo = copy.deepcopy(medal_grid)

    # Get the number of rows
    rows = len(ice_grid)
    # Get the number of columns
    cols = len(ice_grid[0])

    # Count how many medals are already placed in the grid
    medals_existing = 0

    # Iterate through grid looking for top left of medals
    for I, J in product(range(rows - 1), range(cols - 1)):
        # Check if this position is the top left of a medal by checking if there are other portions in the right place
        partial_check = any(foo[I + i][J + j] == 2 * i + j for i, j in product(range(2), range(2)))
        if partial_check:
            # If so increment the medals_existing count...
            medals_existing += 1
            # And fill in the medal
            for i, j in product(range(2), range(2)):
                foo[i][j] = 2 * i + j
            # Check if all the medals have been added yet
                if medals_existing == medal_number:
                    # If so return the new medal grid
                    return foo

    # List all the coordinates in the grid
    to_check = list(itertools.product(range(rows - 1), range(cols - 1)))

    # Remove any of these coordinates in they don't have ice or there is already a medal there
    for index in range(len(to_check) - 1, -1, -1):
        # Get coordinates
        I, J = to_check[index]

        # Generator to check for gaps in the ice, yields True if ice or False if there is a gap
        ice_check = (ice_grid[I + i][J + j] == 0 for i, j in product(range(2), range(2)))
        # Generator to check for existing medals, yields True if no madal or False if there is a medal
        medal_check = (foo[I + i][J + j] == -1 for i, j in product(range(2), range(2)))

        if not(all(ice_check) and all(medal_check)):
            # If there is a gap in the ice remove from to_check
            to_check.pop(index)

    # Loop if medals still need placing
    while medal_number != medals_existing:
        # Record how many of the missing medals have been added
        added = 0
        # Copy the medals grid
        bar = copy.deepcopy(foo)
        # Copy the list of coordinates to check
        to_check_copy = copy.copy(to_check)

        # Loop whilst there are still coordinates to check
        while to_check_copy:
            # Pick and remove a a random coordinate
            I, J = to_check_copy.pop(random.randrange(len(to_check_copy)))

            # Generator to check for existing medals, yields True if no madal or False if there is a medal
            medal_check = (bar[I + i][J + j] == -1 for i, j in product(range(2), range(2)))

            # Check if a medal can go here
            if all(medal_check):
                # Increment counter
                added += 1
                # Add a medal
                for i, j in product(range(2), range(2)):
                    bar[I + i][J + j] = 2 * i + j
                # Check if all the medals have been added yet
                if medals_existing + added == medal_number:
                    # If so return the new medal grid
                    return bar

# Empty ice grid
ig = [[-1 for _ in range(9)] for _ in range(9)]
# Empty medal grid
mg = [[-1 for _ in range(9)] for _ in range(9)]

# Put a 5 x 2 ice section in at (0, 1)
ig[0][1:6] = ig[1][1:6] = (0,) * 5

# Put a partially visible medal at (0, 0)
mg[0][0] = 0
mg[1][0] = 2

# Print ice grid
print(ig)
# Print partial medal grid
print(mg)
# Print filled medal grid
print(medal_grid(ig, mg, 3))
