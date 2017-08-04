import numpy as np
from keras import backend as K
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.optimizers import SGD

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

# Generate dummy data
# x_train = np.random.random((100, 100, 100, 3))
# y_train = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)
x_train = np_4D_states
labels = np.array([1])
labels = np.expand_dims(labels, axis=0)
y_train = labels
# x_test = np.random.random((20, 100, 100, 3))
# y_test = keras.utils.to_categorical(np.random.randint(10, size=(20, 1)), num_classes=10)

model = Sequential()
# input: 100x100 images with 3 channels -> (100, 100, 3) tensors.
# this applies 32 convolution filters of size 3x3 each.
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy', optimizer=sgd)

model.fit(x_train, y_train, batch_size=32, epochs=10)
# score = model.evaluate(x_test, y_test, batch_size=32)
