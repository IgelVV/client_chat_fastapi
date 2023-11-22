from typing import Optional

from fastapi import FastAPI

from db.connector import get_connection
from services.user_services import UserSelector, UserService
from schemas import User

connection = get_connection()

app = FastAPI(title="Service Chat")


@app.get("/")
def hello():
    with connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT IGNORE INTO User(username, password, is_admin) VALUES ('admin', 'password', true)
                """
            cursor.execute(sql)

        connection.commit()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            print(cursor.fetchall())

    return "hello world"


@app.get("/user/{username}", response_model=Optional[User])
def get_by_username(username: str):
    user = UserSelector().get_user_by_username(username)
    return user


@app.post("/user/", response_model=Optional[dict[str, int]])
def create_user(username: str, password: str, is_admin: bool):
    user_id = UserService().create_user(username, password, is_admin)
    return user_id
