from datetime import timedelta, datetime
from typing import Optional

from jose import jwt

from src.auth.hashing import Hasher
from src.config import SECRET_KEY, ALGORITHM


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
    def authenticate(db_connection, username, password):
        user = UserSelector.get_user_by_username(db_connection, username)
        if user:
            if Hasher.verify_password(password, user["password"]):
                return user
        return None

    @staticmethod
    def create_access_token(data: dict,
                            expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
