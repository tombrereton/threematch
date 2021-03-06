"""
This is the file for the game logic of three match.
"""
import os
from copy import deepcopy
from itertools import product
from operator import itemgetter
from random import randint, choice
from time import time

from events.event_manager import EventManager
from events.events import TickEvent, SwapGemsRequest, UpdateBagEvent, StateEvent
from events.update_bag import UpdateBag
from global_variables import *


class Grid:
    """
    The parent class to define the grid size and
    initialise an empty 2D array.
    """

    def __init__(self, rows, columns):
        self.grid = [[-1] * columns for _ in range(rows)]


class SimpleBoard:
    def __init__(self, rows, columns, gem_types, medals_remaining, moves_remaining):

        # grids
        self.gem_grid = Grid(rows, columns)
        self.ice_grid = Grid(rows, columns)
        self.medal_grid = Grid(rows, columns)

        # board variables
        self.moves_remaining = moves_remaining
        self.rows = rows
        self.columns = columns
        self.gem_types = gem_types
        self.total_medals = medals_remaining
        self.medals_remaining = medals_remaining
        self.game_state = ""

        self.additions = []
        self.movements = []
        self.medals_removed = []
        self.ice_removed = []
        self.match_list = []
        self.gem_grid_copy = []
        self.cascade = 0
        self.medal_locations = []  # TODO make it so board_simulator adds to this
        self.action = []
        self.score = 0
        self.bonus_list = []
        self.swapped_gems = [(), ()]
        self.medal_state = [[-1] * self.columns for _ in range(self.rows)]

        self.quit_on_end = True

    def __str__(self):
        medal_grid = self.print_grid(self.medal_grid.grid)
        ice_grid = self.print_grid(self.ice_grid.grid)
        gem_grid = self.print_grid(self.gem_grid.grid)

        s = "Medal grid:\n{}\nIce grid:\n{}\nGem grid:\n{}".format(medal_grid, ice_grid, gem_grid)
        return s

    def print_grid(self, grid):
        s = ''
        for i in range(self.rows):
            s += f'{grid[i]}\n'
        return s

    def new_gem(self, gem_type=None):
        """
        Creates a tuple to represent a gem.

        The gem type is randomised.

        (gem type, bonus type, activation)
        :return:
        """
        if gem_type is not None:
            gem_type = gem_type
        else:
            gem_type = randint(0, self.gem_types - 1)

        bonus_type = 0
        activation = 0
        return gem_type, bonus_type, activation

    def set_swap_locations(self, swap_locations: list):
        """
        A list containing the swapped gems is passed in. The
        list is in the format:

        [(gem1_row, gem1_col),(gem2_row, gem2_col)]

        It sets the swapped gems which is in the format:
        [(row, column, type, bonus_type, activation),(same again)]
        :param swap_locations:
        :return:
        """
        self.action = swap_locations

        gem1_row = swap_locations[0][0]
        gem1_col = swap_locations[0][1]
        gem2_row = swap_locations[1][0]
        gem2_col = swap_locations[1][1]

        self.swapped_gems = []
        self.swapped_gems.append(self.get_gem_info(gem1_row, gem1_col))
        self.swapped_gems.append(self.get_gem_info(gem2_row, gem2_col))

        self.game_state = "input_received"

    def swap_gems(self):

        gem1_row = self.swapped_gems[0][0]
        gem1_col = self.swapped_gems[0][1]
        gem2_row = self.swapped_gems[1][0]
        gem2_col = self.swapped_gems[1][1]

        self.gem_grid.grid[gem1_row][gem1_col], self.gem_grid.grid[gem2_row][gem2_col] = \
            self.gem_grid.grid[gem2_row][gem2_col], self.gem_grid.grid[gem1_row][gem1_col]

    def update_score(self):
        """
        Takes in match list. Adds points based on
        the number of gems.

        Future implementation: multipliers for combos
        :return:
        """
        match_list = self.match_list
        bonus_list = self.bonus_list
        medals_freed = len(self.medals_removed)
        bonus_removed = len([0 for y, x, t, bt, activation in match_list if bt is not 0])
        self.score += 100 * self.cascade * (len(match_list) + len(bonus_list) + 5 * bonus_removed + 40 * medals_freed)

    def find_matches(self):
        """
        Find the matches in the gem grid.

        If the vertical and horizontal matches intersect, create
        a bonus of type 3.
        :return:
        """
        h, h_from_bonus, h_bonuses = self.find_horizontal_matches()
        v, v_from_bonus, v_bonuses = self.find_vertical_matches()

        # merge all lists but matches from bonuses to avoid
        # lots of T-type bonuses
        matches = h + v
        bonuses = h_bonuses + v_bonuses

        # reduced bonus list for operations later
        reduced_bonuses = [(r, c) for r, c, t, bt, a in bonuses]

        # if matches intersect, create bonus type 3
        t_match = list(set(h).intersection(v))

        if len(t_match) > 0:

            # remove t_match bonus from its list if in bonuses
            for gem in reversed(t_match):
                if gem[:2] in reduced_bonuses:
                    t_match.remove(gem)

            # add t_match bonus to bonus list
            for r, c, t, bt, a in t_match:
                bonuses.append(self.get_gem_info(r, c, 3))
                reduced_bonuses.append((r, c))

        # merge all the matches
        matches.extend(h_from_bonus)
        matches.extend(v_from_bonus)
        matches = list(set(matches))

        # sort list (remove, if too slow)
        matches.sort(key=itemgetter(0, 1))
        bonuses.sort(key=itemgetter(0, 1))

        # remove all bonuses in matches
        for gem in reversed(matches):
            if gem[:2] in reduced_bonuses:
                matches.remove(gem)

        return matches, bonuses

    def find_horizontal_matches(self):
        """
        Finds the horizontal matches in the gem grid and adds them to a match_list.

        It checks if any bonus should be created with the following criteria:
        4-in-a-row = bonus type 1
        5-in-a-row = bonus type 2
        Intersection (T or L shape) = bonus type 3 (determined in the calling method)
        These are added to a bonus_list.

        It then check if any gems in the match_list are bonuses
        and if so, performs the appropriate action.
        bonus type 1 = (remove entire row/column)
        bonus type 2 = (remove all gems of the same type)
        bonus type 3 = (remove 9 surrounding gems)

        We return matches and matches_from_bonus separately
        so we don't get lots of intersection bonuses.
        :return: matches, matches_from_bonus, bonuses
        """
        matches = []
        bonuses = []

        rows = self.rows
        columns = self.columns

        # get all matches
        for row in range(rows):
            column = 0
            while column < columns:
                # find the horizontal match at location row, column
                temp_matches = self.get_row_match(row, column)

                # Get bonus gems
                temp_above_3_matches, temp_bonuses = self.get_bonus_types_1_2_and_matches(row, column, temp_matches)

                # Add gems to lists
                matches.extend(temp_above_3_matches)
                bonuses.extend(temp_bonuses)

                # add length of matches to column
                column += len(temp_matches)

        # Get matches from bonuses
        matches_from_bonus = self.cascade_bonus_action(matches, row_first=True)

        # remove duplicates
        matches = list(set(matches))
        matches_from_bonus = list(set(matches_from_bonus))

        return matches, matches_from_bonus, bonuses

    def find_vertical_matches(self):
        """
        Finds the vertical matches in the gem grid and adds them to a match_list.

        It checks if any bonus should be created with the following criteria:
        4-in-a-row = bonus type 1
        5-in-a-row = bonus type 2
        Intersection (T or L shape) = bonus type 3 (determined in the calling method)
        These are added to a bonus_list.

        It then check if any gems in the match_list are bonuses
        and if so, performs the appropriate action.
        bonus type 1 = (remove entire row/column)
        bonus type 2 = (remove all gems of the same type)
        bonus type 3 = (remove 9 surrounding gems)

        We return matches and matches_from_bonus separately
        so we don't get lots of intersection bonuses.
        :return: matches, matches_from_bonus, bonuses
        """
        matches = []
        bonuses = []

        rows = self.rows
        columns = self.columns

        # get all matches
        for column in range(columns):
            row = 0
            while row < rows:
                # find the horizontal match at location row, column
                temp_matches = self.get_column_match(row, column)

                # Get bonus gems
                temp_matches_2, temp_bonuses = self.get_bonus_types_1_2_and_matches(row, column, temp_matches)

                # Add gems to lists
                matches.extend(temp_matches_2)
                bonuses.extend(temp_bonuses)

                # add length of matches to column
                row += len(temp_matches)

        # Get matches from bonuses
        matches_from_bonus = self.cascade_bonus_action(matches, row_first=False)

        # remove duplicates
        matches = list(set(matches))
        matches_from_bonus = list(set(matches_from_bonus))

        # return dictionary after looping over all row matches
        return matches, matches_from_bonus, bonuses

    def cascade_bonus_action(self, matches, row_first: bool):
        """
        Loops over matches from bonus and performs bonus
        action.

        Gems removed from bonus action are appended to
        matches from bonuses
        :param row_first:
        :param matches:
        :return:
        """
        breaking_next = matches[:]
        broken = []

        while len(breaking_next):
            breaking_current, breaking_next = breaking_next, []
            for gem in breaking_current:
                row, column, gem_type, bonus_type, activation = gem
                if bonus_type == 1 and gem not in broken:
                    # add row to matches at location row, else add column to matches
                    f = self.remove_row if row_first else self.remove_column
                    temp = f(row, column)
                    temp = [gem for gem in temp if gem not in broken]
                    breaking_next.extend(temp)

                if bonus_type == 2:
                    # add all gems of this gems type to matches
                    temp = self.remove_all_gems_of_type(gem_type, row, column)
                    temp = [gem for gem in temp if gem not in broken]
                    breaking_next.extend(temp)

                if bonus_type == 3:
                    # add 9 surrounding gems of this gem
                    temp = self.remove_surrounding_gems(row, column)
                    temp = [gem for gem in temp if gem not in broken]
                    breaking_next.extend(temp)

                broken.append(gem)
            row_first = not row_first

        return broken

    def get_bonus_types_1_2_and_matches(self, row: int, column: int, temp_matches: list):
        """
        Add bonuses to a list if matches are correct length.

        Adds matches to a list if length 3 or more.

        Returns bonus and match list.
        :param column:
        :param row:
        :param temp_matches:
        :return:
        """
        match_list = []
        bonus_list = []

        match_count = len(temp_matches)

        # if length of match list is 5, create bonus type 2
        if match_count == 5:
            # remove swap location from matches and add to bonus list
            bonus_list.extend(self.get_bonus_list(row, column, temp_matches, 2))

        # if length of match list is 4, create bonus type 1
        elif match_count == 4:
            # remove swap location from matches and add to bonus list
            bonus_list.extend(self.get_bonus_list(row, column, temp_matches, 1))

        # if length of match list >= 3, add temp matches to matches
        if match_count >= 3:
            match_list.extend(temp_matches)

        return match_list, bonus_list

    def remove_row(self, row, column):
        """
        Adds entire row to list
        :param column:
        :param row:
        :return:
        """
        gem_list = []
        for j in range(self.columns):
            if self.get_gem_info(row, j) != self.get_gem_info(row, column):
                gem_list.append(self.get_gem_info(row, j))
        return gem_list

    def remove_column(self, row, column):
        """
        Add entire column to list
        :param row:
        :param column:
        :return:
        """
        gem_list = []
        for i in range(self.rows):
            if self.get_gem_info(i, column) != self.get_gem_info(row, column):
                gem_list.append(self.get_gem_info(i, column))
        return gem_list

    def remove_all_gems_of_type(self, gem_type: int, row, column):
        """
        Add all gems of type gem_type to list
        :param column:
        :param row:
        :param gem_type:
        :return:
        """
        gem_list = []
        for i, j in product(range(self.rows), range(self.columns)):
            if self.gem_grid.grid[i][j][0] == gem_type and self.get_gem_info(i, j) != self.get_gem_info(row, column):
                gem_list.append(self.get_gem_info(i, j))
        return gem_list

    def remove_surrounding_gems(self, row: int, column: int):
        """
        Add 9 surrounding gems of location row,column to list.
        :param row:
        :param column:
        :return:
        """
        gem_list = []
        row_max = min(row + 2, self.rows)
        row_min = max(row - 1, 0)
        col_max = min(column + 2, self.columns)
        col_min = max(column - 1, 0)
        for i, j in product(range(row_min, row_max), range(col_min, col_max)):
            if self.get_gem_info(i, j) != self.get_gem_info(row, column):
                gem_list.append(self.get_gem_info(i, j))
        return gem_list

    def get_row_match(self, row: int, column: int):
        """
        rows match count
        :param row:
        :param column:
        :return:
        """
        columns = self.columns
        grid = self.gem_grid.grid
        match_index = column + 1
        match_list = [self.get_gem_info(row, column)]

        # check if its a match
        while match_index < columns and grid[row][column][0] == grid[row][match_index][0]:
            # if match, append to list
            match_list.append(self.get_gem_info(row, match_index))
            match_index += 1
        return match_list

    def get_column_match(self, row: int, column: int):
        """
        find matches along the column
        :param row:
        :param column:
        :return:
        """
        rows = self.rows
        grid = self.gem_grid.grid
        match_index = row + 1
        match_list = [self.get_gem_info(row, column)]

        # check if its a match
        while match_index < rows and grid[row][column][0] == grid[match_index][column][0]:
            # if match, append to list
            match_list.append(self.get_gem_info(match_index, column))
            match_index += 1
        return match_list

    def get_gem_info(self, row: int, column: int, new_bonus=None, top_row=False):
        """
        Return the coordinates of the gem, along with its
        type and bonus type. This information is returned
        as a tuple. The structure is:
        (row, column, type, bonus_type, activation
        :param top_row:
        :param new_bonus:
        :param row:
        :param column:
        :return:
        """
        if top_row:
            gem = self.gem_grid.grid[row + 1][column]
        else:
            gem = self.gem_grid.grid[row][column]

        if new_bonus is None:
            return row, column, gem[0], gem[1], gem[2]
        else:
            return row, column, gem[0], new_bonus, gem[2]

    def get_bonus_list(self, row, column, temp_matches, bonus_type):
        """
        Determines the location of the bonus
        :param row:
        :param column:
        :param temp_matches:
        :param bonus_type:
        :return:
        """
        bonus_list = []
        reduced_temp_matches = [(i, j) for i, j, t, bt, a in temp_matches]

        # create bonus at swap location otherwise at the first location of the match
        if self.swapped_gems[0][:2] in reduced_temp_matches:
            # bonus at first swap location
            i, j = self.swapped_gems[0][:2]
            bonus_gem = self.get_gem_info(i, j, bonus_type)
            bonus_list.append(bonus_gem)
        elif self.swapped_gems[1][:2] in reduced_temp_matches:
            # bonus at second swap location
            i, j = self.swapped_gems[1][:2]
            bonus_gem = self.get_gem_info(i, j, bonus_type)
            bonus_list.append(bonus_gem)
        else:
            # bonus at first location in match
            bonus_gem = self.get_gem_info(row, column, bonus_type)
            bonus_list.append(bonus_gem)

        return bonus_list

    def remove_gems_add_bonuses(self, init=False):
        """
        This loops over the gems in the match_list and
        removes them all from the grid.
        :return:
        """
        self.ice_removed = []
        for row, column, gem_type, bonus_type, activation in self.match_list:
            self.gem_grid.grid[row][column] = -1

            if not init:
                self.remove_ice(row, column)

        # try to free medals after removing ice
        self.free_medals()

        for row, column, gem_type, bonus_type, activation in self.bonus_list:
            self.gem_grid.grid[row][column] = (gem_type, bonus_type, activation)

            if not init:
                self.remove_ice(row, column)

    def pull_gems_down(self):
        """
        Pulls gems down vertically to simulate gravity.

        We create new gems if required.

        At the end of this method the gems will be at the position
        listed in new_positions.
        :return:
        """
        repeat = False
        original_positions = []
        new_positions = []
        additions = []

        grid = self.gem_grid.grid

        for j in range(self.columns):
            for i in range(self.rows - 1, 0, -1):
                # start from bottom row

                if grid[i][j] == -1 and grid[i - 1][j] != -1:
                    # if cell j,i is empty and the cell above is not empty, swap them.
                    repeat = True
                    original_positions.append(self.get_gem_info(i - 1, j))
                    grid[i][j], grid[i - 1][j] = grid[i - 1][j], -1
                    new_positions.append(self.get_gem_info(i, j))

            if grid[0][j] == -1:
                # if empty in the top row, create new gem, add to additions list
                # and set original position to above top row,
                # and new position to top row.
                repeat = True
                gem = self.new_gem()
                grid[0][j] = gem
                additions.append(self.get_gem_info(-1, j, top_row=True))
                original_positions.append(self.get_gem_info(-1, j, top_row=True))
                new_positions.append(self.get_gem_info(0, j))

        self.additions = additions
        self.movements = [original_positions, new_positions]
        return repeat

    def remove_ice(self, row: int, column: int):
        """
        If ice is present in the grid cell,
        reduce the layer by 1.
        :param row:
        :param column:
        :return:
        """
        grid = self.ice_grid.grid
        if grid[row][column] != -1:
            # if there is ice, decrease the layer by 1
            new_layer = grid[row][column] - 1
            grid[row][column] = new_layer

            # add to the ice_removed list
            self.ice_removed.append((row, column, new_layer))

    def free_medals(self):
        """
        Loops over the medal locations list and
        frees any completely uncovered medals.
        :return:
        """
        self.medals_removed = []
        ice_grid = self.ice_grid.grid
        medal_grid = self.medal_grid.grid
        for row, column in product(range(self.rows), range(self.columns)):
            if ice_grid[row][column] == -1 and medal_grid[row][column] == 0 and self.is_freeable_medal(row, column):
                # medal is completely uncovered, remove it from grid
                self.remove_medal(row, column)

                # decrement medals
                self.medals_remaining -= 1

    def remove_medal(self, row: int, column: int):
        """
        Loops over the 4 portions of the medal
        and sets them to -1.

        Also removes medal portions from medal_locations list.
        :param row:
        :param column:
        :return:
        """
        for i, j in product(range(2), range(2)):
            # remove from grid
            self.medal_grid.grid[row + i][column + j] = -1

            # remove from medal locations list
            portion = j + 2 * i
            # self.medal_locations.remove((row + i, column + j, portion))

            # add to medals removed list
            self.medals_removed.append((row + i, column + j, portion))

    def is_freeable_medal(self, row: int, column: int):
        """
        Returns true if medal completely uncovered from ice,
        otherwise return false
        :param row:
        :param column:
        :return:
        """
        for i, j in product(range(2), range(2)):
            if self.ice_grid.grid[row + i][column + j] != -1:
                return False
        return True

    def get_game_state(self):
        """
        returns a tuple of 4 of arrays.

        (gem_type, bonus_type, ice, medal_portion)
        :return:
        """
        # get medals uncovered and score
        medals_uncovered = self.total_medals - self.medals_remaining
        score = self.score

        game_state = str(score) + '\t' + str(medals_uncovered) + '\t'

        gems = self.gem_grid_copy
        ice = self.ice_grid.grid
        medals = self.medal_grid.grid
        for i in range(self.rows):
            for j in range(self.columns):
                # get type, bonus_type, ice_layer
                s = str(gems[i][j][0]) + '\t' + str(gems[i][j][1]) + '\t' + str(ice[i][j]) + '\t'

                # get medal portion
                m = -1
                if self.medal_state[i][j] != -1:
                    m = self.medal_state[i][j]
                elif ice[i][j] == -1:
                    m = medals[i][j]
                    self.medal_state[i][j] = m

                # combine to get t, bt, ice_layer, portion
                s = s + str(m) + '\t'
                game_state += s

        return game_state

    def get_progress_state(self):
        """
        Returns a string representing the progress state
        in the form:

        'medals_uncovered score action' eg:
        '1 \t 900 \t 0102'

        where action is: row1 column1 row2 column2

        The action is the action TO BE performed from the
        current state.
        :return:
        """

        # unpack the swap locations to get the 'action'
        action = self.action
        action = str(action[0][0]) + '-' + str(action[0][1]) + '-' + str(action[1][0]) + '-' + str(action[1][1])

        return action

    def get_obscured_game_state(self):
        gem_grid = deepcopy(self.gem_grid.grid)
        ice_grid = deepcopy(self.ice_grid.grid)
        medal_grid = self.medal_grid.grid
        medal_grid = [[medal if ice else -1 for ice, medal in zip(*rows)] for rows in zip(ice_grid, medal_grid)]
        moves_medals = (self.moves_remaining, self.medals_remaining)

        return gem_grid, ice_grid, medal_grid, moves_medals

    def get_full_game_state(self):
        gem_grid = deepcopy(self.gem_grid.grid)
        ice_grid = deepcopy(self.ice_grid.grid)
        medal_grid = deepcopy(self.medal_grid.grid)
        moves_medals = (self.moves_remaining, self.medals_remaining)

        return gem_grid, ice_grid, medal_grid, moves_medals

    def move_made(self):
        self.moves_remaining -= 1

    def check_medal_boundaries(self, y_coord: int, x_coord: int):
        """
        Method to check is a medal can be added at a certain location
        :param y_coord: y coordinate to check (top left of medal)
        :param x_coord: x coordinate to check (top left of medal)
        :return: None
        """
        rows = self.rows
        columns = self.columns
        if x_coord < columns - 1 and y_coord < rows - 1:
            for i in range(2):
                for j in range(2):
                    if self.medal_grid.grid[y_coord + i][x_coord + j] != -1:
                        return False
            return True
        return False

    def add_medal(self, row: int, column: int):
        """
        Method to add a medal (four medal portions) to the grid. The medal
        portions will appear like the following:

        |0|1|
        -----
        |2|3|

        :param row: y coordinate to add medal at (top left of medal)
        :param column: x coordinate to add beat at (top left of medal)
        :return: None
        """
        for i in range(2):
            for j in range(2):
                portion = j + 2 * i
                self.medal_grid.grid[row + i][column + j] = portion

                # add portion to medal location list
                self.medal_locations.append((row + i, column + j, portion))


class Board(SimpleBoard):
    """
    The class which contains all the grids for gems, ice, and medals.

    -1 represents an empty cell in all grids.

    The gem grid contains tuples in each cell, which represent:
    (type, bonus_type, activation)

    The ice grid contains a single value in each cell, represented by:
    (layer)

    The medal_grid contains a single value in each cell, represented by:
    (corner)

    Swapped gems is a list of tuples, represented as:
    [(row, column, type, bonus_type, activation),(same again)]

    test parameter should be "vertical" or "horizontal" to specify test grid type.
    """

    def __init__(self,
                 rows: int,
                 columns: int,
                 ice_rows: int,
                 medals_remaining: int,
                 moves_remaining: int,
                 event_manager: EventManager,
                 gem_types: int = GEM_TYPES,
                 bonus_types: int = BONUS_TYPES,
                 ice_layers=ICE_LAYERS,
                 test=None,
                 random_seed=RANDOM_SEED,
                 stats_file_path=None):
        super().__init__(rows, columns, gem_types, medals_remaining, moves_remaining)

        # event manager
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        # game variables
        self.ice_rows = ice_rows
        self.total_moves = None  # set by number of ice rows
        self.set_max_moves()
        self.bonus_types = bonus_types
        self.terminal_state = False
        self.win_state = False
        self.game_state = "waiting_for_input"
        self.ice_layers = ice_layers - 1
        self.test = test
        self.random_seed = random_seed

        # helper variables
        self.ice_removed = []
        self.movements = []
        self.additions = []
        self.activated_gems = []

        # state variables
        self.file_name = ''
        self.line_number = 0

        # file operations
        self.stats_file_path = stats_file_path

        # initialise grids
        self.init_gem_grid()
        self.init_ice_grid()
        self.init_medal_grid()
        state_event = StateEvent(self.get_obscured_game_state())
        self.event_manager.post(state_event)

    # ----------------------------------------------------------------------

    def state(self):
        return self.gem_grid.grid, self.ice_grid.grid, self.medal_grid.grid, (
            self.moves_remaining, self.medals_remaining, self.score, False, False)

    def notify(self, event):
        if isinstance(event, SwapGemsRequest):
            if self.game_state == "waiting_for_input":
                self.set_swap_locations(event.swap_locations)
        elif isinstance(event, TickEvent):
            # TODO check
            if self.game_state != "waiting_for_input":
                self.get_update()

    def init_gem_grid(self):
        """
        Initialises the gem grid with tuples.
        """
        if self.test == "vertical":
            self.test_grid_vertical()
        elif self.test == "horizontal":
            self.test_grid_horizontal()
        else:
            rows = self.rows
            columns = self.columns
            for row, column in product(range(rows), range(columns)):
                self.gem_grid.grid[row][column] = self.new_gem()

            # find matches
            match_list, bonus_list = self.find_matches()

            while len(match_list) + len(bonus_list):
                for gem in match_list:
                    i, j = gem[:2]
                    self.gem_grid.grid[i][j] = self.new_gem()

                for gem in bonus_list:
                    i, j = gem[:2]
                    self.gem_grid.grid[i][j] = self.new_gem()

                match_list, bonus_list = self.find_matches()

    def test_grid_vertical(self):
        """
        Creates a test grid where all the columns are
        the same type of gem.
        :return:
        """
        for j, i in product(range(self.columns), range(self.rows)):
            gem_type = j % self.gem_types
            gem = self.new_gem(gem_type)
            self.gem_grid.grid[i][j] = gem

    def test_grid_horizontal(self):
        """
        Creates a test grid where all the rows are
        the same type of gem.
        :return:
        """
        for i, j in product(range(self.rows), range(self.columns)):
            gem_type = i % self.gem_types
            gem = self.new_gem(gem_type)
            self.gem_grid.grid[i][j] = gem

    def init_ice_grid(self):
        """
        Initialises the ice grid with the number of layers.

        The ice is initialised from the bottom row first,
        up to the number of ICE_ROWS.
        :return:
        """
        rows = self.rows - 1
        columns = self.columns
        ice_rows = rows - self.ice_rows
        for row in range(rows, ice_rows, -1):
            for col in range(columns):
                self.ice_grid.grid[row][col] = self.ice_layers

    def set_max_moves(self):
        if self.ice_rows == 5:
            self.total_moves = 20
        elif self.ice_rows == 7:
            self.total_moves = 25
        elif self.ice_rows == 9:
            self.total_moves = 30

    def init_medal_grid(self):
        """
        Initialises the medal grid with portions of medals.

        Each medal is represented by a portion and a 2x2 medal
        is represented by the following 4 portions.

        |0|1|
        -----
        |2|3|
        :return:
        """
        rows = self.rows
        columns = self.columns
        i = 0
        while i < self.medals_remaining:
            # get random choice
            row = choice(range(rows - self.ice_rows, rows - 1))
            column = choice(range(columns - 1))
            if self.check_medal_boundaries(row, column):
                # if no medal already there, add medal
                self.add_medal(row, column)
                i = i + 1

    def get_swap_movement(self):
        """
        Returns a list of lists which represents movement.

        The first inner list is the original positions,
        the second inner list is the new position.
        :return:
        """
        original = self.swapped_gems
        new = [self.swapped_gems[1], self.swapped_gems[0]]
        return [original, new]

    def get_game_info(self):
        """
        Simple getter to get game information
        :return:
        """
        return self.moves_remaining, self.medals_remaining, self.score, self.terminal_state, self.win_state

    def extrapolate_score(self):
        """
        Extrapolates the score by finding the players
        average score per move and adding that to the score
        for the number of moves left.
        :return:
        """
        avg_per_move = self.score / (self.total_moves - self.moves_remaining)
        bonus_points = avg_per_move * self.moves_remaining

        self.score += bonus_points

    def get_update(self):
        """
        Gets the updates.

        This method swaps the gems, looks for matches,
        removes gems, and pulls them down. This is done
        until no more successive matches are found.

        Update bags are posted to registered listeners after
        every pull down and also if it is not a valid swap.
        :return:
        """

        self.gem_grid_copy = deepcopy(self.gem_grid.grid)
        state = self.get_game_state()
        update_bag = UpdateBag([], [], [], [], [], [], [], state)
        update_bag.gems = self.gem_grid.grid

        # ---------------------------------------
        if not self.game_state == "input_received":
            # do nothing
            return update_bag

        if self.terminal_state:
            # do nothing if terminal state
            return update_bag

        if not self.check_swap():
            # do nothing if user clicked on non adjacent gem
            self.game_state = "waiting_for_input"
            return update_bag

        self.game_state = "doing_stuff"
        # ---------------------------------------
        # Swap is adjacent, send some update bags:

        # reset cascade to zero
        self.cascade = 0

        # save state and chosen action before doing anything
        self.write_state_action()

        # create bag
        info = self.get_game_info()
        movements = self.get_swap_movement()
        update_bag = UpdateBag([], [], [], movements, [], [], info)
        update_bag.gems = self.gem_grid.grid

        # send bag to view
        event = UpdateBagEvent(update_bag)
        self.event_manager.post(event)

        # swap gems and find matches
        self.swap_gems()
        matches, bonuses = self.find_matches()
        match_count = len(matches)
        bonus_count = len(bonuses)

        # ---------------------------------------
        # if not match, swap back and send bag
        if match_count + bonus_count < 3:
            self.swap_gems()

            # create bag
            info = self.get_game_info()
            movements = self.get_swap_movement()
            update_bag = UpdateBag([], [], [], movements, [], [], info)
            update_bag.gems = self.gem_grid.grid

            # send bag to view and return
            event = UpdateBagEvent(update_bag)
            self.event_manager.post(event)
            self.game_state = "waiting_for_input"
            return update_bag

        # ---------------------------------------
        # else, match - perform remove gems, pull down, etc, and send bag
        else:
            self.move_made()

            # do until no more pull downs

            while match_count + bonus_count > 0:
                first_loop = True
                self.cascade += 1

                # find more matches after pulling down
                matches, bonuses = self.find_matches()
                self.match_list = matches
                self.bonus_list = bonuses
                match_count = len(matches)
                bonus_count = len(bonuses)

                # remove gems in grid that are in matches_list
                self.remove_gems_add_bonuses()
                self.update_score()

                repeat = True
                while repeat:

                    # pull gems down
                    repeat = self.pull_gems_down()

                    # create bag
                    if not first_loop:
                        matches = []
                        bonuses = []

                    # else:
                    additions = self.additions
                    movements = self.movements
                    update_bag = UpdateBag(matches, bonuses, additions, movements,
                                           self.ice_removed, self.medals_removed, self.get_game_info())
                    update_bag.gems = self.gem_grid.grid

                    # send bag to view
                    event = UpdateBagEvent(update_bag)
                    self.event_manager.post(event)

                    # don't send anymore matches, bonuses
                    first_loop = False

            # ---------------------------------------
            # check for terminal state
            if self.medals_remaining == 0:
                # WON

                # write state if terminal state
                self.action = [(-1, -1), (-1, -1)]
                self.write_state_action()

                self.win_state = True
                self.terminal_state = True

                # give bonus points for moves remaining
                self.extrapolate_score()

            elif self.moves_remaining == 0:
                # LOST

                # write state if terminal state
                self.action = [(-1, -1), (-1, -1)]
                self.write_state_action()

                self.win_state = False
                self.terminal_state = True

            # write stats to file
            if self.stats_file_path and self.terminal_state:
                outcome = 1 if self.win_state else 0
                medals_left = self.medals_remaining
                moves_made = self.total_moves - self.moves_remaining
                score = self.score
                line = f'{outcome}, {medals_left}, {moves_made}, {score:0.0f}'
                with open(self.stats_file_path, 'a') as file:
                    file.write(line)

            # Create bag
            info = self.get_game_info()
            state = self.get_game_state()
            update_bag = UpdateBag([], [], [], [], [], [], info, state)
            update_bag.gems = self.gem_grid.grid

            # send bag to view
            event = UpdateBagEvent(update_bag)
            self.event_manager.post(event)
            self.game_state = "waiting_for_input"

            # send state to MCTS controller
            state_event = StateEvent(self.get_obscured_game_state())
            self.event_manager.post(state_event)

            return update_bag
            # ----------------------------------------------------------------------

    def check_swap(self):
        """
        return true if swap locations are adjacent, false if not
        :return:
        """
        row1 = self.swapped_gems[0][0]
        column1 = self.swapped_gems[0][1]
        row2 = self.swapped_gems[1][0]
        column2 = self.swapped_gems[1][1]

        if row2 == row1 - 1 and column2 == column1:
            # swap up
            return True

        elif row2 == row1 + 1 and column2 == column1:
            # swap down
            return True

        elif row2 == row1 and column2 == column1 + 1:
            # swap right
            return True

        elif row2 == row1 and column2 == column1 - 1:
            # swap left
            return True

        else:
            return False

    def file_header(self):
        """
        This method build a string to be the header of the
        game state files.
        :return:
        """
        line1 = 'Preamble\n'
        header_underline = '===============================================================================\n'
        glossary = 't = gem type\nbt = bonus type\ni = ice layer\nmp = medal portion\nmu = medals uncovered\n' + \
                   's = score\na = action\ntmo = total moves\ntme = total medals\nr = row\nc = columns\n'

        line3 = 'tmo\ttme\tr\tc\n'
        divider = '\n'
        line5 = str(self.moves_remaining) + '\t' + str(self.total_medals) + '\t' + str(self.rows) + '\t' + str(
            self.columns) + '\n'

        key_about = '\nKey for state and progress information.\n2 lines represent a state-action pair:\n'
        header1 = 's\tmu\t' + 't\tbt\ti\tmp\t' * self.rows * self.columns + '\n'
        header2 = 'a\n'

        preamble = line1 + header_underline + glossary + divider + line3 + \
                   header_underline + line5 + divider + key_about + header1 + \
                   header_underline + header2 + header_underline + '\n'

        return preamble

    def create_file(self):
        if self.test is None:
            main_dir = os.getcwd()
            data_dir = os.path.join(main_dir, 'training_data')
            name = 'game-' + time() + '.txt'
            self.file_name = os.path.join(data_dir, name)

            with open(self.file_name, 'x') as file:
                file.write(self.file_header())

    def write_state_action(self):
        """
        gets the state and the action and
        write it to the open file.
        :return:
        """

        # if self.test is None:
        #     state = self.get_game_state()
        #     progress = self.get_progress_state()
        #
        #     string = state + '\n' + progress + '\n'
        #
        #     with open(self.file_name, 'a') as file:
        #         file.write(string)

    def move_to_completed(self):
        """
        if game finishes, move the training data to the completed
        directory.
        :return:
        """
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, 'training_data')
        completed_dir = os.path.join(data_dir, 'completed')

        old_file_name = os.path.join(data_dir, self.file_name)
        new_file_name = os.path.join(completed_dir, self.file_name)
        os.rename(old_file_name, new_file_name)

    def get_game_state_tuple(self):
        """
        returns (gem info) as 2d tuple, (moves, medals) as index 9
        :return:
        """
        gems = self.gem_grid.grid
        ice = self.ice_grid.grid
        medals = self.medal_grid.grid

        state = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                m = -1
                if self.medal_state[i][j] != -1:
                    m = self.medal_state[i][j]
                elif ice[i][j] == -1:
                    m = medals[i][j]
                    self.medal_state[i][j] = m

                row.append((gems[i][j][0], gems[i][j][1], ice[i][j], m))
            state.append(tuple(row))

        state.append((self.moves_remaining, self.medals_remaining))

        return tuple(state)
