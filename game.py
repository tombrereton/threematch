"""
This is the file for the game logic of three match.
"""
from itertools import product
from operator import itemgetter
from random import randint, choice

from global_variables import PUZZLE_ROWS, PUZZLE_COLUMNS, GEM_TYPES, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, BONUS_TYPES, \
    MOVES_LEFT


class Grid:
    """
    The parent class to define the grid size and
    initialise an empty 2D array.
    """

    def __init__(self):
        self.rows = PUZZLE_ROWS
        self.columns = PUZZLE_COLUMNS
        self.grid = [[-1] * self.columns for _ in range(self.rows)]


class Board:
    """
    The class which contains all the grids for gems, ice, and medals.

    The gem grid contains tuples in each cell, which represent:
    (type, bonus_type, activation)

    The ice grid contains a single value in each cell, represented by:
    (layer)

    The medal_grid contains a single value in each cell, represented by:
    (corner)

    Swapped gems is a list of tuples, represented as:
    [(row, column, type, bonus_type, activation),(same again)]
    """

    def __init__(self, rows: int, columns: int, ice_rows: int, medals: int,
                 moves: int, gem_types: int = GEM_TYPES, bonus_types: int = BONUS_TYPES):
        # grids
        self.gem_grid = Grid()
        self.ice_grid = Grid()
        self.medal_grid = Grid()

        # game variables
        self.rows = rows
        self.columns = columns
        self.ice_rows = ice_rows
        self.medals = medals
        self.moves = moves
        self.gem_types = gem_types
        self.bonus_types = bonus_types

        # initialise grids
        self.init_gem_grid()
        self.init_ice_grid()
        self.init_medal_grid()

        # helper variables
        self.swapped_gems = [(), ()]

    def new_gem(self):
        """
        Creates a tuple to represent a gem.

        The gem type is randomised.
        :return:
        """
        gem_type = randint(0, self.gem_types - 1)
        bonus_type = 0
        activation = 0
        return gem_type, bonus_type, activation

    def init_gem_grid(self):
        """
        Initialises the gem grid with tuples.
        """
        rows = self.rows
        columns = self.columns
        for row, column in product(range(rows), range(columns)):
            self.gem_grid.grid[row][column] = self.new_gem()

    def init_ice_grid(self):
        """
        Initialises the ice grid with the number of layers.

        The ice is initialised from the bottom row first,
        up to the number of ICE_ROWS.
        :return:
        """
        rows = self.ice_grid.rows - 1
        columns = self.ice_grid.columns
        ice_rows = rows - self.ice_rows
        for row in range(rows, ice_rows, -1):
            for col in range(columns):
                self.ice_grid.grid[row][col] = 1

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
        rows = self.medal_grid.rows
        columns = self.medal_grid.columns
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
        rows = self.medal_grid.rows
        columns = self.medal_grid.columns
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
                self.medal_grid.grid[row + i][column + j] = j + 2 * i

    def swap_gems(self, swap_locations: list):
        """
        A list containing the swapped gems is passed in. The
        list is in the format:

        [(gem1_row, gem1_col),(gem2_row, gem2_col)]

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



    def get_swapped_gems(self):
        """
        Simple getter to get the list of swapped gems.

        This returns the gems to be swapped, i.e.
        they are in their original position.
        :return:
        """
        return self.swapped_gems

    def find_matches(self):
        """
        Find the matches in the gem grid.

        If the vertical and horizontal matches intersect, create
        a bonus of type 3.
        :return:
        """
        h, h_from_bonus, h_bonuses = self.find_horizontal_matches()
        v, v_from_bonus, v_bonuses = self.find_vertical_matches()

        # merge lists but not matches from bonuses to avoid
        # lots of T-type bonuses
        matches = h + v
        bonuses = h_bonuses + v_bonuses

        # if matches intersect, create bonus type 3
        t_match = list(set(h).intersection(v))

        if len(t_match) > 0:

            # if gem in t_match and matches, remove it and make it a T-type bonuses
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
                # add row to matches at location row
                for j in range(self.columns):
                    matches_from_bonus.append(self.get_gem_info(row, j))

            if bonus_type == 2:
                # add all gems of this gems type to matches
                for i, j in product(range(self.rows), range(self.columns)):
                    if self.gem_grid.grid[i][j][0] == gem_type:
                        matches_from_bonus.append(self.get_gem_info(i, j))

            if bonus_type == 3:
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
                # add column to matches at location column
                for i in range(self.rows):
                    matches_from_bonus.append(self.get_gem_info(i, column))

            if bonus_type == 2:
                # add all gems of this gems type to matches
                for i, j in product(range(self.rows), range(self.columns)):
                    if self.gem_grid.grid[i][j][0] == gem_type:
                        matches_from_bonus.append(self.get_gem_info(i, j))

            if bonus_type == 3:
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
        columns = self.gem_grid.columns
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
        columns = self.columns
        grid = self.gem_grid.grid
        match_index = row + 1
        match_list = [self.get_gem_info(row, column)]

        # check if its a match
        while match_index < columns and grid[row][column][0] == grid[match_index][column][0]:
            # if match, append to list
            match_list.append(self.get_gem_info(match_index, column))
            match_index += 1
        return match_list

    def get_gem_info(self, row: int, column: int, new_bonus=None):
        """
        Return the coordinates of the gem, along with its
        type and bonus type. This information is returned
        as a tuple. The structure is:
        (row, column, type, bonus_type, activation
        :param new_bonus:
        :param row:
        :param column:
        :return:
        """
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
    b.swap_gems(swap_locations)
    print("Swapped gems:")
    print(b.get_swapped_gems())

    matches, bonuses = b.find_matches()
    print("Matches")
    print(matches)
    print("Bonuses")
    print(bonuses)


if __name__ == '__main__':
    main()
