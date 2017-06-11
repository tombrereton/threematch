import pygame

import game_utilities as util
from game_state import GameState
from global_variables import HD_SCALE, WINDOW_HEIGHT, WINDOW_WIDTH, GEM_SIZE


class Background(object):
    def __init__(self, game_state: GameState):
        self.score = 000
        self.score_text = None
        self.game_over_text = None
        self.moves_left_text = None
        self.medals_left_text = None
        self.game_over_text_pos = None
        self.gem_images = []
        self.explosions = []
        self.font = pygame.font.Font(None, int(24 * HD_SCALE))
        self.game_state = game_state
        self.background = util.load_background("background.jpg", WINDOW_WIDTH, WINDOW_HEIGHT)
        self.init_text()
        self.init_gem_images()

    def set_game_over_text(self, win: bool = False):
        game_over_font = pygame.font.Font(None, int(60 * HD_SCALE))
        if win:
            self.game_over_text = game_over_font.render("You Win!", 1, (10, 10, 10))
        else:
            self.game_over_text = game_over_font.render("Game Over", 1, (10, 10, 10))
        self.game_over_text_pos = self.game_over_text.get_rect(centery=WINDOW_HEIGHT / 2, centerx=WINDOW_WIDTH / 2)

    def set_moves_left(self):
        moves_left = self.game_state.moves_left
        self.moves_left_text = self.font.render("Moves Left: {}".format(moves_left), 1, (10, 10, 10))

    def set_medals_left(self):
        medals_left = self.game_state.medals_left
        self.medals_left_text = self.font.render("Medals Left: {}".format(medals_left), 1, (10, 10, 10))

    def init_text(self):
        self.set_moves_left()
        self.set_medals_left()
        temp_text = 'Score: {:03.0f}'.format(self.score)
        self.score_text = self.font.render(temp_text, 1, (10, 10, 10))
        self.game_over_text = self.font.render("", 1, (10, 10, 10))
        self.game_over_text_pos = self.game_over_text.get_rect(centery=WINDOW_HEIGHT / 2, centerx=WINDOW_WIDTH / 2)

    def update_score(self, points: int):
        self.score += points
        temp_text = 'Score: {:03.0f}'.format(self.score)
        self.score_text = self.font.render(temp_text, 1, (10, 10, 10))

    def init_gem_images(self):
        for i in range(1, 5):
            type_list = []
            for j in range(1, 7):
                name = f'stones/Stone_0{j}_0{i}.png'
                image = util.load_image_only(name, GEM_SIZE)
                type_list.append(image)
            self.gem_images.append(type_list)

    def init_explosions(self):
        for i in range(10):
            name = f'explosions/black_smoke/blackSmoke0{i}.png'
            image = util.load_image_only(name, GEM_SIZE)
            self.explosions.append(image)
