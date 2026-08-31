from datetime import datetime
from datetime import timezone
from utils.databasePG import get_db_connection

conn = None

def insert_log_from_device(log_id, level, tag, message, created_at, device_id):
    global conn

    conn = get_db_connection()

    sql = "INSERT INTO log (id, level, tag, message, created_at, device_id) VALUES (%s, %s, %s, %s, %s, %s)"

    converted_created_at = datetime.fromtimestamp(int(created_at), tz=timezone.utc)

    cur = conn.cursor()
    cur.execute(sql, (log_id, level, tag, message, converted_created_at, device_id))
    conn.commit()
    conn.close()