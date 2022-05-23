from flask import Flask, render_template, request, jsonify
import os
from youtube_search import YouTubeClient

# Configuration
app = Flask(__name__)


# Routes
@app.route('/getYouTubeResults', methods=['GET'])
def get_youtube_results():
    """
    Responds with a list of YouTube URLs and thumbnail image resource URLs
    """

    # If the given song name is empty then return an empty list
    if request.args.get("songName") == "":
        return jsonify([])

    youtube_client = YouTubeClient()
    search_results = youtube_client.search(request.args.get("songName"), 3)

    # Build video URL and thumbnail URL list
    url_list = []
    thumbnail_list = []
    base_url = "https://www.youtube.com/watch?v="
    thumbnail_base_url = "https://img.youtube.com/vi/"

    for video_id in search_results:
        url_list.append(base_url + video_id)
        thumbnail_list.append(thumbnail_base_url + video_id + "/0.jpg")

    # Build dict to return
    results = {"video_urls": url_list, "thumbnail_urls": thumbnail_list}
    return jsonify(results)


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8050))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
