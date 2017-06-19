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

from events import EventManager, MouseController, CPUSpinnerController
from game import Board
from global_variables import PUZZLE_COLUMNS, PUZZLE_ROWS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS
from gui import GUI


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def main():
    """..."""
    evManager = EventManager()

    mouse_cont = MouseController(evManager)
    spinner = CPUSpinnerController(evManager)
    game = Board(PUZZLE_ROWS, PUZZLE_COLUMNS, ICE_ROWS, LEVEL_1_TOTAL_MEDALS, evManager)
    view = GUI(*game.state(), evManager)

    spinner.Run()


if __name__ == "__main__":
    main()
