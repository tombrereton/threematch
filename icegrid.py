import pygame

import game_utilities as util
import grid as g

ice_group = pygame.sprite.Group()


class Ice(pygame.sprite.Sprite):
    def __init__(self, size: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, ice_group)
        self.layer = 3
        self.ice_layer = "ice_layer_{}.png".format(self.layer)
        self.image, self.rect = util.load_image(self.ice_layer, size)


class IceGrid(g.Grid):
    """
    Sub class of Grid
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cell_size: int):
        super().__init__(screen, rows, columns, cell_size)

    def new_grid(self):
        """
        override method in Grid class.

        adds the gems to the screen
        :return:
        """
        for i in range(0, self.rows):
            for j in range(5, self.columns):
                sprite = Ice(self.cell_size + int(self.cell_size/4) + 4)
                self.grid[i][j] = sprite
                self.screen.blit(sprite.image,
                                 (i * (self.cell_size + self.cell_size / 4),
                                  j * (self.cell_size + self.cell_size / 4)))

    def addIce(self, ice: Ice, x_coord: int, y_coord: int):
        pass

    def removeIce(self, x_coord: int, y_coord: int):
        pass
