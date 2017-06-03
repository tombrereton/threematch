import random

import pygame

import game_utilities as util
import global_variables as globals
import grid as g

medal_group = pygame.sprite.Group()


class Medal(pygame.sprite.Sprite):
    """
    A class to load in the medal image
    """

    def __init__(self, cell_size: int):
        # call super constructor
        # and add bear to bears group
        pygame.sprite.Sprite.__init__(self, medal_group)

        self.medal_file = "tiles/medal_02_01.png"
        self.medal_size = cell_size * 2
        self.image, self.rect = util.load_image(self.medal_file, self.medal_size)


class MedalPortion(object):
    """
    A class to represent a portion of a bear.
    For a 2x2 bear we have 4 bear portions, each
    one either top left, top right, bottom left,
    or bottom right.
    """

    def __init__(self, medal_id: int, portion: int):
        # bear is id number, starting from 0
        self.medal_id = medal_id

        # for a 2x2 bear, portion = {0,1,2,3}
        # where 0 = top left, 3 = bottom right
        self.portion = portion
        self.uncovered = False


class MedalGrid(g.Grid):
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
        i = 0
        while i < globals.LEVEL_1_TOTAL_MEDALS:
            x = random.choice(range(self.columns - 1))
            y = random.choice(range(4, self.rows - 1))
            if self.check_medal_boundaries(y, x):
                self.add_medal(i, y, x)
                i = i + 1

    def add_medal(self, medal_id: int, y_coord: int, x_coord: int):
        """
        Method to add a medal (four medal portions) to the grid
        :param medal_id: Number of medal to be added
        :param y_coord: y coordinate to add medal at (top left of medal)
        :param x_coord: x coordinate to add beat at (top left of medal)
        :return: None
        """
        medal = Medal(self.cell_size)
        x = int(self.margin + x_coord * self.cell_size)
        y = int(self.margin + y_coord * self.cell_size)
        medal.rect.left = x
        medal.rect.top = y
        self.sprites[medal_id] = medal
        for i in range(2):
            for j in range(2):
                self.grid[y_coord + i][x_coord + j] = MedalPortion(medal_id, i + 2 * j)

    def remove_medal(self, medal_ID: int, y_coord: int, x_coord: int):
        """
        Method to remove a medal (four medal portions) from the grid
        :param medal_ID: Number of medal to be removed
        :param y_coord: y coordinate to remove medal from (top left of medal)
        :param x_coord: x coordinate to remove medal from (top left of medal)
        :return: None
        """
        medal = self.sprites.pop(medal_ID)
        medal_group.remove(medal)
        for i in range(2):
            for j in range(2):
                self.grid[y_coord + i][x_coord + j] = 0

    def check_medal_boundaries(self, y_coord: int, x_coord: int):
        """
        Method to check is a medal can be added at a certain location
        :param y_coord: y coordinate to check (top left of medal)
        :param x_coord: x coordinate to check (top left of medal)
        :return: None
        """
        if x_coord < self.columns - 1 and y_coord < self.rows - 1:
            for i in range(2):
                for j in range(2):
                    if self.grid[y_coord + i][x_coord + j] != 0:
                        return False
            return True
        return False

    def get_medal_locations(self):
        pass

    def free_medals(self):
        """
        Method to free all freeable medals
        :return: None
        """
        for i in range(self.rows - 1):
            for j in range(self.columns - 1):
                if self.freeable(i, j):
                    medal_id = self.grid[i][j].medal_id
                    self.remove_medal(medal_id, i, j)

    def freeable(self, y_coord: int, x_coord: int):
        """
        Method to check if a uncovered medal exists at this location
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if uncovered medal exists, False if not
        """
        if self.grid[y_coord][x_coord] != 0 and self.grid[y_coord][x_coord].portion == 0:
            for i in range(2):
                for j in range(2):
                    if not self.grid[y_coord + i][x_coord + j].uncovered:
                        return False
            return True
        return False
