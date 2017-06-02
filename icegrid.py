import pygame

import game_utilities as util

ice = pygame.sprite.Group()


class Ice(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.display, size: int):
        # call super constructor
        self.screen = screen
        pygame.sprite.sprite.__init__(self, ice)
        self.layer = 3
        self.iceLayer = "ice_layer_{}.png".format(self.layer)
        self.image, self.rect = util.loadImage(self.iceLayer, size)


class IceGrid(object):
    def __init__(self, screen: pygame.display, rows: int, columns: int, iceSize: int):
        self.screen = screen
        self.iceSize = iceSize
        self.rows = rows
        self.columns = columns
        self.icegrid = [[1 for x in range(self.rows)] for y in range(self.columns)]

    def addIce(self, ice: Ice, x_coord: int, y_coord: int):
        pass

    def removeIce(self, x_coord: int, y_coord: int):
        pass
