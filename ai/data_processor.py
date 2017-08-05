import numpy as np

from ai.state_parser import StateParser

file_name = 'game-20170803-170103.txt'

state_parser = StateParser()
full_file_name = state_parser.get_full_filename(file_name)

state_4 = state_parser.get_state(full_file_name, 4)

screen_cell_list = state_4.split('\t')

screen_cell_list.pop(0)
screen_cell_list.pop(0)
screen_cell_list.remove('\n')
print('screen list: ', screen_cell_list)

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
while i < len(screen_cell_list):
    # convert to int and normalise between 0 and 1
    type_temp.append(int(screen_cell_list[i]) / 5)
    bonus_type_temp.append(int(screen_cell_list[i + 1]) / 3)
    ice_temp.append(int(screen_cell_list[i + 2]) + 1)
    medal_portion_temp.append((int(screen_cell_list[i + 3]) + 1) / 4)

    if i != 0 and (i + 4) % 36 == 0:
        type.append(type_temp)
        bonus_type.append(bonus_type_temp)
        ice.append(ice_temp)
        medal_portion.append(medal_portion_temp)
        type_temp = []
        bonus_type_temp = []
        ice_temp = []
        medal_portion_temp = []

    i += 4

screen_cell_3D = [type, bonus_type, ice, medal_portion]
np_3D_state = np.array(screen_cell_3D)
np_4D_states = np.expand_dims(np_3D_state, axis=0)

# read in file
# read last line and determine if winning game
# move file to win or loss folder

# read in first file
# get state
# turn state into 3d array
# append to 4D array
# loop until no more files

# save 4D numpy array

print(type)
print(bonus_type)
print(ice)
print(medal_portion)

print('3d: ', screen_cell_3D)

print(np_3D_state.shape)
print(np_4D_states.shape)
