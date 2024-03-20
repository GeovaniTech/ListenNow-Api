from auth.configuration import ytmusic


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