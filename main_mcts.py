import argparse

from ai.board_simulator import BoardSimulator
from ai.evaluation_functions import EvaluationFunction
from ai.mcts import MonteCarlo
from ai.policies import AllPolicy
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Three match with AI', allow_abbrev=True)
    parser.add_argument('-game_limit', '-g', type=int, default=200,
                        help='The number of games simulated (default: 100)')
    parser.add_argument('-move_limit', '-m', type=int, default=5,
                        help='The number of moves per simulated game (default: 5)')
    parser.add_argument('-C', '-c', type=float, default=1.4,
                        help='The exploration factor for UCT (default: 1.4)')
    args = parser.parse_args()
    game_limit = args.game_limit
    move_limit = args.move_limit
    c = args.C
    print(f'Game Limit: {game_limit}, Move Limit: {move_limit}, C: {c}')

    # misc setup
    gui_vars = GUIVariables.from_global()
    event_manager = EventManager()

    # ai controller setup
    board_simulator = BoardSimulator()
    eval_function_object = EvaluationFunction()
    eval_function = eval_function_object.evaluation_func_heuristic
    mc = MonteCarlo(board_simulator=board_simulator,
                    game_limit=game_limit,
                    move_limit=move_limit,
                    c=c,
                    policy=AllPolicy(),
                    eval_function=eval_function)
    mcts_cont = MonteCarloController(event_manager, mc)

    # mouse controller setup
    mouse_cont = MouseController(event_manager, gui_vars)

    # board setup
    game_board = Board(rows=PUZZLE_ROWS,
                       columns=PUZZLE_COLUMNS,
                       ice_rows=ICE_ROWS,
                       medals_remaining=LEVEL_1_TOTAL_MEDALS,
                       moves_remaining=MOVES_LEFT,
                       event_manager=event_manager)

    # view setup
    view = GUI(gui_vars, *game_board.state(), event_manager=event_manager)

    # spinner setup
    spinner = CPUSpinnerController(event_manager)
    spinner.run()


if __name__ == "__main__":
    main()
