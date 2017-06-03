import pygame

import gemgrid
import icegrid
import medalgrid


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
        self.medal_grid = medalgrid.MedalGrid(screen, rows, columns, cell_size, margin)
        self.ice_grid = icegrid.IceGrid(screen, rows, columns, cell_size, margin)
        self.gem_grid = gemgrid.GemGrid(screen, rows, columns, cell_size, margin)
        self.screen = screen

    def is_ice(self, y_coord: int, x_coord: int):
        """
        Method to evaluate if a position contains ice
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if ice, False if not
        """
        return self.ice_grid.grid[y_coord][x_coord] != 0

    def remove_ice(self, y_coord: int, x_coord: int):
        if self.is_ice(y_coord, x_coord):
            self.ice_grid.removeIce(y_coord, x_coord)

            if self.is_medal(y_coord, x_coord):
                self.set_medals_portion_uncovered(y_coord, x_coord)
                self.free_medals()

    def free_medals(self):
        self.medal_grid.free_medals()

    def set_medals_portion_uncovered(self, y_coord: int, x_coord: int):
        self.medal_grid.grid[y_coord][x_coord].uncovered = True

    def is_medal(self, y_coord: int, x_coord: int):
        """
        Method to evaluate if a position contains a bear
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if a bear, False if not
        """
        return self.medal_grid.grid[y_coord][x_coord] != 0

    def is_medal_uncovered(self, y_coord: int, x_coord: int):
        """
        Method to evaluate if a position contains a visible bear
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if visible and a bear, False if not
        """
        return not self.is_ice(y_coord, x_coord) and self.is_medal(y_coord, x_coord)

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

    def get_medal_group(self):
        return medalgrid.medal_group
