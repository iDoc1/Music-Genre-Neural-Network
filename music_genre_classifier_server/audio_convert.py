import subprocess
import os


class ConvertedAudioWav:
    """
    This class represents an audio converter that takes a given MP3 audio
    file and can convert that file to a wav file
    """

    def __init__(self, file_name):
        self._file_name = file_name
        self._wav_saved = False

    def convert_mp3_to_wav(self):
        """
        Use a ffmpeg subprocess to convert the given MP3 file to a wav file
        and save in the current directory
        """

        # Check that the file is an MP3 file
        if self.get_filetype() == "mp3":
            base = self._get_base_name()

            # Only perform subprocess if file not already saved -hide_banner -loglevel error
            if not self._wav_saved:
                subprocess.call(['ffmpeg', '-loglevel', 'error', '-i', self._file_name,
                                 base + '.wav'])
                self._wav_saved = True
        else:
            raise ValueError("File type not MP3")

    def get_filetype(self):
        """
        Returns the file extension of this object's associated audio file
        """
        return self._get_ext_name()

    def _get_base_name(self):
        """
        Returns base name of file without extension
        """
        base, ext = self._file_name.split(".")
        return base

    def _get_ext_name(self):
        """
        Returns extension of file name without base
        """
        base, ext = self._file_name.split(".")
        return ext

    def delete_wav_file(self):
        """
        Deletes saved wav file associated with this object
        """
        if self._wav_saved:
            wav_name = self._get_base_name() + ".wav"
            try:
                os.remove(wav_name)
            except OSError:
                pass
            else:
                self._wav_saved = False

    def get_wav_file_name(self):
        """
        Returns the name of the converted wav file
        """
        if self._wav_saved:
            return self._get_base_name() + ".wav"

    def get_file_name(self):
        return self._file_name


# Test code
if __name__ == "__main__":
    convert = ConvertedAudioWav("ACDC - Back In Black (Official Video).mp3")
    print(convert.get_filetype())
    convert.convert_mp3_to_wav()
    # convert.delete_wav_file()
