from itertools import product

import numpy as np

from ai.state_functions import one_hot


class EvaluationFunction:
    def __init__(self, board_simulator, model_path=None):
        self.board_simulator = board_simulator
        self.model_path = model_path
        if model_path:
            from keras.models import load_model
            self.model = load_model(model_path)

    @staticmethod
    def evaluation_func_binary(initial_state, final_state):
        """
        Takes in a terminal state and returns 1 if it is a win, 0 for a loss.
        :param final_state:
        :return:
        """

        gem_grid, ice_grid, medal_grid, moves_medals = final_state
        moves_remaining, medals_remaining = moves_medals

        if medals_remaining == 0:
            return 1
        else:
            return 0

    def evaluation_func_crude(self, initial_state, final_state):
        """
        Takes in the state and evaluates it by giving a number between 0 and 1,
        where 1 is most optimal.

        This simple one counts the number of medal portions and also counts
        the moves remaining. Higher number of medal portions is better and
        also more moves remaining is better.

        The features are given a weighting so that the output is still
        between 0 and 1.
        :return:
        :param initial_state:
        :param final_state:
        :return:
        """
        gem_grid, ice_grid, medal_grid, moves_medals = final_state

        # feature weightings
        medal_portion_weight = 5
        ice_removed_weight = 0
        moves_rem_weight = 0
        total_weight = medal_portion_weight + moves_rem_weight + ice_removed_weight

        feature_medal_portions = self.feature_medal_portions(ice_grid,
                                                             medal_grid,
                                                             medal_portion_weight,
                                                             total_weight,
                                                             initial_state[-1][1])

        feature_ice_removed = self.feature_ice_removed(ice_grid,
                                                       ice_removed_weight,
                                                       total_weight)

        feature_moves_remaining = self.feature_moves_remaining(moves_medals,
                                                               moves_rem_weight,
                                                               total_weight)

        return feature_medal_portions + feature_moves_remaining + feature_ice_removed

    @staticmethod
    def feature_moves_remaining(moves_medals, moves_rem_weight, total_weight):
        # moves remaining feature calculation
        moves_remaining = moves_medals[0]
        total_moves = 20
        rating = moves_remaining / total_moves * moves_rem_weight / total_weight
        return rating

    @staticmethod
    def feature_ice_removed(ice_grid, ice_removed_weight, total_weight):
        # ice removed feature calculation
        ice_removed = 0
        total_ice = 81
        for i, j in product(range(9), range(9)):
            if ice_grid[i][j] == -1:
                ice_removed += 1
        return ice_removed / total_ice * ice_removed_weight / total_weight

    @staticmethod
    def feature_medal_portions(ice_grid, medal_grid, medal_portion_weight, total_weight, medals_remaining):
        if medals_remaining == 0:
            return medal_portion_weight / total_weight

        # Most portions that can be removed
        portions_remaining = 4 * medals_remaining

        # Count how many medals are in the grid
        medals_in_grid = 0
        # Count how many portions are showing
        showing_sections = 0

        for i, j in product(range(9), range(9)):
            # Portion showing
            if ice_grid[i][j] == -1 and medal_grid[i][j] != -1:
                # Increment count
                showing_sections += 1

            # Medal in grid
            if medal_grid[i][j] == 0:
                # Increment count
                medals_in_grid += 1

        # How many medals have been full removed
        fully_removed = medals_remaining - medals_in_grid
        # How many portions have been completely removed
        portion_count = 4 * fully_removed + showing_sections

        if (portion_count / portions_remaining) > 1:
            print('over one!')

        return (portion_count / portions_remaining) * medal_portion_weight / total_weight

    def evaluation_simple_conv_NN(self, initial_state, final_state):
        """
        Takes in the state uses a neural network to evaluate how likely
        the state will result in a win.
        :param initial_state:
        :param final_state:
        :return: A rating where a value of 1 is certain that it will win.
        """

        # convert state to one hot encoding
        gem_grid, ice_grid, medal_grid, moves_medals = final_state

        # feature weightings
        nn_weight = 1

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
        final_state = np.array([one_hot(state_for_one_hot)])

        # predict likelihood of winning
        prediction = self.model.predict(x=final_state, batch_size=1)[0][0]

        feature_nn = prediction * nn_weight / total_weight

        return feature_nn + feature_moves_remaining
