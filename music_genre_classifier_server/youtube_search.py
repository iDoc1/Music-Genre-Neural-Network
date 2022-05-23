# Author: Ian Docherty
# Description: Defines a YouTubeClient class that allows the client to run search
#              queries on Google's YouTube API

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class YouTubeClient:
    """
    This class represents a client that can search for YouTube videos
    """

    def __init__(self):
        load_dotenv()
        api_key = os.getenv('YOUTUBE_API_KEY')
        self._youtube_service = build('youtube', 'v3', developerKey=api_key)

    def search(self, search_string, max_results):
        """
        Given a search string, submits a GET request to the YouTube API using this string 
        as the search parameter, then returns the specified number of results as a list of
        video IDs
        :param search_string: the string to submit a search request for
        :param max_results: the max number of URLs to return
        :return: A list of URLs of the top 3 results
        """

        # Create and execute request
        request = self._youtube_service.search().list(
            part="snippet",
            maxResults=max_results,
            type="videos",
            q=search_string
        )
        response = request.execute()

        # Create URLs and store in a list
        video_id_list = []
        for video in response['items']:
            video_id_list.append(video['id']['videoId'])

        return video_id_list


# Test code to print search results for a specified query
if __name__ == "__main__":
    api = YouTubeClient()
    print(api.search("tim mcgraw", 3))
