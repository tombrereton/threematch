import os
from time import time

import numpy as np
from keras import backend as K
from keras import regularizers
from keras.callbacks import TensorBoard
from keras.layers import Conv2D, Activation, BatchNormalization, Input
from keras.layers.convolutional import MaxPooling2D, ZeroPadding2D
from keras.layers.core import Flatten, Dense, Dropout
from keras.models import Model
from keras.models import Sequential
from keras.optimizers import SGD


# -----------------------------------------------
def resize_arrays(np_win_data, np_win_labels, np_loss_data, np_loss_labels, percent=100):
    win_data_size = len(np_win_data)
    loss_data_size = len(np_loss_data)

    slice_win = int(percent / 100 * win_data_size)
    slice_loss = int(percent / 100 * loss_data_size)

    np_win_data = np_win_data[:slice_win]
    np_win_labels = np_win_labels[:slice_win]
    np_loss_data = np_loss_data[:slice_loss]
    np_loss_labels = np_loss_labels[:slice_loss]

    return np_win_data, np_win_labels, np_loss_data, np_loss_labels


# -----------------------------------------------
current_dir = os.getcwd() + '/'

win_filename = current_dir + 'np_win_data.npy'
loss_filename = current_dir + 'np_loss_data.npy'

win_label_filename = current_dir + 'np_win_labels.npy'
loss_label_filename = current_dir + 'np_loss_labels.npy'

np_win_data = np.load(win_filename)
np_win_labels = np.load(win_label_filename)
np_loss_data = np.load(loss_filename)
np_loss_labels = np.load(loss_label_filename)

np_win_data, np_win_labels, np_loss_data, np_loss_labels = resize_arrays(np_win_data, np_win_labels, np_loss_data,
                                                                         np_loss_labels, percent=100)

# print shapes
print('win data shape: ', np_win_data.shape)
print('win labels shape: ', np_win_labels.shape)
print('loss data shape: ', np_loss_data.shape)
print('loss labels shape: ', np_loss_labels.shape)

np_win_loss = np.concatenate((np_win_data, np_loss_data))
np_win_loss_labels = np.concatenate((np_win_labels, np_loss_labels))
# np_win_loss_labels = np_utils.to_categorical(np_win_loss_labels, 2)
print('np win loss shape: ', np_win_loss.shape)
print('np win loss label shape: ', np_win_loss_labels.shape)

# -----------------------------------------------
K.set_image_data_format('channels_first')
print(K.image_data_format())
input_shape = (4, 9, 9)


def VGG_16(weights_path=None):
    model = Sequential()
    model.add(ZeroPadding2D((2, 2), input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((2, 2)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    if weights_path:
        model.load_weights(weights_path)

    return model


def alex_net(weight_path=None):
    model = Sequential()
    model.add(Conv2D(64, (3, 3), padding='same', input_shape=input_shape))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))

    model.add(Conv2D(128, (5, 5), padding='same'))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))

    model.add(Conv2D(192, (3, 3), padding='same'))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))

    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))

    model.add(Flatten())
    model.add(Dense(4096, kernel_initializer='normal'))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('relu'))
    model.add(Dense(4096, kernel_initializer='normal'))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('relu'))
    model.add(Dense(2, kernel_initializer='normal'))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('softmax'))

    return model


def simple_net(weight_path=None):
    inputs = Input(shape=input_shape)
    x = Flatten()(inputs)
    x = Dense(324, activation='sigmoid')(x)
    x = Dropout(0.2)(x)
    x = Dense(324, activation='sigmoid')(x)
    x = Dropout(0.5)(x)
    x = Dense(162, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=output)

    return model


def simple_conv_net(weight_path=None):
    inputs = Input(shape=input_shape)
    # trial 1, l2 = 1
    # l2 = .1, good with lr = 0.001
    # l3 = 0.01
    # l4 = 10
    # no padding, dropout 0.5
    x = Conv2D(6, (5, 5), kernel_regularizer=regularizers.l2(.1))(inputs)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)
    # x = Conv2D(6, (5, 5), kernel_regularizer=regularizers.l2(.1), padding='same')(x)
    # x = Activation('relu')(x)
    # x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Flatten()(x)
    output = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=output)
    return model


if __name__ == "__main__":
    model = simple_conv_net()

    # lr = 0.001
    sgd = SGD(lr=.001)
    model.compile(optimizer=sgd,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    tensorboard = TensorBoard(log_dir="logs/{}".format(time()))
    # bs = 16 is good, lr =0.001, l2 = 0.1
    batch_size = 16
    model.fit(np_win_loss, np_win_loss_labels, validation_split=0.1, epochs=50, batch_size=batch_size,
              callbacks=[tensorboard], shuffle=True)

    model.save('value_network_trial.h5')  # always save your weights after training or during training
