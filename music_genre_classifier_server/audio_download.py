from pytube import YouTube
import os


class YouTubeAudio:
    """
    This class represents an audio file that has been downloaded from
    a given YouTube URL
    """

    def __init__(self, url):
        self._youtube_obj = YouTube(url)
        self._download_filename = None

    def download_and_save_audio_file(self, output_filename):
        """
        Downloads YouTube video as an MP3 file to the given filename in
        the current directory. This code was adapted from the following source:
        https://www.geeksforgeeks.org/download-video-in-mp3-format-using-pytube/
        """
        video = self._youtube_obj.streams.filter(only_audio=True).first()
        output_file = video.download()

        # Rename as given filename in MP3 format
        new_file = output_filename + ".mp3"

        # Remove file if it already exists
        try:
            os.remove(new_file)

        # Create file if it doesn't exist
        except FileNotFoundError:
            os.rename(output_file, new_file)
            self._download_filename = new_file
        else:
            os.rename(output_file, new_file)
            self._download_filename = new_file

    def delete_audio_file(self):
        """
        Deletes the downloaded audio file associated with this object
        """
        if self._download_filename is not None:
            os.remove(self._download_filename)

    def get_youtube_obj(self):
        """
        Returns the YouTube object
        """
        return self._youtube_obj

    def get_filename(self):
        """
        Returns the filename associated with the downloaded audio. Returns
        None if no audio has been downloaded.
        """
        if self._download_filename is not None:
            return self._download_filename


# Test code to download a video
if __name__ == "__main__":
    yt = YouTubeAudio("https://www.youtube.com/watch?v=pAgnJDJN4VA&ab_channel=acdcVEVO")
    yt.download_and_save_audio_file("test_file1")
