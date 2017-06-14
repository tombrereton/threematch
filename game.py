"""
This is the file for the game logic of three match.
"""
from itertools import product
from random import randint, choice

from global_variables import PUZZLE_ROWS, PUZZLE_COLUMNS, GEM_TYPES, ICE_ROWS, LEVEL_1_TOTAL_MEDALS


class Grid:
    """
    The parent class to define the grid size and
    initialise an empty 2D array.
    """

    def __init__(self):
        self.rows = PUZZLE_ROWS
        self.columns = PUZZLE_COLUMNS
        self.grid = [[-1] * self.columns for row in range(self.rows)]


class Board:
    """
    The class which contains all the gems, ice, and medals.

    The gem grid contains tuples in each cell, which represent:
    (type, bonus_type, activation)

    The ice grid contains a single value in each cell, represented by:
    (layer)

    The medal_grid contains a single value in each cell, represented by:
    (corner)
    """

    def __init__(self):
        self.gem_grid = Grid()
        self.ice_grid = Grid()
        self.medal_grid = Grid()

        # initialise grids
        self.init_gem_grid()
        self.init_ice_grid()
        self.init_medal_grid()

    def new_gem(self):
        """
        Creates a tuple to represent a gem.

        The gem type is randomised.
        :return:
        """
        type = randint(0, GEM_TYPES - 1)
        bonus_type = 0
        activation = 0
        return type, bonus_type, activation

    def init_gem_grid(self):
        """
        Initialises the gem grid with tuples.
        """
        rows = self.gem_grid.rows
        columns = self.gem_grid.columns
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
        ice_rows = rows - ICE_ROWS
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
        while i < LEVEL_1_TOTAL_MEDALS:
            # get random choice
            row = choice(range(rows - ICE_ROWS, rows - 1))
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


# ============================================
# main
# ============================================
def main():
    b = Board()

    def print_grid(grid):
        for i in range(PUZZLE_ROWS):
            print(grid[i])
    print("Medal grid:")
    print_grid(b.medal_grid.grid)
    print("Ice grid:")
    print_grid(b.ice_grid.grid)
    print("Gem grid:")
    print_grid(b.gem_grid.grid)

if __name__ == '__main__':
    main()
