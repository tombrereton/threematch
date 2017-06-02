import random

import pygame

import game_utilities as util
import grid as g

gems = pygame.sprite.Group()


class Gem(pygame.sprite.Sprite):
    def __init__(self, size: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, gems)
        self.type = random.randint(1, 8)
        self.is_bonus = False
        self.gem_name = "Stone_0{}_05.png".format(self.type)
        self.image, self.rect = util.load_image(self.gem_name, size)


class GemGrid(g.Grid):
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
        centering_offset = self.cell_size/4/2
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                sprite = Gem(self.cell_size)
                self.grid[i][j] = sprite
                self.screen.blit(sprite.image,
                                 (self.margin/2 + centering_offset + i * (self.cell_size + self.cell_size / 4),
                                  self.margin/2 + centering_offset + j * (self.cell_size + self.cell_size / 4)))


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
