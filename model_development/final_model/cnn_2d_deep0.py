# Author: Ian Docherty
# Description: This model defines a 2D convolutional neural network with 3 convolutional layers.
#              This model is the final model that achieved the highest accuracy on the test data.
#
# Citation: The starting point for the architecture for this model was borrowed from Chapter 15
#           of the following source. Since the CNN model in Chapter 15 performed relatively well
#           with the ESC-10, a similar dataset, I made the assumption it might also perform well
#           for the GTZAN dataset.
#   Title: Practical Deep Learning: A Python-Based Introduction
#   Author: Ronald T. Kneusel
#   Link to book website: https://nostarch.com/practical-deep-learning-python

import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D


BATCH_SIZE = 16
NUM_CLASSES = 10
EPOCHS = 20
IMAGE_ROWS = 100
IMAGE_COLS = 160
INPUT_SHAPE = (IMAGE_ROWS, IMAGE_COLS, 3)  # The 3 signifies color images
KERNEL_SIZE = (3, 3)


def main():
    x_train = np.load("../spectrogram_100x160_datasets/gtzan_spect_train_images.npy")
    y_train = np.load("../spectrogram_100x160_datasets/gtzan_spect_train_labels.npy")
    x_test = np.load("../spectrogram_100x160_datasets/gtzan_spect_test_images.npy")
    y_test = np.load("../spectrogram_100x160_datasets/gtzan_spect_test_labels.npy")

    # Normalize image data to be in the range [0, 1]
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    y_train = keras.utils.to_categorical(y_train, NUM_CLASSES)
    y_test = keras.utils.to_categorical(y_test, NUM_CLASSES)

    # Build 2D CNN model
    model = Sequential()
    model.add(Conv2D(32, kernel_size=KERNEL_SIZE, activation='relu', input_shape=INPUT_SHAPE,
                     kernel_initializer='he_normal'))

    model.add(Conv2D(64, KERNEL_SIZE, activation='relu', kernel_initializer='he_normal'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, KERNEL_SIZE, activation='relu', kernel_initializer='he_normal'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128, activation='relu', kernel_initializer='he_normal'))
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, activation='softmax'))

    # Compile, train, and print score for this model on test data
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(0.0005),
                  metrics=['accuracy'])

    # Train using first half of test data for validation
    test_data_num_samples = x_test.shape[0]
    validation_data = (x_test[:(test_data_num_samples // 2)], y_test[:(test_data_num_samples // 2)])
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              verbose=1,
              validation_data=validation_data)

    # Evaluate using second half of test data for validation
    score = model.evaluate(x_test[(test_data_num_samples // 2):], y_test[(test_data_num_samples // 2):],
                           verbose=0)
    print("Test data accuracy:", score[1])
    model.save("gtzan_2d_cnn_deep0.h5")


if __name__ == "__main__":
    main()
