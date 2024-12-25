import datetime
import uuid

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
    cur.execute(sql_query, (str(uuid.uuid4()), song_id, client_id, datetime.date.today()))
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


def get_qtde_songs_by_user(user_id):
    global conn
    conn =  get_db_connection()

    sql = f"SELECT COUNT(id) FROM client_song WHERE client_id = '{user_id}'"

    cur = conn.cursor()
    cur.execute(sql)

    qtde = cur.fetchone()

    return qtde[0]