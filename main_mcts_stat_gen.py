import sys

from ai.board_simulator import PseudoBoard
from ai.evaluation_functions import EvaluationFunction
from ai.mcts import MonteCarlo
from ai.policies import AllPolicy
from controller.controllers import CPUSpinnerController, MonteCarloController
from events.event_manager import EventManager
from global_variables import *
from model.game import Board


# ------------------------------------------------------------------------------
# logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
# ------------------------------------------------------------------------------
def main(g_limit, m_limit):
    """..."""

    if len(sys.argv) > 1:
        game_limit, move_limit, c = sys.argv[0], sys.argv[1], sys.argv[2]
    else:
        game_limit, move_limit, c = g_limit, m_limit, 1.4

    # append scores and hyper params to file
    file_name = 'mcts_standard.csv'
    line = f'\n1, {game_limit}, {move_limit}, {c}, '
    with open(file_name, 'a') as file:
        file.write(line)

    # gui_vars = GUIVariables.from_global()
    event_manager = EventManager()

    # ai controller setup
    pseudo_board = PseudoBoard()
    eval_function_object = EvaluationFunction(pseudo_board)
    eval_function = eval_function_object.evaluation_func_binary
    mc = MonteCarlo(pseudo_board, game_limit=game_limit, move_limit=move_limit,
                    c=c, policy=AllPolicy(), eval_function=eval_function)
    mcts_cont = MonteCarloController(event_manager, mc)

    # mouse controller setup
    # mouse_cont = MouseController(event_manager, gui_vars)

    # board setup
    game_board = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, MOVES_LEFT,
                       event_manager=event_manager)

    # view setup
    # view = GUI(gui_vars, *game_board.state(), event_manager=event_manager)

    # spinner setup
    spinner = CPUSpinnerController(event_manager)
    spinner.run()


if __name__ == "__main__":
    for g_limit in [1, 3, 5, 50, 100, 200]:
        for m_limit in [1, 3, 5, 10, 20]:
            for _ in range(100):
                main(g_limit=g_limit, m_limit=m_limit)
