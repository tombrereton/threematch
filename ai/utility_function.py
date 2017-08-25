from ai.evaluation_functions import EvaluationFunction
from ai.helpers.pseudo_board import PseudoBoard
from ai.mcts import MonteCarlo
from ai.policies import AllPolicy


def utility_function(state):
    """
    This functions takes in a state performs uses monte carlo
    tree search. It returns the utility of the state and
    the reward for each possible actions.
    :param state:
    :return: U(state), Q(state,action) for all actions in A
    """
    game_limit = 100
    move_limit = 5
    c = 1.4
    level = 1
    pseudo_board = PseudoBoard(level=level)
    ef = EvaluationFunction(pseudo_board)
    e_function = ef.evaluation_func_simple
    mc = MonteCarlo(board=pseudo_board, game_limit=game_limit, move_limit=move_limit, c=c, policy=AllPolicy(),
                    eval_function=e_function, level=level, get_q_values=True)
    mc.update(state)
    utility, q_values = mc.pick_move()

    return utility, q_values
