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
        centering_offset = 0.05 * self.cell_size
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                gem = Gem(int(0.9 * self.cell_size))
                x = self.margin + centering_offset + j * self.cell_size
                y = self.margin + centering_offset + i * self.cell_size
                gem.rect.left = x
                gem.rect.top = y
                self.grid[i][j] = gem
                self.screen.blit(gem.image, (x, y))

    def addgem(self, gem: Gem, y_coord: int, x_coord: int):
        pass

    def removegem(self, y_coord: int, x_coord: int):
        pass

    def swapgems(self, y_coord: int, x_coord: int, direction: str):
        """
        provide x and y coordinate and direction and
        swap the gem at x and y with the gem in the direction
        of 'direction'
        """
        pass

    def get_gem(self, y_coord: int, x_coord: int):
        """
        returns the rectange of the gem which contains the
        left, top coordinates
        :return:
        """
        return self.grid[y_coord][x_coord]

    def animate_swap(self, y_coord: int, x_coord: int, direction: str):

        # if direction == 'up':
        clicked_gem = self.grid[y_coord][x_coord]
        upper_gem = self.grid[y_coord - 1][x_coord]
        gem_group.remove(clicked_gem)
        gem_group.remove(upper_gem)

        clicked_gem.rect.move_ip(0, -self.cell_size)
        upper_gem.rect.move_ip(0, self.cell_size)
        gem_group.add(clicked_gem)
        gem_group.add(upper_gem)
        self.grid[y_coord][x_coord], self.grid[y_coord - 1][x_coord] = self.grid[y_coord - 1][x_coord], \
                                                                       self.grid[y_coord][x_coord]
        # testing up animation
        # swap gems in new grid
        # remove gems from gem group
        # add new grid to gem group


    def swap_up(self, y_coord: int, x_coord: int):

        # if direction == 'up':
        clicked_gem = self.grid[y_coord][x_coord]
        upper_gem = self.grid[y_coord - 1][x_coord]
        gem_group.remove(clicked_gem)
        gem_group.remove(upper_gem)

        clicked_gem.rect.move_ip(0, -self.cell_size)
        upper_gem.rect.move_ip(0, self.cell_size)
        gem_group.add(clicked_gem)
        gem_group.add(upper_gem)
        self.grid[y_coord][x_coord], self.grid[y_coord - 1][x_coord] = self.grid[y_coord - 1][x_coord], \
                                                                       self.grid[y_coord][x_coord]
