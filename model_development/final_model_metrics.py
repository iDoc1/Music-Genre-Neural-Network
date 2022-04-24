# Author: Ian Docherty
# Description: This script takes the final model h5 file, runs the test dataset on
#              the model, then prints metrics describing the results


import tensorflow as tf
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

NUM_CLASSES = 10


def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(NUM_CLASSES), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


def print_confusion_matrix(labels, predictions):
    conf_matrix = tf.math.confusion_matrix(labels, predictions, num_classes=NUM_CLASSES)
    conf_matrix = np.array(conf_matrix)
    conf_matrix = conf_matrix / conf_matrix.sum(axis=1)[:, None]
    conf_matrix = np.round(conf_matrix, decimals=2)

    headers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    table = tabulate(conf_matrix, headers, tablefmt="fancy_grid", showindex="always")
    print(table)


def main():

    # Load mode and test data
    model = load_model("./final_model/gtzan_2d_cnn_deep0.h5")
    test_data = np.load("./spectrogram_100x160_datasets/gtzan_spect_test_images.npy")
    test_labels = np.load("./spectrogram_100x160_datasets/gtzan_spect_test_labels.npy").astype("uint8")

    # Normalize values and format labels to be used by TF
    test_data = test_data.astype("float32") / 255
    # y_test = keras.utils.to_categorical(y_test, NUM_CLASSES)

    # 2nd half of test data is the test data that was not used as validation data during training
    test_data_num_samples = test_data.shape[0]
    test_data = test_data[(test_data_num_samples // 2):]
    test_labels = test_labels[(test_data_num_samples // 2):]

    # Get predictions for test data
    test_data_predictions = model.predict(test_data)
    test_data_predictions_labels = np.argmax(test_data_predictions, axis=1)

    # Show metrics
    print_confusion_matrix(test_labels, test_data_predictions_labels)


if __name__ == "__main__":
    main()
