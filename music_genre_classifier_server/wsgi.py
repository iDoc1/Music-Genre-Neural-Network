from flask_server import app

# To run via gunicorn use: gunicorn wsgi:app
# To run from project root directory: gunicorn --chdir ./music_genre_classifier_server/ wsgi:app
if __name__ == "__main__":
    app.run()
