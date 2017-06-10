import gemgrid
import icegrid
import medalgrid


class Board(object):
    """
    The game board which is a composition class
    of BearGrid, GemGrid, and IceGrid.
    It is the wrapper class which should be used in the three match
    game to interact with the ice, gems, and bears

    This class will then talk to wrapped classes and update them
    as needed.
    """

    def __init__(self, screen, background, rows: int, columns: int, cell_size: int, margin: int):
        self.medal_grid = medalgrid.MedalGrid(screen, rows, columns, cell_size, margin)
        self.ice_grid = icegrid.IceGrid(screen, rows, columns, cell_size, margin)
        self.gem_grid = gemgrid.GemGrid(screen, rows, columns, cell_size, margin)
        self.screen = screen
        self.background = background
        self.rows = rows
        self.columns = columns

    def is_ice(self, y_coord: int, x_coord: int):
        """
        Method to evaluate if a position contains ice
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if ice, False if not
        """
        return self.ice_grid.grid[y_coord][x_coord] != 0

    def remove_ice(self, y_coord: int, x_coord: int):
        if self.is_ice(y_coord, x_coord):
            self.ice_grid.removeIce(y_coord, x_coord)

            if self.is_medal(y_coord, x_coord):
                self.set_medals_portion_uncovered(y_coord, x_coord)
                self.free_medals()

    def free_medals(self):
        self.medal_grid.free_medals()

    def set_medals_portion_uncovered(self, y_coord: int, x_coord: int):
        self.medal_grid.grid[y_coord][x_coord].uncovered = True

    def is_medal(self, y_coord: int, x_coord: int):
        """
        Method to evaluate if a position contains a bear
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if a bear, False if not
        """
        return self.medal_grid.grid[y_coord][x_coord] != 0

    def is_medal_uncovered(self, y_coord: int, x_coord: int):
        """
        Method to evaluate if a position contains a visible bear
        :param y_coord: y coordinate to check
        :param x_coord: x coordinate to check
        :return: True if visible and a bear, False if not
        """
        return not self.is_ice(y_coord, x_coord) and self.is_medal(y_coord, x_coord)

    def test_board(self):
        self.gem_grid.test_grid()

    def remove_all(self):
        self.gem_grid.remove_all()

    def new_board(self):
        # generates a random new board
        # create 9x9 candies on board
        pass

    def swap_gems(self, y_coord: int, x_coord: int, direction: str):
        # call the gemgrid swap class but also checks
        # for ice and bears
        self.gem_grid.swap_gems(y_coord, x_coord, direction)

    def get_gem(self, y_coord: int, x_coord: int):
        return self.gem_grid.get_gem(y_coord, x_coord)

    def get_gem_group(self):
        return gemgrid.gem_group

    def get_ice_group(self):
        return icegrid.ice_group

    def get_medal_group(self):
        return medalgrid.medal_group

    def check_matches(self, initial_clear: bool):
        """
        Finds the location of the horizontal matches.
        Deletes the gems if match greater than 2
        Pulls down new gems
        Repeats until no horizontal matches
        Finds the location of the vertical matches.
        Deletes the gems if match greater than 2
        Pulls down new gems
        Repeats until no horizontal matches
        Repeats entire loop again until no more matches
        :return:
        """
        total_matches = 0
        find_horizontals = True
        find_verticals = True
        while find_horizontals or find_verticals:

            horizontal_match_length = 0
            while horizontal_match_length is not None:
                # check horizontal matches
                row, column, horizontal_match_length = self.gem_grid.get_row_match()

                if horizontal_match_length is not None and horizontal_match_length > 2:
                    find_verticals = True
                    total_matches = total_matches + 1
                    # remove gems
                    for i in range(row, row + 1):
                        for j in range(column, column + horizontal_match_length):
                            self.gem_grid.removegem(i, j)
                            # self.get_gem_group().update()
                            # self.get_gem_group().draw(self.screen)

                            if self.is_ice(i, j) and not initial_clear:
                                self.remove_ice(i, j)

                # pull down new gems
                repeat = True
                while repeat:
                    repeat = self.gem_grid.pull_down()
                find_horizontals = False

            vertical_match_length = 0
            while vertical_match_length is not None:
                # check vertical matches
                row, column, vertical_match_length = self.gem_grid.get_column_match()

                if vertical_match_length is not None and vertical_match_length > 2:
                    find_horizontals = True
                    total_matches = total_matches + 1
                    # remove gems
                    for j in range(column, column + 1):
                        for i in range(row, row + vertical_match_length):
                            self.gem_grid.removegem(i, j)
                            # self.get_gem_group().update()
                            # self.get_gem_group().draw(self.screen)

                            if self.is_ice(i, j) and not initial_clear:
                                self.remove_ice(i, j)

                # pull down new gems
                repeat = True
                while repeat:
                    repeat = self.gem_grid.pull_down()
                find_verticals = False
        return total_matches

    def find_matches(self):
        """
        find all the matches and returns a list of
        tuples where each tuples comprises:
        (row, column, type, bonus_type)
        :return:
        """

        matches = []

        matches = matches + self.gem_grid.get_row_match_2()
        matches = matches + self.gem_grid.get_column_match_2()

        matches = list(set(matches))

        return matches
