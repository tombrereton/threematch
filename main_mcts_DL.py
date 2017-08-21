import argparse

from ai.evaluation_functions import EvaluationFunction
from ai.mcts import MonteCarlo
from ai.policies import AllPolicy
from ai.pseudo_board import PseudoBoard
from controller.controllers import CPUSpinnerController, MonteCarloController, MouseController
from events.event_manager import EventManager
from global_variables import *
from model.game import Board
from view.gui import GUI
from view.gui_variables import *


# ------------------------------------------------------------------------------
# logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
# ------------------------------------------------------------------------------
def main():
    """..."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Three match with AI', allow_abbrev=True)
    parser.add_argument('-game_limit', '-g', type=int, default=100,
                        help='The number of games simulated (default: 100)')
    parser.add_argument('-move_limit', '-m', type=int, default=5,
                        help='The number of moves per simulated game (default: 5)')
    parser.add_argument('-C', '-c', type=float, default=1.4,
                        help='The exploration factor for UCT (default: 1.4)')
    args = parser.parse_args()
    game_limit = args.game_limit
    move_limit = args.move_limit
    c = args.C
    print(args)

    # Misc setup
    gui_vars = GUIVariables.from_global()
    event_manager = EventManager()

    # ai controller setup
    pseudo_board = PseudoBoard()
    eval_function_object = EvaluationFunction(pseudo_board, model_path='ai/data/value_network.h5')
    eval_function = eval_function_object.evaluation_simple_conv
    mc = MonteCarlo(pseudo_board, game_limit=game_limit, move_limit=move_limit,
                    c=c, policy=AllPolicy(), eval_function=eval_function)
    mcts_cont = MonteCarloController(event_manager, mc)

    # mouse controller setup
    mouse_cont = MouseController(event_manager, gui_vars)

    # board setup
    game_board = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, MOVES_LEFT,
                       event_manager=event_manager)

    # view setup
    view = GUI(gui_vars, *game_board.state(), event_manager=event_manager)

    # spinner setup
    spinner = CPUSpinnerController(event_manager)
    spinner.run()


if __name__ == "__main__":
    main()
