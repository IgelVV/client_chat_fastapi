from typing import Optional

from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.db.connector import get_connection
from src.auth.user_services import UserSelector, UserService
from src import schemas
from src.auth.router import router as auth_router

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


@app.get("/user/{username}", response_model=Optional[schemas.User])
def get_by_username(username: str):
    user = UserSelector().get_user_by_username(username)
    return user


@app.post("/user/", response_model=Optional[dict[str, int]])
def create_user(username: str, password: str, is_admin: bool):
    user_id = UserService().create_user(username, password, is_admin)
    return user_id


@app.post("/register/", response_model=schemas.LiteUser, status_code=201)
def create_user(user_data: schemas.UserCreate):
    selector = UserSelector()
    service = UserService()
    if selector.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this username already exists.",
        )
    user_id = service.create_user(
        user_data.username,
        user_data.password,
        user_data.is_admin,
    )
    return user_id


app.include_router(auth_router)
