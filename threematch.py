import pygame
from pygame.locals import *

import board as b

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# ============================================
# Global Constants
# ============================================


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HD_SCALE = 2  # Scale for changing the number of pixels
CELL_SIZE = 25 * HD_SCALE  # Width of each shape (pixels).
PUZZLE_ROWS = 9  # Number of rows on the board.
PUZZLE_COLUMNS = 9  # Number of columns on the board.
MARGIN = 100 * HD_SCALE  # Margin around the board (pixels).
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
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    # create the board
    board = b.Board(screen, PUZZLE_ROWS, PUZZLE_COLUMNS, CELL_SIZE)


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
