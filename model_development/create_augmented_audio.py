# Author: Ian Docherty
# Description: This script takes the split audio files and produces an additional 3
#              augmented audio files by applying time shift, random noise, pitch shift,
#              and time lengthening/compressing to the original audio at random.
#
# Citation: Portions of this code have been adapted from chapter 15 from the following textbook
#   Title: Practical Deep Learning: A Python-Based Introduction
#   Author: Ronald T. Kneusel
#   Link to book website: https://nostarch.com/practical-deep-learning-python


import os
import shutil
import random
import numpy as np
import librosa as rosa
from scipy.io.wavfile import read, write


def augment_audio(file_list):
    aug_file_list = []  # To store augmented file paths and associated class

    for index, file in enumerate(file_list):
        print("Processing audio file #" + str(index) + "...")

        # Get file name and path from file list
        wav_file_path, label = file.split(" ")
        wav_file_name = wav_file_path.split("/")[-1][:-4]  # Name without .wav extension
        wav = read(wav_file_path)

        # Write original sample
        orig_file_path = "./augmented_split_audio/" + wav_file_name + ".wav"
        aug_file_list.append(orig_file_path + " " + label)
        write(orig_file_path, wav[0], wav[1])

        # Create 3 additional augmented samples
        for aug_index in range(3):
            aug_audio = random_augment(wav)
            aug_file_path = "./augmented_split_audio/" + wav_file_name + ".aug" + str(aug_index) + ".wav"
            write(aug_file_path, wav[0], aug_audio.astype(wav[1].dtype))
            aug_file_list.append(aug_file_path + " " + label)

    # Save file list with file paths for each augmented sampe
    with open("gtzan_aug_split_filelist.txt", "w") as file:
        for file_path in aug_file_list:
            file.write(file_path + "\n")


def random_augment(wav):
    samp_rate = wav[0]
    sound_data = wav[1].astype('float32')

    # Perform shift by at most 0.25 seconds with a 50% probability
    if random.random() < 0.5:
        shift = int(samp_rate / 4.0 * (np.random.random() - 0.5))
        sound_data = np.roll(sound_data, shift)

        # Set data before of after shift to 0
        if shift < 0:  # If data shifted to the left
            sound_data[shift:] = 0
        else:
            sound_data[:shift] = 0

    # Add random noise up to 1/10 of the range of the audio signal
    if random.random() < 0.5:
        audio_range = sound_data.max() - sound_data.min()

        # Broadcast random noise to each element in the sound data array
        sound_data += 0.1 * audio_range * np.random.random(sound_data.shape)

    # Apply pitch shift in range -10 to 10
    if random.random() < 0.5:
        pitch_shift = 20.0 * (np.random.random() - 0.5)
        sound_data = rosa.effects.pitch_shift(sound_data, sr=samp_rate, n_steps=pitch_shift)

    # Stretch or compress time by a rate of 0.5 to 1.5
    if random.random() < 0.5:
        rate = 1.0 + (np.random.random() - 0.5)
        sound_data = rosa.effects.time_stretch(sound_data, rate=rate)

        # Chop off extra samples if audio was stretched
        if sound_data.shape[0] > wav[1].shape[0]:
            sound_data = sound_data[:wav[1].shape[0]]  # Chop off end of audio

        # Add zeroes if audio was compressed
        else:
            sound_copy = np.zeros(wav[1].shape[0], dtype='float32')
            sound_copy[:sound_data.shape[0]] = sound_data  # Leave the end of array as zeroes
            sound_data = sound_copy.copy()

    return sound_data


def main():

    # Create output directories
    try:
        shutil.rmtree("augmented_split_audio")
    except FileNotFoundError:
        os.mkdir("augmented_split_audio")
    else:
        os.mkdir("augmented_split_audio")

    # Read file list for split audio files then save augmented versions of each file
    all_file_list = [file.rstrip() for file in open("gtzan_raw_split_filelist.txt")]
    augment_audio(all_file_list)


if __name__ == "__main__":
    main()
