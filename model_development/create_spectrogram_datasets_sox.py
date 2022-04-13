# Author: Ian Docherty
# Description: The script uses the raw or augmented split audio files to create spectrogram
#              images which are then stored as train and test numpy arrays to be used by the
#              2D convolutional neural network.
#
# Citation: Portions of this code have been adapted from chapter 15 from the following textbook
#   Title: Practical Deep Learning: A Python-Based Introduction
#   Author: Ronald T. Kneusel
#   Link to book website: https://nostarch.com/practical-deep-learning-python


import os
import shutil
from time import sleep
import numpy as np
import random
from PIL import Image
from balance_datasets import get_balanced_datasets

IMAGE_ROWS = 100
IMAGE_COLS = 160


def build_spectrogram_datasets(filelist):
    random.shuffle(filelist)  # Randomize input file list

    image_data = np.zeros((len(filelist), IMAGE_ROWS, IMAGE_COLS, 3), dtype='uint8')
    labels = np.zeros(len(filelist), dtype='uint8')

    # Iterate over each file and create a spectrogram
    for index, file_path in enumerate(filelist):
        print("Creating spectrogram for file #%s" % str(index))
        source_file, label = file_path.split(" ")

        # Use sox to create spectrogram image in current directory
        os.system("sox %s -n spectrogram -z 60" % source_file)  # High contrast
        image_arr = np.array(Image.open("spectrogram.png").convert('RGB'))

        # Extract the spectrogram image by eliminating the borders and info section
        image_arr = image_arr[42:542, 58:858, :]

        # Resize image to reduce data
        image_arr = Image.fromarray(image_arr).resize((IMAGE_COLS, IMAGE_ROWS))

        # Insert current spectrogram image into image array
        image_data[index, :, :, :] = np.array(image_arr)
        labels[index] = label

        # Prevent strange issue where permission error occurs on my PC
        try:
            os.remove("spectrogram.png")
        except PermissionError:
            sleep(1)
            os.remove("spectrogram.png")

    # Get dataset arrays that are uniformly balanced by each class
    train_data, train_labels, test_data, test_labels = get_balanced_datasets(image_data, labels, 90)

    np.save("./spectrogram_100x160_hc_datasets/gtzan_spect_train_images.npy", train_data)
    np.save("./spectrogram_100x160_hc_datasets/gtzan_spect_train_labels.npy", train_labels)
    np.save("./spectrogram_100x160_hc_datasets/gtzan_spect_test_images.npy", test_data)
    np.save("./spectrogram_100x160_hc_datasets/gtzan_spect_test_labels.npy", test_labels)


def main():

    # Create output directories
    try:
        shutil.rmtree("spectrogram_100x160_hc_datasets")
    except FileNotFoundError:
        os.mkdir("spectrogram_100x160_hc_datasets")
    else:
        os.mkdir("spectrogram_100x160_hc_datasets")

    # Read file list for split audio files then save spectrogram datasets
    all_file_list = [file.rstrip() for file in open("gtzan_raw_split_filelist.txt")]
    build_spectrogram_datasets(all_file_list)


if __name__ == "__main__":
    main()
