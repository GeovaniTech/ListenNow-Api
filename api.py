import os
from functools import partial
from threading import Thread

from flask import Flask, jsonify, render_template, make_response, request
from gunicorn.app.base import BaseApplication

from config.configuration import configure_env
from functions.download import download
from functions.search import *
from service import PlaylistDao
from service.ClientSongDao import save_client_song, exists_client_song, get_ids_songs_by_user, \
    insert_songs_from_another_user, delete_client_song
from service.SongDao import get_user_songs, get_song_file, exists_song_in_database, find_song_by_id_db
from service.UserDao import *
from utils.MessageUtil import log_message_response, log_message_response_error
from service.AppVersionDao import get_latest_version

app = Flask(__name__)

PUBLIC_ROUTES = ["home_listennow"]

@app.before_request
def verify_api_key():
    api_key = request.headers.get('Api-Key')

    if request.endpoint in PUBLIC_ROUTES:
        return None

    if api_key is None or os.getenv("API_KEY") != api_key:
        return jsonify(message = "API key is invalid"), 401

    return None


@app.route('/')
def index():
    return make_response()

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
    params = request.json

    user_id = params['client_id']
    ignore_ids = None

    if "ignoreIds" in params:
        ignore_ids = params['ignoreIds']

    return make_response(
        jsonify(
            get_user_songs(user_id, ignore_ids)
        )
    )


@app.route('/listennow/user/songs/delete', methods=['POST'])
def user_songs_delete_route():
    try:
        params = request.json

        delete_client_song(params['clientId'], params['videoId'])

        return log_message_response("Song deleted from user account successfully.")
    except Exception as e:
        return log_message_response_error("Failed to delete song from user account", e)


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
    client_id = request.json['clientId']

    return jsonify(find_song_by_id_db(video_id, client_id))


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
        return log_message_response_error(
            "code: 1",
            e.args
        )


@app.route("/listennow/songs/ids", methods=['POST'])
def get_ids_songs_user():
    user_receiver = request.json['userReceiver']
    user_with_songs = request.json['userWithSongs']

    try:
        return make_response(
            jsonify(
                songsIds = get_ids_songs_by_user(user_receiver, user_with_songs)
            )
        )
    except Exception as e:
        return log_message_response_error(
            f"Error trying to get ids songs for user {user_with_songs}",
            e.args
        )


@app.route("/listennow/songs/copy", methods=['POST'])
def copy_songs_from_another_user():
    try:
        user_receiver = request.json['userReceiver']
        songs_ids = request.json['songsIds']

        insert_songs_from_another_user(user_receiver, songs_ids)

        return make_response(
            jsonify(message = "code: 2")
        )
    except Exception as e:
        return log_message_response_error(
            f"Error trying to copy songs from another user.",
            e.args
        )


@app.route("/listennow/app/last/version", methods=['GET'])
def get_latest_app_version():
    try:
        return make_response(
            jsonify(
                get_latest_version()
            )
        )
    except Exception as e:
        return log_message_response_error(
            "Error trying to get ListenNow latest version.",
            e.args
        )


@app.route("/listennow/playlist/create", methods=['PUT'])
def create_playlist():
    try:
        playlist_name = request.json['playlistName']
        client_id = request.json['clientId']

        playlist_id = PlaylistDao.create_playlist(playlist_name, client_id)

        return make_response(
            jsonify(
                playlist_id = playlist_id
            )
        )
    except Exception as e:
        return log_message_response_error("Failed to create playlist", e), 500


@app.route("/listennow/playlist/update", methods=['PATCH'])
def update_playlist():
    try:
        playlist_id = request.json['playlistId']
        playlist_name = request.json['playlistName']

        PlaylistDao.update_playlist(playlist_id, playlist_name)

        return make_response(
            jsonify(
                playlist_id = playlist_id
            )
        )

    except Exception as e:
        return log_message_response_error("Failed to update playlist", e), 500


@app.route("/listennow/playlist/delete", methods=['DELETE'])
def delete_playlist():
    try:
        playlist_id = request.json['playlistId']

        PlaylistDao.delete_playlist(playlist_id)

        return make_response(
            jsonify(
                playlist_id = playlist_id
            )
        )
    except Exception as e:
        return log_message_response_error("Failed to delete playlist", e), 500



@app.route("/listennow/playlist/add/songs", methods=['PUT'])
def insert_songs_into_playlist():
    try:
        playlist_id = request.json['playlistId']
        songs = request.json['songs']

        PlaylistDao.insert_songs_into_playlist(playlist_id, songs)

        return make_response(
            jsonify(
                message = "Songs Added Successfully"
            )
        )
    except Exception as e:
        return log_message_response_error("Failed to add songs to playlist", e), 500


if __name__ == '__main__':
    configure_env()

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

        options = {
            'bind': '0.0.0.0:8000',
            'workers': 4
        }

        StandaloneApplication(app, options).run()
    else:
        app.run(host='0.0.0.0', port="5000", debug=True)

