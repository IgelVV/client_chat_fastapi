from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.connector import Database
from src.auth.user_services import UserSelector
from src import schemas
from src.auth.router import router as auth_router
from src.config import ALLOWED_ORIGINS

db = Database().connection

app = FastAPI(title="Service Chat")


origins = ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"
                   ],
)


@app.get("/", response_model=Optional[list[schemas.UserDisplay]])
async def hello():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM User")
        result = cursor.fetchall()
    return result


@app.get("/user/{username}", response_model=Optional[schemas.UserDisplay])
async def get_by_username(username: str):
    user = UserSelector().get_user_by_username(db, username)
    return user


app.include_router(auth_router)


@app.on_event("shutdown")
async def shutdown_event():
    Database().close()
