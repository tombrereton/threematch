import numpy as np
import random

from keras.models import Model, Sequential
from keras.layers import Input, Dense


model = Sequential()

model.add(Dense(10, activation='sigmoid', input_shape=(2,)))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

# inputs = Input(shape=(2,))
# x = Dense(10, activation='sigmoid')(inputs)
# x = Dense(10, activation='sigmoid')(x)
# output = Dense(1, activation='sigmoid')(x)
# model = Model(inputs=inputs, outputs=output)

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

x_data = np.array([[random.random(), random.random()] for _ in range(1000)])
y_data = np.array([1.0 if (x[0] - 0.5) * (x[1] - 0.5) < 0 else 0.0 for x in x_data])

for x, y in zip(x_data, y_data): print(x, y)

print(model.evaluate(x_data, y_data))
model.fit(x_data, y_data, epochs=5, batch_size=100)
print(model.evaluate(x_data, y_data))
