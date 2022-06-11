from audio_download import YouTubeAudio
from audio_convert import AudioConverter


def save_youtube_wav_audio(youtube_url):
    """
    Downloads and saves a wav audio file from the given YouTube URL
    """

    # Download audio to mp3
    youtube_audio = YouTubeAudio(youtube_url)
    youtube_audio.download_and_save_audio_file()

    # Convert to wav
    mp3_file_name = youtube_audio.get_file_name()
    audio_converter = AudioConverter(mp3_file_name)
    audio_converter.convert_mp3_to_wav()

    youtube_audio.delete_audio_file()


if __name__ == "__main__":
    save_youtube_wav_audio("https://www.youtube.com/watch?v=pAgnJDJN4VA&ab_channel=acdcVEVO")
