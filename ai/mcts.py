import math
import random
import sys

from ai.psuedo_board import PseudoBoard


def pick_move_helper(element):
    """
    Key to be used in pick move helper
    :param element: An element in the list of moves and their associated statistics: (move, stat)
                    stat is a list of the plays and wins: [plays, wins]
    :return: Tuple comprising the win rate of this move (wins / plays) and a random number
    """
    return element[1][1] / element[1][0], random.random()


def interim_move_helper(stats, c):
    """
    Function to return a key for the interim move helper
    :param stats: List of stats
    :param c: Exploration parameter
    :return: Function for interim move helper to use as a key
    """
    top = math.log(sum(stat[0] for stat in stats))

    def foo(element):
        """
        Key to be used in interim move helper
        :param element: An element in the list of moves and their associated statistics: (move, stat)
                    stat is a list of the plays and wins: [plays, wins]
        :return: Tuple comprising the score of this move (win rate of this move plus an adjustment to encourage
                 exploration: (wins / plays + sqrt(top / plays))) and a random number
        """
        return element[1][1] / element[1][0] + c * math.sqrt(top / element[1][0]), random.random()

    return foo


class MonteCarlo:
    """
    Monte Carlo Tree Search class
    """

    def __init__(self, board: PseudoBoard, game_limit, move_limit, c):
        """
        Constructor for the class
        :param board: Board object containing the game
        :param game_limit: The number of games to play per move choice
        :param move_limit: Maximum depth to play to
        :param c: Parameter to control exploration
        """
        # Set field variables
        self.board = board
        self.game_limit = game_limit
        self.move_limit = move_limit
        self.c = c
        # Initialise list of states
        self.states = []
        # Initialise dictionary of statistics
        self.statistics = {}

    def update(self, state):
        """
        Method to add a new state to the list of states
        :param state: New state to be added
        :return: None
        """
        # Add new state to list of states
        self.states.append(state)

    def interim_move(self, state):
        """
        Method to pick a move whilst building the tree
        :param state: current state
        :return: Move to make during simulation
        """
        # Get the list of all possible moves at this point
        moves = list(self.board.legal_moves(state))

        if not moves:
            # If there are no moves return None
            return None
        elif len(moves) == 1:
            # If there is only one possible move return this
            return moves[0]
        else:
            # There are multiple moves to choose from
            # Get the statistics associated with all these moves
            stats = [self.statistics.get((state, m)) for m in moves]

            if all(stats):
                # If statistics exist for all these moves use UCB to pick the move
                return max(zip(moves, stats), key=interim_move_helper(stats, self.c))[0]
            else:
                # If not then pick a move at random from the unexplored moves
                return random.choice([move for move, stat in zip(moves, stats) if not stat])

    def play(self):
        """
        Simulates a game to build up the tree
        :return: None
        """
        # Copy the states list
        states = [*self.states]
        # Get the last state
        state = states[-1]
        # Create and empty set for the state/move pairs
        visited = set()

        # This is used to only expand the first new state/move
        expand = True
        for _ in range(self.move_limit):
            # Get the list of all possible moves at this point
            move = self.interim_move(state)
            if move is None:
                # No valid moves available, game is over
                break
            if expand:
                # Still expanding, add this to visited set
                visited.add((state, move))
            if expand and not self.statistics.get((state, move)):
                # New state/move pair encountered, stop expanding
                expand = False
            # Update state
            state = self.board.next_state(state, move)
            # Add new state to list of states
            states.append(state)

        # Game over or move limit reached
        # Find the winner of the game
        # 1 == win, 0 == loss
        # TODO: check this reaches the last state
        winner = self.board.is_winner(states[-1])
        print(len(states), winner)

        # Update statistics
        # for player in self.board.players():
        #     # Go through all of the games players
        #     # See if they won
        #     win = winner == player
        for state, move in visited:
            # Get statistics for this player/state/move
            stat = self.statistics.get((state, move))
            if stat:
                # Statistics exist, increment plays
                stat[0] += 1
                if winner == 2:
                    # If this was a win increment wins
                    stat[1] += 1
                elif winner == 0:
                    # If this was a loss decrement wins
                    stat[1] -= 1
            else:
                # If statistics did not exist add them now
                self.statistics[(state, move)] = [1, 1 if winner else 0]

    def pick_move(self):
        """
        Simulates some games and picks a move
        :return: Picked move
        """
        # Simulate games, builds tree
        for _ in range(self.game_limit):
            # Simulate one game
            self.play()

        # Get the list of all possible moves at this point
        moves = list(self.board.legal_moves(self.states[-1]))

        if not moves:
            # If there are no moves return None
            return None
        elif len(moves) == 1:
            # If there is only one possible move return this
            return moves[0]
        else:
            # Get the last state
            state = self.states[-1]
            # Get the statistics associated with all moves
            stats = [self.statistics.get((state, move)) for move in moves]
            # How many of these moves had statistics
            stats_number = sum(1 for stat in stats if stat)

            # Either pick the move with the best win rate or one at random depending on if there were enough statistics
            if random.random() < stats_number / len(stats):
                # Return move with the best win rate
                return max((el for el in zip(moves, stats) if el[1]), key=pick_move_helper)[0]
            else:
                # Return a random move from the moves without statistics
                return random.choice([move for move, stat in zip(moves, stats) if not stat])


if __name__ == '__main__':
    b = PseudoBoard()
    states = [b.get_state_from_data(2, 0)]
    if len(sys.argv) > 1:
        game_limit, move_limit, c = sys.argv[0], sys.argv[1], sys.argv[2]
    else:
        game_limit, move_limit, c = 20, 19, 1.4

    mc = MonteCarlo(b, game_limit=game_limit, move_limit=move_limit, c=c)
    mc.update(states[-1])

    total_moves = 20
    i = 0
    while i < total_moves:
        move = mc.pick_move()
        print(f'move picked: {move}')

        new_state = b.next_state(states[-1], move)
        states.append(new_state)
        mc.update(new_state)
        i += 1
        # print board
