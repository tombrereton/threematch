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

    l = {game_ids[i]: i for i in range(len(game_ids))}.values()
    l = [0, *l]
    game_id_indices = [random.randrange(l[i - 1], l[i]) for i in range(1, len(l))]

    states = states[game_id_indices]

    # TODO change this label to a expected utility
    # Do this by running MCTS on sampled state
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

        index_list = list(range(len(states)))
        while index_list:
            index = index_list.pop(random.randrange(len(index_list)))

            # inner loop generates randomised states for 1 epoch
            original_state = states[index]
            for perm in permutations(range(6)):
                # we convert to one hot encoding
                state = one_hot(original_state, perm)

                yield state, labels[index]


def batch_generator_eval(generator, batch_size):
    while True:
        states = []
        labels = []

        for _ in range(batch_size):
            state, label = generator.__next__()
            states.append(state)
            labels.append(label)

        yield np.array(states), np.array(labels)


if __name__ == '__main__':
    # s, l = get_states_labels()
    generate_files()
    # print(s, l)
