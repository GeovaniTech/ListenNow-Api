from utils.databasePG import get_cursor_db, conn


def exist_user_with_email(email):
    sql = f"SELECT * FROM user_listennow WHERE email = '{email}'"

    cur = get_cursor_db()
    cur.execute(sql)
    user = cur.fetchall()

    if len(user) == 0:
        return False

    return True


def save(email, password):
    sql = "INSERT INTO user_listennow VALUES (%s, %s)"
    cur = get_cursor_db()
    cur.execute(sql, (email, password))
    conn.commit()

