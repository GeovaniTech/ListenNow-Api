from utils.databasePG import get_cursor_db, conn


def exist_user_with_email(email):
    sql = f"SELECT * FROM user_listennow WHERE email = '{email}'"

    cur = get_cursor_db()
    cur.execute(sql)
    user = cur.fetchall()

    if len(user) == 0:
        return False

    return True


def save(uuid, email, password):
    sql = "INSERT INTO user_listennow (id, email, password) VALUES (%s, %s, %s)"
    cur = get_cursor_db()
    cur.execute(sql, (uuid, email, password))
    conn.commit()


def valid_login(email, password):
    sql = f"SELECT * FROM user_listennow WHERE email = '{email}' AND password = '{password}'"
    cur = get_cursor_db()
    cur.execute(sql)
    users = cur.fetchall()

    if len(users) == 0:
        return False

    return True


def get_user_id_by_email(email):
    sql = f"SELECT id FROM user_listennow WHERE email = '{email}'"
    cur = get_cursor_db()
    cur.execute(sql)
    user_id = cur.fetchone()

    return user_id

