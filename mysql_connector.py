import os

import pymysql
from dotenv import load_dotenv

load_dotenv('.env')



config = {'host': os.getenv('DB_HOST'),
          'user': os.getenv('DB_USER'),
          'password': os.getenv('DB_PASSWORD'),
          'database': os.getenv('DB_NAME'),
          }

def get_connection():
    return pymysql.connect(**config)
