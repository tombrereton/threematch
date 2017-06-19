"""
This is the file for the game logic of three match.
"""
import logging
from itertools import product
from operator import itemgetter
from random import randint, choice

logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

from events import TickEvent, SwapGemsRequest, UpdateBagEvent, EventManager
from global_variables import PUZZLE_ROWS, PUZZLE_COLUMNS, GEM_TYPES, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, BONUS_TYPES, \
    MOVES_LEFT, ICE_LAYERS
from update_bag import UpdateBag


class Grid:
    """
    The parent class to define the grid size and
    initialise an empty 2D array.
    """

    def __init__(self, rows, columns):
        self.grid = [[-1] * columns for _ in range(rows)]


class Board:
    """
    The class which contains all the grids for gems, ice, and medals.

    -1 represents an empty cell in all grids.

    The gem grid contains tuples in each cell, which represent:
    (type, bonus_type, activation)

    The ice grid contains a single value in each cell, represented by:
    (layer)

    The medal_grid contains a single value in each cell, represenEted by:
    (corner)

    Swapped gems is a list of tuples, represented as:
    [(row, column, type, bonus_type, activation),(same again)]

    test parameter should be "vertical" or "horizontal" to specify test grid type.
    """

    def __init__(self, rows: int, columns: int, ice_rows: int, medals: int,
                 moves: int, event_manager: EventManager, gem_types: int = GEM_TYPES, bonus_types: int = BONUS_TYPES,
                 ice_layers=ICE_LAYERS, test=None):
        # grids
        self.gem_grid = Grid(rows, columns)
        self.ice_grid = Grid(rows, columns)
        self.medal_grid = Grid(rows, columns)

        # event manager
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        # game variables
        self.rows = rows
        self.columns = columns
        self.ice_rows = ice_rows
        self.medals = medals
        self.moves = moves
        self.gem_types = gem_types
        self.bonus_types = bonus_types
        self.score = 0
        self.terminal_state = False
        self.win_state = False
        self.game_state = "waiting_for_input"
        self.ice_layers = ice_layers - 1
        self.test = test

        # helper variables
        self.medal_locations = []
        self.swapped_gems = [(), ()]
        self.match_list = []
        self.bonus_list = []
        self.ice_removed = []
        self.medals_removed = []
        self.movements = []
        self.additions = []
        self.cascade = 0

        # initialise grids
        self.init_gem_grid()
        self.init_ice_grid()
        self.init_medal_grid()

    def state(self):
        return self.gem_grid.grid, self.ice_grid.grid, self.medal_grid.grid, (
            self.moves, self.medals, self.score, False, False)

    def __str__(self):
        medal_grid = self.print_grid(self.medal_grid.grid)
        ice_grid = self.print_grid(self.ice_grid.grid)
        gem_grid = self.print_grid(self.gem_grid.grid)

        s = "Medal grid:\n{}\nIce grid:\n{}\nGem grid:\n{}".format(medal_grid, ice_grid, gem_grid)
        return s

    # ----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, SwapGemsRequest):
            if self.game_state == "waiting_for_input":
                self.set_swap_locations(event.swap_locations)
        elif isinstance(event, TickEvent):
            if self.game_state != "waiting_for_input":
                self.get_update()

    def print_grid(self, grid):
        s = ''
        for i in range(self.rows):
            s += f'{grid[i]}\n'
        return s

    def new_gem(self, gem_type=None):
        """
        Creates a tuple to represent a gem.

        The gem type is randomised.
        :return:
        """
        if gem_type is not None:
            gem_type = gem_type
        else:
            gem_type = randint(0, self.gem_types - 1)

        bonus_type = 0
        activation = 0
        return gem_type, bonus_type, activation

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
            match_count = len(match_list)

            count = 0
            while match_count >= 3:
                self.match_list = match_list
                self.bonus_list = bonus_list
                self.remove_gems_add_bonuses(init=True)

                remove = True
                while remove:
                    remove = self.pull_gems_down()

                # debug logging line
                logging.debug(f"\nInit gem loop {count}:\n\n{self}")

                match_list, bonus_list = self.find_matches()
                match_count = len(match_list)

                count += 1

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
        while i < self.medals:
            # get random choice
            row = choice(range(rows - self.ice_rows, rows - 1))
            column = choice(range(columns - 1))
            if self.check_medal_boundaries(row, column):
                # if no medal already there, add medal
                self.add_medal(row, column)
                i = i + 1

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
        self.update_score()
        return self.moves, self.medals, self.score, self.terminal_state, self.win_state

    def update_score(self):
        """
        Takes in match list. Adds points based on
        the number of gems.

        Future implementation: multipliers for combos
        :param match_list:
        :param bonus_list:
        :param medals_freed:
        :param cascade:
        :return:
        """
        match_list = self.match_list
        bonus_list = self.bonus_list
        medals_freed = len(self.medals_removed)
        bonus_removed = len([0 for y, x, t, bt, activation in match_list if bt is not 0])
        self.score += 100 * self.cascade * (len(match_list) + len(bonus_list) + 2 * bonus_removed + 5 * medals_freed)

    def get_update(self):
        """
        Returns an UpdateBag and processes what action to take.
        :return:
        """
        update_bag = UpdateBag([], [], [], [], [], [], [])

        # if waiting for input, block
        if self.game_state == "waiting_for_input":
            logging.warning(update_bag)
            return update_bag

        elif self.terminal_state:
            info = self.get_game_info()
            update_bag = UpdateBag([], [], [], [], [], [], info)

            # send bag to view
            event = UpdateBagEvent(update_bag)
            self.event_manager.post(event)

        # if input received state, return swap movements, make swap, and try to find matches
        elif self.game_state == "input_received":

            # if adjacent swap, continue
            if self.check_swap():
                info = self.get_game_info()
                movements = self.get_swap_movement()
                update_bag = UpdateBag([], [], [], movements, [], [], info)

                # send bag to view
                event = UpdateBagEvent(update_bag)
                self.event_manager.post(event)

                self.swap_gems()

                # find matches
                match_list, bonus_list = self.find_matches()
                match_count = len(match_list)

                if match_count >= 3:
                    self.match_list = match_list
                    self.bonus_list = bonus_list
                    self.move_made()
                    self.game_state = "matches_found"
                else:
                    self.swap_gems()
                    self.game_state = "not_valid_swap"

            else:
                # swap locations not adjacent
                self.game_state = "waiting_for_input"

        # if not valid swap state, return inverse swap movement
        elif self.game_state == "not_valid_swap":
            info = self.get_game_info()
            movements = self.get_swap_movement()
            update_bag = UpdateBag([], [], [], movements, [], [], info)

            # send bag to view
            event = UpdateBagEvent(update_bag)
            self.event_manager.post(event)

            self.game_state = "waiting_for_input"

        # if matches found state, return matches, bonuses, etc, then pull gems down
        elif self.game_state == "matches_found":
            self.cascade += 1

            # remove gems in grid that are in matches_list
            self.remove_gems_add_bonuses()

            match_list = self.match_list
            bonus_list = self.bonus_list
            ice = self.ice_removed
            medals = self.medals_removed
            info = self.get_game_info()
            update_bag = UpdateBag(match_list, bonus_list, [], [], ice, medals, info)

            # send bag to view
            event = UpdateBagEvent(update_bag)
            self.event_manager.post(event)

            # pull gems down
            _ = self.pull_gems_down()

            # enter pulled down state
            self.game_state = "pulled_down"

        # if pulled down state, return additions, movements, etc, then try to pull down again
        elif self.game_state == "pulled_down":
            additions = self.additions
            movements = self.movements

            info = self.get_game_info()

            update_bag = UpdateBag([], [], additions, movements, [], [], info)

            # send bag to view
            event = UpdateBagEvent(update_bag)
            self.event_manager.post(event)

            # check for more pull downs
            more_pull_downs = self.pull_gems_down()

            if more_pull_downs:
                # if true, game state still pulled down
                self.game_state = "pulled_down"
            else:
                # if false, check for matches
                # find matches
                match_list, bonus_list = self.find_matches()
                match_count = len(match_list)

                if match_count >= 3:
                    self.match_list = match_list
                    self.bonus_list = bonus_list
                    self.game_state = "matches_found"
                else:
                    # no more matches, then wait for user input
                    self.game_state = "waiting_for_input"
                    self.cascade = 0

                    if self.medals == 0:
                        self.win_state = True
                        self.terminal_state = True

                    elif self.moves == 0:
                        self.win_state = False
                        self.terminal_state = True

                    info = self.get_game_info()

                    update_bag = UpdateBag([], [], [], [], [], [], info)

                    # send bag to view
                    event = UpdateBagEvent(update_bag)
                    self.event_manager.post(event)

        # Leave in for testing
        return update_bag

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

    def find_matches(self):
        """
        Find the matches in the gem grid.

        If the vertical and horizontal matches intersect, create
        a bonus of type 3.

        # TODO: try to remove ice and medals
        :return:
        """
        h, h_from_bonus, h_bonuses = self.find_horizontal_matches()
        v, v_from_bonus, v_bonuses = self.find_vertical_matches()

        # merge all lists but matches from bonuses to avoid
        # lots of T-type bonuses
        matches = h + v
        bonuses = h_bonuses + v_bonuses

        # if matches intersect, create bonus type 3
        t_match = list(set(h).intersection(v))

        if len(t_match) > 0:

            # if gem in t_match and matches, remove it from matches
            # and make it a T-type bonuses
            matches = [gem for gem in matches if gem not in t_match]
            for row, column, gem_type, bonus_type, activation in t_match:
                bonuses.append(self.get_gem_info(row, column, 3))

        # merge all the matches
        matches += h_from_bonus + v_from_bonus

        # sort list (remove, if too slow)
        matches.sort(key=itemgetter(0, 1))
        bonuses.sort(key=itemgetter(0, 1))

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
        so we dont get lots of intersection bonuses.
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
                temp_bonuses = []

                match_count = len(temp_matches)

                # if length of match list is 5, create bonus type 2
                if match_count == 5:
                    # remove swap location from matches and add to bonus list
                    temp_matches, temp_bonuses = self.get_bonus_list(row, column, temp_matches, 2)
                    matches += temp_matches
                    bonuses += temp_bonuses

                # if length of match list is 4, create bonus type 1
                elif match_count == 4:
                    # remove swap location from matches and add to bonus list
                    temp_matches, temp_bonuses = self.get_bonus_list(row, column, temp_matches, 1)
                    matches += temp_matches
                    bonuses += temp_bonuses

                # if length of match list >= 3, add temp matches to matches
                elif match_count >= 3:
                    matches += temp_matches

                # add length of matches to column
                column += len(temp_matches) + len(temp_bonuses)

        # loop over matches to check for bonuses and perform bonus action
        matches_from_bonus = []
        for row, column, gem_type, bonus_type, activation in matches:
            if bonus_type == 1:
                # remove original gem
                matches.remove(self.get_gem_info(row, column))
                # add row to matches at location row
                for j in range(self.columns):
                    matches_from_bonus.append(self.get_gem_info(row, j))

            if bonus_type == 2:
                # remove original gem
                matches.remove(self.get_gem_info(row, column))
                # add all gems of this gems type to matches
                for i, j in product(range(self.rows), range(self.columns)):
                    if self.gem_grid.grid[i][j][0] == gem_type:
                        matches_from_bonus.append(self.get_gem_info(i, j))

            if bonus_type == 3:
                # remove original gem
                matches.remove(self.get_gem_info(row, column))
                # add 9 surrounding gems of this gem
                row_max = min(row + 2, self.rows)
                row_min = max(row - 1, 0)
                col_max = min(column + 2, self.columns)
                col_min = max(column - 1, 0)
                for i, j in product(range(row_min, row_max), range(col_min, col_max)):
                    matches_from_bonus.append(self.get_gem_info(i, j))

        # remove duplicates
        matches = list(set(matches))
        matches_from_bonus = list(set(matches_from_bonus))

        # return dictionary after looping over all row matches
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
        so we dont get lots of intersection bonuses.
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
                temp_bonuses = []

                match_count = len(temp_matches)

                # if length of match list is 5, create bonus type 2
                if match_count == 5:
                    # remove swap location from matches and add to bonus list
                    temp_matches, temp_bonuses = self.get_bonus_list(row, column, temp_matches, 2)
                    matches += temp_matches
                    bonuses += temp_bonuses

                # if length of match list is 4, create bonus type 1
                elif match_count == 4:
                    # remove swap location from matches and add to bonus list
                    temp_matches, temp_bonuses = self.get_bonus_list(row, column, temp_matches, 1)
                    matches += temp_matches
                    bonuses += temp_bonuses

                # if length of match list >= 3, add temp matches to matches
                elif match_count >= 3:
                    matches += temp_matches

                # add length of matches to column
                row += len(temp_matches) + len(temp_bonuses)

        # loop over matches to check for bonuses and perform bonus action
        matches_from_bonus = []
        for row, column, gem_type, bonus_type, activation in matches:
            if bonus_type == 1:
                # remove original gem
                matches.remove(self.get_gem_info(row, column))
                # add column to matches at location column
                for i in range(self.rows):
                    matches_from_bonus.append(self.get_gem_info(i, column))

            if bonus_type == 2:
                # remove original gem
                matches.remove(self.get_gem_info(row, column))
                # add all gems of this gems type to matches
                for i, j in product(range(self.rows), range(self.columns)):
                    if self.gem_grid.grid[i][j][0] == gem_type:
                        matches_from_bonus.append(self.get_gem_info(i, j))

            if bonus_type == 3:
                # remove original gem
                matches.remove(self.get_gem_info(row, column))
                # add 9 surrounding gems of this gem
                row_max = min(row + 2, self.rows)
                row_min = max(row - 1, 0)
                col_max = min(column + 2, self.columns)
                col_min = max(column - 1, 0)
                for i, j in product(range(row_min, row_max), range(col_min, col_max)):
                    matches_from_bonus.append(self.get_gem_info(i, j))

        # remove duplicates
        matches = list(set(matches))
        matches_from_bonus = list(set(matches_from_bonus))

        # return dictionary after looping over all row matches
        return matches, matches_from_bonus, bonuses

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

        # create bonus at swap location otherwise at the first location of the match
        if self.swapped_gems[0] in temp_matches:
            i, j = self.swapped_gems[0][:2]
            gem = self.get_gem_info(i, j)
            bonus_gem = self.get_gem_info(i, j, bonus_type)
            temp_matches.remove(gem)
            bonus_list.append(bonus_gem)
        elif self.swapped_gems[1] in temp_matches:
            i, j = self.swapped_gems[1][:2]
            gem = self.get_gem_info(i, j)
            bonus_gem = self.get_gem_info(i, j, bonus_type)
            temp_matches.remove(gem)
            bonus_list.append(bonus_gem)
        else:
            gem = self.get_gem_info(row, column)
            bonus_gem = self.get_gem_info(row, column, bonus_type)
            temp_matches.remove(gem)
            bonus_list.append(bonus_gem)

        return temp_matches, bonus_list

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
                gem = self.new_gem()
                grid[0][j] = gem
                additions.append(self.get_gem_info(-1, j, top_row=True))
                original_positions.append(self.get_gem_info(-1, j, top_row=True))
                new_positions.append(self.get_gem_info(0, j))
                repeat = True

        self.additions = additions
        self.movements = [original_positions, new_positions]
        return repeat

    def move_made(self):
        self.moves -= 1

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
        grid = self.ice_grid.grid
        for row, column, portion in self.medal_locations:
            if grid[row][column] == -1 and portion == 0 and self.is_freeable_medal(row, column):
                # medal is completely uncovered, remove it from grid
                self.remove_medal(row, column)

                # decrement medals
                self.medals -= 1

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
            self.medal_locations.remove((row + i, column + j, portion))

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

    def get_movements(self):
        return self.movements

    def get_additions(self):
        return self.additions


# ============================================
# main
# ============================================
def main():
    b = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, MOVES_LEFT)

    def print_grid(grid):
        for i in range(PUZZLE_ROWS):
            print(grid[i])

    print("Medal grid:")
    print_grid(b.medal_grid.grid)
    print("Ice grid:")
    print_grid(b.ice_grid.grid)
    print("Gem grid:")
    print_grid(b.gem_grid.grid)

    swap_locations = [(1, 2), (2, 2)]
    b.set_swap_locations(swap_locations)

    # state = b.get_update()
    # print("State 1:")
    # print(state)
    #
    # state2 = b.get_update()
    # print("\nState 2:")
    # print(state2)

    count = 0
    while not b.get_update().is_empty():
        print(f'\nUpdate {count}:')
        print(b.get_update())
        count += 1

        # print("Empty bag:")
        # print(b.get_update())


if __name__ == '__main__':
    main()
