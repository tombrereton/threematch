import random
import copy

from itertools import product


def medal_grid_filler(ice_grid: list, foo: list, medal_number: int):
    """
    Fills in a medal grid
    :param ice_grid: Grid of ice
    :param foo: Partial medal grid, only uncovered medals will show
    :param medal_number: Number of medals that need to be in the grid
    :return: Filled medal grid
    """

    # If there are no medals return now
    if not medal_number:
        yield foo
        return

    # Get the number of rows
    rows = len(ice_grid)
    # Get the number of columns
    cols = len(ice_grid[0])

    # Count how many medals are already placed in the grid
    medals_existing = 0

    # Iterate through grid looking for medals
    for r, c in product(range(rows), range(cols)):
        # Get portion
        portion = foo[r][c]
        # Check if this is a medal portion
        if portion != -1:
            # Don't count existing medals
            if all(foo[r + i][c + j] == 2 * i + j for i, j in product(range(2), range(2))):
                medals_existing -= 1

            # Only want to fill each medal once so check if this is the bottom right as this is encountered last
            elif portion == 3:
                # This is the bottom right
                # Increment the medals_existing count
                medals_existing += 1
                # Fill in the medal
                for i, j in product(range(2), range(2)):
                    foo[r - i][c - j] = 3 - (2 * i + j)
                # Check if all the medals have been added yet
                if medals_existing == medal_number:
                    # If so return the new medal grid
                    yield foo
                    return
            else:
                # This is not the bottom right, set the bottom right so we encounter it later
                # Find the bottom right of the medal and set correctly
                foo[r if portion // 2 else r + 1][c if portion % 2 else c + 1] = 3

    # List all the coordinates in the grid
    to_check = list(product(range(rows - 1), range(cols - 1)))

    # Remove any of these coordinates in they don't have ice or there is already a medal there
    for index in range(len(to_check) - 1, -1, -1):
        # Get coordinates
        r, c = to_check[index]

        # Generator to check for gaps in the ice, yields True if ice or False if there is a gap
        ice_check = (ice_grid[r + i][c + j] == 0 for i, j in product(range(2), range(2)))
        # Generator to check for existing medals, yields True if no medal or False if there is a medal
        medal_check = (foo[r + i][c + j] == -1 for i, j in product(range(2), range(2)))
    
        # Check if there is a gap or a medal here
        if not(all(ice_check) and all(medal_check)):
            # If so remove from to_check
            to_check.pop(index)

    # Loop to place remaining medals
    while True:
        # print('looping')
        # Record how many of the missing medals have been added
        added = 0
        # Copy the medals grid
        bar = copy.deepcopy(foo)
        # Copy the list of coordinates to check
        to_check_copy = copy.copy(to_check)

        # Loop whilst there are still coordinates to check
        while to_check_copy:
            # Pick and remove a a random coordinate
            r, c = to_check_copy.pop(random.randrange(len(to_check_copy)))

            # Generator to check for existing medals, yields True if no medal or False if there is a medal
            medal_check = (bar[r + i][c + j] == -1 for i, j in product(range(2), range(2)))

            # Check if a medal can go here
            if all(medal_check):
                # Increment counter
                added += 1
                # Add a medal
                for i, j in product(range(2), range(2)):
                    bar[r + i][c + j] = 2 * i + j
                # Check if all the medals have been added yet
                if medals_existing + added == medal_number:
                    # If so return the new medal grid
                    yield bar
                    break

if __name__ == '__main__':
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
    print(medal_grid_filler(ig, mg, 3).__next__())
