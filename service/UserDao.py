from utils.databasePG import get_cursor_db, conn


def exists_user(client_id):
    sql = f"SELECT * FROM client WHERE id = '{client_id}'"

    cur = get_cursor_db()
    cur.execute(sql)
    user = cur.fetchall()

    if len(user) == 0:
        return False

    return True


def save(client_id):
    sql = f"INSERT INTO client (id) VALUES (%s)"
    cur = get_cursor_db()
    cur.execute(sql, (client_id,))
    conn.commit()
    conn.close()

