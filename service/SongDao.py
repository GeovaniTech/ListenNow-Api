import os

from functions.search import *
from service.ClientSongDao import save_client_song
from utils.ThumbUtil import *
from utils.databasePG import *
from utils.BytesUtil import bytes_to_base64


def save(video_id, name, artist, album, thumb, file, lyrics):
    sql_query = """
        INSERT INTO song (video_id, name, artist, album, thumb, file, lyrics)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cur = get_cursor_db()
    cur.execute(sql_query, (video_id, name, artist, album, thumb, file, lyrics))
    conn.commit()


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
    sql = f"""
        SELECT title, 
               artist, 
               album, 
               lyrics, 
               small_thumb, 
               large_thumb, 
               video_id,
               song_id
               FROM song WHERE user_id = '{uuid}'"""

    cur = get_cursor_db()
    cur.execute(sql)

    songs_db = cur.fetchall()

    songs = list()

    for song in songs_db:
        json_song = {
            "title": song[0],
            "artist": song[1],
            "album": song[2],
            "lyrics": song[3],
            "small_thumb": song[4],
            "large_thumb": song[5],
            "video_id": song[6],
            "song_id": song[7]
        }

        songs.append(json_song)

    return songs


def delete_song(song_id):
    sql = f"DELETE FROM song WHERE song_id = '{song_id}'"
    cur = get_cursor_db()
    cur.execute(sql)
    conn.commit()


def get_song_file(song_id):
    sql = f"SELECT file FROM song where song_id = '{song_id}'"

    cur = get_cursor_db()
    cur.execute(sql)

    file = cur.fetchone()

    return bytes_to_base64(file[0])

def exists_song_in_database(video_id):
    sql = f"SELECT video_id FROM song where video_id = '{video_id}'"

    cur = get_cursor_db()
    cur.execute(sql)

    song_id = cur.fetchone()

    if song_id is not None:
        return True
    else:
        return False

