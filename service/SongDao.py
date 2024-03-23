import json
import os

from functions.search import *
from utils.ThumbUtil import *
from utils.databasePG import *
from utils.BytesUtil import *


def save(title, small_thumb, large_thumb, file, lyrics, video_id, artist, album, user_id):
    sql_query = """
        INSERT INTO song (title, small_thumb, large_thumb, file, lyrics, video_id, artist, album, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cur = get_cursor_db()
    cur.execute(sql_query, (title, small_thumb, large_thumb, file, lyrics, video_id, artist, album, user_id))
    conn.commit()


def save_song(file_path, video_id, file_name, user_id):
    with open(f'{file_path}', 'rb') as f:
        data = f.read()

    small_thumb = get_small_thumb(video_id)
    large_thumb = get_large_thumb(video_id)

    lyrics = get_lyrics(video_id)
    artist = get_artist(video_id)
    album = get_album(video_id)

    save(file_name, small_thumb, large_thumb, data, lyrics, video_id, artist, album, user_id)
    os.remove(file_path)


def get_user_songs(uuid):
    sql = f"""
        SELECT title, 
               artist, 
               album, 
               lyrics, 
               small_thumb, 
               large_thumb, 
               video_id 
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
            "video_id": song[6]
        }

        songs.append(json_song)

    return songs

