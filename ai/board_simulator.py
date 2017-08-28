from itertools import product

from ai.state_functions import StateParser
from model.game import SimpleBoard


class BoardSimulator:
    def __init__(self, level=1):
        self.current_state = ()
        self.level = level
        self.rows = 9
        self.cols = 9
        self.gem_types = 6
        self.current_move = 0
        self.total_medals = None
        self.total_moves = None
        self.parser = StateParser()

    def next_state(self, state, action):
        """
        Takes the game state, and the move to be applied.
        Returns the new game state.
        Move is a list of the gems to swap (r,c,r,c).
        :param state:
        :param action:
        :return:
        """
        gem_grid, ice_grid, medal_grid, moves_medals = state

        board = SimpleBoard(self.rows, self.cols, self.gem_types, self.total_medals)
        board.gem_grid.grid = gem_grid
        board.ice_grid.grid = ice_grid
        board.medal_grid.grid = medal_grid
        medals_uncovered_before_matches = self.count_medals_uncovered(ice_grid, medal_grid)

        board.set_swap_locations(action)
        board.swap_gems()

        while True:
            matches, bonuses = board.find_matches()
            board.match_list = matches
            board.bonuses = bonuses
            board.remove_gems_add_bonuses()

            while True:
                repeat = board.pull_gems_down()
                if not repeat:
                    break

            if len(matches) + len(bonuses) == 0:
                break

        gem_grid = board.gem_grid.grid
        ice_grid = board.ice_grid.grid
        medal_grid = board.medal_grid.grid

        medals_uncovered_after_matches = self.count_medals_uncovered(ice_grid, medal_grid)
        moves_medals = (moves_medals[0] - 1, moves_medals[1] - (medals_uncovered_after_matches - medals_uncovered_before_matches))

        return gem_grid, ice_grid, medal_grid, moves_medals

    def count_medals_uncovered(self, ice_grid, medal_grid):
        """
        Counts how many medal portions are uncovered
        when ice is removed and a medal portion exists.
        :param medal_grid:
        :param ice_grid:
        :param state:
        :return: Returns a state with updated medals uncovered, or same
        """
        medals_uncovered = 0

        # medal_grid = self.medal_portion_search(medal_grid)

        for i, j in product(range(self.rows), range(self.cols)):
            portion = medal_grid[i][j]

            if portion == 0 and self.check_uncovered(i, j, ice_grid, medal_grid):
                medals_uncovered += 1

        return medals_uncovered

    def medal_portion_search(self, medal_grid):
        """
        Looks for a medal portion and fills in the
        remaining portions if not done already.
        :param medal_grid:
        :return: A state with additional medal portions, or the same
        """
        for i, j in product(range(self.rows), range(self.cols)):
            if medal_grid[i][j] != -1:
                row_origin, col_origin = self.get_medal_portion_origin(i, j, medal_grid[i][j])
                medal_grid = self.fill_out_portions(row_origin, col_origin, medal_grid)

        return medal_grid

    def get_medal_portion_origin(self, row, col, portion):

        new_row = (portion // 2 * -1) + row
        new_col = (portion % 2 * -1) + col

        return new_row, new_col

    def fill_out_portions(self, row, col, medal_grid):
        """
        fills out medal grid with portions
        :param row:
        :param col:
        :param medal_grid:
        :return: returns a grid with additional medal portions
        """

        for i, j in product(range(2), range(2)):
            portion = i * 2 + j
            medal_grid[row + i][col + j] = portion

        return medal_grid

    def check_uncovered(self, row, col, ice_grid, medal_grid):
        """
        Checks if no ice is covering any portions of a medal which has medal portion 0
        at location 'row, col'.
        :param row:
        :param col:
        :param ice_grid:
        :param medal_grid:
        :return:
        """
        for i, j in product(range(2), range(2)):
            if ice_grid[row + i][col + j] != -1 or medal_grid[row + i][col + j] == -1:
                return False
        return True
