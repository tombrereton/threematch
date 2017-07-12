import random, math

class MonteCarlo:

    def __init__(self, board):
        self.board = board
        self.states = []
        self.statistics = {}

    def update(self, state):
        self.states.append(state)

    def pick_move(self, game_limit, move_limit):
        for _ in range(game_limit):
            self.play(move_limit)

        moves = self.board.moves(self.states)
        next_states = [self.board.transition(self.states, move) for moves]
        stats = [self.statistics.get((state, move)) for move, state in zip(moves, next_states)]
        
        move, *_ = max(zip(moves, next_states, stats), key=(lambda el: el[2][1] / el[2][0]))
        
        return move

    def play(self, move_limit):
        visited = set()
        states = [*self.states]

        for _ in range(move_limit):
            moves = self.board.moves(states)

            if not moves:
                break
            
            next_states = [self.board.transition(self.states, move) for moves]
            stats = [self.statistics.get((state, move), False) for move, state in zip(moves, next_states)]
            
            if all(stats):
                top = 2 * math.log(sum(stat[0] for stat in stats))
                move, _ = max(zip(moves, stats), key=(lambda el: el[1][1] / el[1][0] + math.sqrt(top / el[1][1])))
            else:
                move = random.choice(move for move, stat in zip(moves, stats) if not stat)

            state = self.board.transition(states, move)
            states.add(state)
            visisted.add((state, move))

        winner = self.board.winner(states)

        for state, move in visisted:
            if self.statistics.get(state, False):
                self.statistics[state][0] += 1
                if winner:
                    self.statistics[state][1] += 1
            else:
                self.statistics[state] = [1, 1 if winner else 0]
