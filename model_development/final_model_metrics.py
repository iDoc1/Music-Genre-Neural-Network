# Author: Ian Docherty
# Description: This script takes the final model h5 file, runs the test dataset on
#              the model, then prints metrics describing the results


import tensorflow as tf
from keras.models import load_model
import numpy as np
from tabulate import tabulate
from sklearn.metrics import classification_report

NUM_CLASSES = 10
LABELS = {0: "blues",
          1: "classical",
          2: "country",
          3: "disco",
          4: "hiphop",
          5: "jazz",
          6: "metal",
          7: "pop",
          8: "reggae",
          9: "rock"}


def print_confusion_matrix(labels, predictions):
    conf_matrix = tf.math.confusion_matrix(labels, predictions, num_classes=NUM_CLASSES)
    conf_matrix = np.array(conf_matrix)
    conf_matrix = conf_matrix / conf_matrix.sum(axis=1)[:, None]
    conf_matrix = np.round(conf_matrix, decimals=2)

    headers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    table = tabulate(conf_matrix, headers, tablefmt="fancy_grid", showindex="always")
    print("Confusion Matrix: (rows=actual labels, cols=predicted labels)")
    print(table)
    print()


def print_classification_report(test_labels, prediction_labels):
    print("Classification Report:")
    print(classification_report(y_true=test_labels, y_pred=prediction_labels))
    print()


def print_labels_and_classes():
    print("Label        Class")
    for label in LABELS:
        print(" ", label, "\t\t", LABELS[label])
    print()


def main():

    # Load model and test data
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
    print_labels_and_classes()
    print_confusion_matrix(test_labels, test_data_predictions_labels)
    print_classification_report(test_labels, test_data_predictions_labels)


if __name__ == "__main__":
    main()
