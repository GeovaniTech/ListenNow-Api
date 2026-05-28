import uuid

from utils.databasePG import get_db_connection


def create_playlist(playlist_name, client_id):
    playlist_id = None

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        sql = "INSERT INTO playlist (id, name) VALUES (%s, %s); INSERT INTO playlist_clients (id, playlist_id, client_id) VALUES (%s, %s, %s)"

        playlist_id = str(uuid.uuid4())
        playlist_client_id = str(uuid.uuid4())

        cur.execute(sql, (playlist_id, playlist_name, playlist_client_id, playlist_id, client_id))
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



def get_playlists_from_user(client_id, ignore_ids):
    conn = get_db_connection()
    cur = conn.cursor()

    params = list()

    try:
        sql = f"SELECT p.id, p.name FROM playlist p INNER JOIN playlist_clients as pl_cl ON p.id = pl_cl.playlist_id WHERE pl_cl.client_id = '{client_id}'"

        if ignore_ids is not None and len(ignore_ids) > 0:
            placeholders = ','.join(['%s'] * len(ignore_ids))
            sql += f" AND id NOT IN ({placeholders})"
            params.extend(ignore_ids)

        cur.execute(sql, params)
        playlists_response = cur.fetchall()

        playlists = []

        if playlists_response is not None and len(playlists_response) > 0:
            for playlist in playlists_response:
                print(playlist)
                playlists.append({
                    "id": playlist[0],
                    "name": playlist[1],
                    "songs": get_songs_from_playlist(playlist[0])
                })
        return playlists
    except Exception as e:
        print(e.args)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def get_songs_from_playlist(playlist_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        sql = "SELECT video_id FROM playlist_songs WHERE playlist_id = %s"
        cur.execute(sql, (playlist_id,))
        songs_response = cur.fetchall()

        songs = []

        if songs_response is not None and len(songs_response) > 0:
            for song in songs_response:
                songs.append(song[0])

        return songs
    except Exception as e:
        print(e.args)
        conn.rollback()
    finally:
        cur.close()
        conn.close()