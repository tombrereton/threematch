import pygame
import random
import time

from itertools import product
from game_state import GameState
from global_variables import *
import game_utilities as util


def print_array(a):
    print('\n'.join(['\t'.join([str(el) for el in row]) for row in a]))


def rand():
    gems = [[(random.randrange(5), random.randrange(1), 0) for j in range(PUZZLE_COLUMNS)] for i in range(PUZZLE_ROWS)]
    ice = [[random.randint(-1, 1) for j in range(PUZZLE_COLUMNS)] for i in range(PUZZLE_ROWS)]
    medals_small = [[random.randint(-1, 0) for j in range(PUZZLE_COLUMNS // 2)] for i in range(PUZZLE_ROWS // 2)]
    medals = [[-1] * PUZZLE_COLUMNS for i in range(PUZZLE_ROWS)]
    for i, j in product(range(len(medals_small)), range(len(medals_small[0]))):
        medals[2 * i][2 * j] = medals_small[i][j]
    moves_left = random.randrange(30)
    medals_left = len([0 for row in medals for el in row if el == 0])
    score = random.randrange(1000000)
    terminal = True if random.random() < 2 / 3 else False
    win = True if random.random() < 1 / 2 else False
    return gems, ice, medals, (moves_left, medals_left, score, terminal, win)


def grid_to_pixel(y_coord: int, x_coord: int):
    y = MARGIN + y_coord * CELL_SIZE
    x = MARGIN + x_coord * CELL_SIZE
    return y, x


class SpriteGrid:

    def __init__(self, info: list, group):
        self.rows = PUZZLE_ROWS
        self.columns = PUZZLE_COLUMNS
        self.cell_size = CELL_SIZE
        self.margin = MARGIN
        self.grid = [[-1] * self.columns for i in range(self.rows)]
        self.group = group
        self.new_grid(info)

    def new_grid(self, info: list):
        self.group.empty()
        for i, j in product(range(PUZZLE_COLUMNS), range(PUZZLE_ROWS)):
            self.add(i, j, info[i][j])

    def add(self, y_coord: int, x_coord: int, info):
        raise NotImplementedError("Need to be implemented in sub class.")

    def remove(self, y_coord: int, x_coord: int):
        raise NotImplementedError("Need to be implemented in sub class.")


class Gem(pygame.sprite.Sprite):

    def __init__(self, size: int, info: tuple, image_list: list, explosions: list, gem_group):
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

    def update(self):
        if self.origin != self.target:
            # move gem
            self.move()

        elif self.is_exploding:
            # explode gem
            self.explode()

    def explode(self):
        """
        if about to be removed, explode gem first
        :return:
        """
        self.image = self.explosions[self.explosion_step]
        self.explosion_step += 1
        if self.explosion_step > EXPLOSION_FRAMES - 1:
            self.is_exploding = False

    def move(self):
        self.i += 1
        y = int(self.origin[0] + self.i * (self.target[0] - self.origin[0]) / (ANIMATION_SCALE))
        x = int(self.origin[1] + self.i * (self.target[1] - self.origin[1]) / (ANIMATION_SCALE))
        self.rect.top = y
        self.rect.left = x
        if self.i == ANIMATION_SCALE:
            self.i = 0
            self.origin = self.target


class GemGrid(SpriteGrid):

    def __init__(self, gems: list, gem_images: list, explosions: list, group):
        self.gem_images = gem_images
        self.explosions = explosions
        self.centering_offset = 0.05 * CELL_SIZE
        super().__init__(gems, group)

    def add(self, y_coord: int, x_coord: int, info: tuple):
        gem = Gem(0.9 * CELL_SIZE, info, self.gem_images, self.explosions, self.group)
        y, x = grid_to_pixel(y_coord, x_coord)
        y += self.centering_offset
        x += self.centering_offset
        gem.init_rect(y, x)
        self.grid[y_coord][x_coord] = gem

    def remove(self, y_coord: int, x_coord: int):
        gem = self.grid[y_coord][x_coord]
        if gem is not -1:
            self.group.remove(gem)
            self.grid[y_coord][x_coord] = -1


class Ice(pygame.sprite.Sprite):
    def __init__(self, size: int, layer: int, ice_group):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, ice_group)
        self.layer = layer
        self.ice_layer = "ice/ice_layer_{}.png".format(self.layer)
        self.image, self.rect = util.load_image(self.ice_layer, size)


class IceGrid(SpriteGrid):

    def __init__(self, ice: list, group):
        super().__init__(ice, group)

    def add(self, y_coord: int, x_coord: int, layer: int):
        if layer is not -1:
            ice = Ice(self.cell_size, layer, self.group)
            y, x = grid_to_pixel(y_coord, x_coord)
            ice.rect.left = x
            ice.rect.top = y
            self.grid[y_coord][x_coord] = ice

    def remove(self, y_coord: int, x_coord: int):
        ice = self.grid[y_coord][x_coord]
        if ice is not -1:
            self.group.remove(ice)
            self.grid[y_coord][x_coord] = -1


class Medal(pygame.sprite.Sprite):

    def __init__(self, cell_size: int, medal_group):
        pygame.sprite.Sprite.__init__(self, medal_group)
        self.medal_file = "tiles/medal_02_01.png"
        self.medal_size = cell_size * 2
        self.image, self.rect = util.load_image(self.medal_file, self.medal_size)


class MedalGrid(SpriteGrid):

    def __init__(self, medals: list, group):
        super().__init__(medals, group)

    def add(self, y_coord: int, x_coord: int, portion: int):
        if portion is 0:
            medal = Medal(self.cell_size, self.group)
            y, x = grid_to_pixel(y_coord, x_coord)
            medal.rect.left = x
            medal.rect.top = y
            self.grid[y_coord][x_coord] = medal

    def remove(self, y_coord: int, x_coord: int):
        medal = self.grid[y_coord][x_coord]
        if medal is not -1:
            self.group.remove(medal)
            self.grid[y_coord][x_coord] = -1


class Background:

    def __init__(self, moves_left: int, medals_left: int, score: int, terminal: bool, win: bool):
        self.font = pygame.font.Font(None, int(24 * HD_SCALE))
        self.game_over_font = pygame.font.Font(None, int(60 * HD_SCALE))
        self.moves_left = 0
        self.moves_left_text = None
        self.medals_left = 0
        self.medals_left_text = None
        self.score = 0
        self.score_text = None
        self.game_over_text = None
        self.game_over_text_pos = None
        self.background = util.load_background("stone_light_2.jpg", "ground.png", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.gem_images = []
        self.explosions = []
        self.init_gem_images()
        self.init_explosions()
        self.set_all(moves_left, medals_left, score, terminal, win)

    def set_all(self, moves_left: int, medals_left: int, score: int, terminal: bool, win: bool):
        self.set_moves_left(moves_left)
        self.set_medals_left(medals_left)
        self.set_score(score)
        self.set_game_over_text(terminal, win)

    def set_moves_left(self, moves_left: int):
        self.moves_left = moves_left
        self.moves_left_text = self.font.render("Moves Left: {}".format(self.moves_left), 1, (10, 10, 10))

    def set_medals_left(self, medals_left: int):
        self.medals_left = medals_left
        self.medals_left_text = self.font.render("Medals Left: {}".format(self.medals_left), 1, (10, 10, 10))

    def set_score(self, score: int):
        self.score = score
        self.score_text = self.font.render('Score: {:03.0f}'.format(self.score), 1, (10, 10, 10))

    def set_game_over_text(self, terminal: bool, win: bool):
        text = ('You Win!' if win else 'Game Over') if terminal else ''
        self.game_over_text = self.game_over_font.render(text, 1, (10, 10, 10))
        self.game_over_text_pos = self.game_over_text.get_rect(centery=WINDOW_HEIGHT / 2, centerx=WINDOW_WIDTH / 2)

    def init_gem_images(self):
        for i in range(1, 5):
            type_list = []
            for j in range(1, 7):
                name = f'stones/Stone_0{j}_0{i}.png'
                image = util.load_image_only(name, GEM_SIZE)
                type_list.append(image)
            self.gem_images.append(type_list)

    def init_explosions(self):
        for i in range(EXPLOSION_FRAMES):
            back = f'explosions/black_smoke/blackSmoke0{i}.png'
            fore = f'explosions/explosion/explosion0{i}.png'
            image = util.load_explosion(fore, back, GEM_SIZE)
            self.explosions.append(image)


class GUI:

    def __init__(self, gems: list, ice, medals: list, text_info: tuple):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gem Island')
        self.bg = Background(*text_info)
        self.gem_group = pygame.sprite.Group()
        self.gem_grid = GemGrid(gems, self.bg.gem_images, self.bg.explosions, self.gem_group)
        self.ice_group = pygame.sprite.Group()
        self.ice_grid = IceGrid(ice, self.ice_group)
        self.medal_group = pygame.sprite.Group()
        self.medal_grid = MedalGrid(medals, self.medal_group)
        self.draw()

    def new_state(self, gems: list, ice, medals: list, text_info: tuple):
        self.gem_grid.new_grid(gems)
        self.ice_grid.new_grid(ice)
        self.medal_grid.new_grid(medals)
        self.bg.set_all(*text_info)
        self.draw()

    def draw(self):
        self.screen.blit(self.bg.background, (0, 0))
        self.screen.blit(self.bg.moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        self.screen.blit(self.bg.medals_left_text, (10, WINDOW_HEIGHT - MARGIN * 7 / 6))
        self.screen.blit(self.bg.score_text, (10, WINDOW_HEIGHT - MARGIN / 3))
        self.medal_group.draw(self.screen)
        self.ice_group.draw(self.screen)
        self.gem_group.draw(self.screen)
        self.screen.blit(self.bg.game_over_text, self.bg.game_over_text_pos)
        pygame.display.flip()

    def animate_loop(self):
        for i in range(ANIMATION_SCALE):
            # loop the number of times we need to animate given
            # by ANIMATION_SCALE

            # Call the update method on the sprites
            self.gem_group.update()
            self.ice_group.update()
            self.medal_group.update()

            self.draw()

    def explode(self, removals: list):
        for i, j, _, _, _ in removals:
            self.gem_grid.grid[i][j].is_exploding = True
        self.animate_loop()

    def add_bonuses(self, bonuses: list):
        for i, j, _, bt, _ in bonuses:
            self.gem_grid.grid[i][j].update_bonus_type(bt)
        self.draw()

    def remove(self, removals: list):
        for i, j, _, _, _ in removals:
            self.gem_grid.remove(i, j)
        self.draw()

    def add(self, additions: list):
        for gem in additions:
            self.gem_grid.add(*gem[:2], gem[2:])
            rect = self.gem_grid.grid[gem[0]][gem[1]].rect
            y, x = rect.y - CELL_SIZE, rect.x
            self.gem_grid.grid[gem[0]][gem[1]].set_rect(y, x)
            self.gem_grid.grid[gem[0]][gem[1]].set_origin(y, x)
        self.draw()

    def move(self, moving_gems: list):
        for y1, x1, y2, x2 in moving_gems:
            o1 = self.gem_grid.grid[y1][x1].origin
            o2 = self.gem_grid.grid[y2][x2].origin
            self.gem_grid.grid[y1][x1].set_target(*o2)
            self.gem_grid.grid[y2][x2].set_target(*o1)
        self.animate_loop()

    def change(self, removals: list, bonuses: list, additions: list, moving_gems: list):
        self.explode(removals)
        self.add_bonuses(bonuses)
        self.remove(removals)
        self.add(additions)
        self.move(moving_gems)

if __name__ == '__main__':
    gui = GUI(*rand())
    '''
    for i, j in product(range(PUZZLE_ROWS), range(PUZZLE_COLUMNS)):
        time.sleep(1)
        if j % 2 is 0:
            gui.change([(i, j, 0, 0, 0)], [], [], []) # remove
        else:
            gui.change([], [(i, j, 0, random.randint(1, 3), 0)], [], []) # bonus
    '''
    time.sleep(1)
    gui.change([(0, j, 0, 0, 0) for j in range(PUZZLE_ROWS)], [], [], [])
    time.sleep(1)
    gui.change([], [], [(0, j, random.randrange(6), random.randrange(4), 0) for j in range(PUZZLE_ROWS)], [])
    swaps = [(i, j, i, j + 1) for j in range(0, PUZZLE_COLUMNS - 1, 2) for i in range(PUZZLE_ROWS)]
    gui.change([], [], [], swaps)
    time.sleep(1)
