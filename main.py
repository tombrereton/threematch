"""
Rough plan:

1.Mouse creates SwapGemsRequest

2.EventManager send request to game

3.game receives request in notify method

4.if state is waiting for input, game sets swap locations
and calls get_update within notify and send Update Bag to view

5.if state not waiting for input and event is ClockTick
call get_update and send Update Bag to view.
"""

from controller.controllers import MouseController, CPUSpinnerController
from events.event_manager import EventManager
from global_variables import *
from model.game import Board
from view.gui import GUI
from view.gui_variables import *


# logging.basicConfig(filename='game.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)


# ------------------------------------------------------------------------------
def main():
    """..."""
    gui_vars = GUIVariables.from_global()
    evManager = EventManager()

    mouse_cont = MouseController(evManager, gui_vars)
    spinner = CPUSpinnerController(evManager)
    game = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, MOVES_LEFT, event_manager=evManager)
    view = GUI(gui_vars, *game.state(), event_manager=evManager)

    spinner.run()


if __name__ == "__main__":
    main()
