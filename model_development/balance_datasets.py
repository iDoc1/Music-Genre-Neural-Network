# Author: Ian Docherty
# Description: The purpose of this program is to take a full dataset of feature
#              vectors and corresponding labels, and produce a randomized,
#              balanced dataset for training and testing

import numpy as np


def get_balanced_datasets(x_dataset, y_labels, split_percent):
    """
    Takes the given dataset and labels, then returns training and testing
    datasets that are uniformly distributed among the classes, and have
    random ordering. Assumes dataset is already uniformly distributed
    among each class.
    :param x_dataset: Full dataset of feature vectors in 4-dimensions
    :param y_labels: Zero-indexed classes for x_dataset feature vectors
    :param split_percent: The percent of data to put in the training set (ex. 90 = 90%)
    :return: Tuple with (x_train, y_train, x_test, y_test)
    """

    num_of_classes, dataset_shape = get_dataset_dims(x_dataset, y_labels)

    # Split dataset into a dict of each class and initialize curr index for each class to zero
    dataset_by_class, curr_index_by_class = get_dataset_splits_dict(x_dataset, y_labels, num_of_classes, dataset_shape)

    # Create empty arrays for train and test data
    x_train, y_train, x_test, y_test = create_empty_arrays(x_dataset, dataset_shape, split_percent)

    # Copy elements from each class into given split percentage for train and test data
    copy_data_to_empty_sets(dataset_by_class, x_train, y_train, x_test, y_test, split_percent)

    # Randomize ordering of datasets
    x_train, y_train, x_test, y_test = randomize_datasets(x_train, y_train, x_test, y_test)

    return x_train, y_train, x_test, y_test


def get_dataset_dims(x_dataset, y_labels):
    """
    Returns dimensions and classes of given dataset
    :return: Tuple (num_of_classes, dim_rows, dim_cols, dim_channels)
    """
    num_of_classes = int(max(y_labels) + 1)
    dataset_shape = x_dataset.shape

    return num_of_classes, dataset_shape


def get_dataset_splits_dict(x_dataset, y_labels, num_of_classes, dataset_shape):
    """
    Splits dataset up by class using a dictionary. Creates a dictionary initialized
    with zeroes to be used to keep track of current index processed in the dataset
    split by class
    :return: Tuple dataset_by_class, curr_index_by_class
    """
    dataset_by_class = {}
    curr_index_by_class = {}
    samples_per_class = x_dataset.shape[0] // num_of_classes

    # Split dataset into classes 0 through number of classes
    for index in range(num_of_classes):
        dataset_by_class[index] = np.empty((samples_per_class, dataset_shape[1], dataset_shape[2], dataset_shape[3]))
        curr_index_by_class[index] = 0

    for data_index in range(y_labels.shape[0]):
        label = y_labels[data_index]
        class_index = curr_index_by_class[label]

        dataset_by_class[label][class_index] = x_dataset[data_index, :, :, :]
        curr_index_by_class[label] += 1

    return dataset_by_class, curr_index_by_class


def create_empty_arrays(x_dataset, dataset_shape, split_percent):
    """
    Creates empty datasets of the given split size
    :return: x_train, y_train, x_test, y_test
    """

    split_upper_boundary = (split_percent * x_dataset.shape[0] // 100)
    split_lower_boundary = (100 - split_percent) * x_dataset.shape[0] // 100
    x_train = np.empty((split_upper_boundary, dataset_shape[1], dataset_shape[2], dataset_shape[3]))
    y_train = np.empty(split_upper_boundary)
    x_test = np.empty((split_lower_boundary, dataset_shape[1], dataset_shape[2], dataset_shape[3]))
    y_test = np.empty(split_lower_boundary)

    return x_train, y_train, x_test, y_test


def copy_data_to_empty_sets(dataset_by_class, x_train, y_train, x_test, y_test, split_percent):
    """
    Copies the data from the by class dataset dictionary to the given training
    and testing datasets
    """
    x_train_curr_idx = 0
    x_test_curr_idx = 0
    for class_num in dataset_by_class:

        # split_percent samples to train set
        split_boundary = split_percent * dataset_by_class[class_num].shape[0] // 100
        for train_class_index in range(split_boundary):
            x_train[x_train_curr_idx] = dataset_by_class[class_num][train_class_index, :, :, :]
            y_train[x_train_curr_idx] = class_num
            x_train_curr_idx += 1

        # remaining samples to test set
        for test_class_index in range(split_boundary, dataset_by_class[class_num].shape[0]):
            x_test[x_test_curr_idx] = dataset_by_class[class_num][test_class_index, :, :, :]
            y_test[x_test_curr_idx] = class_num
            x_test_curr_idx += 1


def randomize_datasets(x_train, y_train, x_test, y_test):
    """
    Randomizes the order of the given datasets
    """
    idx = np.argsort(np.random.random(x_train.shape[0]))
    x_train = x_train[idx]
    y_train = y_train[idx]

    idx = np.argsort(np.random.random(x_test.shape[0]))
    x_test = x_test[idx]
    y_test = y_test[idx]

    return x_train, y_train, x_test, y_test
