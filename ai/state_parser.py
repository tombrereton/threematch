import os

from model.game import Grid


class StateParser:
    def __init__(self):
        self.rows = 9
        self.cols = 9
        self.gem_grid = Grid(self.rows, self.cols)
        self.ice_grid = Grid(self.rows, self.cols)
        self.medal_grid = Grid(self.rows, self.cols)

    def get_file_list(self):
        os.chdir(os.getcwd() + '/../training_data')
        return os.listdir()

    def get_initial_state(self, file_index):
        """
        returns the first state without the
        score ad medals uncovered (the first 2 integers
        of the game state)
        :param file_index:
        :return:
        """
        grid = Grid(self.rows, self.cols)

        file_name = self.get_file_list()[file_index]
        with open(file_name) as f:
            initial_state = f.readlines()[26:]

        state = initial_state[0][4:].split('\t')
        state.remove('\n')
        state = list(map(int, state))

        for i in range(0, len(state) - 4, 4):
            # get = (type, bonus_type)
            gem = [state[i], state[i + 1]]
            ice = [state[i + 2]]
            medal_portion = [state[i + 3]]
            item = gem + ice + medal_portion
            item = tuple(item)

            row_index = (i // 4 // 9)
            col_index = (i // 4) % 9
            grid.grid[row_index][col_index] = item

        parsed_state = tuple(map(tuple, grid.grid))
        return parsed_state


if __name__ == '__main__':
    s = StateParser()
    print(s.get_initial_state(1))
