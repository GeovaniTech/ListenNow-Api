import os
from functools import partial
from threading import Thread

from flask import Flask, jsonify, render_template, make_response, request
from gunicorn.app.base import BaseApplication

from functions.download import download
from functions.search import *
from service.SongDao import get_user_songs, delete_song
from service.UserDao import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/listennow/search/<string:title>', methods=['GET'])
def search_songs(title):
    return make_response(
        jsonify(
            search(title)
        )
    )


@app.route('/listennow/search/videos/<string:title>', methods=['GET'])
def search_videos(title):
    return make_response(
        jsonify(
            search_videos(title)
        )
    )


@app.route('/listennow/download/song', methods=['POST'])
def download_route():
    params = request.json

    video_id = params['video_id']
    client_id = params['client_id']

    file_name = get_song_title(video_id)

    partial_download = partial(download, video_id, client_id, file_name)
    Thread(target=partial_download).start()

    return render_template("index.html")


@app.route('/listennow/user/songs', methods=['POST'])
def get_user_songs_route():
    user = request.json

    return make_response(
        jsonify(
            get_user_songs(user['client_id'])
        )
    )


@app.route('/listennow/songs/delete', methods=['POST'])
def delete_song_route():
    song = request.json

    delete_song(song['song_id'])

    return make_response(
        jsonify(
            message="Song deleted successfully"
        )
    )


@app.route('/listennow/user/add', methods=['POST'])
def add_user():
    user = request.json

    if exist_user_with_email(user['email']):
        return make_response(
            jsonify(
                message="User already exists"
            )
        )

    save(user['uuid'], user['email'], user['password'])

    return make_response(
        jsonify(
            message="User saved successfully"
        )
    )


@app.route('/listennow/user/login', methods=['POST'])
def login():
    credentials = request.json

    if valid_login(credentials['email'], credentials['password']):
        return make_response(
            jsonify(
                message="Login is valid"
            )
        )

    return make_response(
        jsonify(
            message="Login is not valid"
        )
    )


if __name__ == '__main__':
    project_root = os.path.abspath(os.path.dirname(__file__))

    if project_root == '/projects/ListenNow-Api':
        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super(StandaloneApplication, self).__init__()

            def load_config(self):
                config = {key: value for key, value in self.options.items() if
                          key in self.cfg.settings and value is not None}
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application


        ssl_context = (
        '/certs/server.cert', '/certs/server.key')

        options = {
            'bind': '0.0.0.0:8000',
            'workers': 4,
            'certfile': ssl_context[0],
            'keyfile': ssl_context[1],
        }

        StandaloneApplication(app, options).run()
    else:
        app.run(host='0.0.0.0', port="5000", debug=True)

