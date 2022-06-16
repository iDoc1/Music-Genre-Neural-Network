import tensorflow as tf
import numpy as np
import os
from keras.models import load_model
from audio_download import YouTubeAudioMp3
from audio_convert import ConvertedAudioWav
from scipy.io.wavfile import read, write
from PIL import Image


SAMPLING_RATE_MODEL = 22050  # The Hz value that the model was trained with
AUDIO_LENGTH_MODEL = 3 * SAMPLING_RATE_MODEL  # 3 seconds long audio
MIN_AUDIO_LENGTH = 60  # Min accepted audio length in seconds
IMAGE_ROWS = 100  # Spectrogram image rows
IMAGE_COLS = 160  # Spectrogram image columns


class MusicGenreClassifier:
    """
    This class represents the trained neural network model that is
    capable of taking an input wav file and producing the resulting
    probabilities that the wav audio is of a certain genre
    """

    def __init__(self):
        self._model = load_model("../model_development/final_model/gtzan_2d_cnn_deep0.h5")

        # Class numbers as trained in the neural network
        self._classes = {1: "blues",
                         2: "classical",
                         3: "country",
                         4: "disco",
                         5: "hiphop",
                         6: "jazz",
                         7: "metal",
                         8: "pop",
                         9: "reggae",
                         0: "rock"}

    def classify_youtube_audio(self, youtube_url):
        """
        Downloads the audio from the given YouTube URL then runs it through the
        model and returns the resulting softmax probabilities
        """
        converted_audio_wav = self._save_youtube_wav_audio(youtube_url)
        samp_rate, wav_data = read(converted_audio_wav.get_wav_file_name())

        # Check if downloaded audio has adequate sampling rate
        if samp_rate < SAMPLING_RATE_MODEL:
            raise SamplingRateTooLowError("Sampling rate must be at least " + str(SAMPLING_RATE_MODEL) + " Hz")

        # Check if downloaded audio meets minimum length
        audio_length_seconds = wav_data.shape[0] / samp_rate
        if audio_length_seconds < MIN_AUDIO_LENGTH:
            raise AudioLengthTooLowError("Audio length must be at least " + str(MIN_AUDIO_LENGTH) + " seconds")

        # Process wav file and create spectrogram
        wav_sample_files = self._preprocess_audio(samp_rate, wav_data)
        spectrogram_images_arr = self._create_spectrogram(wav_sample_files)

        # Run spectrogram image array through model to get resulting probabilities
        self._get_model_predictions(spectrogram_images_arr)

        converted_audio_wav.delete_wav_file()

    def _save_youtube_wav_audio(self, youtube_url):
        """
        Downloads and saves a wav audio file from the given YouTube URL. Returns
        the ConvertedAudioWav object associated with the download.
        """

        # Download audio to mp3
        youtube_audio_mp3 = YouTubeAudioMp3(youtube_url)
        youtube_audio_mp3.download_and_save_audio_file()

        # Convert to wav
        mp3_file_name = youtube_audio_mp3.get_file_name()
        converted_audio_wav = ConvertedAudioWav(mp3_file_name)
        converted_audio_wav.convert_mp3_to_wav()

        # Delete old MP3 and return WAV object
        youtube_audio_mp3.delete_audio_file()
        return converted_audio_wav

    def _preprocess_audio(self, samp_rate, wav_data):
        """
        Converts audio to the desired sampling rate and trims it to 3 seconds long
        for input into the model. Returns a reference to the resulting numpy array.
        """

        # Only keep one channel of audio
        wav_data = wav_data[:, 1]

        # Convert audio to sampling rate needed by the model
        samp_rate_ratio = samp_rate // SAMPLING_RATE_MODEL
        wav_data = wav_data[0::samp_rate_ratio]

        # Save 3 second sample from middle of wav file
        mid_sample_start_idx = int((wav_data.shape[0] // 2) - (SAMPLING_RATE_MODEL * 1.5))
        middle_sample = np.zeros((AUDIO_LENGTH_MODEL, 1), dtype="int16")
        middle_sample[:, 0] = wav_data[mid_sample_start_idx:mid_sample_start_idx + AUDIO_LENGTH_MODEL]
        middle_wav_file = "./middle_sample.wav"
        write(middle_wav_file, SAMPLING_RATE_MODEL, middle_sample)

        # Save 3 second sample from beginning of wav file
        begin_sample_start_idx = int(SAMPLING_RATE_MODEL * 10)  # 10 seconds from start of wav file
        begin_sample = np.zeros((AUDIO_LENGTH_MODEL, 1), dtype="int16")
        begin_sample[:, 0] = wav_data[begin_sample_start_idx:begin_sample_start_idx + AUDIO_LENGTH_MODEL]
        begin_wav_file = "./start_sample.wav"
        write(begin_wav_file, SAMPLING_RATE_MODEL, begin_sample)

        # Save 3 second sample from end of wav file
        end_sample_start_idx = int(wav_data.shape[0] - (SAMPLING_RATE_MODEL * 10))  # 10 seconds from end of wav file
        end_sample = np.zeros((AUDIO_LENGTH_MODEL, 1), dtype="int16")
        end_sample[:, 0] = wav_data[end_sample_start_idx:end_sample_start_idx + AUDIO_LENGTH_MODEL]
        end_wav_file = "./end_sample.wav"
        write(end_wav_file, SAMPLING_RATE_MODEL, end_sample)

        return begin_wav_file, middle_wav_file, end_wav_file

    def _create_spectrogram(self, wav_sample_files):
        """
        Takes a numpy array of a 3-second wav audio sample, then uses SOX to build a
        spectrogram image. Returns a numpy array of the spectrogram image.
        """
        image_data = np.zeros((len(wav_sample_files), IMAGE_ROWS, IMAGE_COLS, 3), dtype='uint8')

        for index, source_file in enumerate(wav_sample_files):

            # Create spectrogram from wav file and save in memory
            os.system("sox %s -n spectrogram" % source_file)
            image_arr = np.array(Image.open("spectrogram.png").convert('RGB'))
            os.remove(source_file)
            os.remove("spectrogram.png")

            # Extract the spectrogram image by eliminating the borders and info section
            image_arr = image_arr[42:542, 58:858, :]

            # Resize image to expected model size then return image data array
            image_arr = Image.fromarray(image_arr).resize((IMAGE_COLS, IMAGE_ROWS))
            # image_data = np.zeros((1, IMAGE_ROWS, IMAGE_COLS, 3), dtype='uint8')
            image_data[index, :, :, :] = np.array(image_arr)

        return image_data

    def _get_model_predictions(self, spectrogram_arr):
        """
        Runs the given spectrogram numpy image array through the model then returns
        the resulting per-class probabilities as a list of lists
        """

        # Normalize the image array values to range [0, 1] for Tensorflow input
        spectrogram_arr = spectrogram_arr.astype("float32") / 255

        # Run image array through the model
        predictions = self._model.predict(spectrogram_arr, verbose=0)
        return predictions.tolist()


class SamplingRateTooLowError(Exception):
    """
    This error is to be raised when the passed audio wav file has a sampling
    rate less than needed by the model
    """
    pass


class AudioLengthTooLowError(Exception):
    """
    This error is to be raised when the passed audio wav file is does not meet
    the minimum specified length
    """
    pass


if __name__ == "__main__":
    classifier = MusicGenreClassifier()
    classifier.classify_youtube_audio("https://www.youtube.com/watch?v=pAgnJDJN4VA&ab_channel=acdcVEVO")
    # classifier.classify_youtube_audio("https://www.youtube.com/watch?v=u9Dg-g7t2l4&ab_channel=Disturbed")
    # classifier.classify_youtube_audio("https://www.youtube.com/watch?v=BSzSn-PRdtI&ab_channel=Maroon5VEVO")  # Maroon5