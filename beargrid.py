import pygame

import game_utilities as util

bears = pygame.sprite.Group


class Bear(pygame.sprite.Sprite):
    """
    A class to load in the bear image
    """

    def __init__(self, cellSize: int):
        # call super constructor
        # and add bear to bears group
        pygame.sprite.Sprite.__init__(self, bears)

        self.bearFile = "bear.png"
        self.bearSize = cellSize * 2
        self.image, self.rect = util.loadImage(self.bearFile, self.bearSize)


class BearPortion(object):
    """
    A class to represent a portion of a bear.
    For a 2x2 bear we have 4 bear portions, each
    one either top left, top right, bottom left,
    or bottom right.
    """

    def __init__(self, bearID: int, portion: int):
        # bear is id number, starting from 0
        self.bear = bearID

        # for a 2x2 bear, portion = {0,1,2,3}
        # where 0 = top left, 3 = bottom right
        self.portion = portion


class BearGrid(object):
    """
    A class to store the bear locations as a 2D grid
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cellSize: int):
        self.screen = screen
        self.cellSize = cellSize
        self.rows = rows
        self.columns = columns
        self.beargrid = [[1 for x in range(self.rows)] for y in range(self.columns)]

    def addBear(self, x_coord: int, y_coord: int):
        # adds a bear portion something like
        # self.beargrid[x_coord][y_coord] = BearPortion(bearID, portion)
        pass

    def removeBear(self, x_coord: int, y_coord: int):
        pass

    def checkBearBoundaries(self, x_coord: int, y_coord: int):
        pass

    def getBearLocations(self):
        pass
