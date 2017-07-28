from itertools import product

from ai.move_finder import moves_three
from ai.state_parser import StateParser
from model.game import Grid
from model.game import SimpleBoard


# TODO: update score when going to next state
# TODO: keep track of the next state which is sampled from the game logic

class PseudoBoard:
    def __init__(self):
        self.current_state = ()
        self.rows = 9
        self.cols = 9
        self.gem_types = 6
        self.total_medals = 3
        self.current_move = 0
        self.total_moves = 20
        self.parser = StateParser()

    def __str__(self):
        gem_grid, ice_grid, medal_grid, score_medals = self.state_to_grid(self.current_state)
        b = SimpleBoard(self.rows, self.cols, self.gem_types, self.total_medals)
        b.gem_grid.grid = gem_grid
        b.ice_grid.grid = ice_grid
        b.medal_grid.grid = medal_grid

        s = f'Score, medals: {score_medals}\n' + b.__str__()
        return s

    def first_state(self, file_index):
        # Returns a representation of the starting state of the game.
        state = self.parser.get_state(file_index, 0)
        return state

    def get_state_from_data(self, file_index, state_index):
        state = self.parser.get_state(file_index, state_index)
        return state

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        pass

    def next_state(self, state, action):
        """
        Takes the game state, and the move to be applied.
        Returns the new game state.
        Move is a list of the gems to swap (r,c,r,c).
        :param state:
        :param action:
        :return:
        """
        gem_grid, ice_grid, medal_grid, score_medals_init = self.state_to_grid(state)

        board = SimpleBoard(self.rows, self.cols, self.gem_types, self.total_medals)
        board.gem_grid.grid = gem_grid
        board.ice_grid.grid = ice_grid
        board.medal_grid.grid = medal_grid

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

        medals_uncovered = self.count_medals_uncovered(ice_grid, medal_grid)
        score_medals = [score_medals_init[0], medals_uncovered]

        next_state = self.grid_to_state(gem_grid, ice_grid, medal_grid, score_medals)

        return next_state

    def legal_moves(self, state):
        """
        Takes in a state, converts it to grids, and returns a list of legal moves
        where each item is 2 coordinates.
        item = ((r1,c1),(r2,c2))
        :param state:
        :return:
        """
        gem_grid, _, _, _ = self.state_to_grid(state)
        legal_moves = moves_three(gem_grid)
        return legal_moves

    def is_winner(self, state):
        """
        takes in the state and checks if the medals uncovered
        is equal to the total medals for the level.
        :param state:
        :return: 2 for win, 1 for loss, 0 for ongoing
        """
        moves_left = state[9][0]
        medals_left = state[9][1]
        if medals_left == 0:
            return 1
        elif moves_left == 0:
            return -1
        else:
            return 0

    def state_to_grid(self, state):
        """
        converts the state (t,bt,i,mp) to 3 grids
        :param state:
        :return:
        """
        gem_grid = Grid(self.rows, self.cols)
        ice_grid = Grid(self.rows, self.cols)
        medal_grid = Grid(self.rows, self.cols)

        for i, j in product(range(self.rows), range(self.cols)):
            # get = (type, bonus_type)
            act = 0
            gem = (state[i][j][0], state[i][j][1], act)
            ice = state[i][j][2]
            medal_portion = state[i][j][3]

            gem_grid.grid[i][j] = gem
            ice_grid.grid[i][j] = ice
            medal_grid.grid[i][j] = medal_portion

        score_medals = state[9]

        return gem_grid.grid, ice_grid.grid, medal_grid.grid, score_medals

    def grid_to_state(self, gem_grid, ice_grid, medal_grid, score_medals):
        """
        converts the 3 grids into a state
        :param score_medals:
        :param gem_grid:
        :param ice_grid:
        :param medal_grid:
        :return:
        """
        grid = Grid(self.rows, self.cols)

        for i, j in product(range(self.rows), range(self.cols)):
            item = (gem_grid[i][j][0],
                    gem_grid[i][j][1],
                    ice_grid[i][j],
                    medal_grid[i][j])
            grid.grid[i][j] = item

        grid.grid.append(score_medals)
        state = tuple(map(tuple, grid.grid))
        return state

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

    def get_medal_portion_origin(self, row, col, portion):

        new_row = (portion // 2 * -1) + row
        new_col = (portion % 2 * -1) + col

        return new_row, new_col

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

        medal_grid = self.medal_portion_search(medal_grid)

        for i, j in product(range(self.rows), range(self.cols)):
            portion = medal_grid[i][j]

            if portion == 0 and self.check_uncovered(i, j, ice_grid, medal_grid):
                medals_uncovered += 1

        return medals_uncovered

    def check_uncovered(self, row, col, ice_grid, medal_grid):
        for i, j in product(range(2), range(2)):
            if ice_grid[row + i][col + j] != -1 or medal_grid[row + i][col + j] == -1:
                return False
        return True


if __name__ == '__main__':
    # get initial state
    s = PseudoBoard()
    cs = s.get_state_from_data(2, 16)
    s.current_state = cs
    print(s)

    # get legal moves
    legal_moves = s.legal_moves(cs)

    # get next state from move 23
    move = legal_moves[23]
    ns = s.next_state(cs, move)
    print(s.is_winner(ns))
