import random

import pygame

import game_utilities as util
from global_variables import GEM_SIZE, ANIMATION_SCALE, EXPLOSION_FRAMES
from grid import Grid

gem_group = pygame.sprite.Group()

names = ['stones/Stone_0{}_05.png']


class Gem(pygame.sprite.Sprite):
    def __init__(self, size: int, image_list: list, explosions: list):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, gem_group)
        self.gem_size = size
        self.type = random.randint(0, 2)
        self.bonus_type = 0
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

    def test_gem(self, size: int, type: int):
        self.type = type
        test_gem = "stones/Stone_0{}_01.png".format(type)
        self.image, self.rect = util.load_image(test_gem, size)

    # Functions to test animations

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
        y = int(self.origin[0] + self.i * (self.target[0] - self.origin[0]) / (ANIMATION_SCALE))
        x = int(self.origin[1] + self.i * (self.target[1] - self.origin[1]) / (ANIMATION_SCALE))
        self.rect.top = y
        self.rect.left = x
        if self.i == ANIMATION_SCALE:
            self.i = 0
            self.origin = self.target


class GemGrid(Grid):
    """
    Sub class of Grid
    """

    def __init__(self, screen, background, rows: int, columns: int, cell_size: int, margin: int):
        self.background = background
        self.gem_images = background.gem_images
        self.explosions = background.explosions
        self.gem_size = GEM_SIZE
        self.centering_offset = 0.05 * self.gem_size
        super().__init__(screen, rows, columns, cell_size, margin)

    def test_grid(self):
        for j in range(0, self.columns):
            for i in range(0, self.rows):
                gem = Gem(self.gem_size, self.gem_images, self.explosions)
                gem.test_gem(self.gem_size, (j % 6) + 1)
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
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.add_gem(i, j)

    def add_gem(self, y_coord: int, x_coord: int):
        """
        Method to add a gem to the grid
        :param y_coord: y coordinate to add gem at
        :param x_coord: x coordinate to add gem at
        :return: None
        """
        gem = Gem(self.gem_size, self.gem_images, self.explosions)
        x = self.margin + self.centering_offset + x_coord * self.cell_size
        y = self.margin + self.centering_offset + y_coord * self.cell_size
        gem.init_rect(y, x)
        self.grid[y_coord][x_coord] = gem

    def remove_gem(self, y_coord: int, x_coord: int):
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
                gem = Gem(self.gem_size, self.gem_images, self.explosions)
                y = self.margin + self.centering_offset - self.cell_size
                x = self.margin + self.centering_offset + i * self.cell_size
                gem.init_rect(int(y), int(x))
                gem.set_target(int(y + self.cell_size), int(x))
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
        used_bonus_list = []

        # add first gem if it is a bonus
        if self.grid[i][j].bonus_type > 0:
            used_bonus_list.append((self.get_gem_info(i, j)))

        # check if its a match
        while match_index < self.columns and self.grid[i][j].type == self.grid[i][match_index].type:

            # if bonus, add to used bonus list
            if self.grid[i][match_index].bonus_type > 0:
                used_bonus_list.append(self.get_gem_info(i, match_index))

            row_count = row_count + 1
            match_index = match_index + 1
        return row_count, used_bonus_list

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
        used_bonus_list = []

        # add first gem if it is a bonus
        if self.grid[i][j].bonus_type > 0:
            used_bonus_list.append((self.get_gem_info(i, j)))

        while match_index < self.rows and self.grid[i][j].type == self.grid[match_index][j].type:

            # if bonus, add to used bonus list
            if self.grid[match_index][j].bonus_type > 0:
                used_bonus_list.append(self.get_gem_info(match_index, j))

            column_count = column_count + 1
            match_index = match_index + 1
        return column_count, used_bonus_list

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
                row_match_count, _ = self.row_match_count(row, column)
                if row_match_count >= 3:
                    return row, column, row_match_count

        return None, None, None

    def get_row_match_2(self, swap_locations: list):
        """
        check for matching gems in rows
        :param swap_locations:
        :param gemgrid:
        :param rows:
        :param columns:
        :return:
        """
        matches = []
        bonuses = []
        for row in range(self.rows):
            column = 0
            while column < self.columns:
                row_match_count, used_bonus_list = self.row_match_count(row, column)
                if row_match_count >= 3:

                    if len(used_bonus_list) > 0:

                        for r, c, type, bonus_type in used_bonus_list:
                            if bonus_type == 3:
                                # append matches to dictionary
                                matches = matches + (self.get_coord_list(row, column, row_match_count, 0))

                                # diamond bonus, remove 9 surrounding gems
                                for i in range(r - 1, (r + 2) % self.rows):
                                    for j in range(c - 1, (c + 2) % self.columns):
                                        matches.append(self.get_gem_info(i, j))

                            if bonus_type == 1:
                                # if bonus of type 1, remove row
                                for col in range(self.columns):
                                    matches.append(self.get_gem_info(row, col))

                    elif row_match_count == 4:
                        self.row_match_4_bonus(bonuses, column, matches, row, swap_locations)
                    else:
                        # append matches to dictionary
                        matches = matches + (self.get_coord_list(row, column, row_match_count, 0))

                    # add row_match_count to column to avoid duplicates
                    column = column + row_match_count

                else:
                    column = column + 1

        # return dictionary after looping over all row matches
        return matches, bonuses

    def row_match_4_bonus(self, bonuses, column, matches, row, swap_locations):
        """
        Determines the locations of any bonuses for a match 4
        :param bonuses:
        :param column:
        :param matches:
        :param row:
        :param swap_locations:
        :return:
        """
        bonus = None
        for i in range(column, column + 4):
            # add swap location to bonus list
            if (row, i) == swap_locations[0]:
                bonus = self.get_gem_info(row, i, 1)
                bonuses.append(bonus)
            elif (row, i) == swap_locations[1]:
                bonus = self.get_gem_info(row, i, 1)
                bonuses.append(bonus)
            else:
                # if not swap location, add to match list
                gem = self.get_gem_info(row, i)
                matches.append(gem)
        if bonus is None:
            # if swap location doesnt match, add first point
            matches.pop(0)
            bonus = self.get_gem_info(row, column, 1)
            bonuses.append(bonus)

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
                column_match_count, _ = self.column_match_count(row, column)
                if column_match_count >= 3:
                    return row, column, column_match_count
        return None, None, None

    def get_column_match_2(self, swap_locations: list):
        """
        check for matching gems in columns
        :param swap_locations:
        :return:
        """
        matches = []
        bonuses = []
        for column in range(self.columns):
            row = 0
            while row < self.rows:
                column_match_count, used_bonus_list = self.column_match_count(row, column)
                if column_match_count >= 3:

                    if len(used_bonus_list) > 0:

                        for r, c, type, bonus_type in used_bonus_list:

                            if bonus_type == 3:
                                # append matches to dictionary
                                matches = matches + self.get_coord_list(row, column, 0, column_match_count)

                                # diamond bonus, remove 9 surrounding gems
                                for i in range(r - 1, (r + 2) % self.rows):
                                    for j in range(c - 1, (c + 2) % self.columns):
                                        matches.append(self.get_gem_info(i, j))

                            if bonus_type == 1:
                                # if bonus of type 1, remove column
                                for r in range(self.rows):
                                    matches.append(self.get_gem_info(r, column))

                    elif column_match_count == 4:
                        # get bonuses for 4 in a row
                        self.column_match_4_bonus(bonuses, column, matches, row, swap_locations)

                    else:
                        # append matches to dictionary
                        matches = matches + self.get_coord_list(row, column, 0, column_match_count)

                    # add column_match_count to column to avoid duplicates
                    row = row + column_match_count
                else:
                    row = row + 1

        # return dictionary after looping over all row matches
        return matches, bonuses

    def column_match_4_bonus(self, bonuses, column, matches, row, swap_locations):
        """
        Determines location for bonuses and normal matches
        :param bonuses:
        :param column:
        :param matches:
        :param row:
        :param swap_locations:
        :return:
        """

        bonus = None
        for i in range(row, row + 4):
            # add swap location to bonus list
            if (i, column) == swap_locations[0]:
                bonus = self.get_gem_info(i, column, 1)
                bonuses.append(bonus)
            elif (i, column) == swap_locations[1]:
                bonus = self.get_gem_info(i, column, 1)
                bonuses.append(bonus)
            else:
                # if not swap location, add to match list
                gem = self.get_gem_info(i, column)
                matches.append(gem)
        if bonus is None:
            # if swap location doesnt match, add first point
            matches.pop(0)
            bonus = self.get_gem_info(row, column, 1)
            bonuses.append(bonus)

    def get_coord_list(self, y_coord: int, x_coord: int, row_matches: int, col_matches: int):
        matches = []

        for column in range(x_coord, x_coord + row_matches):
            matches.append((self.get_gem_info(y_coord, column)))

        for row in range(y_coord, y_coord + col_matches):
            matches.append((self.get_gem_info(row, x_coord)))

        return matches

    def get_gem_info(self, y_coord: int, x_coord: int, new_bonus=None):
        """
        Return the coordinates of the gem, along with its
        type and bonus type. This information is returned
        as a tuple. The structure is:
        (row, column, type, bonus_type)
        :param new_bonus:
        :param y_coord:
        :param x_coord:
        :return:
        """
        if new_bonus is None:
            return y_coord, x_coord, self.grid[y_coord][x_coord].type, self.grid[y_coord][x_coord].bonus_type
        else:
            return y_coord, x_coord, self.grid[y_coord][x_coord].type, new_bonus
