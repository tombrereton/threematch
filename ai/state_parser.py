import logging
import os

from model.game import Grid

logging.basicConfig(level=logging.INFO)


class StateParser:
    def __init__(self):
        self.rows = 9
        self.cols = 9
        self.gem_grid = Grid(self.rows, self.cols)
        self.ice_grid = Grid(self.rows, self.cols)
        self.medal_grid = Grid(self.rows, self.cols)

    def get_file_list(self):
        os.chdir(os.getcwd() + '/../training_data')
        logging.debug(f'files in directory: \n{os.listdir()}\n')
        return os.listdir()

    def get_state(self, file_index, state_index):
        # skip every second line
        state_index *= 2

        file_name = self.get_file_list()[file_index]

        logging.debug(f'File name of initial state: {file_name}')

        with open(file_name) as f:
            initial_state = f.readlines()[26:]

        first_state = initial_state[state_index]

        return self.parse_state(first_state)

    def parse_state(self, string_state):
        """
        parses a string representing the state and returns it
        as a 2d array of tuples, the last row is a tuple
        of (score, medals uncovered).
        :param string_state:
        :return:
        """
        grid = Grid(self.rows, self.cols)

        first_state = string_state.split('\t')
        if 'n' in first_state:
            first_state.remove('\n')
        if '' in first_state:
            first_state.remove('')
        state = list(map(int, first_state))

        for i in range(2, len(state), 4):
            # get = (type, bonus_type)
            gem = [state[i], state[i + 1]]
            ice = [state[i + 2]]
            medal_portion = [state[i + 3]]
            item = gem + ice + medal_portion
            item = tuple(item)

            row_index = (i // 4 // 9)
            col_index = (i // 4) % 9
            grid.grid[row_index][col_index] = item

        grid.grid.append(state[:2])
        parsed_state = tuple(map(tuple, grid.grid))
        return parsed_state


if __name__ == '__main__':
    s = StateParser()
    print(s.get_initial_state(1))
