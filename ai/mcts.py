import math
import random

from ai.pseudo_board import PseudoBoard


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


lots_of_print = False

if lots_of_print:
    def p(arg):
        print(arg)
else:
    def p(arg):
        pass


class MonteCarlo:
    """
    Monte Carlo Tree Search class
    """

    def __init__(self, board: PseudoBoard, game_limit, move_limit, c, policy, eval_function):
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
        if self.states and state[9][0] == self.states[-1][9][0]:
            p('state', state)
            p('state in list', self.states[-1])
        self.states.append(state)
        p('State appended')

    def interim_move(self, state):
        """
        Method to pick a move whilst building the tree
        :param state: current state
        :return: Move to make during simulation
        """
        # Get the list of all possible moves at this point
        # moves = self.board.legal_moves(state)
        moves = self.policy.moves(state)

        p('Choosing interim move')

        if not moves:
            # If there are no moves return None
            p('No moves to chose from')
            move = None
        elif len(moves) == 1:
            # If there is only one possible move return this
            p('Only one move')
            move = moves[0]
        else:
            # There are multiple moves to choose from
            # Get the statistics associated with all these moves
            stats = [self.statistics.get(m) for m in moves]

            if all(stats):
                # If statistics exist for all these moves use UCB to pick the move
                p('Move picked from stats')
                move = max(zip(moves, stats), key=interim_move_helper(stats, self.c))[0]
            else:
                # If not then pick a move at random from the unexplored moves
                p('Move picked at random from moves with no stats')
                move = random.choice([move for move, stat in zip(moves, stats) if not stat])

        p(f'Move: {move}')
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
            p('No moves to chose from')
            move = None
        elif len(moves) == 1:
            # If there is only one possible move return this
            p('Only one move')
            move = moves[0]
        else:
            p('Move picked at random from moves with no stats')
            move = random.choice([move for move in moves])

        return move

    def play(self):
        """
        Simulates a game to build up the tree
        :return: None
        """
        # Copy the states list
        states = [*self.states]
        # print('start length', len(states))
        # Get the last state
        old_state = states[-1]
        state = self.board.simulate_medals(old_state)
        p(f'Medals: {state[9][1]}')
        # Create and empty set for the state/move pairs
        visited = set()

        p('Starting simulation')

        first_move = None
        for move_count in range(self.move_limit):
            # Get the list of all possible moves at this point
            move = self.interim_move(state) if move_count == 0 else self.roll_out(state)
            if move is None:
                # No valid moves available, game is over
                # print('move limit', self.move_limit)
                p('No moves available, terminal game state')
                break
            if move_count == 0:
                # Still expanding, add this to visited set
                first_move = move
            state = self.board.next_state(state, move)
            # Add new state to list of states
            states.append(state)

        # Game over or move limit reached
        # Find the winner of the game
        # 1 == win, 0 == loss
        winner = self.eval_function.evaluation_func_simple(states[-1])
        p(f'Winner: {winner}')

        # Update statistics
        stat = self.statistics.get(first_move)
        if stat:
            # Statistics exist, increment plays
            stat[0] += 1
            if winner == 1:
                # If this was a win increment wins
                stat[1] += 1
        else:
            # If statistics did not exist add them now
            self.statistics[first_move] = [1, winner if winner != 0 else 0]

    def pick_move(self):
        """
        Simulates some games and picks a move
        :return: Picked move
        """
        self.statistics = {}
        # Simulate games, builds tree
        for _ in range(self.game_limit):
            # Simulate one game
            self.play()

        p('Picking a move')

        # Get the list of all possible moves at this point
        current_state = self.states[-1]
        # moves = self.board.legal_moves(current_state)
        moves = self.policy.moves(current_state)

        count = 0
        print('\nNext move:')
        for move in moves:
            play_wins = self.statistics.get(move)
            if play_wins:
                plays, wins = play_wins
                win_rate = wins / plays
                print('Count: {}, Move: {}, Win rate: {:.3f}'.format(count, move, win_rate))
                count += 1

        print(f'Medals remaining: {current_state[9][1]}')
        if not moves:
            # If there are no moves return None
            p('No moves to choose from')
            move = None
        elif len(moves) == 1:
            # If there is only one possible move return this
            p('Only one move')
            move = moves[0]
        else:
            # Get the statistics associated with all moves
            stats = [self.statistics.get(move) for move in moves]
            # How many of these moves had statistics
            stats_number = sum(1 for stat in stats if stat)

            p(f'Possible moves: {len(stats)} (with statistics: {stats_number})')

            # Either pick the move with the best win rate or one at random depending on if there were enough statistics
            if len(stats):
                # Return move with the best win rate
                move, stat = max((el for el in zip(moves, stats) if el[1]), key=pick_move_helper)
                print('\nStats based move: {}, Win rate: {:.3}'.format(move, stat[1] / stat[0]))
            else:
                # Return a random move from the moves without statistics
                move = random.choice([move for move, stat in zip(moves, stats) if not stat])
                print('\nRandom move: {}'.format(move))

        # print('Move: ', move)
        return move
