import random

import numpy as np
from keras.layers import Input, Dense
from keras.models import Model

# model = Sequential()
#
# model.add(Dense(2, activation='sigmoid', input_shape=(2,)))
# model.add(Dense(2, activation='sigmoid', input_shape=(2,)))
# model.add(Dense(1, activation='sigmoid'))

inputs = Input(shape=(2,))
x = Dense(2, activation='sigmoid')(inputs)
# x = Dense(10, activation='sigmoid')(x)
output = Dense(1, activation='sigmoid')(x)
model = Model(inputs=inputs, outputs=output)

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

x_data = np.array([[random.random(), random.random()] for _ in range(2000)])
y_data = np.array([1.0 if (x[0] - 0.5) * (x[1] - 0.5) < 0 else 0.0 for x in x_data])
x_train = x_data[:-100]
x_test = x_data[-100:]
y_train = y_data[:-100]
y_test = y_data[-100:]
# print(x_data, y_data)

# for x, y in zip(x_data, y_data): print(x, y)

print('\nevaluate before: ', model.evaluate(x_train, y_train))
model.fit(x_data, y_data, epochs=300, batch_size=8, validation_split=0.1)
print('\n evaluate after: ', model.evaluate(x_test, y_test))
