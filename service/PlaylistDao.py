import uuid

from psycopg2._psycopg import cursor

from utils.databasePG import get_db_connection

def create_playlist(playlist_name, client_id):
    playlist_id = None

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        sql = "INSERT INTO playlist (id, name, client_id) VALUES (%s, %s, %s)"

        playlist_id = str(uuid.uuid4())

        cur.execute(sql, (playlist_id, playlist_name, client_id))
        conn.commit()

    except Exception:
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    return playlist_id


def update_playlist(playlist_id, name):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        sql = "UPDATE playlist SET name = %s WHERE id = %s"

        cur.execute(sql, (name, playlist_id))
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def delete_playlist(playlist_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        sql = "DELETE FROM playlist WHERE id = %s"
        cur.execute(sql, (playlist_id,))
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def insert_songs_into_playlist(playlist_id, songs):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        for song in songs:
            sql = "INSERT INTO playlist_songs (id, playlist_id, video_id) VALUES (%s, %s, %s)"

            cur.execute(sql, (str(uuid.uuid4()), playlist_id, song))
            conn.commit()
    except Exception:
        conn.rollback()
    finally:
        cur.close()
        conn.close()

