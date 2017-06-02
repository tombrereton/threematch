import random

import pygame

import game_utilities as util

gems = pygame.sprite.Group()


class Gem(pygame.sprite.Sprite):
    def __init__(self, size: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, gems)
        self.type = random.randint(1, 8)
        self.isBonus = False
        self.gemName = "bean{}.png".format(self.type)
        self.image, self.rect = util.loadImage(self.gemName, size)


class GemGrid(object):
    def __init__(self, screen: pygame.display, rows: int, columns: int, gemSize: int):
        self.screen = screen
        self.rows = rows
        self.columns = columns
        self.gemSize = gemSize
        self.gemgrid = [[-1 for x in range(self.rows)] for y in range(self.columns)]

        # generate gem grid
        self.newGemGrid()

    def newGemGrid(self):
        """
        adds the gems to the screen
        :return:
        """
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                gem = Gem(self.gemSize)
                self.gemgrid[i][j] = gem
                self.screen.blit(gem.image, (i * self.gemSize, j * self.gemSize))

    def addGem(self, gem: Gem, x_coord: int, y_coord: int):
        pass

    def removeGem(self, x_coord: int, y_coord: int):
        pass

    def swapGems(self, x_coord: int, y_coord: int, direction: str):
        """
        Provide x and y coordinate and direction and
        swap the gem at x and y with the gem in the direction
        of 'direction'
        """
        pass
