from typing import Optional

from fastapi import FastAPI

from src.db.connector import get_connection
from src.auth.user_services import UserSelector
from src import schemas
from src.auth.router import router as auth_router

connection = get_connection()

app = FastAPI(title="Service Chat")


@app.get("/")
async def hello():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            result = cursor.fetchall()

    from src.auth.hashing import Hasher
    print(Hasher.get_password_hash("password"))
    print(Hasher.get_password_hash("password"))
    print(len(Hasher.get_password_hash("password")))
    return result


@app.get("/user/{username}", response_model=Optional[schemas.User])
async def get_by_username(username: str):
    user = UserSelector().get_user_by_username(username)
    return user


app.include_router(auth_router)
