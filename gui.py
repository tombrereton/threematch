import random
from itertools import product

import pygame
import logging

import game_utilities as util
from events import UpdateBagEvent, EventManager
from update_bag import UpdateBag
import global_variables as gv
from gui_variables import GUIVariables

logging.basicConfig(level=logging.DEBUG)

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
    rows = gv.PUZZLE_ROWS
    columns = gv.PUZZLE_COLUMNS
    gems = [[(random.randrange(5), random.randrange(1), 0) for _ in range(columns)] for _ in range(rows)]
    ice = [[random.randint(-1, 1) for _ in range(columns)] for _ in range(rows)]
    medals_small = [[random.randint(-1, 0) for _ in range(columns // 2)] for _ in range(rows // 2)]
    medals = [[-1] * columns for _ in range(rows)]
    for i, j in product(range(len(medals_small)), range(len(medals_small[0]))):
        medals[2 * i][2 * j] = medals_small[i][j]
    return gems, ice, medals, rand_text(medals)


class SpriteGrid:
    """
    Abstract class to hold a grid of sprites.
    """

    def __init__(self, gui_vars: GUIVariables, group, info: list):
        """
        Constructor for the SpriteGrid class.
        :param group: Group that sprites in this grid should go in
        :param info: Information about sprites to be held in grid
        """
        # Set field variables
        self.gui_vars = gui_vars
        self.group = group
        # Create blank grid of the correct size
        self.grid = [[-1] * self.gui_vars.columns for _ in range(self.gui_vars.rows)]
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
        for i, j in product(range(self.gui_vars.columns), range(self.gui_vars.rows)):
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
        y = self.gui_vars.margin + y_coord * self.gui_vars.cell_size
        x = self.gui_vars.margin + x_coord * self.gui_vars.cell_size
        return y, x


class Gem(pygame.sprite.Sprite):
    """
    Class for the gem sprites.
    """

    def __init__(self, gui_vars: GUIVariables, gem_info: tuple, image_list: list, explosions: list, gem_group):
        # Call to super constructor
        pygame.sprite.Sprite.__init__(self, gem_group)
        # Set field variables
        self.gui_vars = gui_vars
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

    def __str__(self):
        return '({}, {}, {})'.format(self.type, self.bonus_type, self.activation)

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
        if self.explosion_step > self.gui_vars.explosion_frames - 1:
            self.is_exploding = False

    def move(self):
        self.i += 1
        y = int(self.origin[0] + self.i * (self.target[0] - self.origin[0]) / self.gui_vars.animation_scale)
        x = int(self.origin[1] + self.i * (self.target[1] - self.origin[1]) / self.gui_vars.animation_scale)
        self.rect.top = y
        self.rect.left = x
        if self.i == self.gui_vars.animation_scale:
            self.i = 0
            self.origin = self.target


class GemGrid(SpriteGrid):
    """
    Class to hold a grid of gem sprites.
    """

    def __init__(self, gui_vars: GUIVariables, gem_images: list, explosions: list, group,
                 gems: list):
        """
        Constructor for the GemGrid class.
        :param gem_images: Matrix of gem images
        :param explosions: List of explosion images
        :param group: Group that gem sprites should go in
        :param gems: Information about gem sprites to be held in grid
        """
        # Set field variables
        self.gem_images = gem_images
        self.explosions = explosions
        # Call to super constructor
        super().__init__(gui_vars, group, gems)

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
        gem = Gem(self.gui_vars, gem_info, self.gem_images, self.explosions, self.group)
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
        y += self.gui_vars.gem_offset
        x += self.gui_vars.gem_offset
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
        self.size = size
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
        self.image, _ = util.load_image(self.ice_layer, self.size)


class IceGrid(SpriteGrid):
    """
    Class to hold a grid of ice sprites.
    """

    def __init__(self, gui_vars: GUIVariables, group, ice: list):
        """
        Constructor for IceGrid class.
        :param group: Group that ice sprites should go in
        :param ice: Information about ice sprites to be held in grid
        """
        # Call to super constructor
        super().__init__(gui_vars, group, ice)

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
            ice = Ice(self.gui_vars.cell_size, layer, self.group)
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

    def __init__(self, gui_vars: GUIVariables, medal_group):
        """
        Constructor for the Medal class.
        :param medal_group: Group to put this sprite in
        """
        # Call to super constructor
        pygame.sprite.Sprite.__init__(self, medal_group)
        # Set field variables
        self.gui_vars = gui_vars
        self.medal_file = "tiles/medal_02_01.png"
        self.image, self.rect = util.load_image(self.medal_file, self.gui_vars.medal_size)


class MedalGrid(SpriteGrid):
    """
    Class to hold a grid of medal sprites
    """

    def __init__(self, gui_vars: GUIVariables, group, medals: list):
        """
        Constructor for the MedalGrid class.
        :param group: Group that medal sprites should go in
        :param medals: Information about medal sprites to be held in grid
        """
        # Call to super constructor
        super().__init__(gui_vars, group, medals)

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
            medal = Medal(self.gui_vars, self.group)
            # Calculate pixel coordinates it should go at
            y, x = self.grid_to_pixel(y_coord, x_coord)
            # Set correct coordinates
            medal.rect.left = x
            medal.rect.top = y
            # Add to medal grid
            self.grid[y_coord][x_coord] = medal


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
        self.medal_group.draw(self.screen)
        self.ice_group.draw(self.screen)
        self.gem_group.draw(self.screen)
        self.screen.blit(self.bg.game_over_text, self.bg.game_over_text_pos)
        pygame.display.flip()

    def animate_loop(self):
        for i in range(self.gui_vars.animation_scale):
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
        self.add_bonuses_fix(update_bag.bonuses)
        self.move_and_add(update_bag.movements, update_bag.additions)
        self.compare(update_bag.gems)

    def notify(self, event):
        if isinstance(event, UpdateBagEvent):
            print(event.update_bag)
            self.change(event.update_bag)

    def compare(self, gems):
        for i, j in product(range(self.gui_vars.rows), range(self.gui_vars.columns)):
            game_gem = gems[i][j]
            gui_gem = self.gem_grid.grid[i][j]
            if (game_gem == -1) and (gui_gem == -1):
                continue
            elif type(game_gem) is tuple and type(gui_gem) is Gem:
                if game_gem[0] != gui_gem.type or game_gem[1] != gui_gem.bonus_type or game_gem[2] != gui_gem.activation:
                    continue
            else:
                logging.warning(f'Comparison failed at: ({i}, {j})')
                logging.warning(f'Game gem: {game_gem}')
                logging.warning(f'GUI gem: {gui_gem}')
