"""
background image credit:
Designed by Freepik
http://www.freepik.com

asset credit:
1001.com
"""

import pygame
from pygame.locals import *

import board as b
import game_utilities as util
import global_variables as c

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# ============================================
# Global Constants
# ============================================
HD_SCALE = 1.4  # Scale for changing the number of pixels

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CELL_SIZE = int(30 * HD_SCALE)  # Width of each shape (pixels).
MARGIN = int(70 * HD_SCALE)  # Margin around the board (pixels).
TEXT_AREA = int(75 * HD_SCALE)
PUZZLE_ROWS = 9  # Number of rows on the board.
PUZZLE_COLUMNS = 9  # Number of columns on the board.
WINDOW_WIDTH = PUZZLE_COLUMNS * CELL_SIZE + 2 * MARGIN
WINDOW_HEIGHT = PUZZLE_ROWS * CELL_SIZE + 2 * MARGIN + TEXT_AREA


# FONT_SIZE = 36
# TEXT_OFFSET = MARGIN + 5


# ============================================
# locator functions
# ============================================
def getLeftTopOfTile(tile_x, tile_y):
    left = (tile_x * CELL_SIZE) + (tile_x - 1)
    top = (tile_y * CELL_SIZE) + (tile_y - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for i in range(0, PUZZLE_ROWS):
        for j in range(0, PUZZLE_COLUMNS):
            gemRect = pygame.Rect(board.get_gem(i, j).rect)
            if gemRect.collidepoint(x, y):
                c.MOVES_LEFT = c.MOVES_LEFT - 1
                # board.animate_gem_swap(i, j, "up")
                return board.get_gem(i, j).punched()
    return (None)


# ============================================
# event loop
# ============================================


# ============================================
# main
# ============================================
def main():
    """
    Initialising game
    :return:
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Gem Island")

    # create the background
    background, _ = util.load_background("background.jpg", WINDOW_WIDTH, WINDOW_HEIGHT)
    background = background.convert()
    screen.blit(background, (0, 0))

    # Put Text On The Background
    if pygame.font:
        font = pygame.font.Font(None, int(24 * HD_SCALE))
        moves_left_text = font.render("Moves Left: {}".format(c.MOVES_LEFT), 1, (10, 10, 10))
        score_text = font.render("Score: 000", 1, (10, 10, 10))
        game_over_text = ""
        game_over_text = font.render("", 1, (10, 10, 10))
        textpos = game_over_text.get_rect(centery=WINDOW_HEIGHT / 2, centerx=WINDOW_WIDTH / 2)
        screen.blit(moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        screen.blit(score_text, (10, WINDOW_HEIGHT - MARGIN / 3))

    # create the board
    board = b.Board(screen, PUZZLE_ROWS, PUZZLE_COLUMNS, CELL_SIZE, MARGIN)

    # flip the screen after adding everything to it
    pygame.display.flip()

    clock = pygame.time.Clock()

    going = True
    while going:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif c.MOVES_LEFT == 0:
                game_over_font = pygame.font.Font(None, int(60 * HD_SCALE))
                game_over_text = game_over_font.render("Game Over", 1, (10, 10, 10))
                textpos = game_over_text.get_rect(centery=WINDOW_HEIGHT / 2, centerx=WINDOW_WIDTH / 2)
                screen.blit(game_over_text, (textpos))
                # going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                spotx = getSpotClicked(board, event.pos[0], event.pos[1])

        board.get_gem_group().update()
        board.get_ice_group().update()

        # Draw Everything
        screen.blit(background, (0, 0))
        moves_left_text = font.render("Moves Left: {}".format(c.MOVES_LEFT), 1, (10, 10, 10))
        screen.blit(moves_left_text, (10, WINDOW_HEIGHT - MARGIN * 3 / 4))
        screen.blit(score_text, (10, WINDOW_HEIGHT - MARGIN / 3))
        board.get_bear_group().draw(screen)
        board.get_ice_group().draw(screen)
        board.get_gem_group().draw(screen)
        screen.blit(game_over_text, (textpos))
        pygame.display.flip()


if __name__ == '__main__':
    main()
