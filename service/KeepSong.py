import base64

from utils.databasePG import conn
def save(title, small_thumb, large_thumb, small_thumb_bytes, large_thumb_bytes, file, lyrics, videoId, artist, album):
    sql_query = """
        INSERT INTO song (title, small_thumb, large_thumb, small_thumb_bytes, large_thumb_bytes, file, lyrics, videoId, artist, album)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cur = conn.cursor()
    cur.execute(sql_query, (title, small_thumb, large_thumb, small_thumb_bytes, large_thumb_bytes, file, lyrics, videoId, artist, album))
    conn.commit()


def listSongs():
    sql = "SELECT * FROM song"

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    songs = []

    for song in cur.fetchall():
        songConverted = list(song)

        songConverted[5] = base64.encodebytes(songConverted[5]).decode("utf-8")
        songConverted[6] = base64.encodebytes(songConverted[6]).decode("utf-8")
        songConverted[7] = base64.encodebytes(songConverted[7]).decode("utf-8")

        songs.append(songConverted)

    return songs