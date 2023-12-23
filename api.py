import os
import time
from functools import partial

from gunicorn.app.base import BaseApplication

from functions.search import *

from threading import Thread
from functions.download import download, convertThumbToBytes
from flask import Flask, jsonify, render_template
from service.KeepSong import save, listSongs

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/listennow/search/<string:title>', methods=['GET'])
def getSongs(title):
    return jsonify(search(title))

@app.route('/listennow/download/<string:videoIdParam>/<string:clientTokenParam>', methods=['GET'])
def loadDownloadPage(videoIdParam, clientTokenParam):
    videoId = videoIdParam
    clientToken = clientTokenParam

    fileName = getSongTitle(videoId)

    partial_download = partial(downloadFun, videoId, fileName, clientToken)
    Thread(target=partial_download).start()

    return render_template("index.html")

@app.route("/listennow/synchronize", methods=['GET'])
def synchronizeSongs():
    return jsonify(listSongs())

def downloadFun(videoId, fileName, clientToken):
    download(videoId, fileName, clientToken)

    time.sleep(5)

    project_root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(project_root, 'songs', f'{fileName}.mp3')

    saveSong(file_path, videoId, fileName)

def saveSong(filePath, videoId, fileName):
    with open(f'{filePath}', 'rb') as f:
        data = f.read()

    small_thumb = getSmallThumb(videoId)
    large_thumb = getLargeThumb(videoId)
    lyrics = getLyrics(videoId)
    artist = getArtist(videoId)
    album = getAlbum(videoId)

    save(fileName, small_thumb, large_thumb, convertThumbToBytes(small_thumb), convertThumbToBytes(large_thumb), data, lyrics, videoId, artist, album)
    time.sleep(2)
    os.remove(filePath)


if __name__ == '__main__':
    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super(StandaloneApplication, self).__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    ssl_context = ('/certs/server.cert', '/certs/server.key')  # Update with your SSL certificate and private key paths

    options = {
        'bind': '0.0.0.0:8000',
        'workers': 4,  # You can adjust the number of workers based on your needs
        'certfile': ssl_context[0],
        'keyfile': ssl_context[1],
    }

    StandaloneApplication(app, options).run()
    # app.run( host='0.0.0.0', port="5000", debug=True)