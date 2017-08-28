from itertools import product

import numpy as np

from ai.state_functions import one_hot


class EvaluationFunction:
    def __init__(self, pseudo_board, model_path=None):
        self.pseudo_board = pseudo_board
        self.model_path = model_path
        if model_path:
            from keras.models import load_model
            self.model = load_model(model_path)

    def evaluation_func_binary(self, state, level=1):
        """
        Takes in a terminal state and returns 1 if it is a win, 0 for a loss.
        :param level:
        :param state:
        :return:
        """

        gem_grid, ice_grid, medal_grid, moves_medals = state

        # medal portion feature calculation
        medals_remaining = moves_medals[1]
        total_portions = 4 * (2 + level)
        portion_count = 0
        for i, j in product(range(9), range(9)):
            if ice_grid[i][j] == -1 and medal_grid[i][j] != -1:
                portion_count += 1

        portion_ratio = portion_count / total_portions

        return 1 if portion_ratio == 1 else 0

    def evaluation_func_simple(self, state, level=1):
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
        medal_portion_weight = 5
        ice_removed_weight = 0
        moves_rem_weight = 1
        total_weight = medal_portion_weight + moves_rem_weight + ice_removed_weight

        # medal portion feature calculation
        medals_remaining = moves_medals[1]
        portions_remaining = medals_remaining * 4
        total_portions = 4 * (2 + level)
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

    def evaluation_simple_conv(self, state):
        """
        Takes in the state uses a neural network to evaluate how likely
        the state will result in a win.
        :param state:
        :return: A rating where a value of 1 is certain that it will win.
        """

        # convert state to one hot encoding
        gem_grid, ice_grid, medal_grid, moves_medals = state

        # feature weightings
        nn_weight = 1
        moves_rem_weight = 0
        total_weight = nn_weight + moves_rem_weight

        # moves remaining feature calculation
        moves_remaining = moves_medals[0]  # feature weightings
        medal_portion_weight = 2
        ice_removed_weight = 0
        moves_rem_weight = 1
        total_weight = medal_portion_weight + moves_rem_weight + ice_removed_weight
        total_moves = 20
        feature_moves_remaining = moves_remaining / total_moves * moves_rem_weight / total_weight

        # nn evaluation function feature calculation
        gem_colour = []
        bonus = []
        for row in range(9):
            temp_colour = []
            temp_bonus = []
            for col in range(9):
                t, bt, _ = gem_grid[row][col]
                temp_colour.append(t)
                temp_bonus.append(bt)

            gem_colour.append(temp_colour)
            bonus.append(temp_bonus)

        state_for_one_hot = np.array([gem_colour, bonus, ice_grid, medal_grid])
        state = np.array([one_hot(state_for_one_hot)])

        # predict likelihood of winning
        prediction = self.model.predict(x=state, batch_size=1)[0][0]

        feature_nn = prediction * nn_weight / total_weight

        return feature_nn + feature_moves_remaining
