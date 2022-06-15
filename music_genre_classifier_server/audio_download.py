from pytube import YouTube
import os


class YouTubeAudioMp3:
    """
    This class represents an audio file that has been downloaded from
    a given YouTube URL
    """

    def __init__(self, url):
        self._youtube_obj = YouTube(url)
        self._audio_filepath = None

    def download_and_save_audio_file(self):
        """
        Downloads YouTube video as an MP3 file to the given filename in
        the current directory. This code was adapted from the following source:
        https://www.geeksforgeeks.org/download-video-in-mp3-format-using-pytube/
        """
        video = self._youtube_obj.streams.filter(only_audio=True).first()
        output_file = video.download()

        # Create MP3 file name
        base, ext = os.path.splitext(output_file)
        new_file = base + ".mp3"

        # Remove file if it already exists, then rename
        try:
            os.remove(new_file)
        except OSError:
            pass

        os.rename(output_file, new_file)
        self._audio_filepath = new_file

    def delete_audio_file(self):
        """
        Deletes the downloaded audio file associated with this object
        """
        if self._audio_filepath is not None:
            os.remove(self._audio_filepath)
            self._audio_filepath = None

    def get_file_name(self):
        """
        Extracts the file name from the filepath and returns it
        """
        if self._audio_filepath is not None:
            return self._audio_filepath.split("\\")[-1]

    def get_youtube_obj(self):
        """
        Returns the YouTube object
        """
        return self._youtube_obj

    def get_filepath(self):
        """
        Returns the filepath associated with the downloaded audio. Returns
        None if no audio has been downloaded.
        """
        if self._audio_filepath is not None:
            return self._audio_filepath.replace("\\", "/")  # User posix forward slash


# Test code to download a video
if __name__ == "__main__":
    yt = YouTubeAudioMp3("https://www.youtube.com/watch?v=pAgnJDJN4VA&ab_channel=acdcVEVO")
    yt.download_and_save_audio_file()
    print(yt.get_filepath())
    print(yt.get_file_name())
    yt.delete_audio_file()
