import copy
import logging
import os
import random
import time
from collections import Counter
from copy import deepcopy
from itertools import product

import numpy as np

from model.game import Grid


class StateParser:
    def __init__(self):
        self.rows = 9
        self.cols = 9
        self.gem_grid = Grid(self.rows, self.cols)
        self.ice_grid = Grid(self.rows, self.cols)
        self.medal_grid = Grid(self.rows, self.cols)

    @staticmethod
    def get_file_list():
        os.chdir(os.getcwd() + '/../training_data')
        logging.debug(f'files in directory: \n{os.listdir()}\n')
        return os.listdir(path='.')

    @staticmethod
    def get_full_filename(file_name):
        main_dir = os.getcwd() + '/../training_data/'
        file_path = main_dir + file_name
        return file_path

    @staticmethod
    def get_state(file_name, state_index):
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


def start_state(state):
    gem_grid, ice_grid, medal_grid, moves_medals = state
    medal_grid = medal_grid_filler(ice_grid, medal_grid, moves_medals[1]).__next__()

    return deepcopy(gem_grid), deepcopy(ice_grid), medal_grid, moves_medals


def medal_grid_filler(ice_grid: list, partial_medal_grid: list, medals_remaining: int):
    """
    Fills in a medal grid
    :param ice_grid: Grid of ice
    :param partial_medal_grid: Partial medal grid, only uncovered medals will show
    :param medals_remaining: Number of medals that need to be in the grid
    :return: Filled medal grid
    """
    # Copy medal grid
    foo = copy.deepcopy(partial_medal_grid)

    # If there are no medals return now
    if not medals_remaining:
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
                if medals_existing == medals_remaining:
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
        # Shuffle list of coordinated to check
        random.shuffle(to_check)

        # Go through coordinates to check
        for r, c in to_check:
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
                if medals_existing + added == medals_remaining:
                    # If so return the new medal grid
                    yield bar
                    break


def find_legal_moves(grid: list):
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
    moves = find_legal_moves(grid)
    return random.choice(moves) if len(moves) else None


def one_hot(state, permutation=range(6)):
    colour_channels = [state[0] == colour for colour in permutation]
    type_channels = [state[1] == t for t in range(2, 5)]
    ice_channels = [state[2] != -1]
    medal_channels = [state[3] == portion for portion in range(4)]

    state = np.concatenate((colour_channels, type_channels, ice_channels, medal_channels))

    return state


def numpy_to_native(grid, moves_left, medals_left):
    gem_grid = grid[:2]
    gem_grid = np.array([*gem_grid, np.full((9, 9), 0)])
    gem_grid = np.transpose(gem_grid, (1, 2, 0))
    gem_grid = [[(*el,) for el in row] for row in gem_grid]
    ice_grid = grid[2]
    ice_grid = [[el for el in row] for row in ice_grid]
    medal_grid = grid[3]
    medal_grid = [[el for el in row] for row in medal_grid]

    moves_medals = moves_left, medals_left

    return gem_grid, ice_grid, medal_grid, moves_medals


def utility_function(state, monte_carlo):
    """
    This functions takes in a state and performs monte carlo
    tree search. It returns the utility of the state and
    the reward for each possible actions.
    :param monte_carlo: a monte_carlo class
    :param state: The state should be in the form that monte_carlo requires.
    :return: U(state), Q(state,action) for all actions in A
    """
    monte_carlo.update(state)
    utility, q_values = monte_carlo.pick_move()

    return utility, q_values


def new_labels_section(monte_carlo, grids, moves_left, medals_left, game_ids, start, amount, one_per_game):
    t = time.time()

    grids = grids[start:start + amount]
    moves_left = moves_left[start:start + amount]
    medals_left = medals_left[start:start + amount]
    game_ids = game_ids[start:start + amount]

    utility_ids = []
    utility_values = []
    q_ints = []
    q_floats = []

    indices = None

    if one_per_game:
        indices = []
        foo = 0
        for game_id in sorted(set(game_ids)):
            l = sum(1 for i in range(foo, min(len(game_ids), foo + 30)) if game_ids[i] == game_id)
            indices.append(random.randint(foo, foo + l - 1))
            foo += l
    else:
        indices = range(len(grids))

    for i in indices:
        grid = grids[i]
        moves = moves_left[i]
        medals = medals_left[i]

        state = numpy_to_native(grid, moves, medals)
        u, q = utility_function(state, monte_carlo)
        utility_ids.append(start + i)
        utility_values.append(u)
        q_ints.extend((start + i, *[coord for coord_pair in q_value[0] for coord in coord_pair]) for q_value in q)
        q_floats.extend(q_value[1] for q_value in q)

    np.save(f'utility_ids[{start}-{amount}]', utility_ids)
    np.save(f'utility_values[{start}-{amount}]', utility_values)
    np.save(f'q_ints[{start}-{amount}]', q_ints)
    np.save(f'q_floats[{start}-{amount}]', q_floats)

    print(time.time() - t)


def new_labels():
    grids = np.load('../file_parser/grids.npy')
    grids = np.reshape(grids, (-1, 9, 9, 4))
    grids = np.transpose(grids, (0, 3, 1, 2))
    grids[:, 2][grids[:, 2] == 1] = 0
    grids[:, 1] -= 1
    moves_left = np.load('../file_parser/moves_left.npy')
    medals_left = np.load('../file_parser/medals_left.npy')
    game_ids = np.load('../file_parser/game_ids.npy')

    # TODO make this nice
    from ai.mcts import MonteCarlo
    from ai.board_simulator import BoardSimulator
    from ai.evaluation_functions import EvaluationFunction
    from ai.policies import AllPolicy

    board_simulator = BoardSimulator()
    game_limit = 100
    move_limit = 5
    c = 1.4
    eval_function = EvaluationFunction(board_simulator).evaluation_func_crude
    monte_carlo = MonteCarlo(board_simulator,
                             game_limit=game_limit,
                             move_limit=move_limit,
                             c=c,
                             policy=AllPolicy(),
                             eval_function=eval_function,
                             get_q_values=True,
                             print_move_ratings=False)  # Change this to True if you want a formatted print of q_values

    start = 1000
    batch_size = 1000
    batches = 1

    for i in range(batches):
        s = start + i * batch_size
        new_labels_section(monte_carlo, grids, moves_left, medals_left, game_ids, s, batch_size, one_per_game=True)

if __name__ == '__main__':
    new_labels()
