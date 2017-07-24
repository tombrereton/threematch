import random, math

def pick_move_helper(element):
    return (element[1][1] / element[1][0], random.random()) if element[1] else (0, random.random())

def interim_move_helper(stats):
    top = 2 * math.log(sum(stat[0] for stat in stats))
    def foo(element):
        return (element[1][1] / element[1][0] + math.sqrt(top / element[1][0]), random.random())
    return foo

class MonteCarlo:

    def __init__(self, board, game_limit, move_limit):
        self.board = board
        self.game_limit = game_limit
        self.move_limit = move_limit
        self.states = []
        self.statistics = {}

    def update(self, state):
        self.states.append(state)

    def interim_move(self, states):
        player = self.board.player(states)
        state = states[-1]
        moves = list(self.board.moves(states))

        if not moves:
            return None
        elif len(moves) == 1:
            return moves[0]
        else:
            stats = [self.statistics.get((player, state, move)) for move in moves]

            if all(stats):
                return max(zip(moves, stats), key=interim_move_helper(stats))[0]
            else:
                return random.choice([move for move, stat in zip(moves, stats) if not stat])

    def play(self):
        states = [*self.states]
        state = states[-1]
        visited = set()
        
        expand = True
        for _ in range(self.move_limit):
            move = self.interim_move(states)
            if move is None:
                break
            if expand:
                visited.add((state, move))
            if False and expand and not self.statistics.get((state, move)):
                expand = False
            state = self.board.transition(states, move)
            states.append(state)

        winner = self.board.winner(states)

        for player in self.board.players():
            win = winner == player
            for state, move in visited:
                stat = self.statistics.get((player, state, move))
                if stat:
                    stat[0] += 1
                    if win:
                        stat[1] += 1
                else:
                    self.statistics[(player, state, move)] = [1, 1 if win else 0]

    def pick_move(self):
        for _ in range(self.game_limit):
            self.play()

        moves = list(self.board.moves(self.states))

        if not moves:
            return None
        elif len(moves) == 1:
            return moves[0]
        else:
            player = self.board.player(self.states)
            state = self.states[-1]
            stats = [self.statistics.get((player, state, move)) for move in moves]
            stats_number = sum(1 for stat in stats if stat)
            
            if random.random() < stats_number / len(stats):
                return max((el for el in zip(moves, stats) if el[1]), key=pick_move_helper)[0]
            else:
                return random.choice([move for move, stat in zip(moves, stats) if not stat])
