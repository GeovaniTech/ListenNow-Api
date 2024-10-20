from auth.configuration import ytmusic


def get_thumb(video_id):
    try:
        return ytmusic.get_song(video_id)['videoDetails']['thumbnail']['thumbnails'][1]['url']
    except Exception as e:
        return f"An error occurred when trying to get Thumb. Error: {e.args}"