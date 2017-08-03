from itertools import product


class EvaluationFunction:
    def __init__(self, pseudo_board):
        self.pseudo_board = pseudo_board

    def evaluation_func_simple(self, state):
        """
        Takes in the state and evaluates it by giving a number between 0 and 1,
        where 1 is most optimal.

        This simple one counts the number of medal portions and also counts
        the moves remaining. Higher number of medal portions is better and
        also more moves remaining is better.

        The features are given a weighting so that the output is still
        between 0 and 1.
        :return:
        :param state:
        :return:
        """
        gem_grid, ice_grid, medal_grid, moves_medals = state

        # feature weightings
        medal_portion_weight = 2
        ice_removed_weight = 0
        moves_rem_weight = 1
        total_weight = medal_portion_weight + moves_rem_weight + ice_removed_weight

        # medal portion feature calculation
        medals_remaining = moves_medals[1]
        total_portions = 12
        portion_count = 0
        for i, j in product(range(9), range(9)):
            if ice_grid[i][j] == -1 and medal_grid[i][j] != -1:
                portion_count += 1
        feature_medal_portions = (portion_count / total_portions) * medal_portion_weight / total_weight

        # ice removed feature calculation
        ice_removed = 0
        total_ice = 81
        for i, j in product(range(9), range(9)):
            if ice_grid[i][j] == -1:
                ice_removed += 1
        feature_ice_removed = ice_removed / total_ice * ice_removed_weight / total_weight

        # moves remaining feature calculation
        moves_remaining = moves_medals[0]
        total_moves = 20
        feature_moves_remaining = moves_remaining / total_moves * moves_rem_weight / total_weight

        return feature_medal_portions + feature_moves_remaining + feature_ice_removed
