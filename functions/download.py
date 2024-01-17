from __future__ import unicode_literals
import youtube_dl
import requests

base_url = "https://www.youtube.com/watch?v="

def progress(value):
    if value['status'] == 'finished':
        print("Download finished")

    elif value['status'] == 'downloading':
        print(value['filename'], value['_percent_str'], value['_eta_str'])

def download(videoId, fileName, clientToken):
    ytdl_options = {
        'outtmpl': f'/projects/ListenNow-Api/songs/{fileName}.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress]
    }

    with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
        url = base_url + videoId
        print(f"DOWNLOADING: {url}")
        ytdl.download([url])


def convertThumbToBytes(thumb):
    try:
        response = requests.get(thumb)
        response.raise_for_status()  # Raise an exception if the request was not successful

        image_bytes = response.content
        return image_bytes
    except:
        print("ERRO: convert image to bytes")