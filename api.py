import os
from functools import partial
from threading import Thread

from flask import Flask, jsonify, render_template, make_response, request
from gunicorn.app.base import BaseApplication

from functions.download import download
from functions.search import *
from service.ClientSongDao import save_client_song, exists_client_song
from service.SongDao import get_user_songs, delete_song, get_song_file, exists_song_in_database, find_song_by_id_db
from service.UserDao import *
from utils.MessageUtil import log_message_response

app = Flask(__name__)


@app.route('/listennow')
def home_listennow():
    return render_template("home.html")


@app.route('/listennow/search/<string:title>', methods=['GET'])
def search_songs(title):
    return make_response(
        jsonify(
            search(title)
        )
    )


@app.route('/listennow/search/videos/<string:title>', methods=['GET'])
def search_videos_route(title):
    return make_response(
        jsonify(
            search_videos(title)
        )
    )


@app.route('/listennow/songs/search', methods=['POST'])
def search_songs_to_app():
    params = request.json

    return make_response(
        jsonify(
            search_to_app(params['search_for'])
        )
    )


@app.route('/listennow/download/song', methods=['POST'])
def download_route():
    params = request.json

    video_id = params['video_id']
    client_id = params['client_id']

    if exists_song_in_database(video_id):
        if exists_client_song(client_id, video_id):
            log_message_response("Client already has song saved on the database")
        else:
            save_client_song(client_id, video_id)

        return log_message_response("Song already exists in database, skipping download.")
    else:
        file_name = get_song_title(video_id)

        partial_download = partial(download, video_id, client_id, file_name)
        Thread(target=partial_download).start()

        return log_message_response(f"Download song: {video_id} has been started.")


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


@app.route('/listennow/songs/file', methods=['POST'])
def song_file_route():
    song = request.json

    return make_response(
        jsonify(
            file=str(get_song_file(song['videoId']))
        )
    )


@app.route('/listennow/songs/find', methods=['POST'])
def find_song_by_id():
    video_id = request.json['videoId']

    return jsonify(find_song_by_id_db(video_id))


@app.route('/listennow/user/add', methods=['POST'])
def add_user():
    try:
        user = request.json
        save(user['uuid'])

        return make_response(
            jsonify(
                message="Client saved successfully"
            )
        )
    except Exception as e:
        return log_message_response(
            "code: 1",
            e.args
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
        '/certs/certificate.crt', '/certs/key.key')

        options = {
            'bind': '0.0.0.0:8000',
            'workers': 4,
            'certfile': ssl_context[0],
            'keyfile': ssl_context[1],
        }

        StandaloneApplication(app, options).run()
    else:
        app.run(host='0.0.0.0', port="5000", debug=True)

