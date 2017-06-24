import pygame

import game_utilities as util
from view.gui_variables import GUIVariables
from view.sprite_grid import SpriteGrid


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
