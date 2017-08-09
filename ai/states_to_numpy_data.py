import os

import numpy as np

from ai.state_parser import StateParser

# change this depending on the win/loss folder
is_win_folder = True

label = 1 if is_win_folder else 0
np_data_file_name = 'np_win_data' if is_win_folder else 'np_loss_data'
np_label_file_name = 'np_win_labels' if is_win_folder else 'np_loss_labels'

training_data_4D = []
training_labels_4D = []

# get all the file names in directory
state_parser = StateParser()
current_dir = os.getcwd()
files = os.listdir(current_dir)

# remove non training files
files.remove('states_to_numpy_data.py')

while files:

    state_3D_array = []

    file_name = files.pop(0)
    full_file_name = current_dir + '/' + file_name

    # randomise state index?
    state_index = 4
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
        type_temp.append(int(state_as_list[i]) / 5)
        bonus_type_temp.append(int(state_as_list[i + 1]) / 3)
        ice_temp.append(int(state_as_list[i + 2]) + 1)
        medal_portion_temp.append((int(state_as_list[i + 3]) + 1) / 4)

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
np_training_data_4D = np.asarray(training_data_4D)
np_training_labels_4D = np.asarray(training_labels_4D)
np.save(np_data_file_name, np_training_data_4D)
np.save(np_label_file_name, np_training_labels_4D)