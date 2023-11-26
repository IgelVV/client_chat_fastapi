from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from jose import jwt, JWTError, ExpiredSignatureError

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
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Token is expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        username: str = payload.get("sub")
        if username is None:
            raise ValueError
        token_data = TokenData(username=username)
        user = self.get_user_by_username(db, username=token_data.username)
        return user

    def get_user_by_token_or_401(self, db, token):
        credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            user = self.get_user_by_token(db, token=token)
        except (ValueError, JWTError) as e:
            raise credentials_exception
        if not user:
            raise credentials_exception
        return user

    def get_admin_by_token_or_403(self, db, token):
        user = self.get_user_by_token_or_401(db, token)
        if not user["is_admin"]:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
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
