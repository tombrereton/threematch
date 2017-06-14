class GameState(object):
    """
    A class to represent the states it can be in, which are:

    waiting_for_input
    input_received
    not_valid_swap
    matches_found
    pulled_down

    """

    def __init__(self):
        self.state = "empty"


    def animate_swap(self, second_row: int, second_column: int):

        self.second_row = second_row
        self.second_column = second_column

        if second_row == self.row - 1 and second_column == self.column:
            # swap up
            self.state = "animate_swap"
            self.direction = "up"

        elif second_row == self.row + 1 and second_column == self.column:
            # swap down
            self.state = "animate_swap"
            self.direction = "down"

        elif second_row == self.row and second_column == self.column + 1:
            # swap right
            self.state = "animate_swap"
            self.direction = "right"

        elif second_row == self.row and second_column == self.column - 1:
            # swap left
            self.state = "animate_swap"
            self.direction = "left"

        else:
            self.state = "empty"
            self.row = None
            self.column = None
            self.second_row = None
            self.second_column = None
            self.direction = None

    def animate_reverse(self):
        self.state = "animate_reverse"

    def check_matches(self):
        self.state = "check_matches"

    def no_more_matches(self):
        self.state = "no_more_matches"

    def animate_explode(self, matches: int, match_list: list, bonus_list: list):
        self.state = "animate_explode"
        self.matches = matches
        self.match_list = match_list
        self.bonus_list = bonus_list

    def remove_gems(self):
        self.state = "remove_gems"
        self.cascade += 1

    def animate_pull_down(self):
        self.state = "animate_pull_down"

    def animate_pull_down_repeat(self):
        self.state = "animate_pull_down_repeat"

    def pull_down(self):
        self.state = "pull_down"

    def empty(self):
        self.state = "empty"
        self.row = None
        self.column = None
        self.direction = None
        self.matches = 0
        self.cascade = 0

    def stop_going(self):
        self.going = False

    def restart(self):
        self.state = "restart"

    def not_valid_swap(self):
        self.state = "not_valid_swap"

    def move_made(self):
        self.moves_left = self.moves_left - 1

    def medal_freed(self, number_found: int):
        self.medals_left -= number_found

    def check_swap(self):
        self.state = "check_swap"

    def get_swaps(self):
        """
        returns the 2 locations from the swap
        as a list of tuples
        :return:
        """
        swap_loc = [(self.row, self.column), (self.second_row, self.second_column)]
        return swap_loc
