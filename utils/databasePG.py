import os

import psycopg2


import os
import time
import psycopg2


def get_db_connection(retries=5, delay=2):
    attempt = 0

    while attempt < retries:
        try:
            attempt += 1
            return psycopg2.connect(
                database=os.getenv("DATABASE_NAME"),
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                port=os.getenv("DATABASE_PORT"),
            )
        except psycopg2.OperationalError as e:
            if attempt == retries:
                raise e
            time.sleep(delay)
    return None