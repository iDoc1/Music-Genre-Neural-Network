from flask import Flask, request, jsonify
import os
from youtube_search import YouTubeSearch
from flask_cors import CORS

# Configuration
app = Flask(__name__)
CORS(app)


# Routes
@app.route('/youtube-search-results', methods=['GET'])
def get_youtube_results():
    """
    Responds with a JSON string of YouTube video URLs and thumbnail image URLs
    """

    # If the given song name is empty then return an empty list
    if request.args.get("songName") == "":
        return jsonify([])

    youtube_search = YouTubeSearch(request.args.get("songName"), 3)
    video_id_list = youtube_search.get_video_ids()

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


@app.route('/model-results', methods=['GET'])
def model_results():
    """
    Request should contain a URL to a YouTube video. Audio will be extracted and
    run through the neural network model, then a JSON string of the resulting
    probabilities for each class/genre of music will be sent in the response.
    """
    pass


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8050))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
