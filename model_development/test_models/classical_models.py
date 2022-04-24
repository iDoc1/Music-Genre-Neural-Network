# Author: Ian Docherty
# Description: This script uses the given datasets to train and test a variety
#              of classical machine learning models, then prints the results

import numpy as np
from sklearn.neighbors import NearestCentroid, KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC


def run_model(x_train, y_train, x_test, y_test, classifier):
    classifier.fit(x_train, y_train)
    score = classifier.score(x_test, y_test)
    print("Test Data Score: %0.4f" % score)


def train(x_train, y_train, x_test, y_test):
    print("Nearest centroid: ", end="")
    run_model(x_train, y_train, x_test, y_test, NearestCentroid())

    print("kNN classifier (k=3): ", end="")
    run_model(x_train, y_train, x_test, y_test, KNeighborsClassifier(n_neighbors=3))

    print("kNN classifier (k=6): ", end="")
    run_model(x_train, y_train, x_test, y_test, KNeighborsClassifier(n_neighbors=6))

    print("Naive Bayes Gaussian: ", end="")
    run_model(x_train, y_train, x_test, y_test, GaussianNB())

    print("Random Forest (trees=5): ", end="")
    run_model(x_train, y_train, x_test, y_test, RandomForestClassifier(n_estimators=5))

    print("Random Forest (trees=50): ", end="")
    run_model(x_train, y_train, x_test, y_test, RandomForestClassifier(n_estimators=50))

    print("Random Forest (trees=500): ", end="")
    run_model(x_train, y_train, x_test, y_test, RandomForestClassifier(n_estimators=500))

    print("LinearSVM (C=0.01): ", end="")
    run_model(x_train, y_train, x_test, y_test, LinearSVC(C=0.01))

    print("LinearSVM (C=0.1): ", end="")
    run_model(x_train, y_train, x_test, y_test, LinearSVC(C=0.1))


def main():

    # Load first two dimensions of data (last dim is only for Tensorflow models)
    x_train = np.load("aug_split_datasets/gtzan_aug_split_train_audio.npy")[:, :, 0]
    y_train = np.load("aug_split_datasets/gtzan_aug_split_train_labels.npy")
    x_test = np.load("aug_split_datasets/gtzan_aug_split_test_audio.npy")[:, :, 0]
    y_test = np.load("aug_split_datasets/gtzan_aug_split_test_labels.npy")

    # Scale data to the range to be in absolute value range [0, 1]
    x_train = (x_train.astype("float32") + 32768) / 65536  # 32768 is max 16 bit integer value in audio files
    x_test = (x_test.astype("float32") + 32768) / 65536

    train(x_train, y_train, x_test, y_test)


if __name__ == "__main__":
    main()
