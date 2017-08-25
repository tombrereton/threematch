import os
import random
import re
from itertools import permutations

import numpy as np


def shuffle_multiple(*lists):
    """
        Function to shuffle a list
        :param lists: A list of lists to shuffle
        :return: None
    """
    i = len(lists[0]) - 1
    while 0 < i:
        j = random.randrange(i)
        for l in lists:
            l[i], l[j] = l[j], l[i]
        i -= 1


def renumber(game_ids):
    translate = {orig: new for new, orig in enumerate(set(game_ids))}
    return np.array([translate[orig] for orig in game_ids], dtype='i2')


def one_hot(state, permutation=range(6)):
    colour_channels = [state[0] == colour for colour in permutation]
    type_channels = [state[1] == t for t in range(2, 5)]
    ice_channels = [state[2] != -1]
    medal_channels = [state[3] == portion for portion in range(4)]

    state = np.concatenate((colour_channels, type_channels, ice_channels, medal_channels))

    return state


def reformat_action(action):
    if action[1] == action[3]:
        # Swap along y axis
        return 0, min(action[0], action[2]), action[3]
    else:
        # Swap along x axis
        return 1, action[0], min(action[1], action[3])


def data_generator(states, actions, labels, game_ids, moves_remaining):
    perms = list(permutations(range(6)))

    while True:
        index = random.randrange(len(states))

        state = states[index]
        action = actions[index]
        label = labels[index]
        game_id = game_ids[index]
        moves = moves_remaining[index]

        r = range(max(0, index - 30), min(len(game_ids), index + 30))
        this_game_indices = [i for i in r if game_ids[i] == game_id]
        states_in_game = len(this_game_indices)
        sub_index = this_game_indices.index(index)
        this_state_perms = perms[sub_index::states_in_game]

        output = np.full((1, 4, 9, 9), False)
        action = reformat_action(action)
        output[0, action[0], action[1], action[2]] = True
        if label:
            output[0, 2 + action[0], action[1], action[2]] = True

        for p in this_state_perms:
            state = one_hot(state, p)

            print("don't use this generator")
            yield np.array([state]), output


def move_evaluator(states, actions, labels, game_ids, moves_remaining):
    state_perm = []

    colour_perms = list(permutations(range(6)))
    games = sorted(set(game_ids))
    index = 0

    for game_id in games:
        top = min(index + 30, len(game_ids))
        sub_indices = [i for i in range(index, top) if game_ids[i] == game_id]
        states_in_game = len(sub_indices)

        for i in sub_indices:
            state_perm.extend((i, p) for p in range(i - index, 720, states_in_game))

        index += states_in_game

    while True:
        random.shuffle(state_perm)

        for state_i, perm_i in state_perm:
            state = states[state_i]
            action = actions[state_i]
            label = labels[state_i]
            moves = moves_remaining[state_i]

            perm = colour_perms[perm_i]

            state = one_hot(state, perm)

            move_channel = np.full((9, 9), False)
            move_channel[action[0]][action[1]] = True
            move_channel[action[2]][action[3]] = True

            state = np.concatenate((state, [move_channel]))

            yield state, label


def batch_generator(generator, batch_size, ):
    states = []
    labels = []

    while True:
        for _ in range(2 * batch_size):
            state, label = generator.__next__()

            states.append(state)
            labels.append(label)

        yield np.array(states), np.array(labels)

        states.clear()
        labels.clear()


def batch_generator2(generator, batch_size):
    states = []
    labels = []

    while True:
        wins_expected = int(batch_size * random.random())
        losses_expected = batch_size - wins_expected

        wins = 0
        losses = 0

        while len(states) < batch_size:
            state, label = generator.__next__()

            if (label and (wins < wins_expected)) or (not label and (losses < losses_expected)):
                states.append(state)
                labels.append(label)

                wins, losses = wins + 1 if label else wins, losses if label else losses + 1

        yield np.array(states), np.array(labels)

        states.clear()
        labels.clear()


def data_from_generator(generator, steps):
    gen = [g for g, _ in zip(generator, range(steps))]

    return np.concatenate([g[0] for g in gen]), np.concatenate([g[1] for g in gen])


def splitter(split_fractions, states, actions, labels, game_ids, moves_remaining):
    data_length = len(game_ids)

    # Size of sections
    foo = [int(data_length * fraction) for fraction in split_fractions]

    # Indices of splits
    foo = [data_length - sum(foo[i:]) for i in range(len(split_fractions))]

    # Game IDs at these splits
    bar = [game_ids[i] for i in foo]

    # Start of these games
    baz = [min(j for j in range(max(0, foo[i] - 30), foo[i] + 1) if game_ids[j] == game_id) for i, game_id in
           enumerate(bar)]

    qux = [0, *baz, data_length]

    for i in range(len(split_fractions) + 1):
        yield states[qux[i]:qux[i + 1]], actions[qux[i]:qux[i + 1]], labels[qux[i]:qux[i + 1]], \
              game_ids[qux[i]:qux[i + 1]], moves_remaining[qux[i]:qux[i + 1]]


class FileParser:
    """
        Class to process files in a directory
    """

    def __init__(self):
        """
            Constructor for class
        """
        # Initialise lists for data
        self.states = []
        self.actions = []
        self.labels = []
        self.game_ids = []
        self.moves_left = []

        # Compile regex patterns for finding lines
        self.info_line_check = re.compile(r'(\d+(\t|(\r?\n))){4}')
        self.state_line_check = re.compile(r'(-?\d+\t)+\r?\n')
        self.action_line_check = re.compile(r'\d+\t[-\d]+\r?\n')

        # Compile regex patterns for breaking lines apart
        self.info_line_parse = re.compile('\d+')
        self.state_line_parse = re.compile('-?\d+')
        self.action_line_parse = re.compile(r'(\d+)\t(-?\d)-(-?\d)-(-?\d)-(-?\d)')

    def process_line(self, line):
        """
            Method to check a line and split it.
            :param line: Line of the file to process.
            :return: Code for the line (0: info line, 1: state line, 2: action line, -1: other)
                     and the split contents of that line.
        """
        if re.fullmatch(self.info_line_check, line):
            # Info line
            return 0, [int(element) for element in re.findall(self.info_line_parse, line)]
        elif re.fullmatch(self.state_line_check, line):
            # State line
            s = np.array([int(element) for element in re.findall(self.state_line_parse, line)], dtype='b')[3:]
            return 1, np.array([int(element) for element in re.findall(self.state_line_parse, line)], dtype='b')
        elif re.fullmatch(self.action_line_check, line):
            # Action line
            m = re.search(self.action_line_parse, line)
            return 2, np.array([int(m.group(i)) for i in range(1, 6)], dtype='b')
        else:
            # Nothing
            return -1,

    def process_file(self, file):
        """"
            Method to read in a file and extract the relevant data from it.
            :param file: Name of the file to open.
            :return: Number of medals, number of moves and a list of states and actions.
        """
        with open(file) as file:
            lines = file.readlines()

        # Initialise variables
        medals = None
        moves = None
        states_actions = []

        # Go through lines in the file
        for line in lines:
            # Process each line
            result = self.process_line(line)

            if result[0] == 0:
                # This was the info line, get the moves and medals
                moves = result[1][0]
                medals = result[1][1]
            elif result[0] != -1:
                # This was a state or action line
                states_actions.append(result[1])

        # Sort the lines by line number
        states_actions.sort(key=lambda element: element[0])

        # Return medals, moves and the list of states and actions
        return medals, moves, states_actions

    @staticmethod
    def fix(medals, moves, states_actions):
        """
            Method the check of this data usable, and if it needs correcting.
            :param medals: Number of medals in this level
            :param moves: Number of moves in this level
            :param states_actions: List of states and actions
            :return: The fixed data from a file, may return an empty list if
                      file was too badly corrupted
        """
        if 3 < len(states_actions) and medals is not None and moves is not None and \
                        states_actions[-1][1] == -1 and states_actions[-2][0] + 1 == states_actions[-1][0]:

            states = []
            actions = []

            for i in range(len(states_actions) - 2):
                # Check this line is a state
                if states_actions[i][0] % 2 == 0:
                    # Check no missing lines
                    if states_actions[i][0] + 1 == states_actions[i + 1][0]:
                        states.append(states_actions[i])
                        actions.append(states_actions[i + 1])

            return states, actions, medals, moves, medals == states_actions[-2][2]
        else:
            return [],

    def add_to_lists(self, game_id, medals, moves, states_actions):
        """
            Method to add all the data into the lists.
            :param game_id: ID of this game.
            :param medals: Number of medals in this level
            :param moves: Number of moves in this level
            :param states_actions: List of states and actions
            :return: None
            
        """
        # Fix/check the data
        states, *others = self.fix(medals, moves, states_actions)

        # Unpack others if states is non-empty
        if states:
            actions, medals, moves, win = others

        # Add all state/action paris to instance lists along with labels, game_ids and moves_left
        for i in range(len(states)):
            self.states.append(states[i][3:])
            self.actions.append(actions[i][1:])
            self.labels.append(win)
            self.game_ids.append(game_id)
            self.moves_left.append(moves - states[i][0] // 2)

    def open_files(self, directory=None):
        """
            Method to read in all files
            :param directory: Optional argument of the directory to process
            :return: None
        """
        # Change directory if required
        if directory:
            os.chdir(directory)

        # Get a list of all .txt files
        files = [file for file in os.listdir() if file.find('.txt') != -1]

        # TODO For testing, remove this eventually
        random.shuffle(files)

        # Go through all files, getting the data from them
        for game_id, file in enumerate(files):
            # Get raw data from file
            medals, moves, states_actions = self.process_file(file)

            # Pass this data for more processing and adding to instance lists
            self.add_to_lists(game_id, medals, moves, states_actions)

        states = np.array(self.states)
        actions = np.array(self.actions)
        labels = np.array(self.labels)
        game_ids = renumber(self.game_ids)
        moves_left = np.array(self.moves_left, dtype='b')

        np.save('states', states)
        np.save('actions', actions)
        np.save('labels', labels)
        np.save('game_ids', game_ids)
        np.save('moves_left', moves_left)


if __name__ == '__main__':
    # t0 = time.time()
    # FileParser().open_files('data')
    # t1 = time.time()
    # print(t1 - t0)

    states = np.transpose(np.reshape(np.load('../ai/data/states.npy'), (-1, 9, 9, 4)), (0, 3, 1, 2))
    actions = np.load('../ai/data/actions.npy')
    labels = np.load('../ai/data/labels.npy')
    game_ids = np.load('../ai/data/game_ids.npy')
    moves_left = np.load('../ai/data/moves_left.npy')

    for output in data_generator(states, actions, labels, game_ids, moves_left):
        print(output)
        break
