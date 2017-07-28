from ai.move_finder import pick_move
from controller.controllers import NaiveAIControllerV1, MouseController, CPUSpinnerController
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
    gui_vars = GUIVariables.from_global()
    evManager = EventManager()

    game_board = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, MOVES_LEFT, event_manager=evManager)
    ai_cont = NaiveAIControllerV1(evManager, game_board, pick_move)
    mouse_cont = MouseController(evManager, gui_vars)
    spinner = CPUSpinnerController(evManager)
    view = GUI(gui_vars, *game_board.state(), event_manager=evManager)

    spinner.run()


if __name__ == "__main__":
    main()
