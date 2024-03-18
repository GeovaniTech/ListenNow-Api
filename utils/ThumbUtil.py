import requests

from auth.configuration import ytmusic


def convert_thumb_to_bytes(thumb):
    try:
        response = requests.get(thumb)
        response.raise_for_status()  # Raise an exception if the request was not successful

        image_bytes = response.content
        return image_bytes
    except:
        print("ERROR: convert image to bytes")


def get_small_thumb(video_id):
    try:
        return ytmusic.get_song(video_id)['videoDetails']['thumbnail']['thumbnails'][0]['url']
    except Exception:
        return "Not Found"


def get_large_thumb(video_id):
    try:
        return ytmusic.get_song(video_id)['videoDetails']['thumbnail']['thumbnails'][1]['url']
    except Exception:
        return "Not Found"