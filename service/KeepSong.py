import base64
import os
from webbrowser import get

from utils.databasePG import *
from utils.ThumbUtil import *
from functions.search import *


def save(title, small_thumb, large_thumb, small_thumb_bytes, large_thumb_bytes, file, lyrics, video_id, artist, album, user_id):
    sql_query = """
        INSERT INTO song (title, small_thumb, large_thumb, small_thumb_bytes, large_thumb_bytes, file, lyrics, videoId, artist, album, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cur = get_cursor_db()
    cur.execute(sql_query, (title, small_thumb, large_thumb, small_thumb_bytes, large_thumb_bytes, file, lyrics, video_id, artist, album, user_id))
    conn.commit()


def save_song(file_path, video_id, file_name, user_id):
    with open(f'{file_path}', 'rb') as f:
        data = f.read()

    small_thumb = get_small_thumb(video_id)
    large_thumb = get_large_thumb(video_id)

    small_thumb_bytes = None
    large_thumb_bytes = None

    if small_thumb != "Not Found":
        small_thumb_bytes = convert_thumb_to_bytes(small_thumb)

    if large_thumb != "Not Found":
        large_thumb_bytes = convert_thumb_to_bytes(large_thumb)

    lyrics = get_lyrics(video_id)
    artist = get_artist(video_id)
    album = get_album(video_id)

    save(file_name, small_thumb, large_thumb, small_thumb_bytes, large_thumb_bytes, data, lyrics, video_id, artist, album, user_id)
    os.remove(file_path)

