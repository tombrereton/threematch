import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP

from global_variables import *


def debug_print(msg):
    print(msg)


def pixel_to_grid(y_coord: int, x_coord: int):
    """
    Method to calculate the row and column from pixel coordinates.
    :param y_coord: Grid y coordinate
    :param x_coord: Grid x coordinate
    :return: A tuple of the pixel coordinates (y, x)
    """
    row = (y_coord - MARGIN) // CELL_SIZE
    column = (x_coord - MARGIN) // CELL_SIZE
    if row < 0 or row >= PUZZLE_ROWS:
        row = -1

    if column < 0 or column >= PUZZLE_COLUMNS:
        column = -1
    return row, column


class Event:
    """this is a superclass for any events that might be generated by an
    object and sent to the EventManager"""

    def __init__(self):
        self.name = "Generic Event"


class TickEvent(Event):
    def __init__(self):
        self.name = "CPU Tick Event"


class QuitEvent(Event):
    def __init__(self):
        self.name = "Program Quit Event"


class SwapGemsRequest(Event):
    def __init__(self, swap_locations):
        self.name = "Swap Gems Request"
        self.swap_locations = swap_locations


class UpdateBagEvent(Event):
    def __init__(self, update_bag):
        self.name = "Update Bag Event"
        self.update_bag = update_bag


class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []

    # ----------------------------------------------------------------------
    def register_listener(self, listener):
        self.listeners[listener] = 1

    # ----------------------------------------------------------------------
    def unregister_listener(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    # ----------------------------------------------------------------------
    def post(self, event):
        if not isinstance(event, TickEvent):
            debug_print("\n     Message: " + event.name)
        for listener in self.listeners:
            # NOTE: If the weakref has died, it will be
            # automatically removed, so we don't have
            # to worry about it.
            listener.notify(event)


class MouseController:
    """KeyboardController takes Pygame events generated by the
    keyboard and uses them to control the model, by sending Requests
    or to control the Pygame display directly, as with the QuitEvent
    """

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)
        self.is_second_click = False
        self.first_row = -1
        self.first_column = -1

    # ----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, TickEvent):
            # Handle Input Events
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    ev = QuitEvent()
                elif event.type == MOUSEBUTTONDOWN and not self.is_second_click:
                    # First click, save coordinates
                    x = event.pos[0]
                    y = event.pos[1]
                    row, column = pixel_to_grid(y, x)

                    if row == -1 or column == -1:
                        # clicked not on grid
                        self.is_second_click = False
                    else:
                        # clicked on grid
                        self.first_row = row
                        self.first_column = column
                        self.is_second_click = True

                elif event.type == MOUSEBUTTONUP and self.is_second_click:
                    # Second click, create event object to send
                    x = event.pos[0]
                    y = event.pos[1]
                    row, column = pixel_to_grid(y, x)
                    if row == -1 or column == -1:
                        # clicked not on grid
                        self.is_second_click = False
                    else:
                        # clicked on grid
                        swap_locations = [(self.first_row, self.first_column), (row, column)]
                        ev = SwapGemsRequest(swap_locations)
                        self.is_second_click = False

                if ev:
                    self.evManager.post(ev)


class CPUSpinnerController:
    """..."""

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)

        self.keepGoing = 1

    # ----------------------------------------------------------------------
    def run(self):
        while self.keepGoing:
            event = TickEvent()
            self.evManager.post(event)

    # ----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, QuitEvent):
            # this will stop the while loop from running
            self.keepGoing = False
