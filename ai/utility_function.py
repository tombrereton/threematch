from ai.evaluation_functions import EvaluationFunction
from ai.helpers.pseudo_board import PseudoBoard
from ai.mcts import MonteCarlo


def utility_function(state):
    """
    This functions takes in a state performs uses monte carlo
    tree search. It returns the utility of the state and
    the reward for each possible actions.
    :param state:
    :return: U(state), Q(state,action) for all actions in A
    """
    pseudo_board = PseudoBoard()
    ef = EvaluationFunction()
    mc = MonteCarlo()

