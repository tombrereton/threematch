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

    def is_ice(self, y_coord: int, x_coord: int):
        return self.ice_grid.isIce(y_coord, x_coord)

    def remove_ice(self, y_coord: int, x_coord: int):
        if self.is_ice(y_coord, x_coord):
            self.ice_grid.removeIce(y_coord, x_coord)


    def free_bears(self):
        self.bear_grid.free_bears()

    def set_bear_portion_uncovered(self, y_coord: int, x_coord: int):
        if self.bear_grid[y_coord][x_coord] != 0:
            self.bear_grid.grid[y_coord][x_coord].uncovered = True

    def is_bear(self, y_coord: int, x_coord: int):
        pass

    def is_bear_uncovered(self, y_coord: int, x_coord: int):
        pass

    def new_board(self):
        # generates a random new board
        # create 9x9 candies on board
        pass

    def swap_gems(self, y_coord: int, x_coord: int, direction: str):
        # call the gemgrid swap class but also checks
        # for ice and bears
        self.gem_grid.swap_gems(y_coord, x_coord, direction)

    def get_gem(self, y_coord: int, x_coord: int):
        return self.gem_grid.get_gem(y_coord, x_coord)

    def get_gem_group(self):
        return gemgrid.gem_group

    def get_ice_group(self):
        return icegrid.ice_group

    def get_bear_group(self):
        return beargrid.bear_group
