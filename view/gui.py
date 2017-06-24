import logging
import random
from itertools import product

import pygame

import global_variables as gv
from events.event_manager import EventManager
from events.events import UpdateBagEvent
from events.update_bag import UpdateBag
from view.background import Background
from view.gem_grid import Gem
from view.gem_grid import GemGrid
from view.gui_variables import GUIVariables
from view.ice_grid import IceGrid
from view.medal_grid import MedalGrid


# Functions for testing


def print_array(a):
    print('\n'.join(['\t'.join([str(el) for el in row]) for row in a]))


def build_array_string(a):
    return '\n' + '\n'.join([', '.join([str(el) for el in row]) for row in a])


def rand_text(medals=None):
    moves_left = random.randrange(30)
    medals_left = random.randrange(10) if medals is None else len([0 for row in medals for el in row if el == 0])
    score = random.randrange(1000000)
    terminal = True if random.random() < 2 / 3 else False
    win = True if random.random() < 1 / 2 else False
    return moves_left, medals_left, score, terminal, win


def rand():
    rows = gv.PUZZLE_ROWS
    columns = gv.PUZZLE_COLUMNS
    gems = [[(random.randrange(5), random.randrange(1), 0) for _ in range(columns)] for _ in range(rows)]
    ice = [[random.randint(-1, 1) for _ in range(columns)] for _ in range(rows)]
    medals_small = [[random.randint(-1, 0) for _ in range(columns // 2)] for _ in range(rows // 2)]
    medals = [[-1] * columns for _ in range(rows)]
    for i, j in product(range(len(medals_small)), range(len(medals_small[0]))):
        medals[2 * i][2 * j] = medals_small[i][j]
    return gems, ice, medals, rand_text(medals)


class GUI:
    def __init__(self, gui_vars: GUIVariables, gems: list, ice, medals: list, text_info: tuple,
                 event_manager: EventManager):
        self.gui_vars = gui_vars
        pygame.init()
        self.screen = pygame.display.set_mode((self.gui_vars.width, self.gui_vars.height))
        pygame.display.set_caption('Gem Island')
        self.bg = Background(self.gui_vars, *text_info)
        self.gem_group = pygame.sprite.Group()
        self.gem_grid = GemGrid(self.gui_vars, self.bg.gem_images, self.bg.explosions, self.gem_group, gems)
        self.ice_group = pygame.sprite.Group()
        self.ice_grid = IceGrid(self.gui_vars, self.ice_group, ice)
        self.medal_group = pygame.sprite.Group()
        self.medal_grid = MedalGrid(self.gui_vars, self.medal_group, medals)
        self.draw()
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

    def new_state(self, gems: list, ice, medals: list, text_info: tuple):
        self.gem_grid.new_grid(gems)
        self.ice_grid.new_grid(ice)
        self.medal_grid.new_grid(medals)
        self.bg.set_all(*text_info)
        self.draw()

    def draw(self):
        self.screen.blit(self.bg.background, (0, 0))
        self.screen.blit(self.bg.moves_left_text, (10, self.gui_vars.height - self.gui_vars.margin * 3 / 4))
        self.screen.blit(self.bg.medals_left_text, (10, self.gui_vars.height - self.gui_vars.margin * 7 / 6))
        self.screen.blit(self.bg.score_text, (10, self.gui_vars.height - self.gui_vars.margin / 3))

        # TODO: move it appropriate place
        rows = self.gui_vars.rows
        columns = self.gui_vars.columns
        margin = self.gui_vars.margin
        cells = self.gui_vars.cell_size

        for j in range(columns):
            # top border
            self.screen.blit(self.bg.border_top, (margin * 0.78 + j * cells, margin * 0.85))

        for j in range(columns):
            # bottom border
            self.screen.blit(self.bg.border_bottom, (margin * 0.78 + j * cells, margin * 0.84 + rows * cells))
        for i in range(rows):
            # left border
            self.screen.blit(self.bg.border_left, (margin * 0.85, margin * 0.77 + i * cells))

        for i in range(rows):
            # right border
            self.screen.blit(self.bg.border_right, (margin * 0.82 + columns * cells, margin * 0.79 + i * cells))

        # TODO: remove the 'minus 1' and centre gems?
        for i, j in product(range(rows), range(columns)):
            # grid background
            self.screen.blit(self.bg.grid_image_top_left, (margin - 1 + j * cells, margin - 1 + i * cells))

        self.screen.blit(self.bg.moves_left_text, (10, self.gui_vars.height - self.gui_vars.margin * 3 / 4))
        self.screen.blit(self.bg.medals_left_text, (10, self.gui_vars.height - self.gui_vars.margin * 7 / 6))
        self.screen.blit(self.bg.score_text, (10, self.gui_vars.height - self.gui_vars.margin / 3))
        self.medal_group.draw(self.screen)
        self.ice_group.draw(self.screen)
        self.gem_group.draw(self.screen)
        self.screen.blit(self.bg.game_over_text, self.bg.game_over_text_pos)
        pygame.display.flip()

    def animate_loop(self, loop=None):
        loop = self.gui_vars.animation_scale if loop is None else loop
        for i in range(loop):
            # loop the number of times we need to animate given
            # by ANIMATION_SCALE

            # Call the update method on the sprites
            self.gem_group.update()
            self.ice_group.update()
            self.medal_group.update()

            self.draw()

    def explode(self, removals: list):
        if len(removals):
            for i, j, _, _, _ in removals:
                self.gem_grid.grid[i][j].is_exploding = True
            self.animate_loop(self.gui_vars.explosion_frames)

    def break_ice(self, ice_broken: list):
        for i, j, layer in ice_broken:
            if layer is -1:
                self.ice_grid.remove(i, j)
            else:
                if self.ice_grid.grid[i][j] is -1:
                    self.ice_grid.add(i, j, layer)
                else:
                    self.ice_grid.grid[i][j].update_image(layer)
        self.draw()

    def remove_medals(self, medals_freed: list):
        for i, j, _ in medals_freed:
            self.medal_grid.remove(i, j)
        self.draw()

    def add_bonuses(self, bonuses: list):
        for i, j, _, bt, _ in bonuses:
            self.gem_grid.grid[i][j].update_bonus_type(bt)
        self.draw()

    def remove(self, removals: list):
        for i, j, _, _, _ in removals:
            self.gem_grid.remove(i, j)
        self.draw()

    def add_bonuses_fix(self, bonuses: list):
        for i, j, *gem in bonuses:
            if self.gem_grid.grid[i][j] == -1:
                logging.warning(f'Fixed bonus at ({i}, {j}) type: {gem[1]}')
                self.gem_grid.add(i, j, gem)
        self.draw()

    def move_and_add(self, moving_gems: list, additions: list):
        temp = []
        for coord1, coord2 in zip(*moving_gems):
            if coord1[0] == -1:
                continue
            gem = self.gem_grid.grid[coord1[0]][coord1[1]]
            self.gem_grid.grid[coord1[0]][coord1[1]] = -1
            gem.set_target(*self.gem_grid.grid_to_pixel(*coord2[:2]))
            temp.append((coord2, gem))
        for coord2, gem in temp:
            self.gem_grid.grid[coord2[0]][coord2[1]] = gem
        for gem in additions:
            self.gem_grid.add(0, gem[1], gem[2:])
            rect = self.gem_grid.grid[0][gem[1]].rect
            y, x = rect.y - self.gui_vars.cell_size, rect.x
            self.gem_grid.grid[0][gem[1]].set_rect(y, x)
            self.gem_grid.grid[0][gem[1]].set_origin(y, x)
        self.animate_loop()

    def change(self, update_bag: UpdateBag):
        if len(update_bag.info) is not 0:
            self.bg.set_all(*update_bag.info)
        self.draw()
        self.explode(update_bag.removals)
        self.break_ice(update_bag.ice_removed)
        self.remove_medals(update_bag.medals_removed)
        self.add_bonuses(update_bag.bonuses)
        self.remove(update_bag.removals)
        # self.add_bonuses_fix(update_bag.bonuses)
        self.move_and_add(update_bag.movements, update_bag.additions)
        self.compare(update_bag.gems, update_bag)

    def notify(self, event):
        if isinstance(event, UpdateBagEvent):
            self.change(event.update_bag)

    def compare(self, gems, update_bag):
        for i, j in product(range(self.gui_vars.rows), range(self.gui_vars.columns)):
            game_gem = gems[i][j]
            gui_gem = self.gem_grid.grid[i][j]
            if (game_gem == -1) and (gui_gem == -1):
                continue
            elif type(game_gem) is tuple and type(gui_gem) is Gem:
                if game_gem[0] != gui_gem.type or game_gem[1] != gui_gem.bonus_type or \
                                game_gem[2] != gui_gem.activation:
                    continue
            else:
                logging.warning('\n\nFrom model gem grid: \n' + build_array_string(gems))
                logging.warning('\n\nFrom GUI gem grid: \n' + build_array_string(self.gem_grid.grid))
                logging.warning('\n\n' + str(update_bag) + '\n')
                logging.warning('\n\nComparison failed:')
                logging.warning(f'row {i} column {j}')
                logging.warning(game_gem)
                logging.warning(gui_gem)
