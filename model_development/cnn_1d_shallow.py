# Author: Ian Docherty
# Description: This model uses a convolutional neural network to train the raw
#              split datasets on a shallow depth network

import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D


BATCH_SIZE = 128
NUM_CLASSES = 10
EPOCHS = 12
INPUT_SHAPE = (1323, 1)
KERNEL_SIZE = 11


def main():

    # Get the raw numpy array datasets
    x_train = np.load("raw_split_datasets/gtzan_raw_split_train_audio.npy")
    y_train = np.load("raw_split_datasets/gtzan_raw_split_train_labels.npy")
    x_test = np.load("raw_split_datasets/gtzan_raw_split_test_audio.npy")
    y_test = np.load("raw_split_datasets/gtzan_raw_split_test_labels.npy")

    # Normalize feature vectors to the range [0, 1] and convert labels to categorical
    x_train = (x_train.astype('float32') + 32768) / 65536  # 32768 is max possible amplitude in dataset
    x_test = (x_test.astype('float32') + 32768) / 65536
    y_train = keras.utils.to_categorical(y_train, NUM_CLASSES)
    y_test = keras.utils.to_categorical(y_test, NUM_CLASSES)

    # Build the CNN model
    model = Sequential()
    model.add(Conv1D(32, kernel_size=KERNEL_SIZE, activation='relu', input_shape=INPUT_SHAPE))
    model.add(MaxPooling1D(pool_size=3))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, activation='softmax'))

    # Compile, train, and print score for this model on test data
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])

    # Evaluate using first half of test data for validation
    test_data_num_samples = x_test.shape[0]
    validation_data = (x_test[:(test_data_num_samples // 2)], y_test[:(test_data_num_samples // 2)])
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              verbose=1,
              validation_data=validation_data)

    score = model.evaluate(x_test[(test_data_num_samples // 2):], y_test[(test_data_num_samples // 2):],
                           verbose=0)
    print("Test data accuracy:", score[1])


if __name__ == "__main__":
    main()
