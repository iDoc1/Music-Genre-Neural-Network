# Author: Ian Docherty
# Description: This script finds each WAV file in the GTZAN_dataset directory and
#              builds a file list the contains the absolute file path and the
#              corresponding class (genre) separated by a space

import os
import shutil


def build_filelist():

    # Define class numbers for each music genre
    classes = {"blues": 0,
               "classical": 1,
               "country": 2,
               "disco": 3,
               "hiphop": 4,
               "jazz": 5,
               "metal": 6,
               "pop": 7,
               "reggae": 8,
               "rock": 9}

    gtzan_audio_dir = "../GTZAN_dataset/"
    raw_data_filelist = []  # List to store file path and corresponding class numbers

    # Add each file path and class to list
    for root, dirs, files in os.walk(gtzan_audio_dir, topdown=True):

        for file in files:
            if file[-3:] == "wav":
                genre, file_num, file_type = file.split(".")
                rel_file_path = gtzan_audio_dir + genre + "/" + file
                raw_data_filelist.append(rel_file_path + " " + str(classes[genre]))

    # Save file list to disk
    with open("gtzan_raw_filelist.txt", "w") as file:
        for file_path in raw_data_filelist:
            file.write(file_path + "\n")


if __name__ == "__main__":
    build_filelist()
