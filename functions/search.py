from auth.configuration import ytmusic


def search(title):
    return ytmusic.search(title, "songs")


def search_to_app(search_for):
    if search_for is not None and len(str(search_for)) != 0:
        songs = list()

        for song in search(search_for):
            json_song = {
                "videoId": song['videoId'],
                "title": song['title'],
                "artist": song['artists'][0]['name'],
                "thumb": song['thumbnails'][0]['url']
            }

            songs.append(json_song)

        return songs


def search_videos(title):
    return ytmusic.search(title, "videos")


def get_song_title(video_id):
    title = str(ytmusic.get_song(video_id)['videoDetails']['title'])
    title = title.replace('"', '')
    title = title.replace(':', '')
    title = title.replace("/", ' ')

    return title


def get_lyrics(video_id):
    try:
        lyrics = str(ytmusic.get_lyrics(ytmusic.get_watch_playlist(video_id)['lyrics'])['lyrics'])

        return lyrics
    except Exception:
        return "Not Found"


def get_artist(video_id):
    try:
        return str(ytmusic.get_artist(ytmusic.get_song(video_id)['videoDetails']['channelId'])['name'])
    except Exception:
        return "Not Found"


def get_album(video_id):
    try:
        return str(ytmusic.get_watch_playlist(video_id)['tracks'][0]['album']['name'])
    except Exception:
        return "Not Found"

