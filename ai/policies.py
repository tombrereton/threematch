from ai.state_functions import find_legal_moves


class AbstractPolicy:
    def __init__(self):
        raise NotImplementedError()

    def moves(self, states):
        raise NotImplementedError()


class AllPolicy(AbstractPolicy):
    def __init__(self):
        pass

    def moves(self, state):
        """
        Takes in a state, converts it to grids, and returns a list of legal moves
        where each item is 2 coordinates.
        item = ((r1,c1),(r2,c2))
        :param state:
        :return: List of possible moves
        """
        if all(state[-1]):
            legal_moves = find_legal_moves(state[0])
            return legal_moves
        else:
            return []


class SimplePolicy(AllPolicy):
    def __init__(self, limit: int):
        self.limit = limit

    def moves(self, state, limit=None):
        if limit is None:
            limit = self.limit

        moves = super().moves(state)

        # moves.sort()

        return moves[:limit]


class IceTargetPolicy(AllPolicy):
    def __init__(self):
        pass

    def moves(self, state, limit=None):
        if all(state[-1]):
            legal_moves = find_legal_moves(state[0])
            return legal_moves
        else:
            return []

        moves.sort()

        return moves[:limit]

