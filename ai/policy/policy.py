import numpy as np

from keras.models import Sequential
from keras.layers import Conv2D, Dense, Reshape, Flatten
from file_parser.file_parser import move_evaluator

states = np.transpose(np.reshape(np.load('../../file_parser/states.npy'), (-1, 9, 9, 4)), (0, 3, 1, 2))
actions = np.load('../../file_parser/actions.npy')
labels = np.load('../../file_parser/labels.npy')
game_ids = np.load('../../file_parser/game_ids.npy')
moves_left = np.load('../../file_parser/moves_left.npy')

train_gen = move_evaluator(states[:-1000], actions[:-1000], labels[:-1000], game_ids[:-1000], moves_left[:-1000])
validation_data = move_evaluator(states[-1000:], actions[-1000:], labels[-1000:], game_ids[-1000:], moves_left[-1000:])

model = Sequential()
model.add(Conv2D(32, (5, 5), input_shape=(15, 9, 9)))
# model.add(Conv2D(32, (5, 5)))
model.add(Flatten())
# model.add(Dense(100))
# model.add(Dense(100))
model.add(Dense(1))
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
model.fit_generator(train_gen, steps_per_epoch=1000, epochs=1000, validation_data=validation_data, validation_steps=1000)
