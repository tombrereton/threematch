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
    def deregister_listener(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    # ----------------------------------------------------------------------
    def post(self, event):
        # if not isinstance(event, TickEvent):
        #     debug_print("\n     Message: " + event.name)
        for listener in self.listeners:
            # NOTE: If the weakref has died, it will be
            # automatically removed, so we don't have
            # to worry about it.
            listener.notify(event)