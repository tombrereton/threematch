import logging
import sys

from ai.mcts import MonteCarlo
from ai.pseudo_board import PseudoBoard
from controller.controllers import MouseController, CPUSpinnerController, MonteCarloController
from events.event_manager import EventManager
from global_variables import *
from model.game import Board
from view.gui import GUI
from view.gui_variables import *

# ------------------------------------------------------------------------------
# logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
# ------------------------------------------------------------------------------
def main():
    """..."""

    if len(sys.argv) > 1:
        game_limit, move_limit, c = sys.argv[0], sys.argv[1], sys.argv[2]
    else:
        game_limit, move_limit, c = 50, 21, 1.4

    #
    gui_vars = GUIVariables.from_global()
    event_manager = EventManager()

    # ai controller setup
    pseudo_board = PseudoBoard()
    mcts_cont = MonteCarloController(event_manager,
                                     MonteCarlo(pseudo_board, game_limit=game_limit, move_limit=move_limit, c=c))

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
