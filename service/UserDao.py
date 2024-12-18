from utils.databasePG import get_db_connection

conn = None

def exists_user(client_id):
    global conn

    sql = f"SELECT * FROM client WHERE id = '{client_id}'"

    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute(sql)
    user = cur.fetchall()
    conn.close()

    if len(user) == 0:
        return False

    return True


def save(client_id):
    global conn

    sql = f"INSERT INTO client (id) VALUES (%s)"

    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute(sql, (client_id,))
    conn.commit()
    conn.close()


