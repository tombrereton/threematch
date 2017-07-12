import random

class MonteCarlo:

    def __init__(self, board):
        self.board = board
        self.states = []
        self.statistics = {}

    def update(self, state):
        self.states.append(state)

    def play(self, move_limit):
        visited = set()
        states = [*self.states]
        
        for _ in range(move_limit):
            moves = self.board.moves(states)
            
            if not moves:
                break
            
            move = random.choice(moves)
            state = self.board.transition(states, move)
            states.add(state)
            visisted.add((state, move))
        
        winner = self.board.winner(states)
        
        for state, move in visisted:
            if self.statistics.get(state, False):
                self.statistics[state].plays += 1
                if winner:
                    self.statistics[state].wins += 1
            else:
                self.statistics[state].plays = 1
                self.statistics[state].wins = 1 if winner else 0
