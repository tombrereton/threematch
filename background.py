import pygame

from game_state import GameState
from global_variables import HD_SCALE, WINDOW_HEIGHT, WINDOW_WIDTH


class Background(object):
    def __init__(self, game_state: GameState):
        self.background = None
        self.score_text = None
        self.game_over_text = None
        self.moves_left_text = None
        self.game_over_text_pos = None
        self.font = pygame.font.Font(None, int(24 * HD_SCALE))
        self.game_state = game_state

    def set_game_over_text(self):
        game_over_font = pygame.font.Font(None, int(60 * HD_SCALE))
        self.game_over_text = game_over_font.render("Game Over", 1, (10, 10, 10))
        self.game_over_text_pos = self.game_over_text.get_rect(centery=WINDOW_HEIGHT / 2, centerx=WINDOW_WIDTH / 2)

    def set_moves_left(self):
        moves_left = self.game_state.moves_left
        self.moves_left_text = self.font.render("Moves Left: {}".format(moves_left), 1, (10, 10, 10))


MOVES_LEFT = 16