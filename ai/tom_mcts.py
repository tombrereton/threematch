"""
This implementation of monte carlo tree search is
for educational/learning purposes only.
"""
import random
import sys
import time
from math import log, sqrt

from ai.mcts import State


class MonteCarlo(object):
    def __init__(self, board: State, **kwargs):
        # Takes an instance of a State and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.board = board
        cs = board.get_state_from_data(2, 0)
        self.state_list = [cs]
        self.calculation_time = kwargs.get('timer', 30)
        self.max_moves = kwargs.get('max_moves', 20)
        self.wins = {}
        self.plays = {}
        self.C = kwargs.get('C', 1.4)

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.state_list.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.state_list[-1]
        legal = self.board.legal_moves(state)

        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        move_states = [(move, self.board.next_state(state, move)) for move in legal]

        # display the number of calls of run_simulation and
        # the time elapsed
        print('Games: ', games, ', Sim Time: ', time.time() - begin, '\n')

        percent_wins, move = max(
            (self.wins.get(state, 0) / self.plays.get(state, 1), move) for move, state in move_states)

        # display stats for each possible play
        for stats in sorted(
                ((100 * self.wins.get(state, 0) / self.plays.get(state, 1),
                  self.wins.get(state, 0),
                  self.plays.get(state, 0),
                  m)
                 for m, state in move_states), reverse=True):
            print("Move: {3}, Percent Win: {0:.2f}%, Wins/Plays: ({1} / {2})".format(*stats))

        print(f'Maximum depth searched: {self.max_depth}')

        return move

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays, wins = self.plays, self.wins

        visited_states = set()
        state_list_copy = self.state_list[:]
        current_state = state_list_copy[-1]

        expand = True
        for t in range(self.max_moves):
            moves = self.board.legal_moves(current_state)
            move_states = [(move, self.board.next_state(current_state, move)) for move in moves]

            # if we have stats on all moves, use UCB
            if all(plays.get(state) for move, state in move_states):
                log_total = log(sum(plays[state] for move, state in move_states))

                value, move, next_state = max((wins[state] / plays[state] + self.C * sqrt(log_total / plays[state]),
                                               move,
                                               state) for move, state in move_states)
            else:
                # select move randomly
                move, next_state = random.choice(move_states)

            # next_state = self.state.next_state(current_state, move)
            state_list_copy.append(next_state)

            # if state not in plays, expand
            if expand and next_state not in plays:
                expand = False
                self.plays[next_state] = 0
                self.wins[next_state] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add(next_state)

            winner = self.board.is_winner(next_state)
            if winner in [1, 2]:
                # 2 represents win
                # 1 represents loss (no moves left)
                break

        for state in visited_states:
            if state not in self.plays:
                continue
            self.plays[state] += 1

            # change to state == next_state?
            winner = self.board.is_winner(state)
            if winner == 2:
                # 2 represents win
                # 1 represents loss (no moves left)
                self.wins[state] += 1
            elif winner == 1:
                self.wins[state] -= 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        timer, max_moves, C = sys.argv[0], sys.argv[1], sys.argv[2]
    else:
        timer, max_moves, C = 5, 20, 1.4
    print('timer, max_moves, C:', timer, max_moves, C)

    s = State()
    cs = s.get_state_from_data(2, 0)
    s.current_state = cs
    # print(s)

    mc = MonteCarlo(State(), timer=timer, max_moves=max_moves, C=C)
    move = mc.get_play()
    print(f'Move from MCTS: {move}')
