import sys

from ai.mcts import MonteCarlo
from ai.psuedo_board import PseudoBoard
from ai.state_parser import StateParser
from controller.controllers import MouseController, CPUSpinnerController, MonteCarloController
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

    if len(sys.argv) > 1:
        game_limit, move_limit, c = sys.argv[0], sys.argv[1], sys.argv[2]
    else:
        game_limit, move_limit, c = 20, 19, 1.4

    gui_vars = GUIVariables.from_global()
    evManager = EventManager(gui_vars)
    game_board = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, MOVES_LEFT, event_manager=evManager)

    # ai setup
    b = PseudoBoard()
    mcts_cont = MonteCarloController(evManager, MonteCarlo(b, game_limit=game_limit, move_limit=move_limit, c=c),
                                     StateParser(), game_board)

    # ai_cont = NaiveAIControllerV1(evManager, game_board, pick_move)
    mouse_cont = MouseController(evManager)
    spinner = CPUSpinnerController(evManager)
    view = GUI(gui_vars, *game_board.state(), event_manager=evManager)

    spinner.run()


if __name__ == "__main__":
    main()
