import random

import pygame

import game_utilities as util
import grid as g

gem_group = pygame.sprite.Group()


class Gem(pygame.sprite.Sprite):
    def __init__(self, size: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, gem_group)
        self.type = random.randint(1, 8)
        self.is_bonus = False
        self.gem_name = "stones/Stone_0{}_05.png".format(self.type)
        self.image, self.rect = util.load_image(self.gem_name, size)
        self.dizzy = 0

    # Functions to test animations

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()

    def _spin(self):
        "spin the gem image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


class GemGrid(g.Grid):
    """
    Sub class of Grid
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cell_size: int, margin: int):
        super().__init__(screen, rows, columns, cell_size, margin)

    def new_grid(self):
        """
        override method in Grid class.

        adds the gems to the screen
        :return:
        """
        self.gem_size = int(0.9 * self.cell_size)
        self.centering_offset = 0.05 * self.cell_size
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.addgem(i, j)

    def addgem(self, y_coord: int, x_coord: int):
        """
        Method to add a gem to the grid
        :param y_coord: y coordinate to add gem at
        :param x_coord: x coordinate to add gem at
        :return: None
        """
        gem = Gem(self.gem_size)
        x = self.margin + self.centering_offset + x_coord * self.cell_size
        y = self.margin + self.centering_offset + y_coord * self.cell_size
        gem.rect.left = x
        gem.rect.top = y
        self.grid[y_coord][x_coord] = gem

    def removegem(self, y_coord: int, x_coord: int):
        """
        Method to remove a gem from the grid
        :param y_coord: y coordinate to remove gem from
        :param x_coord: x coordinate to remove gem from
        :return: None
        """
        gem_group.remove(self.grid[y_coord][x_coord])
        self.grid[y_coord][x_coord] = 0

    def get_gem(self, y_coord: int, x_coord: int):
        """
        returns the rectangle of the gem which contains the
        left, top coordinates
        :return:
        """
        return self.grid[y_coord][x_coord]

    def swap_gems(self, y_coord: int, x_coord: int, direction: str):
        """
        provide x and y coordinate and direction and
        swap the gem at x and y with the gem in the direction
        of 'direction'
        :param y_coord:
        :param x_coord:
        :param direction:
        :return:
        """

        if direction == 'up':
            self.swap_up(y_coord, x_coord)
        elif direction == 'down':
            self.swap_down(y_coord, x_coord)
        elif direction == 'right':
            self.swap_right(y_coord, x_coord)
        elif direction == 'left':
            self.swap_left(y_coord, x_coord)

    def swap_up(self, y_coord: int, x_coord: int):
        """
        swaps the clicked gem with the gem above it

        :param y_coord:
        :param x_coord:
        :return:
        """
        # get gems
        gem_clicked = self.grid[y_coord][x_coord]
        gem_above = self.grid[y_coord - 1][x_coord]

        # swap gems in gem group
        gem_clicked.rect.move_ip(0, -self.cell_size)
        gem_above.rect.move_ip(0, self.cell_size)

        # swap gems in gem grid
        self.grid[y_coord][x_coord], self.grid[y_coord - 1][x_coord] = self.grid[y_coord - 1][x_coord], \
                                                                       self.grid[y_coord][x_coord]

    def swap_down(self, y_coord: int, x_coord: int):
        """
        swaps the clicked gem with the gem below it

        :param y_coord:
        :param x_coord:
        :return:
        """
        # get gems
        gem_clicked = self.grid[y_coord][x_coord]
        gem_below = self.grid[y_coord + 1][x_coord]

        # swap gems in gem group
        gem_clicked.rect.move_ip(0, self.cell_size)
        gem_below.rect.move_ip(0, -self.cell_size)

        # swap gems in gem grid
        self.grid[y_coord][x_coord], self.grid[y_coord + 1][x_coord] = self.grid[y_coord + 1][x_coord], \
                                                                       self.grid[y_coord][x_coord]

    def swap_right(self, y_coord: int, x_coord: int):
        """
        swaps the clicked gem with the gem right of it

        :param y_coord:
        :param x_coord:
        :return:
        """
        # get gems
        gem_clicked = self.grid[y_coord][x_coord]
        gem_right = self.grid[y_coord][x_coord + 1]

        # swap gems in gem group
        gem_clicked.rect.move_ip(self.cell_size, 0)
        gem_right.rect.move_ip(-self.cell_size, 0)

        # swap gems in gem grid
        self.grid[y_coord][x_coord], self.grid[y_coord][x_coord + 1] = self.grid[y_coord][x_coord + 1], \
                                                                       self.grid[y_coord][x_coord]

    def swap_left(self, y_coord: int, x_coord: int):
        """
        swaps the clicked gem with the gem left of it

        :param y_coord:
        :param x_coord:
        :return:
        """
        # get gems
        gem_clicked = self.grid[y_coord][x_coord]
        gem_left = self.grid[y_coord][x_coord - 1]

        # swap gems in gem group
        gem_clicked.rect.move_ip(-self.cell_size, 0)
        gem_left.rect.move_ip(self.cell_size, 0)

        # swap gems in gem grid
        self.grid[y_coord][x_coord], self.grid[y_coord][x_coord - 1] = self.grid[y_coord][x_coord - 1], \
                                                                       self.grid[y_coord][x_coord]
