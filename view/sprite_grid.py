from itertools import product

from view.gui_variables import GUIVariables


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
        self.grid = None
        # Populate grid with sprites
        self.new_grid(info)

    def new_grid(self, info: list):
        """
        Method to fill grid with sprites.
        :param info: Information about sprites to be held in grid
        :return: None
        """
        # Create blank grid of the correct size
        self.grid = [[-1] * self.gui_vars.columns for _ in range(self.gui_vars.rows)]
        # Remove old sprites from group (if any)
        self.group.empty()
        # Add sprites
        for i, j in product(range(self.gui_vars.rows), range(self.gui_vars.columns)):
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
