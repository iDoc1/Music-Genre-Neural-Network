# Author: Ian Docherty
# Description: Defines a YouTubeClient class that allows the client to run search
#              queries on Google's YouTube API

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import html


class YouTubeSearch:
    """
    This class represents a search performed on teh YouTube API
    """

    def __init__(self, search_string, max_results, duration):
        """
        Creates a YouTubeSearch object given a search string, max number of
        results, and a string 'short', 'medium', or 'long' specifying video
        length
        """

        # Get API key
        load_dotenv()
        api_key = os.getenv('YOUTUBE_API_KEY')

        # Create and execute search request, and store result
        request = build('youtube', 'v3', developerKey=api_key).search().list(
            part="snippet",
            maxResults=max_results,
            type="video",
            videoDuration=duration,
            q=search_string
        )
        self._response = request.execute()

    def get_video_ids(self):
        """
        Returns a list of video IDs stored in this YouTubeSearch object
        """
        video_id_list = []
        for video in self._response['items']:
            video_id_list.append(video['id']['videoId'])

        return video_id_list

    def get_video_titles(self):
        """
        Returns a list of video titles stored in this YouTubeSearch object
        """
        video_title_list = []
        for video in self._response['items']:
            video_title_list.append(html.unescape(video['snippet']['title']))  # Unescape HTML chars like '&'

        return video_title_list
