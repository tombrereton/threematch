import math
import random

from ai.board_simulator import BoardSimulator
from ai.state_functions import start_state


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

    def __init__(self, board: BoardSimulator, game_limit, move_limit, c, policy, eval_function, level=1,
                 get_q_values=False, print_move_ratings=True):
        """
        Constructor for the class
        :param board: Board object containing the game
        :param game_limit: The number of games to play per move choice
        :param move_limit: Maximum depth to play to
        :param c: Parameter to control exploration
        :param policy: Policy object to use
        """
        # Set field variables
        self.board = board
        self.game_limit = game_limit
        self.move_limit = move_limit
        self.c = c
        self.policy = policy
        self.eval_function = eval_function
        # Initialise list of states
        self.state = None
        # Initialise dictionary of statistics
        self.statistics = {}
        self.print_move_ratings = print_move_ratings
        self.level = level
        self.get_q_values = get_q_values

    def update(self, state):
        """
        Method to add a new state to the list of states
        :param state: New state to be added
        :return: None
        """
        # Store new state
        self.state = state

    def interim_move(self, state):
        """
        Method to pick a move whilst building the tree
        :param state: current state
        :return: Move to make during simulation
        """
        # Get the list of all possible moves at this point
        # moves = self.board.legal_moves(state)
        moves = self.policy.moves(state)

        if not moves:
            # If there are no moves return None
            move = None
        elif len(moves) == 1:
            # If there is only one possible move return this
            move = moves[0]
        else:
            # There are multiple moves to choose from
            # Get the statistics associated with all these moves
            stats = [self.statistics.get(m) for m in moves]

            if all(stats):
                # If statistics exist for all these moves use UCB to pick the move
                move = max(zip(moves, stats), key=interim_move_helper(stats, self.c))[0]
            else:
                # If not then pick a move at random from the unexplored moves
                move = random.choice([move for move, stat in zip(moves, stats) if not stat])

        return move

    def roll_out(self, state):
        """
        Method to pick a move after transitions to the next state.
        It randomly selects a move without relying on generated statistics
        :param state:
        :return:
        """
        moves = self.policy.moves(state)

        if not moves:
            # If there are no moves return None
            move = None
        elif len(moves) == 1:
            # If there is only one possible move return this
            move = moves[0]
        else:
            move = random.choice([move for move in moves])

        return move

    def play(self):
        """
        Simulates a game to build up the tree
        :return: None
        """
        # Make the start state, adds medals
        state = start_state(self.state)

        first_move = None
        for move_count in range(self.move_limit):
            # first check if winning state and break if so
            medals_remaining = state[3][1]
            if medals_remaining == 0:
                break

            # Get the list of all possible moves at this point
            move = self.interim_move(state) if move_count == 0 else self.roll_out(state)
            if move is None:
                # No valid moves available, game is over
                break
            if move_count == 0:
                # Still expanding, add this to visited set
                first_move = move
            state = self.board.next_state(state, move)

        # Game over or move limit reached
        # Find the winner of the game
        # 1 == win, 0 == loss
        state_score = self.eval_function(state, self.level)

        # Update statistics
        stat = self.statistics.get(first_move)
        if stat:
            # Statistics exist, increment plays
            stat[0] += 1
            stat[1] += state_score
        else:
            # If statistics did not exist add them now
            self.statistics[first_move] = [1, state_score]

    def pick_move(self):
        """
        Simulates some games and picks a move
        :return: Picked move
        """
        self.statistics = {}
        stats = None
        # Simulate games, builds tree
        for _ in range(self.game_limit):
            # Simulate one game
            self.play()

        # Get the list of all possible moves at this point
        current_state = self.state
        # moves = self.board.legal_moves(current_state)
        moves = self.policy.moves(current_state)

        count = 0
        if self.print_move_ratings:
            print('\nNext move:')
            for move in moves:
                play_wins = self.statistics.get(move)
                if play_wins:
                    plays, wins = play_wins
                    win_rate = wins / plays
                    print(f'Count: {count}, Move: {move}, Rating: {win_rate:.3f}')
                    count += 1

            print(f'Medals remaining: {current_state[-1][1]}')
        if not moves:
            # If there are no moves return None
            move = None
        elif len(moves) == 1:
            # If there is only one possible move return this
            move = moves[0]
        else:
            # Get the statistics associated with all moves
            stats = [self.statistics.get(move) for move in moves]

            # Either pick the move with the best win rate or one at random if there were no statistics
            if len(stats):
                # Return move with the best win rate
                move, stat = max((el for el in zip(moves, stats) if el[1]), key=pick_move_helper)
                if self.print_move_ratings:
                    print(f'\nStats based move: {move}, Rating: {stat[1] / stat[0]:.3}')
            else:
                # Return a random move from the moves without statistics
                move = random.choice([move for move, stat in zip(moves, stats) if not stat])
                if self.print_move_ratings:
                    print(f'\nRandom move: {move}')

        if self.get_q_values:
            q_values = [(m, s[1] / s[0]) for m, s in zip(moves, stats)]
            utility = max(q_values, key=lambda x: x[1])[1]
            return utility, q_values
        else:
            return move
