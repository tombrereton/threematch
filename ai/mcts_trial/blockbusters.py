import random
import sys
from itertools import product

from ai.mcts_trial.board import Board
from ai.mcts_trial.mcts import MonteCarlo

size = int(sys.argv[1])


def print_board(state):
    global size
    print('*' * size)
    print('\n'.join([''.join([' ' if el == 0 else str(el) for el in row]) for row in state[0]]))
    print('*' * size)


class Blockbusters(Board):

    def __init__(self):
        pass

    def start(self):
        global size
        return ((0,) * size,) * size, 1

    def players(self):
        return (1, 2)

    def player(self, states):
        return states[-1][1]
    
    def winner(self, states):
        global size
        grid = states[-1][0]
        # check if player one has a horizontal
        checked = []
        to_check = [(i, -1) for i in range(size)]
        while to_check:
            coord = to_check.pop()
            checked.append(coord)
            new = [(coord[0] - 1, coord[1]), (coord[0] + 1, coord[1]), (coord[0], coord[1] - 1), (coord[0], coord[1] + 1)]
            if size in [i[1] for i in new]:
                return 1
            new = [i for i in new if i not in checked]
            new = [i for i in new if 0 <= i[0] < size and 0 <= i[1] < size]
            new = [i for i in new if grid[i[0]][i[1]] == 1]           
            to_check.extend(new)
        # check if player two has a vertical
        checked = []
        to_check = [(-1, i) for i in range(size)]
        while to_check:
            coord = to_check.pop()
            checked.append(coord)
            new = [(coord[0] - 1, coord[1]), 
            (coord[0] + 1, coord[1]), 
            (coord[0], coord[1] - 1), 
            (coord[0], coord[1] + 1)]
            if size in [i[0] for i in new]:
                return 2
            new = [i for i in new if i not in checked]
            new = [i for i in new if 0 <= i[0] < size and 0 <= i[1] < size]
            new = [i for i in new if grid[i[0]][i[1]] == 2]  
            to_check.extend(new)
        return 0

    def moves(self, states):
        global size
        if not self.winner(states):
            state = states[-1]
            grid = state[0]
            player = state[1]
            for i, j in product(*[range(size)] * 2):
                if grid[i][j] == 0:
                    yield (i, j, player)

    def transition(self, states, move):
        global size
        old_state = states[-1]
        grid = old_state[0]
        player = old_state[1]
        new_grid = [[*grid[i]] for i in range(size)]
        new_grid[move[0]][move[1]] = move[2]
        new_grid = tuple(tuple(row) for row in new_grid)
        return (new_grid, 3 - player)

def recur_len(a):
    if type(a) == tuple:
        return sum(recur_len(i) for i in a)
    else:
        return 1

bb = Blockbusters()
states = [bb.start()]
print_board(states[-1])
i = 0
mc = MonteCarlo(bb, int(sys.argv[2]), int(sys.argv[3]))
mc.update(states[-1])
while True:
    if i:
        moves = tuple(bb.moves(states))
        if not moves:
            break
        move = random.choice(moves)
    else:
        move = mc.pick_move()
        if not move:
            break
    new_state = bb.transition(states, move)
    states.append(new_state)
    mc.update(new_state)
    print_board(new_state)
    i = 1 - i
print(bb.winner(mc.states))
# s = mc.statistics
# c = 0
# for key, value in s.items():
#     c += recur_len(key)
#     c += len(value)
# print(4 * c, 'bytes')
