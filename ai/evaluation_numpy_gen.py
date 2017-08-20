from file_parser.file_parser import *


def generate_files():
    # generate files
    parser = FileParser()
    parser.open_files(directory='data')


def get_states_labels(evaluation_data=False, eval_data_split=200):
    # read in game_ids, states, labels
    # select one state & label from one game
    # loop over game_ids, find indices for 1 game, randomly pick one of the indices, store in list
    game_ids = np.load('data/game_ids.npy')
    states = np.load('data/states.npy')
    labels = np.load('data/labels.npy')

    game_id_indices = []
    start_index = 0
    end_index = 0
    current_id = None
    rolling_id = game_ids[0]

    while end_index < len(game_ids):
        start_index = end_index
        current_id = game_ids[end_index]

        while end_index != len(game_ids) and rolling_id == current_id:
            rolling_id = game_ids[end_index]
            end_index += 1

        game_id_indices.append(random.randrange(start_index, end_index))

    game_id_indices = np.array(game_id_indices, dtype='int8')
    states = states[game_id_indices]
    labels = labels[game_id_indices]

    states = np.reshape(states, [-1, 9, 9, 4])
    states = np.transpose(states, [0, 3, 1, 2])

    shuffle_multiple(states, labels)

    if evaluation_data:
        states = states[-eval_data_split:]
        labels = labels[-eval_data_split:]
    else:
        states = states[:-eval_data_split]
        labels = labels[:-eval_data_split]

    return states, labels


def data_generator_eval(states, labels):
    while True:
        # outer loop for each epoch

        index_list = [i for i in range(len(states))]
        while index_list:
            index = index_list.pop(random.randrange(len(index_list)))

            # inner loop generates randomised states for 1 epoch
            original_state = states[index]
            for perm in permutations(range(6)):
                # we convert to one hot encoding
                state = one_hot(original_state, perm)

                yield np.array([state]), np.array([labels[index]])


if __name__ == '__main__':
    s, l = get_states_labels()
    # print(s, l)
