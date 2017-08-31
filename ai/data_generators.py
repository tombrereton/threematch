import random
from itertools import permutations

import numpy as np

from ai.state_functions import one_hot
from file_parser.file_parser import FileParser


def generate_files():
    # generate files
    parser = FileParser()
    parser.open_files(directory='../data')


def get_states_labels(eval_data_split=200):
    # read in game_ids, states, labels
    # select one state & label from one game
    # loop over game_ids, find indices for 1 game, randomly pick one of the indices, store in list
    game_ids = np.load('data/game_ids.npy')
    states = np.load('data/states.npy')
    labels = np.load('data/labels.npy')

    l = {game_ids[i]: i for i in range(len(game_ids))}.values()
    l = [0, *[i + 1 for i in l]]
    game_id_indices = [random.randrange(l[i - 1], l[i]) for i in range(1, len(l))]

    states = states[game_id_indices]
    labels = labels[game_id_indices]

    states = np.reshape(states, [-1, 9, 9, 4])
    states = np.transpose(states, [0, 3, 1, 2])

    shuffle_multiple(states, labels)

    eval_states = states[-eval_data_split:]
    eval_labels = labels[-eval_data_split:]
    states = states[:-eval_data_split]
    labels = labels[:-eval_data_split]

    return states, labels, eval_states, eval_labels


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


def load_numpy_file(file_path):
    return np.load(file_path)


def slice_states(states, indices):
    return states[indices]


def reshape_states(states_array):
    states_array = np.reshape(states_array, [-1, 9, 9, 4])
    states_array = np.transpose(states_array, [0, 3, 1, 2])
    return states_array


def batch_generator_eval(generator, batch_size):
    while True:
        states = []
        labels = []

        for _ in range(batch_size):
            state, label = generator.__next__()
            states.append(state)
            labels.append(label)

        yield np.array(states), np.array(labels)


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


def shuffle_multiple(*lists):
    """
        Function to shuffle a list.
        :param lists: A list of lists to shuffle.
        :return: None
    """
    i = len(lists[0]) - 1
    while 0 < i:
        j = random.randrange(i)
        for l in lists:
            l[i], l[j] = l[j], l[i]
        i -= 1


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


def splitter(split_fractions, control, *lists):
    data_length = len(control)

    # Size of sections.
    individual_section_sizes = [int(data_length * fraction) for fraction in split_fractions]

    # Cumulative section sizes.
    cumulative_section_sizes = [data_length - sum(individual_section_sizes[i:]) for i in range(len(split_fractions))]

    # Control IDs at these splits.
    control_ids = [control[i] for i in cumulative_section_sizes]

    # Start of these sections according to control.
    shifted_indices = [min(index for index in range(max(0, size - 29), size + 1) if control[index] == control_id)
                       for size, control_id in zip(cumulative_section_sizes, control_ids)]

    # Add start and end of the lists
    all_indices = [0, *shifted_indices, data_length]

    for i in range(len(split_fractions) + 1):
        yield [control[all_indices[i]:all_indices[i + 1]], *[l[all_indices[i]:all_indices[i + 1]] for l in lists]]


def reformat_action(action):
    # TODO remove this
    if action[1] == action[3]:
        # Swap along y axis.
        return 0, min(action[0], action[2]), action[3]
    else:
        # Swap along x axis.
        return 1, action[0], min(action[1], action[3])
