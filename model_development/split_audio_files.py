# Author: Ian Docherty
# Description: This script reads all the 30-second raw GTZAN audio files then
#              splits them into 3 second chunks. New files are saved in the
#              split_audio directory and a corresponding file list is saved.

import shutil
import os
from scipy.io.wavfile import read, write


def split_audio(filelist, output_dir):

    # For each file in the filelist, split into 3 second chunks and save to output directory
    all_file_list = [file.rstrip() for file in open(filelist)]
    split_filelist = []  # To store new file names

    for file in all_file_list:
        wav_file_path, label = file.split(" ")
        samp_rate, wav_audio_arr = read(wav_file_path)

        # Get file names so new file name can be appended
        curr_file_name = wav_file_path.split("/")[-1][:-4]  # -4 removes .wav extension

        start_split = 0
        end_split = samp_rate * 3  # End first split at 3 second mark

        # Split into nine 3 second chunks since min file length is 29.9 seconds
        for index in range(9):

            # Extract and save 3 second split
            split_wav_arr = wav_audio_arr[start_split:end_split]
            new_file_name = output_dir + curr_file_name + ".split" + str(index) + ".wav"
            write(new_file_name, samp_rate, split_wav_arr)

            split_filelist.append(new_file_name + " " + label)

            # Advance by 3 seconds
            start_split += (samp_rate * 3)
            end_split += (samp_rate * 3)

    with open("gtzan_raw_split_filelist.txt", "w") as file:
        for file_path in split_filelist:
            file.write(file_path + "\n")


def main():

    # Create output directories
    try:
        shutil.rmtree("split_audio")
    except FileNotFoundError:
        os.mkdir("split_audio")
    else:
        os.mkdir("split_audio")

    split_audio("gtzan_raw_filelist.txt", "./split_audio/")


if __name__ == "__main__":
    main()

