class GameState(object):
    def __init__(self):
        self.state = "empty"
        self.row = None
        self.column = None
        self.direction = None
        self.matches = 0
        self.going = True

    def user_clicked(self, row: int, column: int):
        self.state = "user_clicked"
        self.row = row
        self.column = column

    def animate_swap(self, direction: str):
        self.state = "animate_swap"
        self.direction = direction

    def check_matches(self):
        self.state = "check_matches"

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
