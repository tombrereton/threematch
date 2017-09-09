from model.game import SimpleBoard


class BoardSimulator:
    def __init__(self, rows=9, cols=9, gem_types=6):
        self.rows = rows
        self.cols = cols
        self.gem_types = gem_types

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
        moves_remaining, medals_remaining = moves_medals

        board = SimpleBoard(self.rows, self.cols, self.gem_types, medals_remaining, moves_remaining)
        board.gem_grid.grid = gem_grid
        board.ice_grid.grid = ice_grid
        board.medal_grid.grid = medal_grid

        board.set_swap_locations(action)
        board.swap_gems()
        board.move_made()

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

        state = board.get_full_game_state()

        return state
