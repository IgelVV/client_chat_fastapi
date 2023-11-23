import pymysql.cursors
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


class Database:
    connection = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self.connection is None:
            self.connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                charset='utf8mb4',
                port=DB_PORT,
                cursorclass=pymysql.cursors.DictCursor,
            )

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None


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
