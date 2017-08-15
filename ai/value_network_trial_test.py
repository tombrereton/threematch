import os

import numpy as np
from keras.models import load_model

model = load_model('ai/value_network_trial.h5')

current_dir = os.getcwd() + '/'

win_filename = current_dir + 'np_win_test.npy'
loss_filename = current_dir + 'np_loss_test.npy'

win_label_filename = current_dir + 'np_win_labels_test.npy'
loss_label_filename = current_dir + 'np_loss_labels_test.npy'

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
# np_win_loss_labels = np_utils.to_categorical(np_win_loss_labels, 2)
print('np win loss shape: ', np_win_loss.shape)
print('np win loss label shape: ', np_win_loss_labels.shape)

x = np_win_loss[:1000]
y = np_win_loss_labels[:1000]

t_test = 120

score = model.evaluate(x, y, batch_size=32, verbose=1)
print('\n\nTest loss:', score[0])
print('\nTest accuracy:', score[1])

# predictions = model.predict(x=x, batch_size=128, verbose=1)
# print('labels: ', np_win_loss_labels)
# print('\n predictions: ', predictions)
