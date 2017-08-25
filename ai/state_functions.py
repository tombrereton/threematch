import copy
import logging
import os
import random
from collections import Counter
from copy import deepcopy
from itertools import product

import numpy as np

from model.game import Grid


def gems_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[state[i][j][0] for j in rows] for i in cols]


def gems_plus_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[(state[i][j][0], state[i][j][1], 0) for j in rows] for i in cols]


def ice_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[state[i][j][2] for j in rows] for i in cols]


def medals_from_state(state, rows=None, cols=None):
    if not rows or not cols:
        rows = range(len(state) - 1)
        cols = range(len(state[0]))

    return [[state[i][j][3] for j in rows] for i in cols]


def state_to_grids(state):
    rows = range(len(state) - 1)
    cols = range(len(state[0]))

    gem_grid_wrapper = Grid(0, 0)
    ice_grid_wrapper = Grid(0, 0)
    medal_grid_wrapper = Grid(0, 0)

    moves_medals = state[-1]

    gem_grid = gems_plus_from_state(state, rows, cols)
    ice_grid = ice_from_state(state, rows, cols)
    medal_grid = medals_from_state(state, rows, cols)
    medal_grid = medal_grid_filler(ice_grid, medal_grid, moves_medals[1]).__next__()

    gem_grid_wrapper.grid = gem_grid
    ice_grid_wrapper.grid = ice_grid
    medal_grid_wrapper.grid = medal_grid

    return gem_grid_wrapper.grid, ice_grid_wrapper.grid, medal_grid_wrapper.grid, moves_medals


def start_state(state):
    gem_grid, ice_grid, medal_grid, moves_medals = state
    medal_grid = medal_grid_filler(ice_grid, medal_grid, moves_medals[1]).__next__()

    return deepcopy(gem_grid), deepcopy(ice_grid), medal_grid, moves_medals


class StateParser:
    def __init__(self):
        self.rows = 9
        self.cols = 9
        self.gem_grid = Grid(self.rows, self.cols)
        self.ice_grid = Grid(self.rows, self.cols)
        self.medal_grid = Grid(self.rows, self.cols)

    def get_file_list(self):
        os.chdir(os.getcwd() + '/../training_data')
        logging.debug(f'files in directory: \n{os.listdir()}\n')
        return os.listdir()

    def get_full_filename(self, file_name):
        main_dir = os.getcwd() + '/../training_data/'
        file_path = main_dir + file_name
        return file_path

    def get_state(self, file_name, state_index):
        # skip every second line
        state_index *= 2

        logging.debug(f'File name of initial state: {file_name}')

        with open(file_name) as f:
            initial_state = f.readlines()[26:]

        state = initial_state[state_index]

        return state

    def parse_state(self, string_state):
        """
        parses a string representing the state and returns it
        as a 2d array of tuples, the last row is a tuple
        of (score, medals uncovered).
        :param string_state:
        :return:
        """
        grid = Grid(self.rows, self.cols)

        first_state = string_state.split('\t')
        if 'n' in first_state:
            first_state.remove('\n')
        if '' in first_state:
            first_state.remove('')
        state = list(map(int, first_state))

        for i in range(2, len(state), 4):
            # get = (type, bonus_type)
            gem = [state[i], state[i + 1]]
            ice = [state[i + 2]]
            medal_portion = [state[i + 3]]
            item = gem + ice + medal_portion
            item = tuple(item)

            row_index = (i // 4 // 9)
            col_index = (i // 4) % 9
            grid.grid[row_index][col_index] = item

        grid.grid.append(state[:2])
        parsed_state = tuple(map(tuple, grid.grid))
        return parsed_state


def medal_grid_filler(ice_grid: list, partial_medal_grid: list, medal_number: int):
    """
    Fills in a medal grid
    :param ice_grid: Grid of ice
    :param partial_medal_grid: Partial medal grid, only uncovered medals will show
    :param medal_number: Number of medals that need to be in the grid
    :return: Filled medal grid
    """
    # Copy medal grid
    foo = copy.deepcopy(partial_medal_grid)

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
                pass

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
        if not (all(ice_check) and all(medal_check)):
            # If so remove from to_check
            to_check.pop(index)

    # Loop to place remaining medals
    while True:
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


def moves_three(grid: list):
    """
    Function that returns a list of moves that can be made
    :param grid: Grid to search for moves, should not contain matches
    :return: List of moves that can be made, may contain duplicates
    """
    # Create empty list for moves
    moves = []
    # Get number of rows in grid
    rows = len(grid)
    # Get number of columns in grid
    columns = len(grid[0])
    # Iterate over all locations and down/right directions
    for i, j, k in product(range(rows), range(columns), range(2)):
        # Check if this location/direction pair extends three without leaving the grid
        if (i < rows - 2 and k == 0) or (j < columns - 2 and k == 1):
            # Get the coordinates in this section of three
            to_check = [(i + c, j) if k == 0 else (i, j + c) for c in range(3)]
            # Get the types in this section
            types = [grid[i][j][0] for i, j in to_check]
            # Count the occurrences of each type
            c = Counter(types).most_common()
            # If there are 2 types then must be two of one type, one of another
            if len(c) == 2:
                # Get the type which occurred twice
                major_type = c[0][0]
                # Get the type which occurred once
                minor_type = c[1][0]
                # Get the coordinates of the minor_type
                y1, x1 = to_check[types.index(minor_type)]
                # Get the coordinates surrounding this
                surround = [(y1, x1 + offset) for offset in range(-1, 2, 2)] + \
                           [(y1 + offset, x1) for offset in range(-1, 2, 2)]
                # Filter this to make sure they are on the grid and not in the section of three
                surround = [(y2, x2) for y2, x2 in surround if 0 <= y2 < rows and 0 <= x2 < columns
                            and (y2, x2) not in to_check]
                # Iterate through these locations
                for y2, x2 in surround:
                    # If a major_type gem is present this can be used to make a match
                    if grid[y2][x2][0] == major_type and ((y2, x2), (y1, x1)) not in moves:
                        # Check move not already mound
                        if ((y2, x2), (y1, x1)) not in moves and ((y1, x1), (y2, x2)) not in moves:
                            # Add moves to move list
                            moves.append(((y1, x1), (y2, x2)))
    # Return list of moves
    return moves


def pick_move(grid: list):
    moves = moves_three(grid)
    return random.choice(moves) if len(moves) else None


def one_hot(state, permutation=range(6)):
    colour_channels = [state[0] == colour for colour in permutation]
    type_channels = [state[1] == t for t in range(2, 5)]
    ice_channels = [state[2] != -1]
    medal_channels = [state[3] == portion for portion in range(4)]

    state = np.concatenate((colour_channels, type_channels, ice_channels, medal_channels))

    return state


def numpy_to_native(state):
    # If state is flat
    state = np.reshape(state, (9, 9, 4))
    state = np.transpose(state, (2, 0, 1))

    gem_grid = np.transpose(state[0:2], (1, 2, 0))
    ice_grid = state[2]
    medal_grid = state[3]

    moves_medals = None

    return gem_grid, ice_grid, medal_grid, moves_medals


def utility_function(state, monte_carlo, board_simulator):
    """
    This functions takes in a state performs uses monte carlo
    tree search. It returns the utility of the state and
    the reward for each possible actions.
    :param board_simulator: a board_simulator class
    :param monte_carlo: a monte_carlo class
    :param state: The state should be in the form that monte_carlo requires.
    :return: U(state), Q(state,action) for all actions in A
    """
    game_limit = 100
    move_limit = 5
    c = 1.4
    level = 1
    mc = monte_carlo
    # functions to change level on monte carlo?
    pseudo_board = board_simulator
    mc.update(state)
    utility, q_values = mc.pick_move()

    return utility, q_values