import pygame


class Grid(object):
    """
    Abstract class for grids.

    The newGrid must be overridden in the sub classes.
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cell_size: int, margin: int):
        self.screen = screen
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.margin = margin
        self.grid = [[0 for x in range(self.columns)] for y in range(self.rows)]

        # generate gem grid
        self.new_grid()

    def new_grid(self):
        raise NotImplementedError("Need to be implemented in sub class.")
