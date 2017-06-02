import os, sys
import random
import pygame
from pygame.compat import geterror
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

HD_SCALE = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CANDY_WIDTH = 25  # Width of each shape (pixels).
CANDY_HEIGHT = 25  # Height of each shape (pixels).
PUZZLE_COLUMNS = 9  # Number of columns on the board.
PUZZLE_ROWS = 9  # Number of rows on the board.
MARGIN = 100  # Margin around the board (pixels).
WINDOW_WIDTH = PUZZLE_COLUMNS * CANDY_WIDTH + 2 * MARGIN
WINDOW_HEIGHT = PUZZLE_ROWS * CANDY_HEIGHT + 2 * MARGIN + 75
FONT_SIZE = 36
TEXT_OFFSET = MARGIN + 5

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'resources')


# ============================================
# load functions
# ============================================

def load_image(name, width, height, scale, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.smoothscale(image, (width * scale, height * scale))
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(geterror())
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


# ============================================
# basic sprite
# ============================================
class Candy(pygame.sprite.Sprite):
    def __init__(self):
        # call super constructor
        pygame.sprite.Sprite.__init__(self)
        # generate random candy
        self.random_candy()

    def random_candy(self):
        rand_int = random.randint(1, 8)
        bean_name = "bean{}.png".format(rand_int)
        self.image, self.rect = load_image(bean_name, CANDY_WIDTH,
                                           CANDY_HEIGHT, HD_SCALE)


# ============================================
# create board
# size is 9x9, 81 cells
# ============================================

class Board(object):
    """
    A board of 9 by 9
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width, height = 9, 9
        self.sprites = [[0 for x in range(width)] for y in range(height)]
        self.boardGroup = pygame.sprite.Group

    def add_sprite(self, sprite, x_coord, y_coord):
        self.sprites[x_coord][y_coord] = sprite
        self.boardGroup.add(self.sprites[x_coord][y_coord])

    def remove_sprite(self, x_coord, y_coord):
        self.boardGroup.remove(self.sprites[x_coord][y_coord])
        self.sprites[x_coord][y_coord] = 0

    def get_sprite(self, x_coord, y_coord):
        return self.sprites[x_coord][y_coord]
# ============================================
# locator functions
# ============================================
def getLeftTopOfTile(tileX, tileY):
    left = (tileX * CANDY_WIDTH) + (tileX - 1)
    top = (tileY * CANDY_HEIGHT) + (tileY - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for i in range(0,8):
        for j in range(0,8):
    # for candyX in range(len(board)):
    #     for candyY in range(len(board[0])):
    #         left, top = getLeftTopOfTile(candyX, candyY)
            candyRect = pygame.Rect(board.get_sprite(i,j))
            if candyRect.collidepoint(x, y):
                return board.get_sprite(i,j)
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
    screen = pygame.display.set_mode((HD_SCALE * 450, HD_SCALE * 450))
    pygame.display.set_caption("Bean Crush")

    # create the background
    board = pygame.Surface(screen.get_size())
    board = board.convert()
    board.fill((255, 255, 255))
    screen.blit(board, (0, 0))

    # add the candies
    # candy = Candy()
    board = Board()

    # create 9x9 candies on board
    for i in range(0, 8):
        for j in range(0, 8):
            candy = Candy()
            board.add_sprite(candy, i, j)
            screen.blit(board.get_sprite(i, j).image, (i * 25 * HD_SCALE, j * 25 * HD_SCALE))

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
                spotx = getSpotClicked(board,event.pos[0], event.pos[1])



if __name__ == '__main__':
    main()
