import datetime
import uuid

from utils.databasePG import get_cursor_db, conn


def save_client_song(client_id, song_id):
    sql_query = """
        INSERT INTO client_song (id, song_id, client_id, request_date)
        VALUES (%s, %s, %s, %s)
    """

    cur = get_cursor_db()
    cur.execute(sql_query, (str(uuid.uuid4()), song_id, client_id, datetime.date.today()))
    conn.commit()
    conn.close()


def exists_client_song(client_id, song_id):
    sql = f"SELECT id FROM client_song where song_id = '{song_id}' and client_id = '{client_id}'"

    cur = get_cursor_db()
    cur.execute(sql)

    client_song_id = cur.fetchone()

    return client_song_id is not None