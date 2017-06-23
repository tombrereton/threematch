import pygame

import game_utilities as util

from gui_variables import GUIVariables

class Background:
    def __init__(self, gui_vars: GUIVariables, moves_left: int, medals_left: int, score: int,
                 terminal: bool, win: bool):
        self.gui_vars = gui_vars
        self.font = pygame.font.Font(None, int(24 * self.gui_vars.hd_scale))
        self.game_over_font = pygame.font.Font(None, int(60 * self.gui_vars.hd_scale))
        self.moves_left = 0
        self.moves_left_text = None
        self.medals_left = 0
        self.medals_left_text = None
        self.score = 0
        self.score_text = None
        self.game_over_text = None
        self.game_over_text_pos = None

        self.background = util.load_background("stone_light_2.jpg", "ground.png", self.gui_vars.width,
                                               self.gui_vars.height)
        self.grid_image_top_left = util.load_image_only("grid_inner_1.png", self.gui_vars.cell_size, rotate=0)
        self.grid_image_bottom_right = util.load_image_only("grid_inner_2.png", self.gui_vars.cell_size, rotate=0)
        self.border_top = util.load_border("border_2.png", self.gui_vars.cell_size * 2, self.gui_vars.cell_size * 3 / 4)
        self.border_bottom = util.load_border("border_2.png", self.gui_vars.cell_size * 2,
                                              self.gui_vars.cell_size * 3 / 4, rotate=180)
        self.border_left = util.load_border("border_2.png", self.gui_vars.cell_size * 3 / 4,
                                            self.gui_vars.cell_size * 2, rotate=90)
        self.border_right = util.load_border("border_2.png", self.gui_vars.cell_size * 3 / 4,
                                             self.gui_vars.cell_size * 2, rotate=-90)
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
        self.game_over_text_pos = self.game_over_text.get_rect(centery=self.gui_vars.height / 2,
                                                               centerx=self.gui_vars.width / 2)

    def init_gem_images(self):
        for i in range(1, 5):
            type_list = []
            for j in range(1, 7):
                name = f'stones/Stone_0{j}_0{i}.png'
                image = util.load_image_only(name, self.gui_vars.gem_size)
                type_list.append(image)
            self.gem_images.append(type_list)

    def init_explosions(self):
        for i in range(self.gui_vars.explosion_frames):
            back = f'explosions/black_smoke/blackSmoke0{i}.png'
            fore = f'explosions/explosion/explosion0{i}.png'
            image = util.load_explosion(fore, back, self.gui_vars.gem_size)
            self.explosions.append(image)
