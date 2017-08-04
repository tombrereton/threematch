
import numpy as np
from keras import backend as K
from keras.layers import Activation, Flatten, Dense
from keras.layers import Conv2D
from keras.models import Sequential

from ai.state_parser import StateParser

file_name = 'game-20170803-170103.txt'

state_parser = StateParser()
full_file_name = state_parser.get_full_filename(file_name)

state_4 = state_parser.get_state(full_file_name, 4)
# logging.info(state_4)

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

print(type)
print(bonus_type)
print(ice)
print(medal_portion)

print('3d: ', screen_cell_3D)

print(np_3D_state.shape)
print(np_4D_states.shape)

# -----------------------------------------------
# if K.image_data_format() == 'channels_first':
K.set_image_data_format('channels_first')
print(K.image_data_format())
input_shape = (4, 9, 9)  # else:

model = Sequential()
model.add(Conv2D(32, (5, 5), input_shape=input_shape))
model.add(Activation('relu'))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))

# the model so far outputs 3D feature maps (height, width, features)
model.add(Flatten())  # this converts out 3D feature mas to 1D feature vectors
model.add(Dense(81))
model.add(Activation('softmax'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

batch_size = 1

data = np_4D_states
labels = np.array([1])
labels = np.expand_dims(labels, axis=0)
print(labels.shape)

model.fit(data, labels, epochs=1, batch_size=batch_size)

# model.save('value_network_trial.h5')  # always save your weights after training or during training
