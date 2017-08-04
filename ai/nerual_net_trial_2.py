import numpy as np
from keras import applications
from keras import backend as K
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

img_width, img_height = 150, 150
top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 2000
nb_validation_samples = 800
epochs = 50
batch_size_ = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


def save_bottleneck_features():
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size_,
        class_mode=None,  # this means our generator will only yield batches of data, no labels
        shuffle=False  # our data will be in order, so all first 1000 images will be cats, then 1000 dogs
    )

    # the predict_generator method returns the output of a model, given
    # a generator that yields batches of numpy data

    bottleneck_features_train = model.predict_generator(
        generator,
        nb_train_samples // batch_size_
    )

    # save the output as a Numpy array
    np.save('bottleneck_features_train.npy', bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size_,
        class_mode=None,
        shuffle=False
    )

    bottleneck_features_validation = model.predict_generator(
        generator,
        nb_validation_samples // batch_size_
    )

    np.save('bottleneck_features_validation.npy', bottleneck_features_validation)


def train_top_model():
    train_data = np.load('bottleneck_features_train.npy')
    train_labels = np.array(
        [0] * (nb_train_samples // 2) + [1] * (nb_train_samples // 2)
    )

    validation_data = np.load('bottleneck_features_validation.npy')
    validation_labels = np.array([0] * 400 + [1] * 400)

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_data,
              train_labels,
              epochs=50,
              batch_size=batch_size_,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)


save_bottleneck_features()
train_top_model()
