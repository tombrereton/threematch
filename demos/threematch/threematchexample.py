import pygame, random, time, sys
from pygame.locals import *
import itertools
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SHAPE_WIDTH = 50                # Width of each shape (pixels).
SHAPE_HEIGHT = 50               # Height of each shape (pixels).
PUZZLE_COLUMNS = 6              # Number of columns on the board.
PUZZLE_ROWS = 12                # Number of rows on the board.
MARGIN = 2                      # Margin around the board (pixels).
WINDOW_WIDTH = PUZZLE_COLUMNS * SHAPE_WIDTH + 2 * MARGIN
WINDOW_HEIGHT = PUZZLE_ROWS * SHAPE_HEIGHT + 2 * MARGIN + 75
FONT_SIZE = 36
TEXT_OFFSET = MARGIN + 5

# Map from number of matches to points scored.
SCORE_TABLE = {0: 0, 1: .9, 2: 3, 3: 9, 4: 27}
MINIMUM_MATCH = 3
EXTRA_LENGTH_POINTS = .1
RANDOM_POINTS = .3
DELAY_PENALTY_SECONDS = 10
DELAY_PENALTY_POINTS = .5

FPS = 30
EXPLOSION_SPEED = 15            # In frames per second.
REFILL_SPEED = 10               # In cells per second.


main_dir = os.path.split(os.path.abspath(__file__))[0]

class Cell(object):
    """
    A cell on the board, with properties:
    `image` -- a `Surface` object containing the sprite to draw here.
    `offset` -- vertical offset in pixels for drawing this cell.
    """
    def __init__(self, image):
        self.offset = 0.0
        self.image = image

    def tick(self, dt):
        self.offset = max(0.0, self.offset - dt * REFILL_SPEED)

class Board(object):
    """
    A rectangular board of cells, with properties:
    `w` -- width in cells.
    `h` -- height in cells.
    `size` -- total number of cells.
    `board` -- list of cells.
    `matches` -- list of matches, each being a list of exploding cells.
    `refill` -- list of cells that are moving up to refill the board.
    `score` -- score due to chain reactions.
    """
    def __init__(self, width, height):
        self.explosion = [pygame.image.load('{}/images/explosionblue0{}.png'.format(main_dir,i))
                          for i in range(1, 5)]
        shapes = 'bean_blue bean_green bean_orange bean_pink bean_purple bean_red bean_white'
        self.shapes = [pygame.image.load('{}/images/{}.png'.format(main_dir, shape))
                       for shape in shapes.split()]
        self.background = pygame.image.load("{}/images/bg.png".format(main_dir))
        self.blank = pygame.image.load("{}/images/blank.png".format(main_dir))
        self.w = width
        self.h = height
        self.size = width * height
        self.board = [Cell(self.blank) for _ in range(self.size)]
        self.matches = []
        self.refill = []
        self.score = 0.0

    def randomize(self):
        """
        Replace the entire board with fresh shapes.
        """
        for i in range(self.size):
            self.board[i] = Cell(random.choice(self.shapes))

    def pos(self, i, j):
        """
        Return the index of the cell at position (i, j).
        """
        assert(0 <= i < self.w)
        assert(0 <= j < self.h)
        return j * self.w + i

    def busy(self):
        """
        Return `True` if the board is busy animating an explosion or a
        refill and so no further swaps should be permitted.
        """
        return self.refill or self.matches

    def tick(self, dt):
        """
        Advance the board by `dt` seconds: move rising blocks (if
        any); otherwise animate explosions for the matches (if any);
        otherwise check for matches.
        """
        if self.refill:
            for c in self.refill:
                c.tick(dt)
            self.refill = [c for c in self.refill if c.offset > 0]
            if self.refill:
                return
        elif self.matches:
            self.explosion_time += dt
            f = int(self.explosion_time * EXPLOSION_SPEED)
            if f < len(self.explosion):
                self.update_matches(self.explosion[f])
                return
            self.update_matches(self.blank)
            self.refill = list(self.refill_columns())
        self.explosion_time = 0
        self.matches = self.find_matches()
        self.score += len(self.matches) * RANDOM_POINTS

    def draw(self, display):
        """
        Draw the board on the pygame surface `display`.
        """
        display.blit(self.background, (0, 0))
        for i, c in enumerate(self.board):
            display.blit(c.image,
                         (MARGIN + SHAPE_WIDTH * (i % self.w),
                          MARGIN + SHAPE_HEIGHT * (i // self.w - c.offset)))

    def swap(self, cursor):
        """
        Swap the two board cells covered by `cursor` and update the
        matches.
        """
        i = self.pos(*cursor)
        b = self.board
        b[i], b[i+1] = b[i+1], b[i]
        self.matches = self.find_matches()

    def find_matches(self):
        """
        Search for matches (lines of cells with identical images) and
        return a list of them, each match being represented as a list
        of board positions.
        """
        def lines():
            for j in range(self.h):
                yield range(j * self.w, (j + 1) * self.w)
            for i in range(self.w):
                yield range(i, self.size, self.w)
        def key(i):
            return self.board[i].image
        def matches():
            for line in lines():
                for _, group in itertools.groupby(line, key):
                    match = list(group)
                    if len(match) >= MINIMUM_MATCH:
                        yield match
        return list(matches())

    def update_matches(self, image):
        """
        Replace all the cells in any of the matches with `image`.
        """
        for match in self.matches:
            for position in match:
                self.board[position].image = image

    def refill_columns(self):
        """
        Move cells downwards in columns to fill blank cells, and
        create new cells as necessary so that each column is full. Set
        appropriate offsets for the cells to animate into place.
        """
        for i in range(self.w):
            target = self.size - i - 1
            for pos in range(target, -1, -self.w):
                if self.board[pos].image != self.blank:
                    c = self.board[target]
                    c.image = self.board[pos].image
                    c.offset = (target - pos) // self.w
                    target -= self.w
                    yield c
            offset = 1 + (target - pos) // self.w
            for pos in range(target, -1, -self.w):
                c = self.board[pos]
                c.image = random.choice(self.shapes)
                c.offset = offset
                yield c

class Game(object):
    """
    The state of the game, with properties:
    `clock` -- the pygame clock.
    `display` -- the window to draw into.
    `font` -- a font for drawing the score.
    `board` -- the board of cells.
    `cursor` -- the current position of the (left half of) the cursor.
    `score` -- the player's score.
    `last_swap_ticks` --
    `swap_time` -- time since last swap (in seconds).
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bejewelled Clone")
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                               DOUBLEBUF)
        self.board = Board(PUZZLE_COLUMNS, PUZZLE_ROWS)
        self.font = pygame.font.Font(None, FONT_SIZE)

    def start(self):
        """
        Start a new game with a random board.
        """
        self.board.randomize()
        self.cursor = [0, 0]
        self.score = 0.0
        self.swap_time = 0.0

    def quit(self):
        """
        Quit the game and exit the program.
        """
        pygame.quit()
        sys.exit()

    def play(self):
        """
        Play a game: repeatedly tick, draw and respond to input until
        the QUIT event is received.
        """
        self.start()
        while True:
            self.draw()
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt
            for event in pygame.event.get():
                if event.type == KEYUP:
                    self.input(event.key)
                elif event.type == QUIT:
                    self.quit()
            self.board.tick(dt)

    def input(self, key):
        """
        Respond to the player pressing `key`.
        """
        if key == K_q:
            self.quit()
        elif key == K_RIGHT and self.cursor[0] < self.board.w - 2:
            self.cursor[0] += 1
        elif key == K_LEFT and self.cursor[0] > 0:
            self.cursor[0] -= 1
        elif key == K_DOWN and self.cursor[1] < self.board.h - 1:
            self.cursor[1] += 1
        elif key == K_UP and self.cursor[1] > 0:
            self.cursor[1] -= 1
        elif key == K_SPACE and not self.board.busy():
            self.swap()

    def swap(self):
        """
        Swap the two cells under the cursor and update the player's score.
        """
        swap_penalties = int(self.swap_time / DELAY_PENALTY_SECONDS)
        self.swap_time = 0.0
        self.board.swap(self.cursor)
        self.score -= 1 + DELAY_PENALTY_POINTS * swap_penalties
        self.score += SCORE_TABLE[len(self.board.matches)]
        for match in self.board.matches:
            self.score += (len(match) - MINIMUM_MATCH) * EXTRA_LENGTH_POINTS

    def draw(self):
        self.board.draw(self.display)
        self.draw_score()
        self.draw_time()
        self.draw_cursor()
        pygame.display.update()

    def draw_time(self):
        s = int(self.swap_time)
        text = self.font.render('Move Timer: {}:{:02}'.format(s / 60, s % 60),
                                True, WHITE)
        self.display.blit(text, (TEXT_OFFSET, WINDOW_HEIGHT - (FONT_SIZE * 2)))

    def draw_score(self):
        total_score = self.score + self.board.score
        text = self.font.render('Score: {}'.format(total_score), True, WHITE)
        self.display.blit(text, (TEXT_OFFSET, WINDOW_HEIGHT - FONT_SIZE))

    def draw_cursor(self):
        topLeft = (MARGIN + self.cursor[0] * SHAPE_WIDTH,
                   MARGIN + self.cursor[1] * SHAPE_HEIGHT)
        topRight = (topLeft[0] + SHAPE_WIDTH * 2, topLeft[1])
        bottomLeft = (topLeft[0], topLeft[1] + SHAPE_HEIGHT)
        bottomRight = (topRight[0], topRight[1] + SHAPE_HEIGHT)
        pygame.draw.lines(self.display, WHITE, True,
                          [topLeft, topRight, bottomRight, bottomLeft], 3)

if __name__ == '__main__':
    Game().play()