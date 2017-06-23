import pygame

from gui_variables import GUIVariables
from sprite_grid import SpriteGrid


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
