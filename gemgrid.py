import random

import pygame

import game_utilities as util
import global_variables as c
import grid as g

gem_group = pygame.sprite.Group()


class Gem(pygame.sprite.Sprite):
    def __init__(self, size: int):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, gem_group)
        self.type = random.randint(1, 8)
        self.bonus_type = 1
        self.gem_name = "stones/Stone_0{}_05.png".format(self.type)
        self.image, self.rect = util.load_image(self.gem_name, size)
        self.origin = (0, 0)
        self.target = (0, 0)
        self.i = 0

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

    def test_gem(self, size: int, type: int):
        self.type = type
        test_gem = "stones/Stone_0{}_05.png".format(type)
        self.image, self.rect = util.load_image(test_gem, size)

    # Functions to test animations

    def update(self):
        if self.origin != self.target:
            self.move()

    def explode(self):
        """
        if about to be removed, explode gem first
        :return:
        """
        pass

    def move(self):
        self.i += 1
        y = int(self.origin[0] + self.i * (self.target[0] - self.origin[0]) / (c.ANIMATION_SCALE - 1))
        x = int(self.origin[1] + self.i * (self.target[1] - self.origin[1]) / (c.ANIMATION_SCALE - 1))
        self.rect.top = y
        self.rect.left = x
        if self.i == c.ANIMATION_SCALE - 1:
            self.i = 0
            self.origin = self.target


class GemGrid(g.Grid):
    """
    Sub class of Grid
    """

    def __init__(self, screen: pygame.display, rows: int, columns: int, cell_size: int, margin: int):
        super().__init__(screen, rows, columns, cell_size, margin)

    def test_grid(self):
        for j in range(0, self.columns):
            for i in range(0, self.rows):
                gem = Gem(self.gem_size)
                gem.test_gem(self.gem_size, (j % 8) + 1)
                y = self.margin + self.centering_offset + i * self.cell_size
                x = self.margin + self.centering_offset + j * self.cell_size
                gem.set_rect(y, x)
                self.grid[i][j] = gem

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
        gem.init_rect(y, x)
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

    def remove_all(self):
        """
        Method to remove all gems from grid and group
        :return:
        """
        for i in range(self.rows):
            for j in range(self.columns):
                gem_group.remove(self.grid[i][j])
                self.grid[i][j] = 0

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
        # gem_clicked.rect.move_ip(0, -self.cell_size)
        # gem_above.rect.move_ip(0, self.cell_size)
        gem_above.target, gem_clicked.target = gem_clicked.target, gem_above.target

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
        # gem_clicked.rect.move_ip(0, self.cell_size)
        # gem_below.rect.move_ip(0, -self.cell_size)
        gem_below.target, gem_clicked.target = gem_clicked.target, gem_below.target

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
        # gem_clicked.rect.move_ip(self.cell_size, 0)
        # gem_right.rect.move_ip(-self.cell_size, 0)
        gem_right.target, gem_clicked.target = gem_clicked.target, gem_right.target

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
        # gem_clicked.rect.move_ip(-self.cell_size, 0)
        # gem_left.rect.move_ip(self.cell_size, 0)
        gem_left.target, gem_clicked.target = gem_clicked.target, gem_left.target

        # swap gems in gem grid
        self.grid[y_coord][x_coord], self.grid[y_coord][x_coord - 1] = self.grid[y_coord][x_coord - 1], \
                                                                       self.grid[y_coord][x_coord]

    def pull_down(self):
        repeat = False
        for i in range(self.columns):
            for j in range(self.rows - 1, 0, -1):
                if self.grid[j][i] == 0:
                    repeat = True
                    self.grid[j][i], self.grid[j - 1][i] = self.grid[j - 1][i], 0
                    if self.grid[j][i] != 0:
                        y = self.margin + self.centering_offset + j * self.cell_size
                        x = self.margin + self.centering_offset + i * self.cell_size
                        self.grid[j][i].set_target(y, x)
            if self.grid[0][i] == 0:
                gem = Gem(self.gem_size)
                y = self.margin + self.centering_offset - self.cell_size
                x = self.margin + self.centering_offset + i * self.cell_size
                gem.init_rect(y, x)
                gem.set_target(y + self.cell_size, x)
                self.grid[0][i] = gem
        return repeat

    def row_match_count(self, i: int, j: int):
        """
        rows match count
        :param gemgrid:
        :param i:
        :param j:
        :param columns:
        :return:
        """
        row_count = 1
        match_index = j + row_count
        while match_index < self.columns and self.grid[i][j].type == self.grid[i][match_index].type:
            row_count = row_count + 1
            match_index = match_index + 1
        return row_count

    def column_match_count(self, i: int, j: int):
        """
        columns match count
        :param gemgrid:
        :param i:
        :param j:
        :param rows:
        :return:
        """
        column_count = 1
        match_index = i + column_count
        while match_index < self.rows and self.grid[i][j].type == self.grid[match_index][j].type:
            column_count = column_count + 1
            match_index = match_index + 1
        return column_count

    def get_row_match(self):
        """
        check for matching gems in rows
        :param gemgrid:
        :param rows:
        :param columns:
        :return:
        """
        for row in range(self.rows):
            for column in range(self.columns):
                row_match_count = self.row_match_count(row, column)
                if row_match_count >= 3:
                    return row, column, row_match_count

        return None, None, None

    def get_row_match_2(self):
        """
        check for matching gems in rows
        :param gemgrid:
        :param rows:
        :param columns:
        :return:
        """
        matches = []
        column = 0
        for row in range(self.rows):
            while column < self.columns:
                row_match_count = self.row_match_count(row, column)
                if row_match_count >= 3:
                    # append matches to dictionary
                    matches = matches + (self.get_coord_list(row, column, row_match_count, 0))

                    # add row_match_count to column to avoid duplicates
                    column = column + row_match_count

        # return dictionary after looping over all row matches
        return matches

    def get_column_match(self):
        """
        check for matching gems in columns
        :param gemgrid:
        :param row:
        :param columns:
        :return:
        """
        for column in range(self.columns):
            for row in range(self.rows):
                column_match_count = self.column_match_count(row, column)
                if column_match_count >= 3:
                    return row, column, column_match_count
        return None, None, None

    def get_column_match_2(self):
        """
        check for matching gems in columns
        :param gemgrid:
        :param row:
        :param columns:
        :return:
        """
        matches = []
        row = 0
        for column in range(self.columns):
            while row < self.rows:
                column_match_count = self.column_match_count(row, column)
                if column_match_count >= 3:
                    # append matches to dictionary
                    matches = matches + self.get_coord_list(row, column, 0, column_match_count)

                    # add column_match_count to column to avoid duplicates
                    row = row + column_match_count

        # return dictionary after looping over all row matches
        return matches

    def get_coord_list(self, y_coord: int, x_coord: int, row_matches: int, col_matches: int):
        matches = []

        for column in range(x_coord, x_coord + row_matches):
            matches.append((self.get_gem_info(y_coord, column)))

        for row in range(y_coord, y_coord + col_matches):
            # TODO check if this correctly appends a tuple
            matches.append((self.get_gem_info(row, x_coord)))

        return matches

    def get_gem_info(self, y_coord: int, x_coord: int):
        """
        Return the coordinates of the gem, along with its
        type and bonus type. This information is returned
        as a dictionary
        :param y_coord:
        :param x_coord:
        :return:
        """

        return y_coord, x_coord, self.grid[y_coord][x_coord].type, self.grid[y_coord][x_coord].bonus_type
