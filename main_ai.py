from events import EventManager, CPUSpinnerController, NaiveAIControllerV1, MouseController
from game import Board
from global_variables import *
from gui import GUI
from gui_variables import *
from move_finder import pick_move


# ------------------------------------------------------------------------------
# logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
# ------------------------------------------------------------------------------
def main():
    """..."""
    gui_vars = GUIVariables.from_global()
    evManager = EventManager(gui_vars)

    game_board = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, MOVES_LEFT, event_manager=evManager)
    ai_cont = NaiveAIControllerV1(evManager, game_board, pick_move)
    mouse_cont = MouseController(evManager)
    spinner = CPUSpinnerController(evManager)
    view = GUI(gui_vars, *game_board.state(), event_manager=evManager)

    spinner.run()


if __name__ == "__main__":
    main()
