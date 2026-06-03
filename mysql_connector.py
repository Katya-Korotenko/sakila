import os

import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor
from contextlib import contextmanager


load_dotenv('.env')



config = {'host': os.getenv('DB_HOST'),
          'user': os.getenv('DB_USER'),
          'password': os.getenv('DB_PASSWORD'),
          'database': os.getenv('DB_DATABASE'),
          }
@contextmanager
def get_cursor():
    try:
        with pymysql.connect(**config) as connection:
            with connection.cursor(DictCursor) as cursor:
                yield cursor
    except pymysql.Error as e:
        print(f"Database error: {e}")
        raise

def execute_query(query, parameter = None):
    with get_cursor() as cursor:
        cursor.execute(query, parameter)
        return cursor.fetchall()
