import random

from ai.mcts import PseudoBoard


def simulated_state(state):
    """
    read in state.
    Return state with random medal locations
    :param state:
    :return:
    """
    medals_remaining = state[9][0]
    possible_medal_coords = [(i, j) for i in range(9) for j in range(9)]

    gem_grid, ice_grid, medal_grid = PseudoBoard.state_to_grid(state)

    repeat = True
    while repeat:
        while medals_remaining != 0:
            choice = random.randrange(len(possible_medal_coords))
            r, c = possible_medal_coords.pop(choice)

            if ice_grid[r, c] == -1:
                possible_medal_coords.remove((r, c))
            elif medal_grid[r, c] != -1:
                possible_medal_coords.remove((r, c))

            if not possible_medal_coords:
                repeat = True
