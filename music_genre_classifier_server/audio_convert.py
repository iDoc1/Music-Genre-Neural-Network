import subprocess
import os


class AudioConverter:
    """
    This class represents an audio converter that takes a given audio
    file and can apply various conversions operations to that file
    """

    def __init__(self, filepath):
        self._filepath = filepath

    def convert_mp3_to_wav(self):
        """
        Use ffmpeg to convert the file at filepath to a wav file
        """
        subprocess.call(['ffmpeg', '-i', self._filepath,
                         'converted_to_wav_file.wav'])

    def get_filetype(self):
        """
        Returns the file extension of this object's associated audio file
        """
        base, ext = self._filepath.split(".")
        return ext

    def get_filepath(self):
        return self._filepath


if __name__ == "__main__":
    convert = AudioConverter("C:/Users/docma/Documents/Music-Genre-Neural-Network/music_genre_classifier_server/ACDC - Back In Black (Official Video).mp3")
    convert.convert_mp3_to_wav()