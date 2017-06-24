import pygame

import game_utilities as util
from view.gui_variables import GUIVariables
from view.sprite_grid import SpriteGrid


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
