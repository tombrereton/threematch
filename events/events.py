class Event:
    """this is a superclass for any event_files that might be generated by an
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


class StateEvent(Event):
    def __init__(self, state):
        self.name = "State Event"
        self.state = state
