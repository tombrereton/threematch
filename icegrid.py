import pygame

import game_utilities as util
import grid as g

ice_group = pygame.sprite.Group()


class Ice(pygame.sprite.Sprite):
    def __init__(self, size: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, ice_group)
        self.layer = 2
        self.ice_layer = "ice/ice_layer_{}.png".format(self.layer)
        self.image, self.rect = util.load_image(self.ice_layer, size)


class IceGrid(g.Grid):
    """
    Sub class of Grid
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cell_size: int, margin: int):
        super().__init__(screen, rows, columns, cell_size, margin)

    def new_grid(self):
        """
        override method in Grid class.

        adds the gems to the screen
        :return:
        """
        for i in range(4, self.rows):
            for j in range(self.columns):
                self.addIce(i, j)

    def addIce(self, y_coord: int, x_coord: int):
        """
        Method to add ice to the grid
        :param y_coord: y coordinate to add ice at
        :param x_coord: x coordinate to add ice at
        :return: None
        """
        ice = Ice(self.cell_size)
        x = self.margin + x_coord * self.cell_size
        y = self.margin + y_coord * self.cell_size
        ice.rect.left = x
        ice.rect.top = y
        self.grid[y_coord][x_coord] = ice

    def removeIce(self, y_coord: int, x_coord: int):
        """
        Method to remove ice from the grid
        :param y_coord: y coordinate to remove ice from
        :param x_coord: x coordinate to remove ice from
        :return: None
        """
        ice_group.remove(self.grid[y_coord][x_coord])
        self.grid[y_coord][x_coord] = 0

    def isIce(self, y_coord: int, x_coord: int):
        return self.grid[y_coord][x_coord] != 0
