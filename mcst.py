import random

class MonteCarlo:

    def __init__(self, board):
        self.board = board
        self.states = []

    def update(self, state):
        self.states.append(state)

    def play(self, move_limit):
        state = self.states[-1]
        
        for _ in range(move_limit):
            moves = self.board.moves(state)
            
            if moves:
                state = self.board.transition(state, random.choice(moves))
            else:
                return