from flask import Flask, request, jsonify
import os
from youtube_search import YouTubeSearch
from flask_cors import CORS

# Configuration
app = Flask(__name__)
CORS(app)


# Routes
@app.route('/getYouTubeResults', methods=['GET'])
def get_youtube_results():
    """
    Responds with a list of YouTube video URLs and thumbnail image URLs
    """

    # If the given song name is empty then return an empty list
    if request.args.get("songName") == "":
        return jsonify([])

    youtube_search = YouTubeSearch(request.args.get("songName"), 3)
    video_id_list = youtube_search.get_video_ids()

    # If no search result was returned then return empty list

    # Build video URL and thumbnail URL list
    url_list = []
    thumbnail_list = []
    base_url = "https://www.youtube.com/watch?v="
    thumbnail_base_url = "https://img.youtube.com/vi/"

    for video_id in video_id_list:
        url_list.append(base_url + video_id)
        thumbnail_list.append(thumbnail_base_url + video_id + "/0.jpg")

    # Get video title list
    title_list = youtube_search.get_video_titles()

    # Build dict to return
    results = {"video_urls": url_list, "thumbnail_urls": thumbnail_list, "video_titles": title_list}
    return jsonify(results)


@app.route('/test', methods=['GET'])
def get_test():
    return {'Name': "geek",
            "Age": "22",
            "Date": "today",
            "programming": "python"}


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8050))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
