from itertools import product

import numpy as np

from ai.state_functions import one_hot


class EvaluationFunction:
    def __init__(self, model_path=None):
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
        medal_portion_weight = 1
        total_weight = medal_portion_weight

        feature_medal_portions = self.feature_medal_portions(ice_grid,
                                                             medal_grid,
                                                             initial_state[-1][1],
                                                             medal_portion_weight,
                                                             total_weight)

        return feature_medal_portions

    def evaluation_func_heuristic(self, initial_state, final_state):
        i_gem_grid, i_ice_grid, i_medal_grid, i_moves_medals = initial_state
        f_gem_grid, f_ice_grid, f_medal_grid, f_moves_medals = final_state

        # feature weightings
        medal_portion_weight = 10
        ice_removed_weight = 5
        removed_gems_weight = 1
        moves_rem_weight = 0
        star_count_weight = 0
        cross_count_weight = 0
        total_weight = medal_portion_weight + moves_rem_weight + ice_removed_weight + removed_gems_weight + \
                       star_count_weight + cross_count_weight

        feature_medal_portions = self.feature_medal_portions(f_ice_grid,
                                                             f_medal_grid,
                                                             i_moves_medals[1],
                                                             medal_portion_weight,
                                                             total_weight)

        feature_gems_removed = self.feature_removed_gems(i_gem_grid, f_gem_grid, removed_gems_weight, total_weight)

        feature_ice_removed = self.feature_ice_removed(i_ice_grid, f_ice_grid, ice_removed_weight, total_weight)

        return feature_medal_portions + feature_gems_removed + feature_ice_removed

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

    @staticmethod
    def feature_moves_remaining(moves_medals, moves_rem_weight, total_weight):
        # moves remaining feature calculation
        moves_remaining = moves_medals[0]
        total_moves = 20
        rating = moves_remaining / total_moves * moves_rem_weight / total_weight
        return rating

    @staticmethod
    def feature_ice_removed(initial_ice_grid, final_ice_grid, ice_removed_weight, total_weight):
        # ice removed feature calculation
        initial_ice_count = 0
        initial_ice_removed_count = 0
        final_ice_removed_count = 0
        for i, j in product(range(9), range(9)):
            if initial_ice_grid[i][j] != -1:
                initial_ice_count += 1
            if initial_ice_grid[i][j] == -1:
                initial_ice_removed_count += 1
            if final_ice_grid[i][j] == -1:
                final_ice_removed_count += 1

        if initial_ice_count == 0:
            return 1 * ice_removed_weight / total_weight
        else:
            ice_diff = final_ice_removed_count - initial_ice_removed_count
            return ice_diff / initial_ice_count * ice_removed_weight / total_weight

    @staticmethod
    def feature_medal_portions(final_ice_grid, final_medal_grid, initial_medals_remaining, medal_portion_weight,
                               total_weight):
        if initial_medals_remaining == 0:
            return medal_portion_weight / total_weight

        # Most portions that can be removed
        portions_remaining = 4 * initial_medals_remaining

        # Count how many medals are in the grid
        medals_in_grid = 0
        # Count how many portions are showing
        showing_sections = 0

        for i, j in product(range(9), range(9)):
            # Portion showing
            if final_ice_grid[i][j] == -1 and final_medal_grid[i][j] != -1:
                # Increment count
                showing_sections += 1

            # Medal in grid
            if final_medal_grid[i][j] == 0:
                # Increment count
                medals_in_grid += 1

        # How many medals have been full removed
        fully_removed = initial_medals_remaining - medals_in_grid
        # How many portions have been completely removed
        portion_count = 4 * fully_removed + showing_sections

        return (portion_count / portions_remaining) * medal_portion_weight / total_weight

    def feature_star_count(self, initial_gem_grid, final_gem_grid, star_weight, total_weight):
        # count initial and final star gems
        initial_star_count = 0
        final_star_count = 0
        for i, j in product(range(9), range(9)):
            if initial_gem_grid[i][j][1] == 2:
                initial_star_count += 1
            if final_gem_grid[i][j][1] == 2:
                final_star_count += 1

        star_count = final_star_count - initial_star_count
        return star_count * star_weight / total_weight

    def feature_cross_count(self, initial_gem_grid, final_gem_grid, cross_weight, total_weight):
        # count initial and final star gems
        initial_cross_count = 0
        final_cross_count = 0
        for i, j in product(range(9), range(9)):
            if initial_gem_grid[i][j][1] == 1:
                initial_cross_count += 1
            if final_gem_grid[i][j][1] == 1:
                final_cross_count += 1

        star_count = abs(final_cross_count - initial_cross_count)
        return star_count * cross_weight / total_weight

    def feature_removed_gems(self, initial_gem_grid, final_gem_grid, removed_gems_weight, total_weight):
        gem_difference_count = 0

        for i, j in product(range(9), range(9)):
            if initial_gem_grid[i][j] != final_gem_grid[i][j]:
                gem_difference_count += 1

        return gem_difference_count / 81 * removed_gems_weight / total_weight
