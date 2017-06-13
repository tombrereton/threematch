import pygame
import random

from itertools import product
from background import Background
from game_state import GameState
from global_variables import *
import game_utilities as util

gem_group = pygame.sprite.Group()
ice_group = pygame.sprite.Group()
medal_group = pygame.sprite.Group()


class Container:

    def __init__(self, **kwargs):
        self.add(**kwargs)

    def add(self, **kwargs):
        for k, v in kwargs:
            self.__dict__[k] = v


def rand():
    gems = [[(random.randrange(5), random.randrange(4), 0) for j in range(PUZZLE_COLUMNS)] for i in range(PUZZLE_ROWS)]
    ice = [[random.randrange(2) for j in range(PUZZLE_COLUMNS)] for i in range(PUZZLE_ROWS)]
    medals = [[(random.randrange(5), random.randrange(4)) for j in range(PUZZLE_COLUMNS)] for i in range(PUZZLE_ROWS)]
    return gems, ice, medals


class Grid:

    def __init__(self):
        self.rows = PUZZLE_ROWS
        self.columns = PUZZLE_COLUMNS
        self.cell_size = CELL_SIZE
        self.margin = MARGIN
        self.grid = [[0] * self.columns] * (self.rows + 1)


class Gem(pygame.sprite.Sprite):

    def __init__(self, size: int, info: tuple, image_list: list, explosions: list):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, gem_group)
        self.gem_size = size
        self.type, self.bonus_type, self.activation = info
        self.image_list = image_list
        self.explosions = explosions
        self.explosion_step = 0
        self.is_exploding = False
        self.image = self.image_list[self.bonus_type][self.type]
        self.rect = self.image.get_rect()
        self.origin = (0, 0)
        self.target = (0, 0)
        self.i = 0

    def update_bonus_type(self, new_bonus_type: int):
        self.bonus_type = new_bonus_type
        self.image = self.image_list[self.bonus_type][self.type]

    def init_rect(self, y: int, x: int):
        self.set_rect(y, x)
        self.set_origin(y, x)
        self.set_target(y, x)

    def set_target(self, y: int, x: int):
        self.target = (y, x)

    def set_rect(self, y: int, x: int):
        self.rect.top = y
        self.rect.left = x

    def set_origin(self, y: int, x: int):
        self.origin = (y, x)


class GemGrid(Grid):

    def __init__(self, gems: list, gem_images: list, explosions: list):
        super().__init__()
        self.gem_images = gem_images
        self.explosions = explosions
        self.centering_offset = 0.05 * self.cell_size
        for i in range(PUZZLE_COLUMNS):
            for j in range(PUZZLE_ROWS):
                self.add_gem(i, j, gems[i][j])

    def add_gem(self, y_coord: int, x_coord: int, info: tuple):
        gem = Gem(0.9 * CELL_SIZE, info, self.gem_images, self.explosions)
        x = self.margin + self.centering_offset + x_coord * self.cell_size
        y = self.margin + self.centering_offset + y_coord * self.cell_size
        gem.init_rect(y, x)
        self.grid[y_coord][x_coord] = gem


class Ice(pygame.sprite.Sprite):
    def __init__(self, size: int, layer: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, ice_group)
        self.layer = 3
        self.ice_layer = "ice/ice_layer_{}.png".format(self.layer)
        self.image, self.rect = util.load_image(self.ice_layer, size)


class IceGrid(Grid):

    def __init__(self, ice: list):
        super().__init__()
        for i in range(PUZZLE_COLUMNS):
            for j in range(PUZZLE_ROWS):
                self.add_ice(i, j, ice[i][j])

    def add_ice(self, y_coord: int, x_coord: int, layer: int):
        if layer is 0:
            ice = 0
        else:
            ice = Ice(self.cell_size, layer)
            x = self.margin + x_coord * self.cell_size
            y = self.margin + y_coord * self.cell_size
            ice.rect.left = x
            ice.rect.top = y
        self.grid[y_coord][x_coord] = ice


class Medal(pygame.sprite.Sprite):

    def __init__(self, cell_size: int):
        super().__init__(self, medal_group)
        self.medal_file = "tiles/medal_02_01.png"
        self.medal_size = cell_size * 2
        self.image, self.rect = util.load_image(self.medal_file, self.medal_size)


class MedalGrid(Grid):

    def __init__(self, medals: list):
        super().__init__()
        for i in range(PUZZLE_COLUMNS):
            for j in range(PUZZLE_ROWS):
                self.add_medal(i, j, medals[i][j])

    def add_medal(self, y_coord: int, x_coord: int, info: tuple):
        medal = Medal(self.cell_size)
        x = int(self.margin + x_coord * self.cell_size)
        y = int(self.margin + y_coord * self.cell_size)
        medal.rect.left = x
        medal.rect.top = y
        self.sprites[medal_id] = medal

class GUI:

    def __init__(self, gems, ice, medals):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gem Island')
        game_state = GameState(MOVES_LEFT, LEVEL_1_TOTAL_MEDALS)
        self.bg = Background(game_state)
        self.screen.blit(self.bg.background, (0, 0))
        self.gem_grid = GemGrid(gems, self.bg.gem_images, self.bg.explosions)
        self.ice_grid = IceGrid(ice)
        # self.medal_grid = MedalGrid(medals)
        # pygame.display.flip()
        ice_group.draw(self.screen)
        gem_group.draw(self.screen)
        pygame.display.flip()
        print('done')
        while True:
            pass

if __name__ == '__main__':
    GUI(*rand())
