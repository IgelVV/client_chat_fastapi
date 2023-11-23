from typing import Optional

from src.db.connector import get_connection


class UserSelector:
    def get_user_by_id(self, user_id: int):
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM User WHERE User.id=%s", user_id)
                result = cursor.fetchone()
                return result

    def get_user_by_username(self, username: str) -> Optional[dict]:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM User WHERE User.username=%s", username)
                result = cursor.fetchone()
                return result


class UserService:
    def create_user(self, username, password, is_admin):
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
