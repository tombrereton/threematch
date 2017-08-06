import os

import numpy as np
from keras import backend as K
from keras.layers import Activation, Flatten, Dense
from keras.layers import Conv2D
from keras.models import Sequential

current_dir = os.getcwd() + '/'

win_filename = current_dir + 'np_win_data.npy'
loss_filename = current_dir + 'np_loss_data.npy'

win_label_filename = current_dir + 'np_win_labels.npy'
loss_label_filename = current_dir + 'np_loss_labels.npy'

np_win_data = np.load(win_filename)
np_win_labels = np.load(win_label_filename)

# print shapes
print('win data shape: ', np_win_data)
print('win labels shape: ', np_win_labels)

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

batch_size = 2

model.fit(np_win_data, np_win_labels, epochs=10, batch_size=batch_size)

# model.save('value_network_trial.h5')  # always save your weights after training or during training
