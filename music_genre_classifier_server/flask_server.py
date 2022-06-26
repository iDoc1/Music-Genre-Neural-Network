from flask import Flask, request, jsonify
import os
from youtube_search import YouTubeSearch
from genre_classifier import MusicGenreClassifier
from flask_cors import CORS

# Configuration
app = Flask(__name__, static_folder='../music_genre_classifier_ui/build', static_url_path='/')
CORS(app)
classifier = MusicGenreClassifier()


# Routes
@app.route('/')
def index():
    """
    Returns the React UI production build files
    """
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/youtube-search-results', methods=['GET'])
def get_youtube_results():
    """
    Responds with a JSON string of YouTube video URLs and thumbnail image URLs
    """

    # If the given song name is empty then return an empty list
    if request.args.get("songName") == "":
        return jsonify([])

    # Combine results from short and medium duration queries
    youtube_search_short = YouTubeSearch(request.args.get("songName"), 3, "short")
    youtube_search_medium = YouTubeSearch(request.args.get("songName"), 3, "medium")
    video_id_list_short = youtube_search_short.get_video_ids()
    video_id_list_medium = youtube_search_medium.get_video_ids()
    video_id_list = video_id_list_short + video_id_list_medium

    # Build video URL and thumbnail URL list
    url_list = []
    thumbnail_list = []
    base_url = "https://www.youtube.com/watch?v="
    thumbnail_base_url = "https://img.youtube.com/vi/"

    for video_id in video_id_list:
        url_list.append(base_url + video_id)
        thumbnail_list.append(thumbnail_base_url + video_id + "/0.jpg")

    # Get video title list and combine for short and medium queries
    title_list_short = youtube_search_short.get_video_titles()
    title_list_medium = youtube_search_medium.get_video_titles()
    title_list = title_list_short + title_list_medium

    # Build dict to return
    results = {"video_urls": url_list, "thumbnail_urls": thumbnail_list, "video_titles": title_list}
    return jsonify(results)


@app.route('/model-results', methods=['GET'])
def model_results():
    """
    Request should contain a URL to a YouTube video. Audio will be extracted and
    run through the neural network model, then a JSON array of the resulting
    probabilities for each class/genre of music will be sent in the response.
    """
    query_param = request.args.get("songUrl")

    # If input is empty then return an empty list
    if query_param == "" or query_param is None or query_param == "null":
        return jsonify([])

    results = classifier.classify_youtube_audio(query_param)
    return jsonify(results)


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8050))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=False)
