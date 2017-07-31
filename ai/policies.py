from ai.move_finder import moves_three


class AbstractPolicy:
    def __init__(self):
        raise NotImplementedError()

    def moves(self, states):
        raise NotImplementedError()


def gems_from_state(state):
    rows = range(len(state) - 1)
    cols = range(len(state[0]))
    return tuple(tuple(state[i][j][0] for j in rows) for i in cols)


class AllPolicy(AbstractPolicy):
    def __init__(self):
        pass

    def moves(self, state):
        """
        Takes in a state, converts it to grids, and returns a list of legal moves
        where each item is 2 coordinates.
        item = ((r1,c1),(r2,c2))
        :param state:
        :return:
        """
        # print('state 9', state[9])
        # print(all(state[9]))
        if all(state[9]):
            gem_grid = gems_from_state(state)
            legal_moves = moves_three(gem_grid)
            return legal_moves
        else:
            return []
