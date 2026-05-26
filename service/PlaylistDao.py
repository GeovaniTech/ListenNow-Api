import traceback
import uuid
from encodings import palmos

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
        sql = "DELETE FROM playlist_songs WHERE playlist_id = %s; DELETE FROM playlist WHERE id = %s"
        cur.execute(sql, (playlist_id, playlist_id))
        conn.commit()
    except Exception as e:
        print(e.args)
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


def delete_songs_from_playlist(playlist_id, songs):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        for song in songs:
            sql = "DELETE FROM playlist_songs WHERE playlist_id = %s AND video_id = %s"
            cur.execute(sql, (playlist_id, song))
            conn.commit()
    except Exception:
        conn.rollback()
    finally:
        cur.close()
        conn.close()



def get_playlists_from_user(client_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        sql = f"SELECT id, name FROM playlist WHERE client_id = '{client_id}'"

        cur.execute(sql)
        playlists_response = cur.fetchall()
        print(playlists_response)

        playlists = []

        if playlists_response is not None:
            for playlist in playlists_response:
                print(playlist)
                playlists.append({
                    "id": playlist[0],
                    "name": playlist[1],
                })
        return playlists
    except Exception as e:
        print(e.args)
        conn.rollback()
    finally:
        cur.close()
        conn.close()