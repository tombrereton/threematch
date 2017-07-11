from itertools import product

from ai.move_finder import moves_three
from ai.state_parser import StateParser
from model.game import Grid
from model.game import SimpleBoard


class State:
    def __init__(self):
        self.current_state = ()
        self.rows = 9
        self.cols = 9
        self.gem_types = 6
        self.total_medals = 3
        self.board = SimpleBoard(self.rows, self.cols, self.gem_types, self.total_medals)
        self.gem_state = ()
        self.ice_state = ()
        self.medal_state = ()
        self.parser = StateParser()

    def first_state(self):
        # Returns a representation of the starting state of the game.
        state = self.parser.get_initial_state(1)
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
        gem_grid, ice_grid, medal_grid = self.state_to_grid(state)

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

        next_state = self.grid_to_state(gem_grid, ice_grid, medal_grid)

        return next_state

    def legal_moves(self, state):
        """
        Takes in a state, converts it to grids, and returns a list of legal moves
        where each item is 2 coordinates.
        item = ((r1,c1),(r2,c2))
        :param gem_grid:
        :return:
        """
        # print(state)
        gem_grid, _, _ = self.state_to_grid(state)
        legal_moves = moves_three(gem_grid)
        return legal_moves

    def winner(self, state):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass

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

        return gem_grid.grid, ice_grid.grid, medal_grid.grid

    def grid_to_state(self, gem_grid, ice_grid, medal_grid):
        """
        converts the 3 grids into a state
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

        state = tuple(map(tuple, grid.grid))
        return state

    def __str__(self):
        gem_grid, ice_grid, medal_grid = self.state_to_grid(self.current_state)
        b = SimpleBoard(self.rows, self.cols, self.gem_types, self.total_medals)
        b.gem_grid.grid = gem_grid
        b.ice_grid.grid = ice_grid
        b.medal_grid.grid = medal_grid
        return b.__str__()


if __name__ == '__main__':
    # get initial state
    s = State()
    cs = s.first_state()
    s.current_state = cs

    # get legal moves
    legal_moves = s.legal_moves(cs)
    print(legal_moves)

    # get next state from move 0
    move0 = legal_moves[0]
    ns = s.next_state(cs, move0)

