import os
from time import time

import numpy as np
from keras import backend as K
from keras import optimizers
from keras.callbacks import TensorBoard
from keras.layers import Activation, Flatten, Dense, ZeroPadding2D, Dropout, MaxPooling2D
from keras.layers import Conv2D
from keras.models import Sequential
from keras.utils import np_utils

current_dir = os.getcwd() + '/'

win_filename = current_dir + 'np_win_data.npy'
loss_filename = current_dir + 'np_loss_data.npy'

win_label_filename = current_dir + 'np_win_labels.npy'
loss_label_filename = current_dir + 'np_loss_labels.npy'

np_win_data = np.load(win_filename)
np_win_labels = np.load(win_label_filename)
np_loss_data = np.load(loss_filename)
np_loss_labels = np.load(loss_label_filename)

# print shapes
print('win data shape: ', np_win_data.shape)
print('win labels shape: ', np_win_labels.shape)
print('loss data shape: ', np_loss_data.shape)
print('loss labels shape: ', np_loss_labels.shape)

np_win_loss = np.concatenate((np_win_data, np_loss_data))
np_win_loss_labels = np.concatenate((np_win_labels, np_loss_labels))
np_win_loss_labels = np_utils.to_categorical(np_win_loss_labels, 2)
print('np win loss shape: ', np_win_loss.shape)
print('np win loss label shape: ', np_win_loss_labels.shape)

# -----------------------------------------------
# if K.image_data_format() == 'channels_first':
K.set_image_data_format('channels_first')
print(K.image_data_format())
input_shape = (4, 9, 9)  # else:

model = Sequential()
model.add(ZeroPadding2D(padding=(4, 4), input_shape=input_shape))
model.add(Conv2D(6, (5, 5)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))

model.add(ZeroPadding2D(padding=(4, 4)))
model.add(Conv2D(6, (5, 5)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))

model.add(ZeroPadding2D(padding=(4, 4)))
model.add(Conv2D(6, (5, 5)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))

model.add(ZeroPadding2D(padding=(4, 4)))
model.add(Conv2D(6, (5, 5)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))

model.add(ZeroPadding2D(padding=(2, 2)))
model.add(Conv2D(12, (3, 3)))
model.add(Activation('relu'))

model.add(ZeroPadding2D(padding=(2, 2)))
model.add(Conv2D(12, (3, 3)))
model.add(Activation('relu'))

model.add(ZeroPadding2D(padding=(2, 2)))
model.add(Conv2D(12, (3, 3)))
model.add(Activation('relu'))

#
# model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
# model.add(ZeroPadding2D(padding=(2, 2)))
# model.add(Conv2D(32, (3, 3), activation='relu'))
# model.add(ZeroPadding2D(padding=(2, 2)))
# model.add(Conv2D(32, (3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
#
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(ZeroPadding2D(padding=(2, 2)))
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(ZeroPadding2D(padding=(2, 2)))
# model.add(Conv2D(32, (3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
#
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(ZeroPadding2D(padding=(2, 2)))
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(ZeroPadding2D(padding=(2, 2)))
# model.add(Conv2D(32, (3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
#
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='sigmoid'))

sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['accuracy'])

# the model so far outputs 3D feature maps (height, width, features)
# model.add(Flatten())  # this converts out 3D feature mas to 1D feature vectors
# model.add(Dense(81))
# model.add(Activation('sigmoid'))
# model.add(Dense(2))
# model.add(Activation('sigmoid'))


# model.compile(loss='mean_squared_error',
#               optimizer=sgd,
#               metrics=['accuracy'])

batch_size = 32

tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

model.fit(np_win_loss, np_win_loss_labels, validation_split=0.1, epochs=200, batch_size=batch_size,
          callbacks=[tensorboard], shuffle=True)

model.save('value_network_trial.h5')  # always save your weights after training or during training
