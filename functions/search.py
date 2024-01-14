from auth.configuration import ytmusic


def search(title):
    return ytmusic.search(title, "songs")

def searchVideos(title):
    return ytmusic.search(title, "videos")


def getSongTitle(videoId):
    title = str(ytmusic.get_song(videoId)['videoDetails']['title'])
    title = title.replace('"', '')
    title = title.replace(':', '')

    return title


def getSmallThumb(videoId):
    return ytmusic.get_song(videoId)['videoDetails']['thumbnail']['thumbnails'][0]['url']


def getLargeThumb(videoId):
    return ytmusic.get_song(videoId)['videoDetails']['thumbnail']['thumbnails'][1]['url']


def getLyrics(videoId):
    try:
        lyrics = str(ytmusic.get_lyrics(ytmusic.get_watch_playlist(videoId)['lyrics'])['lyrics'])

        return lyrics
    except Exception:
        return "Not found"


def getArtist(videoId):
    return str(ytmusic.get_artist(ytmusic.get_song(videoId)['videoDetails']['channelId'])['name'])


def getAlbum(videoId):
    return str(ytmusic.get_watch_playlist(videoId)['tracks'][0]['album']['name'])


if __name__ == '__main__':
    print("Teste")
