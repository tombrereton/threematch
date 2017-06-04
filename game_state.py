class GameState(object):
    def __init__(self, moves_left: int):
        self.state = "empty"
        self.row = None
        self.column = None
        self.direction = None
        self.matches = 0
        self.going = True
        self.moves_left = moves_left

    def user_clicked(self, row: int, column: int):
        self.state = "user_clicked"
        self.row = row
        self.column = column

    def animate_swap(self, second_row: int, second_column: int):

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
            self.state == "not_valid_swap"

    def animate_reverse(self):
        self.state = "animate_reverse"

    def check_matches(self):
        self.state = "check_matches"

    def no_more_matches(self):
        self.state = "no_more_matches"

    def animate_explode(self, matches: int):
        self.state = "animate_explode"
        self.matches = matches

    def remove_gems(self):
        self.state = "remove_gems"

    def animate_pull_down(self):
        self.state = "animate_pull_down"

    def empty(self):
        self.state = "empty"
        self.row = None
        self.column = None
        self.direction = None
        self.matches = 0

    def stop_going(self):
        self.going = False

    def restart(self):
        self.state = "restart"
