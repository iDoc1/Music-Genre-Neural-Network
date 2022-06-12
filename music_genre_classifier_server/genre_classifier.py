import tensorflow as tf
from keras.models import load_model
import numpy as np
from audio_download import YouTubeAudioMp3
from audio_convert import ConvertedAudioWav
from scipy.io.wavfile import read, write


SAMPLING_RATE_MODEL = 22050  # The Hz value that the model was trained with
AUDIO_LENGTH_MODEL = 3 * SAMPLING_RATE_MODEL  # 3 seconds long audio
SAMPLE_WIDTH_MODEL = 50  # Keep every 50th data point
MIN_AUDIO_LENGTH = 10  # Audio must be at least 9 seconds long


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
        middle_sample = self._preprocess_audio(samp_rate, wav_data)


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

        # Only keep 1st channel of audio
        wav_data = wav_data[:, 1]

        # Convert audio to sampling rate needed by the model
        samp_rate_ratio = samp_rate // SAMPLING_RATE_MODEL
        wav_data = wav_data[0::samp_rate_ratio]

        # Save 3 second sample from middle of wav file in increments of 50
        wav_data_middle_index = wav_data.shape[0] // 2
        sample_start_idx = int(wav_data_middle_index - (SAMPLING_RATE_MODEL * 1.5))
        middle_sample = np.zeros((AUDIO_LENGTH_MODEL // SAMPLE_WIDTH_MODEL, 1), dtype="int16")
        middle_sample[:, 0] = wav_data[sample_start_idx:sample_start_idx + AUDIO_LENGTH_MODEL:SAMPLE_WIDTH_MODEL]

        return middle_sample

    def get_model(self):
        return self._model


class SamplingRateTooLowError(Exception):
    """
    This error is to be raised when the passed audio wav file has a sampling
    rate less than desired
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