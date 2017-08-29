import os
import re
import time

import numpy as np

from itertools import product


def renumber(game_ids):
    translate = {orig: new for new, orig in enumerate(sorted(set(game_ids)))}
    return np.array([translate[orig] for orig in game_ids], dtype='i2')


class FileParser:
    """
        Class to process files in a directory.
    """

    def __init__(self):
        """
            Constructor for class.
        """
        # Initialise lists for data.
        # State info
        self.grids = []
        self.moves_left = []
        self.levels = []
        self.medals_left = []
        # Player action
        self.actions = []
        # Original win label
        self.win = []
        # Game id
        self.game_ids = []

        # Compile regex patterns for finding lines.
        self.info_line_check = re.compile(r'(\d+(\t|(\r?\n))){4}')
        self.state_line_check = re.compile(r'(-?\d+\t)+\r?\n')
        self.action_line_check = re.compile(r'\d+\t[-\d]+\r?\n')

        # Compile regex patterns for breaking lines apart.
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
            # Info line.
            return 0, [int(element) for element in re.findall(self.info_line_parse, line)]
        elif re.fullmatch(self.state_line_check, line):
            # State line.
            return 1, np.array([int(element) for element in re.findall(self.state_line_parse, line)], dtype='b')
        elif re.fullmatch(self.action_line_check, line):
            # Action line.
            m = re.search(self.action_line_parse, line)
            return 2, np.array([int(m.group(i)) for i in range(1, 6)], dtype='b')
        else:
            # Nothing.
            return -1,

    def process_file(self, file):
        """"
            Method to read in a file and extract the relevant data from it.
            :param file: Name of the file to open.
            :return: Number of medals, number of moves and a list of states and actions.
        """
        with open(file) as f:
            lines = f.readlines()

        # Initialise variables.
        medals = None
        level = None
        moves = None
        states_actions = []

        # Go through lines in the file.
        for line in lines:
            # Process each line.
            result = self.process_line(line)

            if result[0] == 0:
                # This was the info line, get the moves and medals.
                moves = result[1][0]
                level = {20: 1, 25: 2, 30: 3}[moves]
                medals = result[1][1]
            elif result[0] != -1:
                # This was a state or action line.
                states_actions.append(result[1])

        # Sort the lines by line number.
        states_actions.sort(key=lambda element: element[0])

        # Return moves, level, medals and the list of states and actions.
        return moves, level, medals, states_actions

    @staticmethod
    def fix(moves, medals, states_actions):
        """
            Method the check of this data usable, and if it needs correcting.
            :param moves: Number of moves in this level.
            :param medals: Number of medals in this level.
            :param states_actions: List of states and actions.
            :return: The fixed data from a file, may return an empty list if
                      file was too badly corrupted.
        """
        if 2 <= len(states_actions) and medals is not None and moves is not None and states_actions[-1][1] == -1 \
                and states_actions[-2][0] + 1 == states_actions[-1][0]:

            states = []
            actions = []

            for i in range(len(states_actions) - 2):
                # Check this line is a state.
                if states_actions[i][0] % 2 == 0:
                    # Check no missing lines.
                    if states_actions[i][0] + 1 == states_actions[i + 1][0]:
                        states.append(states_actions[i])
                        actions.append(states_actions[i + 1])

            return states, actions, moves, medals, medals == states_actions[-2][2]
        else:
            return [],

    def add_to_lists(self, game_id, moves, level, medals, states_actions):
        """
            Method to add all the data into the lists.
            :param game_id: ID of this game.
            :param moves: Number of moves in this level.
            :param level: Level of this game.
            :param medals: Number of medals in this level.
            :param states_actions: List of states and actions.
            :return: None
        """
        actions = win = None

        # Fix/check the data.
        grids, *others = self.fix(moves, medals, states_actions)

        # Unpack others if states is non-empty.
        if grids:
            actions, moves, medals, win = others

        # Add all state/action paris to instance lists along with labels, game_ids and moves_left.
        for i in range(len(grids)):
            self.grids.append(grids[i][3:])
            self.moves_left.append(moves - grids[i][0] // 2)
            self.levels.append(level)
            self.medals_left.append(medals - grids[i][2])
            self.actions.append(actions[i][1:])
            self.win.append(win)
            self.game_ids.append(game_id)

    def open_files(self, directory='.'):
        """
            Method to read in all files.
            :param directory: Optional argument of the directory to process.
            :return: None
        """
        # Get a list of all .txt files.
        files = [f'{directory}/{file}' for file in os.listdir(directory) if file[-4:] == '.txt']

        # Go through all files, getting the data from them.
        for game_id, file in enumerate(files):
            # Get raw data from file.
            moves, level, medals, states_actions = self.process_file(file)

            # Pass this data for more processing and adding to instance lists.
            self.add_to_lists(game_id, moves, level, medals, states_actions)

        grids = np.array(self.grids)
        moves_left = np.array(self.moves_left, dtype='b')
        levels = np.array(self.levels, dtype='b')
        medals_left = np.array(self.medals_left, dtype='b')
        actions = np.array(self.actions)
        win = np.array(self.win)
        game_ids = renumber(self.game_ids)

        # Remove uncovered medals

        medal_grids = np.transpose(np.reshape(grids, (-1, 9, 9, 4)), (0, 3, 1, 2))[:, 3]

        s0 = [sum((medal_grids == i).flatten()) for i in range(4)]
        print(s0)

        # for grid in medal_grids:
        #     for row in grid:
        #         for el in row:
        #             print(str(el).ljust(3), end='')
        #         print()
        #     print()

        for grid, r, c in zip(*np.where(medal_grids == 0)):
            if all(medal_grids[grid, r + i, c + j] == 2 * i + j for i, j in ((0, 1), (1, 0), (1, 1))):
                print(f'removal at {grid}, {r}, {c}')
                for i, j in product(range(2), range(2)):
                    medal_grids[grid, r + i, c + j] = -1

        s1 = [sum((medal_grids == i).flatten()) for i in range(4)]
        print(s1)
        print(*[s0[i] - s1[i] for i in range(4)])

        # np.save('grids', grids)
        # np.save('moves_left', moves_left)
        # np.save('levels', levels)
        # np.save('medals_left', medals_left)
        # np.save('actions', actions)
        # np.save('win', win)
        # np.save('game_ids', game_ids)

if __name__ == '__main__':
    t0 = time.time()
    FileParser().open_files('data')
    t1 = time.time()
    print(t1 - t0)

    #     create_utility_labels('../ai/data/')
    # t0 = time.time()
    # FileParser().open_files('data')
    # t1 = time.time()
    # print(t1 - t0)
    #
    #     states = np.transpose(np.reshape(np.load('../ai/data/states.npy'), (-1, 9, 9, 4)), (0, 3, 1, 2))
    #     actions = np.load('../ai/data/actions.npy')
    #     labels = np.load('../ai/data/labels.npy')
    #     game_ids = np.load('../ai/data/game_ids.npy')
    #     moves_left = np.load('../ai/data/moves_left.npy')
    #
    # for output in data_generator(states, actions, labels, game_ids, moves_left):
    #     print(output)
    #     break
