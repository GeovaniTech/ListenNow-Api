import os

from functions.search import *
from utils.ThumbUtil import *
from utils.databasePG import *


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

