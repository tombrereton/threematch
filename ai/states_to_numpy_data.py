import os
from random import randrange

import numpy as np

from ai.permute import permute
from ai.state_parser import StateParser


def get_number_of_line(file_path):
    with open(file_path, 'r') as file:
        line_count = 0
        for _ in file:
            line_count += 1
    return max((line_count - 26) / 2, 0)


# change this depending on the win/loss folder
is_win_folder = True
is_training_data = True

label = 1 if is_win_folder else 0

if is_training_data:
    np_data_file_name = 'np_win_data' if is_win_folder else 'np_loss_data'
    np_label_file_name = 'np_win_labels' if is_win_folder else 'np_loss_labels'
    path_part = '/data/win/' if is_win_folder else '/data/loss/'
else:
    np_data_file_name = 'np_win_test' if is_win_folder else 'np_loss_test'
    np_label_file_name = 'np_win_labels_test' if is_win_folder else 'np_loss_labels_test'
    path_part = '/data/test_win/' if is_win_folder else '/data/test_loss/'

training_data_4D = []
training_labels_4D = []

# get all the file names in directory
state_parser = StateParser()
current_dir = os.getcwd() + path_part
files = os.listdir(current_dir)

# remove non training files
# files.remove('states_to_numpy_data.py')
file_count = 0
while files:
    # print('file count: ', file_count)
    file_count += 1

    state_3D_array = []

    file_name = files.pop(0)
    full_file_name = current_dir + '/' + file_name

    # randomise state index?
    state_index = randrange(get_number_of_line(full_file_name))
    state = state_parser.get_state(full_file_name, state_index)

    # convert to list and remove redundant elements
    state_as_list = state.split('\t')
    state_as_list.pop(0)
    state_as_list.pop(0)
    state_as_list.remove('\n')

    # split into 3D array where the 3rd dimension is (type, bonus_type, ice, medal_portion)
    type = []
    type_temp = []
    bonus_type = []
    bonus_type_temp = []
    ice = []
    ice_temp = []
    medal_portion = []
    medal_portion_temp = []

    i = 0
    while i < len(state_as_list):
        # convert to int and normalise between 0 and 1
        type_temp.append(int(state_as_list[i]))
        bonus_type_temp.append(int(state_as_list[i + 1]))
        ice_temp.append(int(state_as_list[i + 2]))
        medal_portion_temp.append(int(state_as_list[i + 3]))

        if i != 0 and (i + 4) % 36 == 0:
            # append to list after 9 elements
            type.append(type_temp)
            bonus_type.append(bonus_type_temp)
            ice.append(ice_temp)
            medal_portion.append(medal_portion_temp)
            type_temp = []
            bonus_type_temp = []
            ice_temp = []
            medal_portion_temp = []

        i += 4

    state_3D_array = [type, bonus_type, ice, medal_portion]
    training_data_4D.append(state_3D_array)
    training_labels_4D.append(label)

# save as numpy arrays
np_training_data_4D = np.asarray(training_data_4D, dtype='f')
np_training_data_4D = permute(np_training_data_4D)
np_training_data_4D[:, 0, :, :] /= 5
np_training_data_4D[:, 1, :, :] /= 3
np_training_data_4D[:, 2, :, :] += 1
np_training_data_4D[:, 3, :, :] += 1
np_training_data_4D[:, 3, :, :] /= 4
print(np_training_data_4D.shape)
np_training_labels_4D = np.tile(np.asarray(training_labels_4D), 720)
print(np_training_labels_4D.shape)
np.save(np_data_file_name, np_training_data_4D)
np.save(np_label_file_name, np_training_labels_4D)
