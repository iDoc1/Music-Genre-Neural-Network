# Author: Ian Docherty
# Description: This script takes the GTZAN raw filelist containing the paths of
#              the raw data, then saves a numpy dataset to be used by the machine
#              learning models. Since there is a lot of data, only every 50th data
#              point in the WAV file is kept.

import os
import shutil
import numpy as np
import random
from scipy.io.wavfile import read

SAMPLING_RATE = 22050  # Half the standard Hz for music audio
AUDIO_LENGTH = 3 * SAMPLING_RATE  # 3 seconds long audio
SAMPLE_WIDTH = 50  # Keep every 50th data point


def build_numpy_dataset(file_list, train_or_test):

    # Create empty arrays to store WAV file data
    dataset = np.zeros((len(file_list), AUDIO_LENGTH // SAMPLE_WIDTH, 1), dtype="int16")  # 1 channel
    labels = np.zeros(len(file_list), dtype="uint8")

    for index, file in enumerate(file_list):
        file_path, label = file.split(" ")

        # Keep only the first 3 seconds at every 50th data point
        dataset[index, :, 0] = read(file_path)[1][:AUDIO_LENGTH:SAMPLE_WIDTH]
        labels[index] = int(label)

    # Save to numpy files
    np.save("./raw_split_datasets/gtzan_raw_split_" + train_or_test + "_audio.npy", dataset)
    np.save("./raw_split_datasets/gtzan_raw_split_" + train_or_test + "_labels.npy", labels)


if __name__ == "__main__":

    # Create output directories
    try:
        shutil.rmtree("raw_split_datasets")
    except FileNotFoundError:
        os.mkdir("raw_split_datasets")
    else:
        os.mkdir("raw_split_datasets")

    # Read file list, randomize, then split data into train and test sets
    all_file_list = [file.rstrip() for file in open("gtzan_raw_split_filelist.txt")]
    random.shuffle(all_file_list)

    # Split into 90% train, 10% test
    num_of_files = len(all_file_list)
    train = all_file_list[:(9 * num_of_files // 10)]
    test = all_file_list[(9 * num_of_files // 10):]  # 10% goes to test set

    build_numpy_dataset(train, "train")
    build_numpy_dataset(test, "test")
