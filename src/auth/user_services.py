from typing import Optional

from src.db.connector import get_connection
from src.auth.hashing import Hasher


class UserSelector:
    @staticmethod
    def get_user_by_id(db_connection, user_id: int):
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE User.id=%s", user_id)
            result = cursor.fetchone()
            return result

    @staticmethod
    def get_user_by_username(db_connection, username: str) -> Optional[dict]:
        with db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM User WHERE User.username=%s", username)
            result = cursor.fetchone()
            return result


class UserService:
    @staticmethod
    def create_user(db_connection, username, password, is_admin):
        with db_connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO User(username, password, is_admin) VALUES (%s, %s, %s)",
                (username, Hasher.get_password_hash(password), is_admin,),
            )
            cursor.execute(
                "SELECT id FROM User WHERE User.username=%s", username)
            result = cursor.fetchone()
        db_connection.commit()
        return result

    @staticmethod
    def check_user_password(db_connection, username, password):
        user = UserSelector.get_user_by_username(db_connection, username)
        if user:
            result = Hasher.verify_password(password, user["password"])
        else:
            result = False
        return result
