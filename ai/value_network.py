from keras import backend as K
from keras import regularizers
from keras.callbacks import TensorBoard
from keras.layers import Conv2D, Activation, BatchNormalization, Input, Dense, Dropout, Flatten, MaxPooling2D, \
    ZeroPadding2D
from keras.models import Model
from keras.models import Sequential
from keras.optimizers import SGD

from ai.evaluation_numpy_gen import *
from time import time
from time import time

from keras import backend as K
from keras import regularizers
from keras.callbacks import TensorBoard
from keras.layers import Conv2D, Activation, BatchNormalization, Input, Dense, Dropout, Flatten, MaxPooling2D, \
    ZeroPadding2D
from keras.models import Model
from keras.models import Sequential
from keras.optimizers import SGD

from ai.evaluation_numpy_gen import *

# -----------------------------------------------
input_shape = (14, 9, 9)
K.set_image_data_format('channels_first')

# -----------------------------------------------
"""
Get states and labels. The order has been randomised so
it isn't all wins then losses and so the validation and training
data are random. Each state element is represented as a 14 one hot labels: 
colour_channels, type_channels, ice_channels, medal_channels
"""
states, labels = get_states_labels()
eval_states, eval_labels = get_states_labels(evaluation_data=True)

# split states
split = 400
training_states, validation_states = states[:-split], states[-split:]
training_labels, validation_labels = labels[:-split], labels[-split:]


# -----------------------------------------------

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


# -----------------------------------------------
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


# -----------------------------------------------
def simple_net(weight_path=None):
    input_layer = Input(shape=input_shape)
    x = Flatten()(input_layer)
    x = Dense(324, activation='sigmoid')(x)
    x = Dropout(0.2)(x)
    x = Dense(324, activation='sigmoid')(x)
    x = Dropout(0.5)(x)
    x = Dense(162, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=input_layer, outputs=output)

    return model


# -----------------------------------------------
def simple_conv_net(lmbda, weight_path=None):
    model_name = 'simple_conv_net'
    inputs = Input(shape=input_shape)
    x = Conv2D(6, (5, 5), kernel_regularizer=regularizers.l2(lmbda))(inputs)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)
    x = Flatten()(x)
    output = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=output)
    return model, model_name


# -----------------------------------------------
if __name__ == "__main__":
    # hyper parameters
    learning_rate = 0.001
    lmbda_reg = 0.01
    batch_size = 16
    epochs = 300
    steps_per_epoch = len(training_states) / batch_size
    log_id = time()
    tensorboard = TensorBoard(log_dir=f"logs/{log_id}")

    # compile the model
    model, model_name = simple_conv_net(lmbda=lmbda_reg)
    sgd = SGD(lr=learning_rate)
    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['accuracy'])

    # data generators
    train_gen = data_generator_eval(training_states, training_labels)
    valid_gen = data_generator_eval(validation_states, validation_labels)
    eval_gen = data_generator_eval(eval_states, eval_labels)

    # train the model
    model.fit_generator(generator=train_gen, validation_data=valid_gen,
                        steps_per_epoch=steps_per_epoch, validation_steps=200,
                        epochs=epochs, callbacks=[tensorboard])

    # save model
    model.save('data/value_network.h5')

    # evaluate model
    score = model.evaluate_generator(generator=eval_gen,
                                     steps=len(eval_states))
    print('\n\nTest loss:', score[0], ', Test accuracy: ', score[1])

    # append scores and hyper params to file
    file_name = 'scores_eval.csv'
    line = f'\n{model_name}, {log_id}, {learning_rate}, {lmbda_reg}, {batch_size}, {epochs}, {score[0]}, {score[1]}'
    with open(file_name, 'a') as file:
        file.write(line)
