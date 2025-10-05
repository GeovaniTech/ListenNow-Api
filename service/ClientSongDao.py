import datetime
import uuid
import re

from utils.databasePG import get_db_connection

conn = None

def save_client_song(client_id, song_id):
    global conn
    conn = get_db_connection()

    sql_query = """
        INSERT INTO client_song (id, song_id, client_id, request_date)
        VALUES (%s, %s, %s, %s)
    """

    cur = conn.cursor()
    cur.execute(sql_query, (str(uuid.uuid4()), song_id, client_id, datetime.datetime.today()))
    conn.commit()
    conn.close()


def exists_client_song(client_id, song_id):
    global conn
    conn = get_db_connection()

    sql = f"SELECT id FROM client_song where song_id = '{song_id}' and client_id = '{client_id}'"

    cur = conn.cursor()
    cur.execute(sql)

    client_song_id = cur.fetchone()

    return client_song_id is not None


def get_ids_songs_by_user(id_user_to_receive, id_user_with_songs):
    return fetch_song_ids(id_user_to_receive, id_user_with_songs)


def insert_songs_from_another_user(id_user_to_receive, ids):
    for song_id in ids:
        save_client_song(id_user_to_receive, song_id)


def fetch_song_ids(id_user_to_receive, id_user_with_songs):
    is_valid_uuid = re.match("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", id_user_with_songs)
    if not is_valid_uuid:
        return []

    global conn
    conn = get_db_connection()

    sql = """
        SELECT cs.song_id
        FROM client_song AS cs
        WHERE cs.client_id = %s
        AND NOT EXISTS (
            SELECT 1
            FROM client_song AS css
            WHERE css.client_id = %s
            AND cs.song_id = css.song_id
        )
    """

    cur = conn.cursor()
    cur.execute(sql, (id_user_with_songs, id_user_to_receive))

    ids = cur.fetchall()
    song_ids = [song_id[0] for song_id in ids]

    return song_ids


def delete_client_song(client_id, song_id):
    global conn

    conn = get_db_connection()
    cur = conn.cursor()

    sql = "DELETE FROM client_song AS cs WHERE cs.client_id = %s AND cs.song_id = %s"

    cur.execute(sql, (client_id, song_id))