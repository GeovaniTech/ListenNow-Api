import os

from functions.search import *
from service.ClientSongDao import save_client_song
from utils.BytesUtil import bytes_to_base64
from utils.ThumbUtil import *
from utils.databasePG import get_db_connection

conn = None

def save(video_id, name, artist, album, thumb, file, lyrics):
    global conn
    conn = get_db_connection()

    sql_query = """
        INSERT INTO song (video_id, name, artist, album, thumb, file, lyrics)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cur = conn.cursor()
    cur.execute(sql_query, (video_id, name, artist, album, thumb, file, lyrics))
    conn.commit()
    conn.close()


def before_save_song(file_path, video_id, file_name, client_id):
    with open(f'{file_path}', 'rb') as f:
        data = f.read()

    thumb = get_thumb(video_id)

    lyrics = get_lyrics(video_id)
    artist = get_artist(video_id)
    album = get_album(video_id)

    save(video_id, file_name, artist, album, thumb, data, lyrics)
    save_client_song(client_id, video_id)

    os.remove(file_path)


def get_user_songs(uuid):
    global conn
    conn = get_db_connection()

    sql = f"""
        SELECT video_id,
               name, 
               artist, 
               album, 
               lyrics,
               thumb
        FROM song
        INNER JOIN client_song as cs ON cs.song_id = song.video_id 
        WHERE cs.client_id = '{uuid}'"""

    cur = conn.cursor()
    cur.execute(sql)
    songs_db = cur.fetchall()
    conn.close()

    songs = list()

    for song in songs_db:
        json_song = {
            "video_id": song[0],
            "title": song[1],
            "artist": song[2],
            "album": song[3],
            "lyrics": song[4],
            "thumb": song[5],
        }

        songs.append(json_song)

    return songs


def delete_song(song_id):
    global conn
    conn = get_db_connection()

    sql = f"DELETE FROM song WHERE song_id = '{song_id}'"

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_song_file(video_id):
    global conn
    conn = get_db_connection()

    sql = f"SELECT file FROM song where video_id = '{video_id}'"

    cur = conn.cursor()
    cur.execute(sql)

    file = cur.fetchone()
    conn.close()

    return bytes_to_base64(file[0])


def find_song_by_id_db(video_id):
    global conn
    conn = get_db_connection()

    sql = f"""
            SELECT video_id,
               name, 
               artist, 
               album, 
               lyrics,
               thumb
               FROM song
               WHERE video_id = '{video_id}'
    """

    cur = conn.cursor()
    cur.execute(sql)
    song = cur.fetchone()

    if song is not None:
        json_song = {
            "video_id": song[0],
            "title": song[1],
            "artist": song[2],
            "album": song[3],
            "lyrics": song[4],
            "thumb": song[5],
        }

        return json_song
    else:
        return None


def exists_song_in_database(video_id):
    global conn
    conn = get_db_connection()

    sql = f"SELECT video_id FROM song where video_id = '{video_id}'"

    cur = conn.cursor()
    cur.execute(sql)
    song_id = cur.fetchone()
    conn.close()

    if song_id is not None:
        return True
    else:
        return False

