import random

class MonteCarlo:

    def __init__(self, board):
        self.board = board
        self.states = []

    def update(self, state):
        self.states.append(state)

    def play(self, move_limit):
        states = self.states[:]
        state = states[-1]
        
        for _ in range(move_limit):
            moves = self.board.moves(states)
            
            if not moves:
                break
            
            move = random.choice(moves)
            state = self.board.transition(states, move)
