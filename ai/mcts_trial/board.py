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

    def players(self):
        """
        Returns all players
        """
        raise NotImplementedError()

    def player(self, states):
        """
        Return the current player
        """
        raise NotImplementedError()

    def moves(self, states):
        """
        A generator of possible moves
        """
        raise NotImplementedError()

    def transition(self, states, move):
        """
        Return the next state given a list of states and move to make
        :param states:
        :param move:
        :return:
        """
        raise NotImplementedError()

    def winner(self, states):
        """
        Returns the winner
        """
        raise NotImplementedError()
