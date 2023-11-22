import pymysql.cursors


def get_connection():
    return pymysql.connect(
        host='db',
        user='user',
        password='password',
        database='db',
        charset='utf8mb4',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
    )
