import os

import psycopg2


def get_db_connection(retries = 5):
    attempt = 0

    while attempt < retries:
        attempt += 1
        return psycopg2.connect(
            database=f"{os.getenv('DATABASE_NAME')}",
            host=f"{os.getenv('DATABASE_HOST')}",
            user=f"{os.getenv('DATABASE_USER')}",
            password=f"{os.getenv('DATABASE_PASSWORD')}",
            port=f"{os.getenv('DATABASE_PORT')}"
        )
