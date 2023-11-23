from typing import Optional

from src.db.connector import get_connection


class UserSelector:
    @staticmethod
    def get_user_by_id(user_id: int):
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM User WHERE User.id=%s", user_id)
                result = cursor.fetchone()
                return result

    @staticmethod
    def get_user_by_username(username: str) -> Optional[dict]:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM User WHERE User.username=%s", username)
                result = cursor.fetchone()
                return result


class UserService:
    @staticmethod
    def create_user(username, password, is_admin):
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO User(username, password, is_admin) VALUES (%s, %s, %s)",
                    (username, password, is_admin,),
                )
                cursor.execute(
                    "SELECT id FROM User WHERE User.username=%s", username)
                result = cursor.fetchone()
            connection.commit()
        return result
