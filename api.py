import os
from functools import partial
from threading import Thread

from flask import Flask, jsonify, render_template

from functions.download import download
from functions.search import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/listennow/search/<string:title>', methods=['GET'])
def search_songs(title):
    return jsonify(search(title))


@app.route('/listennow/search/videos/<string:title>', methods=['GET'])
def search_videos(title):
    return jsonify(search_videos(title))


@app.route('/listennow/download/<string:video_id_param>/<string:client_token_param>', methods=['GET'])
def download_route(video_id_param, client_token_param):
    video_id = video_id_param
    client_token = client_token_param

    file_name = get_song_title(video_id)

    partial_download = partial(download, video_id, file_name, client_token)
    Thread(target=partial_download).start()

    return render_template("index.html")


if __name__ == '__main__':
    # class StandaloneApplication(BaseApplication):
    #     def __init__(self, app, options=None):
    #         self.options = options or {}
    #         self.application = app
    #         super(StandaloneApplication, self).__init__()
    #
    #     def load_config(self):
    #         config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
    #         for key, value in config.items():
    #             self.cfg.set(key.lower(), value)
    #
    #     def load(self):
    #         return self.application
    #
    # ssl_context = ('/certs/server.cert', '/certs/server.key')  # Update with your SSL certificate and private key paths
    #
    # options = {
    #     'bind': '0.0.0.0:8000',
    #     'workers': 4,  # You can adjust the number of workers based on your needs
    #     'certfile': ssl_context[0],
    #     'keyfile': ssl_context[1],
    # }
    #
    # StandaloneApplication(app, options).run()
    app.run( host='0.0.0.0', port="5000", debug=True)