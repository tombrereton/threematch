import pygame
import random
import time
import game_utilities as util
from itertools import product
from global_variables import *


# Functions for testing

def print_array(a):
    print('\n'.join(['\t'.join([str(el) for el in row]) for row in a]))


def rand_text(medals=None):
    moves_left = random.randrange(30)
    medals_left = random.randrange(10) if medals is None else len([0 for row in medals for el in row if el == 0])
    score = random.randrange(1000000)
    terminal = True if random.random() < 2 / 3 else False
    win = True if random.random() < 1 / 2 else False
    return moves_left, medals_left, score, terminal, win


def rand():
    gems = [[(random.randrange(5), random.randrange(1), 0) for _ in range(PUZZLE_COLUMNS)] for _ in range(PUZZLE_ROWS)]
    ice = [[random.randint(-1, 1) for _ in range(PUZZLE_COLUMNS)] for _ in range(PUZZLE_ROWS)]
    medals_small = [[random.randint(-1, 0) for _ in range(PUZZLE_COLUMNS // 2)] for _ in range(PUZZLE_ROWS // 2)]
    medals = [[-1] * PUZZLE_COLUMNS for _ in range(PUZZLE_ROWS)]
    for i, j in product(range(len(medals_small)), range(len(medals_small[0]))):
        medals[2 * i][2 * j] = medals_small[i][j]
    return gems, ice, medals, rand_text(medals)


class SpriteGrid:
    """
    Abstract class to hold a grid of sprites.
    """

    def __init__(self, rows: int, columns: int, cell_size: int, margin: int, group, info: list):
        """
        Constructor for the SpriteGrid class.
        :param rows: Number of rows in the game
        :param columns: Number of columns in the game
        :param cell_size: Size of each cell in pixels
        :param margin: Size of the margin in pixels
        :param group: Group that sprites in this grid should go in
        :param info: Information about sprites to be held in grid
        """
        # Set field variables
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.margin = margin
        self.group = group
        # Create blank grid of the correct size
        self.grid = [[-1] * self.columns for _ in range(self.rows)]
        # Populate grid with sprites
        self.new_grid(info)

    def new_grid(self, info: list):
        """
        Method to fill grid with sprites.
        :param info: Information about sprites to be held in grid
        :return: None
        """
        # Remove old sprites from group (if any)
        self.group.empty()
        # Add sprites
        for i, j in product(range(self.columns), range(self.rows)):
            self.add(i, j, info[i][j])

    def add(self, y_coord: int, x_coord: int, info):
        """
        Abstract method to add a sprite to the grid.
        :param y_coord: Y coordinate to add sprite at
        :param x_coord: X coordinate to add sprite at
        :param info: Information about sprite
        :return: None
        """
        raise NotImplementedError("Need to be implemented in sub class.")

    def remove(self, y_coord: int, x_coord: int):
        """
        Removes a sprite from the grid.
        :param y_coord: Y coordinate to remove sprite from
        :param x_coord: X coordinate to remove sprite from
        :return: None
        """
        # Get the sprite from the grid
        sprite = self.grid[y_coord][x_coord]
        # Check if there was a sprite there
        if sprite is not -1:
            # If so remove from sprite group...
            self.group.remove(sprite)
            # ... and remove from grid
            self.grid[y_coord][x_coord] = -1

    def grid_to_pixel(self, y_coord: int, x_coord: int):
        """
        Method to calculate coordinates in pixels from grid coordinates.
        :param y_coord: Grid y coordinate
        :param x_coord: Grid x coordinate
        :return: A tuple of the pixel coordinates (y, x)
        """
        y = self.margin + y_coord * self.cell_size
        x = self.margin + x_coord * self.cell_size
        return y, x


class Gem(pygame.sprite.Sprite):
    """
    Class for the gem sprites.
    """

    def __init__(self, size: int, gem_info: tuple, image_list: list, explosions: list, gem_group):
        # Call to super constructor
        pygame.sprite.Sprite.__init__(self, gem_group)
        # Set field variables
        self.gem_size = size
        self.type, self.bonus_type, self.activation = gem_info
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
        y = int(self.origin[0] + self.i * (self.target[0] - self.origin[0]) / ANIMATION_SCALE)
        x = int(self.origin[1] + self.i * (self.target[1] - self.origin[1]) / ANIMATION_SCALE)
        self.rect.top = y
        self.rect.left = x
        if self.i == ANIMATION_SCALE:
            self.i = 0
            self.origin = self.target


class GemGrid(SpriteGrid):
    """
    Class to hold a grid of gem sprites.
    """

    def __init__(self, rows: int, columns: int, cell_size: int, margin: int, gem_images: list, explosions: list, group, gems: list):
        """
        Constructor for the GemGrid class.
        :param rows: Number of rows in the game
        :param columns: Number of columns in the game
        :param cell_size: Size of each cell in pixels
        :param margin: Size of the margin in pixels
        :param gem_images: Matrix of gem images
        :param explosions: List of explosion images
        :param group: Group that gem sprites should go in
        :param gems: Information about gem sprites to be held in grid
        """
        # Set field variables
        self.gem_images = gem_images
        self.explosions = explosions
        self.gem_size = int(0.9 * cell_size)
        self.centering_offset = int(0.05 * cell_size)
        # Call to super constructor
        super().__init__(rows, columns, cell_size, margin, group, gems)

    def add(self, y_coord: int, x_coord: int, gem_info: tuple):
        """
        Method to add a gem sprite to the grid.
        Implements method required by the superclass.
        :param y_coord: Y coordinate to add gem sprite at
        :param x_coord: X coordinate to add gem sprite at
        :param gem_info: Information about gem sprite (type, bonus_type, activated)
        :return: None
        """
        # Create Gem sprite
        gem = Gem(self.gem_size, gem_info, self.gem_images, self.explosions, self.group)
        # Calculate pixel coordinates it should go at
        y, x = self.grid_to_pixel(y_coord, x_coord)
        # Set correct coordinates
        gem.init_rect(y, x)
        # Add to gem grid
        self.grid[y_coord][x_coord] = gem

    def grid_to_pixel(self, y_coord: int, x_coord: int):
        """
        Method to calculate coordinates in pixels from grid coordinates.
        Overrides method from superclass to offset gems into cells.
        :param y_coord: Grid y coordinate
        :param x_coord: Grid x coordinate
        :return: A tuple of the pixel coordinates (y, x)
        """
        y, x = super().grid_to_pixel(y_coord, x_coord)
        y += self.centering_offset
        x += self.centering_offset
        return y, x


class Ice(pygame.sprite.Sprite):
    """
    Class for the ice sprites
    """

    def __init__(self, size: int, layer: int, ice_group):
        """
        Constructor for the class.
        :param size: Size of the ice sprite
        :param layer: Layers of ice, 0 is thinnest ice
        :param ice_group: Group to put this sprite in
        """
        # Call to super constructor
        pygame.sprite.Sprite.__init__(self, ice_group)
        # Set field variables
        self.layer = layer
        self.ice_layer = "ice/ice_layer_{}.png".format(self.layer)
        self.image, self.rect = util.load_image(self.ice_layer, size)

    def update_image(self, layer: int):
        """
        Method to update this sprites image
        :param layer: New value for how many layers of ice, 0 is thinnest ice
        :return: None
        """
        self.layer = layer
        self.ice_layer = "ice/ice_layer_{}.png".format(self.layer)
        self.image, _ = util.load_image(self.ice_layer, CELL_SIZE)


class IceGrid(SpriteGrid):
    """
    Class to hold a grid of ice sprites.
    """

    def __init__(self, rows: int, columns: int, cell_size: int, margin: int, group, ice: list):
        """
        Constructor for IceGrid class.
        :param rows: Number of rows in the game
        :param columns: Number of columns in the game
        :param cell_size: Size of each cell in pixels
        :param margin: Size of the margin in pixels
        :param group: Group that ice sprites should go in
        :param ice: Information about ice sprites to be held in grid
        """
        # Call to super constructor
        super().__init__(rows, columns, cell_size, margin, group, ice)

    def add(self, y_coord: int, x_coord: int, layer: int):
        """
        Method to add a ice sprite to the grid.
        Implements method required by the superclass.
        :param y_coord: Y coordinate to add ice sprite at
        :param x_coord: X coordinate to add ice sprite at
        :param layer: Layers of ice, 0 is thinnest
        :return: None
        """
        # Check there is meant to be ice at this location
        if layer is not -1:
            # Create Ice sprite
            ice = Ice(self.cell_size, layer, self.group)
            # Calculate pixel coordinates it should go at
            y, x = self.grid_to_pixel(y_coord, x_coord)
            # Set correct coordinates
            ice.rect.left = x
            ice.rect.top = y
            # Add to ice grid
            self.grid[y_coord][x_coord] = ice


class Medal(pygame.sprite.Sprite):
    """
    Class for the medal sprites.
    """

    def __init__(self, size: int, medal_group):
        """
        Constructor for the Medal class.
        :param size: Size of the medal
        :param medal_group: Group to put this sprite in
        """
        # Call to super constructor
        pygame.sprite.Sprite.__init__(self, medal_group)
        # Set field variables
        self.medal_file = "tiles/medal_02_01.png"
        self.image, self.rect = util.load_image(self.medal_file, size)


class MedalGrid(SpriteGrid):
    """
    Class to hold a grid of medal sprites
    """

    def __init__(self, rows: int, columns: int, cell_size: int, margin: int, group, medals: list):
        """
        Constructor for the MedalGrid class.
        :param rows: Number of rows in the game
        :param columns: Number of columns in the game
        :param cell_size: Size of each cell in pixels
        :param margin: Size of the margin in pixels
        :param group: Group that medal sprites should go in
        :param medals: Information about medal sprites to be held in grid
        """
        # Set field variables
        self.medal_size = 2 * cell_size
        # Call to super constructor
        super().__init__(rows, columns, cell_size, margin, group, medals)

    def add(self, y_coord: int, x_coord: int, portion: int):
        """
        Method to add a medal sprite to the grid.
        Implements method required by the superclass.
        :param y_coord: Y coordinate to add medal sprite at
        :param x_coord: X coordinate to add medal sprite at
        :param portion: Portion of the medal, -1 for not a medal, [0, 4) for a medal
        :return: None
        """
        # Check this is the top left of the medal
        if portion is 0:
            # Create Medal sprite
            medal = Medal(self.medal_size, self.group)
            # Calculate pixel coordinates it should go at
            y, x = self.grid_to_pixel(y_coord, x_coord)
            # Set correct coordinates
            medal.rect.left = x
            medal.rect.top = y
            # Add to medal grid
            self.grid[y_coord][x_coord] = medal


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
        self.gem_grid = GemGrid(PUZZLE_ROWS, PUZZLE_COLUMNS, CELL_SIZE, MARGIN, self.bg.gem_images, self.bg.explosions, self.gem_group, gems)
        self.ice_group = pygame.sprite.Group()
        self.ice_grid = IceGrid(PUZZLE_ROWS, PUZZLE_COLUMNS, CELL_SIZE, MARGIN, self.ice_group, ice)
        self.medal_group = pygame.sprite.Group()
        self.medal_grid = MedalGrid(PUZZLE_ROWS, PUZZLE_COLUMNS, CELL_SIZE, MARGIN, self.medal_group, medals)
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

    def add(self, additions: list):
        for gem in additions:
            self.gem_grid.add(*gem[:2], gem[2:])
            rect = self.gem_grid.grid[gem[0]][gem[1]].rect
            y, x = rect.y - CELL_SIZE, rect.x
            self.gem_grid.grid[gem[0]][gem[1]].set_rect(y, x)
            self.gem_grid.grid[gem[0]][gem[1]].set_origin(y, x)
        self.draw()

    def move(self, moving_gems: list):
        for coord1, coord2 in moving_gems:
            self.gem_grid.grid[coord1[0]][coord1[1]].set_target(*self.gem_grid.grid_to_pixel(*coord2))
        self.animate_loop()

    def change(self, removals: list, bonuses: list, additions: list, moving_gems: list, ice_broken: list, medals_freed: list, text_info: tuple):
        if len(text_info) is not 0:
            self.bg.set_all(*text_info)
        self.draw()
        self.explode(removals)
        self.break_ice(ice_broken)
        self.remove_medals(medals_freed)
        self.add_bonuses(bonuses)
        self.remove(removals)
        self.add(additions)
        self.move(moving_gems)

# Testing
if __name__ == '__main__':
    gui = GUI(*rand())
    '''
    for i, j in product(range(PUZZLE_ROWS), range(PUZZLE_COLUMNS)):
        time.sleep(1)
        if j % 2 is 0:
            gui.change([(i, j, 0, 0, 0)], [], [], [], [], [], ()) # remove
        else:
            gui.change([], [(i, j, 0, random.randint(1, 3), 0)], [], [], [], [], ()) # bonus
    '''
    time.sleep(1)
    gui.change([(0, j, 0, 0, 0) for j in range(PUZZLE_ROWS)], [], [], [], [], [], ())
    time.sleep(1)
    gui.change([], [], [(0, j, random.randrange(6), random.randrange(4), 0) for j in range(PUZZLE_ROWS)], [], [], [], ())
    swaps = [[(i, j), (i, j + 1)] for j in range(PUZZLE_COLUMNS) for i in range(PUZZLE_ROWS)]
    gui.change([], [], [], swaps, [], [], ())
    time.sleep(1)
    gui.change([], [], [], [], [(i, j, -1) for i, j in product(range(PUZZLE_ROWS), range(PUZZLE_COLUMNS))], [], ())
    time.sleep(1)
    gui.change([], [], [], [], [], [(i, j, 0) for i, j in product(range(PUZZLE_ROWS), range(PUZZLE_COLUMNS))], ())
    time.sleep(1)
    gui.change([], [], [], [], [], [], rand_text())
    time.sleep(1)
