import pymysql.cursors
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset='utf8mb4',
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
    )
