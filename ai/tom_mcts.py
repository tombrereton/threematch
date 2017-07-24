"""
This implementation of monte carlo tree search is
for educational/learning purposes only.
"""
import random
import time


class MonteCarlo(object):
    def __init__(self, state, **kwargs):
        # Takes an instance of a State and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.state = state
        self.state_list = []
        self.calculation_time = kwargs.get('time', 30)
        self.max_moves = kwargs.get('max_moves', 20)

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.state_list.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            self.run_simulation()

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        state_list_copy = self.state_list[:]
        current_state = state_list_copy[-1]

        for t in range(self.max_moves):
            moves = self.state.legal_moves(current_state)

            move = random.choice(moves)
            next_state = self.state.next_state(current_state, move)
            state_list_copy.append(next_state)

            winner = self.state.is_winner(next_state)
            if winner == 2 or winner == 1:
                # 2 represents win
                # 1 represents loss (no moves left)
                break
