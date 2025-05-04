from utils.databasePG import get_db_connection


def get_latest_version():
    conn = get_db_connection()

    sql = """
        SELECT code,
               name,
               url
        FROM 
            version
        ORDER BY 
            code DESC
        LIMIT 1
    """

    cur = conn.cursor()
    cur.execute(sql)
    version = cur.fetchone()
    conn.close()

    return {
        "code": version[0],
        "name": version[1],
        "url": version[2]
    }
