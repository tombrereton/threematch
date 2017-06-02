import pygame

import beargrid
import gemgrid
import icegrid


class Board(object):
    """
    The game board which is a composition class
    of BearGrid, GemGrid, and IceGrid.
    It is the wrapper class which should be used in the three match
    game to interact with the ice, gems, and bears

    This class will then talk to wrapped classes and update them
    as needed.
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cellSize: int):
        self.bearGrid = beargrid.BearGrid(screen, rows, columns, cellSize)
        self.gemGrid = gemgrid.GemGrid(screen, rows, columns, cellSize)
        self.iceGrid = icegrid.IceGrid(screen, rows, columns, cellSize)
        self.screen = screen

    def isIce(self, x_coord: int, y_coord: int):
        pass

    def isBear(self, x_coord: int, y_coord: int):
        pass

    def isBearUncovered(self, x_coord: int, y_coord: int):
        pass

    def newBoard(self):
        # generates a random new board
        # create 9x9 candies on board
        pass

    def swapGems(self):
        # call the gemgrid swap class but also checks
        # for ice and bears
        pass
