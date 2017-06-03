import pygame

import game_utilities as util
import grid as g

ice_group = pygame.sprite.Group()


class Ice(pygame.sprite.Sprite):
    def __init__(self, size: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, ice_group)
        self.layer = 3
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
        for i in range(5, self.rows):
            for j in range(0, self.columns):
                ice = Ice(self.cell_size)
                x = self.margin + j * self.cell_size
                y = self.margin + i * self.cell_size
                ice.rect.left = x
                ice.rect.top = y
                self.grid[i][j] = ice
                # self.screen.blit(ice.image, (x, y))
                # self.screen.blit(ice.image,
                #                  (self.margin/2 + i * (self.cell_size + self.cell_size / 4),
                #                   self.margin/2 + j * (self.cell_size + self.cell_size / 4)))

    def addIce(self, ice: Ice, y_coord: int, x_coord: int):
        pass

    def removeIce(self, y_coord: int, x_coord: int):
        pass
