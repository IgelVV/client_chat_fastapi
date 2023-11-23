from datetime import timedelta, datetime
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from src.auth.hashing import Hasher
from src.config import SECRET_KEY, ALGORITHM
from src.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


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

    def get_user_by_token(self, db, token):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise ValueError
        token_data = TokenData(username=username)
        user = self.get_user_by_username(db, username=token_data.username)
        return user


class UserService:
    @staticmethod
    def create_user(db_connection, username, password, is_admin):
        with db_connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO User(username, password, is_admin) "
                "VALUES (%s, %s, %s)",
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
