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

    def __init__(self, screen: pygame.display, rows: int, columns: int, cell_size: int, margin: int):
        self.bear_grid = beargrid.BearGrid(screen, rows, columns, cell_size, margin)
        self.ice_grid = icegrid.IceGrid(screen, rows, columns, cell_size, margin)
        self.gem_grid = gemgrid.GemGrid(screen, rows, columns, cell_size, margin)
        self.screen = screen

    def is_ice(self, x_coord: int, y_coord: int):
        pass

    def is_bear(self, x_coord: int, y_coord: int):
        pass

    def is_bear_uncovered(self, x_coord: int, y_coord: int):
        pass

    def new_board(self):
        # generates a random new board
        # create 9x9 candies on board
        pass

    def swap_gems(self):
        # call the gemgrid swap class but also checks
        # for ice and bears
        pass
