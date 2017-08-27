import time

import numpy as np

t = time.time()
from keras.layers import Conv2D, Dense, Flatten, Input
from keras.models import Model
from keras.optimizers import SGD

print(f'Import time: {time.time() - t}')

from file_parser.file_parser import move_evaluator, splitter
from ai.data_generators import batch_generator, batch_generator2, data_from_generator


def rescale(layer, factor):
    w = layer.get_weights()
    w[0] /= factor
    layer.set_weights(w)

# Load data

states = np.transpose(np.reshape(np.load('../../file_parser/states.npy'), (-1, 9, 9, 4)), (0, 3, 1, 2))
actions = np.load('../../file_parser/actions.npy')
labels = np.load('../../file_parser/labels.npy')
game_ids = np.load('../../file_parser/game_ids.npy')
moves_left = np.load('../../file_parser/moves_left.npy')

# Split Data

train, test, valid = splitter([0.1, 0.1], states, actions, labels, game_ids, moves_left)

# Make Generators

train_gen = move_evaluator(*train)
# test_gen = move_evaluator(*test)
validation_gen = move_evaluator(*valid)

# Network parameters

train_data_size = 720 * len(set(train[3]))
batch_size = 10
# steps_per_epoch = train_data_size / batch_size
steps_per_epoch = 10
epochs = 100

learning_rate = 0.0001

# validation_data_size = 720 * len(set(valid[3]))
validation_data_size = 100

# Batch generators

train_gen = batch_generator2(train_gen, batch_size)
# test_gen = batch_generator(test_gen, batch_size)
validation_gen = batch_generator(validation_gen, 1)

validation_data = data_from_generator(validation_gen, 1000)

# Setup network

inpt = Input(shape=(15, 9, 9))

l = Conv2D(30, (5, 5), activation='relu')
x = l(inpt)
# rescale(l, (15 * 25) ** 0.5)

# l = Conv2D(30, (3, 3), activation='relu')
# x = l(x)
# rescale(l, (30 * 9) ** 0.5)

x = Flatten()(x)

# l = Dense(100, activation='sigmoid', activity_regularizer=regularizers.l2(0.01))
# x = l(x)
# rescale(l, (30 * 25) ** 0.5)

# l = Dense(75, activation='sigmoid', activity_regularizer=regularizers.l2(0.01))
# x = l(x)
# rescale(l, 10)

# l = Dense(50, activation='sigmoid', activity_regularizer=regularizers.l2(0.01))
# x = l(x)
# rescale(l, 75 ** 0.5)

l = Dense(10, activation='sigmoid')
x = l(x)
# rescale(l, 50 ** 0.5)

l = Dense(1, activation='sigmoid')
output = l(x)
# rescale(l, 5)

model = Model(inputs=inpt, outputs=output)

sgd = SGD(lr=learning_rate)

model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['accuracy'])

# Train network

model.fit_generator(train_gen, steps_per_epoch=steps_per_epoch, epochs=epochs,
                    validation_data=validation_data)

validation_labels = validation_data[1]
dumb = sum(validation_labels) / len(validation_labels)
print(f'Wins: {dumb}')
dumb = dumb if 0.5 < dumb else 1 - dumb
print(f'From chance: {dumb}')

p = model.predict(validation_data[0])
foo = sum(1 if 0.5 < el[0] else 0 for el in p)
print(f'len(p): {len(p)}, ones: {foo}, zeros: {len(p) - foo}')

