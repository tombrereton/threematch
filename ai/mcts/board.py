class Board:

    def __init__(self):
        """
        Set up the board
        """
        raise NotImplementedError()

    def start(self):
        """
        Return start state of the game
        """
        raise NotImplementedError()

    def moves(self, states):
        """
        Returns a list of possible moves
        """
        raise NotImplementedError()

    def transition(self, states, move):
        """
        Return the next state given the current state and move
        """
        raise NotImplementedError()
