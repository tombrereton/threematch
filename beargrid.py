import pygame

import game_utilities as util
import grid as g

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
        for i in range(4):
            self.add_bear(i, 0, 2 * i)

    def add_bear(self, bear_ID: int, y_coord: int, x_coord: int):
        # adds a bear portion something like
        # self.beargrid[x_coord][y_coord] = BearPortion(bearID, portion)
        bear = Bear(self.cell_size)
        x = int(self.margin + x_coord * self.cell_size)
        y = int(self.margin + y_coord * self.cell_size)
        bear.rect.left = x
        bear.rect.top = y
        for i in range(2):
            for j in range(2):
                self.grid[x_coord + i][y_coord + j] = BearPortion(bear_ID, i + 2 * j)

    def remove_bear(self, y_coord: int, x_coord: int):
        pass

    def check_bear_boundaries(self, y_coord: int, x_coord: int):
        pass

    def get_bear_locations(self):
        pass
