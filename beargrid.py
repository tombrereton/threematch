import pygame

import game_utilities as util
import grid as g
import random

bear_group = pygame.sprite.Group()


class Bear(pygame.sprite.Sprite):
    """
    A class to load in the bear image
    """

    def __init__(self, cell_size: int):
        # call super constructor
        # and add bear to bears group
        pygame.sprite.Sprite.__init__(self, bear_group)

        self.bear_file = "tiles/medal_02_01.png"
        self.bear_size = cell_size * 2
        self.image, self.rect = util.load_image(self.bear_file, self.bear_size)


class BearPortion(object):
    """
    A class to represent a portion of a bear.
    For a 2x2 bear we have 4 bear portions, each
    one either top left, top right, bottom left,
    or bottom right.
    """

    def __init__(self, bear_ID: int, portion: int):
        # bear is id number, starting from 0
        self.bear = bear_ID

        # for a 2x2 bear, portion = {0,1,2,3}
        # where 0 = top left, 3 = bottom right
        self.portion = portion
        self.uncovered = False


class BearGrid(g.Grid):
    """
    Sub class of Grid

    A class to store the bear locations as a 2D grid
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cell_size: int, margin: int):
        super().__init__(screen, rows, columns, cell_size, margin)

    def new_grid(self):
        """
        override method in Grid class.

        adds the bears to the screen
        :return:
        """
        self.sprites = {}
        for i in range(4):
            x = random.choice(range(self.columns - 1))
            y = random.choice(range(5, self.rows - 1))
            if self.check_bear_boundaries(y, x):
                self.add_bear(i, y, x)

    def add_bear(self, bear_ID: int, y_coord: int, x_coord: int):
        """
        Method to add a bear (four bear portions) to the grid
        :param bear_ID: Number of bear to be added
        :param y_coord: y coordinate to add bear at (top left of bear)
        :param x_coord: x coordinate to add beat at (top left of bear)
        :return: None
        """
        bear = Bear(self.cell_size)
        x = int(self.margin + x_coord * self.cell_size)
        y = int(self.margin + y_coord * self.cell_size)
        bear.rect.left = x
        bear.rect.top = y
        self.sprites[bear_ID] = bear
        for i in range(2):
            for j in range(2):
                self.grid[y_coord + i][x_coord + j] = BearPortion(bear_ID, i + 2 * j)

    def remove_bear(self, bear_ID: int, y_coord: int, x_coord: int):
        """
        Method to remove a bear (four bear portions) from the grid
        :param bear_ID: Number of bear to be removed
        :param y_coord: y coordinate to remove bear from (top left of bear)
        :param x_coord: x coordinate to remove bear from (top left of bear)
        :return: None
        """
        bear = self.sprites.pop(bear_ID)
        bear_group.remove(bear)
        for i in range(2):
            for j in range(2):
                self.grid[y_coord + i][x_coord + j] = 0

    def check_bear_boundaries(self, y_coord: int, x_coord: int):
        """
        Method to check is a bear can be added at a certain location
        :param y_coord: y coordinate to check (top left of bear)
        :param x_coord: x coordinate to check (top left of bear)
        :return: None
        """
        if x_coord < self.columns - 1 and y_coord < self.rows - 1:
            for i in range(2):
                for j in range(2):
                    if self.grid[y_coord + i][x_coord + j] != 0:
                        return False
            return True
        return False

    def get_bear_locations(self):
        pass

    def free_bears(self):
        """
        Method to free all freeable bears
        :return: None
        """
        for i in range(self.rows - 1):
            for j in range(self.columns - 1):
                if self.freeable(i, j):
                    self.remove_bear(i, j)

    def freeable(self, y_coord: int, x_coord: int):
        """
        Method to check if a uncovered bear exists at this location
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if uncovered bear exists, False if not
        """
        if self.grid[y_coord][x_coord] != 1 and self.grid[y_coord][x_coord].portion == 0:
            for i in range(2):
                for j in range(2):
                    if not self.grid[y_coord + i][x_coord + j].uncovered:
                        return False
            return True
        return False
