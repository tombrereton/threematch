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

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# ============================================
# Global Constants
# ============================================


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HD_SCALE = 1  # Scale for changing the number of pixels
CELL_SIZE = int(30 * HD_SCALE)  # Width of each shape (pixels).
PUZZLE_ROWS = 9  # Number of rows on the board.
PUZZLE_COLUMNS = 9  # Number of columns on the board.
MARGIN = int(70 * HD_SCALE)  # Margin around the board (pixels).
WINDOW_WIDTH = PUZZLE_COLUMNS * CELL_SIZE + 2 * MARGIN
WINDOW_HEIGHT = PUZZLE_ROWS * CELL_SIZE + 2 * MARGIN + 75


# FONT_SIZE = 36
# TEXT_OFFSET = MARGIN + 5


# ============================================
# locator functions
# ============================================
def getLeftTopOfTile(tileX, tileY):
    left = (tileX * CELL_SIZE) + (tileX - 1)
    top = (tileY * CELL_SIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for i in range(0, 8):
        for j in range(0, 8):
            # for candyX in range(len(board)):
            #     for candyY in range(len(board[0])):
            #         left, top = getLeftTopOfTile(candyX, candyY)
            candyRect = pygame.Rect(board.get_sprite(i, j))
            if candyRect.collidepoint(x, y):
                return board.get_sprite(i, j)
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
        moves_left_text = font.render("Moves Left: 16", 1, (10, 10, 10))
        score_text = font.render("Score: 000", 1, (10, 10, 10))
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
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                spotx = getSpotClicked(background, event.pos[0], event.pos[1])


if __name__ == '__main__':
    main()
