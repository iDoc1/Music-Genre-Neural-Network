import subprocess
import os


class AudioConverter:
    """
    This class represents an audio converter that takes a given MP3 audio
    file and can convert that file to a wav file
    """

    def __init__(self, file_name):
        self._file_path = file_name

    def convert_mp3_to_wav(self):
        """
        Use a ffmpeg subprocess to convert the given MP3 file to a wav file
        and save in the current directory
        """

        # Check that the file is an MP3 file
        if self.get_filetype() == "mp3":
            subprocess.call(['ffmpeg', '-i', self._file_path,
                             'converted_to_wav_file.wav'])
        else:
            raise ValueError("File type not MP3")

    def get_filetype(self):
        """
        Returns the file extension of this object's associated audio file
        """
        base, ext = self._file_path.split(".")
        return ext

    def get_file_name(self):
        return self._file_path


# Test code
if __name__ == "__main__":
    convert = AudioConverter("ACDC - Back In Black (Official Video).mp3")
    convert.convert_mp3_to_wav()
